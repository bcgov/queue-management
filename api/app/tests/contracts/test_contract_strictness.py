import pytest
from app.tests.contracts.conftest import validate_schema
from app.tests.contracts.schemas import (
    APPOINTMENT_RESPONSE_SCHEMA,
    CITIZEN_RESPONSE_SCHEMA,
    PUBLIC_USER_LIST_SCHEMA,
)

pytestmark = [pytest.mark.contracts, pytest.mark.smoke]


def test_appointment_contract_rejects_unexpected_fields():
    """Assert that appointment contracts fail when additive top-level fields sneak into the payload."""
    with pytest.raises(pytest.fail.Exception, match=r"appointment"):
        validate_schema(
            {
                "appointment": {
                    "appointment_id": 1,
                    "office_id": 2,
                    "service_id": 3,
                    "citizen_id": 4,
                    "start_time": "2026-03-25T18:00:00+00:00",
                    "end_time": "2026-03-25T18:30:00+00:00",
                    "checked_in_time": None,
                    "comments": "Comment",
                    "citizen_name": "Pat Citizen",
                    "contact_information": "pat@example.com",
                    "blackout_flag": "N",
                    "recurring_uuid": None,
                    "online_flag": False,
                    "is_draft": False,
                    "stat_flag": False,
                    "office": None,
                    "service": None,
                    "unexpected": "nope",
                },
                "errors": {},
            },
            APPOINTMENT_RESPONSE_SCHEMA,
        )


def test_public_user_contract_rejects_unexpected_fields():
    """Assert that public-user contracts reject additive profile fields."""
    with pytest.raises(pytest.fail.Exception, match=r"unexpected"):
        validate_schema(
            [
                {
                    "telephone": "2505550100",
                    "send_email_reminders": True,
                    "email": "public@example.com",
                    "display_name": "Public User",
                    "last_name": "User",
                    "username": "public@bceid",
                    "user_id": 7,
                    "send_sms_reminders": False,
                    "unexpected": True,
                }
            ],
            PUBLIC_USER_LIST_SCHEMA,
        )


def test_citizen_contract_rejects_unexpected_nested_service_request_fields():
    """Assert that nested citizen/service-request contracts reject additive fields."""
    with pytest.raises(pytest.fail.Exception, match=r"unexpected"):
        validate_schema(
            {
                "citizen": {
                    "citizen_id": 1,
                    "citizen_name": "Citizen",
                    "office_id": 2,
                    "ticket_number": None,
                    "citizen_comments": None,
                    "qt_xn_citizen_ind": 0,
                    "counter_id": None,
                    "start_time": "2026-03-25T18:00:00Z",
                    "accurate_time_ind": None,
                    "service_reqs": [
                        {
                            "sr_id": 9,
                            "citizen_id": 1,
                            "channel_id": 3,
                            "service_id": 4,
                            "quantity": 1,
                            "sr_number": 12,
                            "periods": [
                                {
                                    "period_id": 8,
                                    "sr_id": 9,
                                    "csr_id": 6,
                                    "reception_csr_ind": 0,
                                    "ps_id": 2,
                                    "time_start": "2026-03-25T18:00:00+00:00",
                                    "time_end": None,
                                    "ps": {
                                        "ps_id": 2,
                                        "ps_name": "Ticket Creation",
                                        "ps_desc": None,
                                        "ps_number": 2,
                                    },
                                    "csr": {
                                        "username": "tester",
                                        "counter_id": 2,
                                        "counter": 2,
                                        "qt_xn_csr_ind": 0,
                                    },
                                }
                            ],
                            "sr_state": {
                                "sr_state_id": 1,
                                "sr_code": "Active",
                                "sr_state_desc": None,
                            },
                            "service": {"service_name": "Property Tax"},
                            "channel": {"channel_name": "Phone"},
                            "unexpected": "x",
                        }
                    ],
                    "cs": {
                        "cs_id": 1,
                        "cs_state_name": "Active",
                        "cs_state_desc": None,
                    },
                    "priority": None,
                    "user_id": None,
                    "notification_sent_time": None,
                    "notification_phone": None,
                    "notification_email": None,
                    "reminder_flag": None,
                    "walkin_unique_id": None,
                    "automatic_reminder_flag": None,
                    "created_at": None,
                },
                "errors": {},
            },
            CITIZEN_RESPONSE_SCHEMA,
        )
