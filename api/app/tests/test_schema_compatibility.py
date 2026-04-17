import ast
import importlib
import inspect
import pkgutil
import sys
from datetime import datetime, timezone

import pytest


def _schema_classes():
    import app.schemas as schema_package
    from app.schemas import BaseSchema

    schema_classes = []
    for _, module_name, _ in pkgutil.walk_packages(
        schema_package.__path__, prefix=f"{schema_package.__name__}."
    ):
        module = importlib.import_module(module_name)
        for value in module.__dict__.values():
            if (
                inspect.isclass(value)
                and issubclass(value, BaseSchema)
                and value is not BaseSchema
                and value.__module__ == module_name
            ):
                schema_classes.append(value)

    return sorted(schema_classes, key=lambda schema_cls: schema_cls.__name__)


def test_all_schema_classes_instantiate(app, seeded_database):
    """Assert that every Marshmallow schema class still instantiates with fields."""
    del seeded_database

    with app.app_context():
        schema_classes = _schema_classes()
        assert schema_classes

        for schema_cls in schema_classes:
            schema = schema_cls()
            assert schema.fields


def test_schema_validate_is_safe_for_orm_objects(app, seeded_data):
    """Assert that schema validation still accepts ORM instances under Marshmallow 4."""
    with app.app_context():
        from app.models.theq import Citizen, Service
        from app.schemas.theq import CitizenSchema, ServiceSchema
        from app.utilities.yesno import YesNo

        service = Service(
            service_id=1002,
            service_code="VALIDATE",
            service_name="Validate Service",
            service_desc="Validate service",
            prefix="VL",
            display_dashboard_ind=1,
            actual_service_ind=1,
            is_dlkt=YesNo.NO,
        )
        citizens = Citizen.query.limit(2).all()

        assert ServiceSchema().validate(service) == {}
        assert CitizenSchema(many=True).validate(citizens) == {}


def test_service_schema_serializes_parent_name(app, seeded_data):
    """Assert that services still serialize parent names and DLKT flags correctly."""
    del seeded_data

    with app.app_context():
        from app.models.theq import Service
        from app.schemas.theq import ServiceSchema
        from app.utilities.yesno import YesNo

        parent = Service(
            service_id=1000,
            service_code="PARENT",
            service_name="Parent Service",
            service_desc="Parent service",
            prefix="PR",
            display_dashboard_ind=1,
            actual_service_ind=1,
        )
        service = Service(
            service_id=1001,
            service_code="CHILD",
            service_name="Child Service",
            service_desc="Child service",
            prefix="CH",
            display_dashboard_ind=1,
            actual_service_ind=1,
            is_dlkt=YesNo.YES,
            parent=parent,
        )

        dumped = ServiceSchema().dump(service)

        assert dumped["parent"] == {"service_name": "Parent Service"}
        assert dumped["is_dlkt"] is True


def test_exam_schema_uses_iso_exam_received_date_format(app, seeded_data):
    """Assert that exam received dates use Marshmallow's normal ISO contract."""
    with app.app_context():
        from app.models.bookings import Exam, ExamType, Invigilator
        from app.models.theq import Office
        from app.schemas.bookings import ExamSchema
        from qsystem import db

        office = db.session.get(Office, seeded_data["office_ids"]["test_office"])
        exam_type = db.session.get(ExamType, seeded_data["exam_type_id"])
        invigilator = db.session.get(Invigilator, seeded_data["invigilator_ids"][0])

        exam = Exam(
            exam_id=2001,
            office_id=office.office_id,
            office=office,
            exam_type_id=exam_type.exam_type_id,
            exam_type=exam_type,
            invigilator_id=invigilator.invigilator_id,
            invigilator=invigilator,
            exam_name="Knowledge Test",
            exam_method="paper",
            exam_received_date=datetime(2026, 3, 25, 12, 30, tzinfo=timezone.utc),
            exam_written_ind=0,
        )
        exam.exam_received = 1
        exam.exam_returned_ind = 0
        exam.receipt_number = "R-001"
        exam.fees = "10.00"

        dumped = ExamSchema().dump(exam)

        assert dumped["exam_received_date"] == "2026-03-25T12:30:00+00:00"


