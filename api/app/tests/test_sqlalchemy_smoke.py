from datetime import datetime, timedelta, timezone

from sqlalchemy import text


def test_app_boots_with_disposable_postgres(app, postgres_database):
    assert app.config["SQLALCHEMY_DATABASE_URI"] == postgres_database["database_uri"]

    with app.app_context():
        assert app.extensions["sqlalchemy"]


def test_db_current_command_runs(cli_runner):
    result = cli_runner.invoke(args=["db", "current"])

    assert result.exit_code == 0, result.output


def test_db_upgrade_command_runs(migrated_database):
    assert migrated_database.exit_code == 0, migrated_database.output


def test_healthz_uses_database_connection(client, migrated_database):
    response = client.get("/api/v1/healthz/")

    assert response.status_code == 200
    assert response.get_json() == {"message": "api is healthy"}


def test_appointment_crud_and_version_rows(app, db, migrated_database):
    from app.models.bookings import Appointment
    from app.models.theq.office import Office
    from app.models.theq.smartboard import SmartBoard
    from app.models.theq.timezone import Timezone

    with app.app_context():
        smartboard = SmartBoard(sb_type="callbyticket")
        timezone_row = Timezone(timezone_name="Canada/Pacific")
        db.session.add_all([smartboard, timezone_row])
        db.session.commit()

        office = Office(
            office_name="SQLAlchemy Smoke Office",
            office_number=9999,
            sb_id=smartboard.sb_id,
            exams_enabled_ind=0,
            appointments_enabled_ind=1,
            timezone_id=timezone_row.timezone_id,
        )
        db.session.add(office)
        db.session.commit()

        appointment = Appointment(
            office_id=office.office_id,
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(minutes=30),
            citizen_name="Smoke Test Citizen",
            contact_information="smoke@example.com",
        )
        db.session.add(appointment)
        db.session.commit()

        appointment.comments = "updated by smoke suite"
        db.session.add(appointment)
        db.session.commit()

        db.session.delete(appointment)
        db.session.commit()

        version_count = db.session.execute(
            text(
                "SELECT COUNT(*) FROM appointment_version WHERE appointment_id = :appointment_id"
            ),
            {"appointment_id": appointment.appointment_id},
        ).scalar_one()
        transaction_count = db.session.execute(
            text("SELECT COUNT(*) FROM transaction")
        ).scalar_one()

        assert version_count >= 2
        assert transaction_count >= 2


def test_local_utc_type_round_trips_booking_appointment_and_citizen(app, db, migrated_database):
    from app.models.bookings import Appointment, Booking, Room
    from app.models.theq.citizen import Citizen
    from app.models.theq.citizen_state import CitizenState
    from app.models.theq.office import Office
    from app.models.theq.smartboard import SmartBoard
    from app.models.theq.timezone import Timezone

    with app.app_context():
        smartboard = SmartBoard(sb_type="callbyticket")
        timezone_row = Timezone(timezone_name="Canada/Pacific")
        citizen_state = CitizenState(cs_state_name="Waiting", cs_state_desc="Waiting")
        db.session.add_all([smartboard, timezone_row, citizen_state])
        db.session.commit()

        office = Office(
            office_name="UTC Smoke Office",
            office_number=9998,
            sb_id=smartboard.sb_id,
            exams_enabled_ind=0,
            appointments_enabled_ind=1,
            timezone_id=timezone_row.timezone_id,
        )
        db.session.add(office)
        db.session.commit()

        room = Room(
            office_id=office.office_id,
            room_name="UTC Smoke Room",
            capacity=4,
            color="blue",
        )
        db.session.add(room)
        db.session.commit()

        booking = Booking(
            office_id=office.office_id,
            room_id=room.room_id,
            start_time=datetime(2026, 3, 25, 16, 0, tzinfo=timezone.utc),
            end_time=datetime(2026, 3, 25, 17, 0, tzinfo=timezone.utc),
        )
        citizen = Citizen(
            office_id=office.office_id,
            cs_id=citizen_state.cs_id,
            start_time=datetime(2026, 3, 25, 15, 30, tzinfo=timezone.utc),
        )
        appointment = Appointment(
            office_id=office.office_id,
            start_time=datetime(2026, 3, 25, 18, 0, tzinfo=timezone.utc),
            end_time=datetime(2026, 3, 25, 18, 30, tzinfo=timezone.utc),
            citizen_name="UTC Smoke Citizen",
            contact_information="utc@example.com",
        )
        db.session.add_all([booking, citizen, appointment])
        db.session.commit()

        appointment.comments = "updated"
        db.session.add(appointment)
        db.session.commit()

        booking_id = booking.booking_id
        citizen_id = citizen.citizen_id
        appointment_id = appointment.appointment_id

        db.session.expunge_all()

        saved_booking = db.session.get(Booking, booking_id)
        saved_citizen = db.session.get(Citizen, citizen_id)
        saved_appointment = db.session.get(Appointment, appointment_id)

        assert saved_booking.start_time.utcoffset().total_seconds() == 0
        assert saved_booking.end_time.utcoffset().total_seconds() == 0
        assert saved_citizen.created_at.utcoffset().total_seconds() == 0
        assert saved_appointment.start_time.utcoffset().total_seconds() == 0
        assert saved_appointment.end_time.utcoffset().total_seconds() == 0
        assert saved_appointment.created_at.utcoffset().total_seconds() == 0
        assert saved_appointment.updated_at.utcoffset().total_seconds() == 0