def test_exam_schema_accepts_iso_exam_received_date_inputs(app, seeded_data):
    """Assert that frontend ISO offset dates load without strict literal-Z parsing."""
    with app.app_context():
        from app.schemas.bookings import ExamSchema

        base_payload = {
            "exam_method": "paper",
            "expiry_date": "2026-05-22T07:00:00+00:00",
            "exam_type_id": seeded_data["exam_type_id"],
            "event_id": "test1234887",
            "exam_name": "test exam",
            "examinee_name": "test candidate",
            "notes": "test notes",
            "office_id": seeded_data["office_ids"]["test_office"],
            "payee_ind": 0,
            "receipt_sent_ind": 0,
            "sbc_managed_ind": 0,
            "exam_returned_ind": 0,
            "exam_written_ind": 0,
            "number_of_students": 1,
        }

        offset_exam = ExamSchema().load(
            {
                **base_payload,
                "exam_received_date": "2026-04-17T07:00:00+00:00",
            }
        )
        z_exam = ExamSchema().load(
            {
                **base_payload,
                "exam_received_date": "2026-04-17T07:00:00Z",
            }
        )

        assert offset_exam.exam_received_date.isoformat() == (
            "2026-04-17T07:00:00+00:00"
        )
        assert z_exam.exam_received_date.isoformat() == "2026-04-17T07:00:00+00:00"


def test_no_schema_explicitly_uses_strict_literal_z_datetime_format(app, seeded_database):
    """Assert DateTime fields do not opt into literal-Z-only parsing."""
    del seeded_database

    with app.app_context():
        strict_fields = []
        for schema_cls in _schema_classes():
            source = inspect.getsource(sys.modules[schema_cls.__module__])
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                if not (
                    isinstance(node.func, ast.Attribute)
                    and node.func.attr == "DateTime"
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "fields"
                ):
                    continue
                for keyword in node.keywords:
                    if (
                        keyword.arg == "format"
                        and isinstance(keyword.value, ast.Constant)
                        and keyword.value.value == "%Y-%m-%dT%H:%M:%SZ"
                    ):
                        strict_fields.append(f"{schema_cls.__module__}:{node.lineno}")

        assert strict_fields == []


def test_booking_schema_post_dump_supports_single_and_many(app, seeded_data):
    """Assert that booking post-dump hooks normalize invigilators for single and many dumps."""
    with app.app_context():
        from app.models.bookings import Booking, Invigilator, Room
        from app.models.theq import Office
        from app.schemas.bookings import BookingSchema
        from qsystem import db

        office = db.session.get(Office, seeded_data["office_ids"]["test_office"])
        room = db.session.get(Room, seeded_data["room_id"])
        invigilators = [
            db.session.get(Invigilator, invigilator_id)
            for invigilator_id in seeded_data["invigilator_ids"][:2]
        ]

        booking = Booking(
            booking_id=3001,
            office_id=office.office_id,
            office=office,
            room_id=room.room_id,
            room=room,
            start_time=datetime(2026, 3, 25, 16, 0, tzinfo=timezone.utc),
            end_time=datetime(2026, 3, 25, 17, 0, tzinfo=timezone.utc),
            booking_name="Board Meeting",
            sbc_staff_invigilated=0,
            stat_flag=False,
            invigilators=invigilators,
        )

        schema = BookingSchema()
        dumped_single = schema.dump(booking)
        dumped_many = schema.dump([booking], many=True)

        expected_invigilators = [
            invigilator.invigilator_id for invigilator in invigilators
        ]
        assert dumped_single["invigilators"] == expected_invigilators
        assert dumped_many[0]["invigilators"] == expected_invigilators


def test_csr_schema_post_dump_supports_single_and_many(app, seeded_data):
    """Assert that CSR post-dump hooks preserve the counter alias for single and many dumps."""
    del seeded_data

    with app.app_context():
        from app.models.theq import CSR
        from app.schemas.theq import CSRSchema

        csrs = CSR.query.order_by(CSR.csr_id).limit(2).all()
        assert len(csrs) == 2

        schema = CSRSchema()
        dumped_single = schema.dump(csrs[0])
        dumped_many = schema.dump(csrs, many=True)

        assert dumped_single["counter"] == dumped_single["counter_id"]
        assert [csr["counter"] for csr in dumped_many] == [
            csr["counter_id"] for csr in dumped_many
        ]


def test_appointment_availability_schema_smoke(app, seeded_data):
    """Assert that appointment availability schema dumps the core slot fields needed by the API."""
    with app.app_context():
        from app.models.bookings import Appointment
        from app.schemas.bookings.appointment_availability_schema import (
            AppointmentAvailabilitySchema,
        )

        appointment = Appointment(
            appointment_id=4001,
            office_id=seeded_data["office_ids"]["test_office"],
            service_id=seeded_data["service_ids"]["msp"],
            citizen_id=1234,
            start_time=datetime(2026, 3, 25, 18, 0, tzinfo=timezone.utc),
            end_time=datetime(2026, 3, 25, 18, 30, tzinfo=timezone.utc),
            citizen_name="Pat Citizen",
            blackout_flag="N",
        )

        dumped = AppointmentAvailabilitySchema().dump(appointment)

        assert dumped["appointment_id"] == 4001
        assert dumped["office_id"] == seeded_data["office_ids"]["test_office"]
        assert dumped["service_id"] == seeded_data["service_ids"]["msp"]
        assert dumped["citizen_name"] == "Pat Citizen"
