UTC_DATETIME_SCHEMA = {
    "type": "string",
    "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$",
}
ISO_DATETIME_SCHEMA = {
    "type": "string",
    "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:(?:Z|[+-]\d{2}:\d{2}))?$",
}
DATE_KEY_SCHEMA = {"type": "string", "pattern": r"^\d{2}/\d{2}/\d{4}$"}


def nullable(schema):
    return {"anyOf": [schema, {"type": "null"}]}


def object_schema(*, required, properties, additional_properties=False):
    return {
        "type": "object",
        "required": list(required),
        "properties": properties,
        "additionalProperties": additional_properties,
    }


TIMEZONE_SCHEMA = object_schema(
    required=["timezone_id", "timezone_name"],
    properties={
        "timezone_id": {"type": "integer"},
        "timezone_name": {"type": "string"},
    },
)

COUNTER_SCHEMA = object_schema(
    required=["counter_id", "counter_name"],
    properties={
        "counter_id": {"type": "integer"},
        "counter_name": {"type": "string"},
    },
)

SMARTBOARD_SCHEMA = object_schema(
    required=["sb_id", "sb_type"],
    properties={
        "sb_id": {"type": "integer"},
        "sb_type": {"type": "string"},
    },
)

CHANNEL_SCHEMA = object_schema(
    required=["channel_id", "channel_name"],
    properties={
        "channel_id": {"type": "integer"},
        "channel_name": {"type": "string"},
    },
)

SERVICE_PARENT_SCHEMA = object_schema(
    required=["service_name"],
    properties={"service_name": {"type": "string"}},
)

SERVICE_SCHEMA = object_schema(
    required=[
        "service_id",
        "service_name",
        "parent_id",
        "display_dashboard_ind",
        "actual_service_ind",
    ],
    properties={
        "service_id": {"type": "integer"},
        "service_code": nullable({"type": "string"}),
        "service_name": {"type": "string"},
        "service_desc": nullable({"type": "string"}),
        "parent": nullable(SERVICE_PARENT_SCHEMA),
        "parent_id": nullable({"type": "integer"}),
        "deleted": nullable(ISO_DATETIME_SCHEMA),
        "prefix": nullable({"type": "string"}),
        "display_dashboard_ind": {"type": "integer"},
        "actual_service_ind": {"type": "integer"},
        "external_service_name": nullable({"type": "string"}),
        "online_link": nullable({"type": "string"}),
        "online_availability": nullable({"type": "string"}),
        "timeslot_duration": nullable({"type": "integer"}),
        "email_paragraph": nullable({"type": "string"}),
        "css_colour": nullable({"type": "string"}),
        "is_dlkt": nullable({"type": "boolean"}),
    },
)

CATEGORY_SCHEMA = SERVICE_SCHEMA

SERVICE_REQUEST_SERVICE_SCHEMA = object_schema(
    required=["service_name"],
    properties={
        "service_name": {"type": "string"},
        "parent": nullable(SERVICE_PARENT_SCHEMA),
        "parent_id": nullable({"type": "integer"}),
        "external_service_name": nullable({"type": "string"}),
        "online_link": nullable({"type": "string"}),
        "online_availability": nullable({"type": "string"}),
        "timeslot_duration": nullable({"type": "integer"}),
        "email_paragraph": nullable({"type": "string"}),
        "css_colour": nullable({"type": "string"}),
        "is_dlkt": nullable({"type": "boolean"}),
    },
)

ROLE_SCHEMA = object_schema(
    required=["role_id", "role_code"],
    properties={
        "role_id": {"type": "integer"},
        "role_code": {"type": "string"},
        "role_desc": nullable({"type": "string"}),
    },
)

CSR_STATE_SCHEMA = object_schema(
    required=["csr_state_id", "csr_state_name"],
    properties={
        "csr_state_id": {"type": "integer"},
        "csr_state_name": {"type": "string"},
        "csr_state_desc": nullable({"type": "string"}),
    },
)

OFFICE_SUMMARY_SCHEMA = object_schema(
    required=["office_id", "office_name", "office_number", "timezone"],
    properties={
        "office_id": {"type": "integer"},
        "office_name": {"type": "string"},
        "office_number": {"type": "integer"},
        "appointments_enabled_ind": nullable({"type": "integer"}),
        "exams_enabled_ind": nullable({"type": "integer"}),
        "timezone": TIMEZONE_SCHEMA,
    },
)

OFFICE_APPOINTMENT_SCHEMA = object_schema(
    required=["office_id", "office_name", "office_number", "timezone"],
    properties={
        "office_id": {"type": "integer"},
        "office_name": {"type": "string"},
        "office_number": {"type": "integer"},
        "sb_id": nullable({"type": "integer"}),
        "deleted": nullable(ISO_DATETIME_SCHEMA),
        "exams_enabled_ind": nullable({"type": "integer"}),
        "appointments_enabled_ind": nullable({"type": "integer"}),
        "max_person_appointment_per_day": nullable({"type": "integer"}),
        "telephone": nullable({"type": "string"}),
        "appointments_days_limit": nullable({"type": "integer"}),
        "appointment_duration": nullable({"type": "integer"}),
        "timezone": TIMEZONE_SCHEMA,
        "latitude": nullable({"type": "number"}),
        "longitude": nullable({"type": "number"}),
        "office_appointment_message": nullable({"type": "string"}),
        "civic_address": nullable({"type": "string"}),
        "online_status": nullable({"type": "string"}),
        "optout_status": nullable({"type": "integer"}),
        "external_map_link": nullable({"type": "string"}),
        "check_in_notification": nullable({"type": "integer"}),
        "check_in_reminder_msg": nullable({"type": "string"}),
        "automatic_reminder_at": nullable({"type": "integer"}),
        "currently_waiting": nullable({"type": "integer"}),
        "digital_signage_message": nullable({"type": "integer"}),
        "digital_signage_message_1": nullable({"type": "string"}),
        "digital_signage_message_2": nullable({"type": "string"}),
        "digital_signage_message_3": nullable({"type": "string"}),
        "show_currently_waiting_bottom": nullable({"type": "integer"}),
    },
)

ROOM_SCHEMA = object_schema(
    required=["room_id", "room_name", "capacity", "color", "office"],
    properties={
        "room_id": {"type": "integer"},
        "room_name": {"type": "string"},
        "capacity": {"type": "integer"},
        "color": nullable({"type": "string"}),
        "deleted": nullable({"type": "string"}),
        "office": OFFICE_SUMMARY_SCHEMA,
    },
)

BOOKING_ROOM_SCHEMA = object_schema(
    required=["room_id", "room_name", "capacity", "color"],
    properties={
        "room_id": {"type": "integer"},
        "room_name": {"type": "string"},
        "capacity": {"type": "integer"},
        "color": nullable({"type": "string"}),
        "deleted": nullable({"type": "string"}),
    },
)

INVIGILATOR_SCHEMA = object_schema(
    required=[
        "invigilator_id",
        "invigilator_name",
        "shadow_count",
        "shadow_flag",
        "office_id",
    ],
    properties={
        "invigilator_id": {"type": "integer"},
        "invigilator_name": {"type": "string"},
        "shadow_count": {"type": "integer"},
        "shadow_flag": {"type": "string"},
        "office_id": {"type": "integer"},
        "contact_phone": nullable({"type": "string"}),
        "contact_email": nullable({"type": "string"}),
        "contract_number": nullable({"type": "string"}),
        "contract_expiry_date": nullable({"type": "string"}),
        "invigilator_notes": nullable({"type": "string"}),
        "deleted": nullable({"type": "string"}),
        "office": OFFICE_SUMMARY_SCHEMA,
    },
)

EXAM_TYPE_SCHEMA = object_schema(
    required=[
        "exam_type_id",
        "exam_type_name",
        "number_of_hours",
        "number_of_minutes",
        "group_exam_ind",
        "pesticide_exam_ind",
    ],
    properties={
        "exam_type_id": {"type": "integer"},
        "exam_type_name": {"type": "string"},
        "exam_color": nullable({"type": "string"}),
        "number_of_hours": {"type": "integer"},
        "number_of_minutes": {"type": "integer"},
        "method_type": nullable({"type": "string"}),
        "ita_ind": nullable({"type": "integer"}),
        "group_exam_ind": {"type": "integer"},
        "pesticide_exam_ind": {"type": "integer"},
        "deleted": nullable({"type": "string"}),
    },
)

PERIOD_STATE_SCHEMA = object_schema(
    required=["ps_name"],
    properties={
        "ps_id": nullable({"type": "integer"}),
        "ps_name": {"type": "string"},
        "ps_desc": nullable({"type": "string"}),
        "ps_number": nullable({"type": "integer"}),
    },
)

SR_STATE_SCHEMA = object_schema(
    required=["sr_code"],
    properties={
        "sr_state_id": nullable({"type": "integer"}),
        "sr_code": {"type": "string"},
        "sr_state_desc": nullable({"type": "string"}),
    },
)

CITIZEN_STATE_SCHEMA = object_schema(
    required=["cs_state_name"],
    properties={
        "cs_id": nullable({"type": "integer"}),
        "cs_state_name": {"type": "string"},
        "cs_state_desc": nullable({"type": "string"}),
    },
)

PERIOD_CSR_SCHEMA = object_schema(
    required=["username", "counter_id", "counter"],
    properties={
        "username": {"type": "string"},
        "counter_id": {"type": "integer"},
        "counter": {"type": "integer"},
        "qt_xn_csr_ind": nullable({"type": "integer"}),
    },
)

PERIOD_SCHEMA = object_schema(
    required=["period_id", "time_start", "ps", "csr"],
    properties={
        "period_id": {"type": "integer"},
        "sr_id": nullable({"type": "integer"}),
        "csr_id": nullable({"type": "integer"}),
        "reception_csr_ind": nullable({"type": "integer"}),
        "ps_id": nullable({"type": "integer"}),
        "time_start": nullable(ISO_DATETIME_SCHEMA),
        "time_end": nullable(ISO_DATETIME_SCHEMA),
        "ps": PERIOD_STATE_SCHEMA,
        "csr": PERIOD_CSR_SCHEMA,
    },
)

SERVICE_NAME_ONLY_SCHEMA = object_schema(
    required=["service_name"],
    properties={"service_name": {"type": "string"}},
)

CHANNEL_NAME_ONLY_SCHEMA = object_schema(
    required=["channel_name"],
    properties={"channel_name": {"type": "string"}},
)

SERVICE_REQUEST_SCHEMA = object_schema(
    required=[
        "sr_id",
        "citizen_id",
        "channel_id",
        "service_id",
        "quantity",
        "sr_number",
        "periods",
        "sr_state",
        "service",
        "channel",
    ],
    properties={
        "sr_id": {"type": "integer"},
        "citizen_id": {"type": "integer"},
        "channel_id": {"type": "integer"},
        "service_id": {"type": "integer"},
        "quantity": {"type": "integer"},
        "sr_number": {"type": "integer"},
        "periods": {"type": "array", "items": PERIOD_SCHEMA},
        "sr_state": SR_STATE_SCHEMA,
        "service": SERVICE_REQUEST_SERVICE_SCHEMA,
        "channel": CHANNEL_NAME_ONLY_SCHEMA,
    },
)

CITIZEN_SCHEMA = object_schema(
    required=["citizen_id", "citizen_name", "office_id", "service_reqs", "cs"],
    properties={
        "citizen_id": {"type": "integer"},
        "citizen_name": nullable({"type": "string"}),
        "office_id": {"type": "integer"},
        "ticket_number": nullable({"type": "string"}),
        "citizen_comments": nullable({"type": "string"}),
        "qt_xn_citizen_ind": nullable({"type": "integer"}),
        "counter_id": nullable({"type": "integer"}),
        "start_time": nullable(UTC_DATETIME_SCHEMA),
        "accurate_time_ind": nullable({"type": "integer"}),
        "service_reqs": {"type": "array", "items": SERVICE_REQUEST_SCHEMA},
        "cs": CITIZEN_STATE_SCHEMA,
        "priority": nullable({"type": "integer"}),
        "user_id": nullable({"type": "integer"}),
        "notification_sent_time": nullable(ISO_DATETIME_SCHEMA),
        "notification_phone": nullable({"type": "string"}),
        "notification_email": nullable({"type": "string"}),
        "reminder_flag": nullable({"type": "integer"}),
        "walkin_unique_id": nullable({"type": "string"}),
        "automatic_reminder_flag": nullable({"type": "integer"}),
        "created_at": nullable(ISO_DATETIME_SCHEMA),
    },
)

SERVICE_REQUEST_CITIZEN_SCHEMA = object_schema(
    required=["citizen_id", "citizen_name", "office_id", "cs"],
    properties={
        "citizen_id": {"type": "integer"},
        "citizen_name": nullable({"type": "string"}),
        "office_id": {"type": "integer"},
        "ticket_number": nullable({"type": "string"}),
        "citizen_comments": nullable({"type": "string"}),
        "qt_xn_citizen_ind": nullable({"type": "integer"}),
        "counter_id": nullable({"type": "integer"}),
        "start_time": nullable(UTC_DATETIME_SCHEMA),
        "accurate_time_ind": nullable({"type": "integer"}),
        "cs": CITIZEN_STATE_SCHEMA,
        "priority": nullable({"type": "integer"}),
        "user_id": nullable({"type": "integer"}),
        "notification_sent_time": nullable(ISO_DATETIME_SCHEMA),
        "notification_phone": nullable({"type": "string"}),
        "notification_email": nullable({"type": "string"}),
        "reminder_flag": nullable({"type": "integer"}),
        "walkin_unique_id": nullable({"type": "string"}),
        "automatic_reminder_flag": nullable({"type": "integer"}),
        "created_at": nullable(ISO_DATETIME_SCHEMA),
    },
)

SERVICE_REQUEST_SCHEMA["properties"]["citizen"] = SERVICE_REQUEST_CITIZEN_SCHEMA

OFFICE_SCHEMA = object_schema(
    required=[
        "office_id",
        "office_name",
        "office_number",
        "timezone",
        "counters",
        "timeslots",
    ],
    properties={
        "office_id": {"type": "integer"},
        "office_name": {"type": "string"},
        "office_number": {"type": "integer"},
        "sb_id": nullable({"type": "integer"}),
        "deleted": nullable(ISO_DATETIME_SCHEMA),
        "exams_enabled_ind": nullable({"type": "integer"}),
        "appointments_enabled_ind": nullable({"type": "integer"}),
        "max_person_appointment_per_day": nullable({"type": "integer"}),
        "telephone": nullable({"type": "string"}),
        "appointments_days_limit": nullable({"type": "integer"}),
        "appointment_duration": nullable({"type": "integer"}),
        "sb": nullable(SMARTBOARD_SCHEMA),
        "timezone": TIMEZONE_SCHEMA,
        "counters": {"type": "array", "items": COUNTER_SCHEMA},
        "quick_list": {"type": "array", "items": SERVICE_SCHEMA},
        "back_office_list": {"type": "array", "items": SERVICE_SCHEMA},
        "timeslots": {"type": "array", "items": {"type": "object"}},
        "latitude": nullable({"type": "number"}),
        "longitude": nullable({"type": "number"}),
        "office_appointment_message": nullable({"type": "string"}),
        "civic_address": nullable({"type": "string"}),
        "online_status": nullable({"type": "string"}),
        "optout_status": nullable({"type": "integer"}),
        "external_map_link": nullable({"type": "string"}),
        "check_in_notification": nullable({"type": "integer"}),
        "check_in_reminder_msg": nullable({"type": "string"}),
        "automatic_reminder_at": nullable({"type": "integer"}),
        "currently_waiting": nullable({"type": "integer"}),
        "digital_signage_message": nullable({"type": "integer"}),
        "digital_signage_message_1": nullable({"type": "string"}),
        "digital_signage_message_2": nullable({"type": "string"}),
        "digital_signage_message_3": nullable({"type": "string"}),
        "show_currently_waiting_bottom": nullable({"type": "integer"}),
    },
)

ROOM_SCHEMA["properties"]["office"] = OFFICE_SCHEMA
INVIGILATOR_SCHEMA["properties"]["office"] = OFFICE_SCHEMA

APPOINTMENT_SCHEMA = object_schema(
    required=[
        "appointment_id",
        "office_id",
        "start_time",
        "end_time",
        "citizen_name",
    ],
    properties={
        "appointment_id": {"type": "integer"},
        "office_id": {"type": "integer"},
        "service_id": nullable({"type": "integer"}),
        "citizen_id": nullable({"type": "integer"}),
        "start_time": nullable(ISO_DATETIME_SCHEMA),
        "end_time": nullable(ISO_DATETIME_SCHEMA),
        "checked_in_time": nullable(ISO_DATETIME_SCHEMA),
        "comments": nullable({"type": "string"}),
        "citizen_name": {"type": "string"},
        "contact_information": nullable({"type": "string"}),
        "blackout_flag": nullable({"type": "string"}),
        "recurring_uuid": nullable({"type": "string"}),
        "online_flag": nullable({"type": "boolean"}),
        "is_draft": nullable({"type": "boolean"}),
        "stat_flag": nullable({"type": "boolean"}),
        "office": nullable(OFFICE_APPOINTMENT_SCHEMA),
        "service": nullable(SERVICE_SCHEMA),
    },
)

BOOKING_SCHEMA = object_schema(
    required=["booking_id", "office_id", "start_time", "end_time", "invigilators"],
    properties={
        "booking_id": {"type": "integer"},
        "booking_name": nullable({"type": "string"}),
        "end_time": nullable(ISO_DATETIME_SCHEMA),
        "fees": nullable({"type": "string"}),
        "room_id": nullable({"type": "integer"}),
        "start_time": nullable(ISO_DATETIME_SCHEMA),
        "shadow_invigilator_id": nullable({"type": "integer"}),
        "office_id": {"type": "integer"},
        "sbc_staff_invigilated": nullable({"type": "integer"}),
        "booking_contact_information": nullable({"type": "string"}),
        "blackout_flag": nullable({"type": "string"}),
        "blackout_notes": nullable({"type": "string"}),
        "recurring_uuid": nullable({"type": "string"}),
        "stat_flag": nullable({"type": "boolean"}),
        "room": nullable(BOOKING_ROOM_SCHEMA),
        "office": nullable(OFFICE_SUMMARY_SCHEMA),
        "invigilators": {"type": "array", "items": {"type": "integer"}},
    },
)

EXAM_SCHEMA = object_schema(
    required=[
        "exam_id",
        "office_id",
        "exam_type_id",
        "exam_name",
        "exam_written_ind",
    ],
    properties={
        "booking_id": nullable({"type": "integer"}),
        "deleted_date": nullable({"type": "string"}),
        "event_id": nullable({"type": "string"}),
        "exam_destroyed_date": nullable({"type": "string"}),
        "exam_id": {"type": "integer"},
        "exam_method": nullable({"type": "string"}),
        "exam_name": {"type": "string"},
        "exam_received": nullable({"type": "integer"}),
        "exam_received_date": nullable(ISO_DATETIME_SCHEMA),
        "exam_type_id": {"type": "integer"},
        "examinee_name": nullable({"type": "string"}),
        "examinee_phone": nullable({"type": "string"}),
        "examinee_email": nullable({"type": "string"}),
        "expiry_date": nullable(ISO_DATETIME_SCHEMA),
        "notes": nullable({"type": "string"}),
        "number_of_students": nullable({"type": "integer"}),
        "office_id": {"type": "integer"},
        "invigilator_id": nullable({"type": "integer"}),
        "session_number": nullable({"type": "integer"}),
        "exam_returned_ind": nullable({"type": "integer"}),
        "exam_returned_date": nullable(ISO_DATETIME_SCHEMA),
        "exam_returned_tracking_number": nullable({"type": "string"}),
        "exam_written_ind": {"type": "integer"},
        "upload_received_ind": nullable({"type": "integer"}),
        "offsite_location": nullable({"type": "string"}),
        "sbc_managed_ind": nullable({"type": "integer"}),
        "receipt": nullable({"type": "string"}),
        "receipt_number": nullable({"type": "string"}),
        "fees": nullable({"type": "string"}),
        "payee_ind": nullable({"type": "integer"}),
        "receipt_sent_ind": nullable({"type": "integer"}),
        "payee_name": nullable({"type": "string"}),
        "payee_email": nullable({"type": "string"}),
        "payee_phone": nullable({"type": "string"}),
        "bcmp_job_id": nullable({"type": "string"}),
        "is_pesticide": nullable({"type": "integer"}),
        "candidates_list": nullable({"type": "object"}),
        "booking": nullable(BOOKING_SCHEMA),
        "exam_type": nullable(EXAM_TYPE_SCHEMA),
        "invigilator": nullable(INVIGILATOR_SCHEMA),
        "office": nullable(OFFICE_SUMMARY_SCHEMA),
    },
)

PUBLIC_USER_SCHEMA = object_schema(
    required=[
        "telephone",
        "send_email_reminders",
        "email",
        "display_name",
        "last_name",
        "username",
        "user_id",
        "send_sms_reminders",
    ],
    properties={
        "telephone": nullable({"type": "string"}),
        "send_email_reminders": nullable({"type": "boolean"}),
        "email": nullable({"type": "string"}),
        "display_name": nullable({"type": "string"}),
        "last_name": nullable({"type": "string"}),
        "username": {"type": "string"},
        "user_id": {"type": "integer"},
        "send_sms_reminders": nullable({"type": "boolean"}),
    },
)

SLOT_SCHEMA = object_schema(
    required=["start_time", "end_time", "no_of_slots"],
    properties={
        "start_time": {"type": "string", "pattern": r"^\d{2}:\d{2}$"},
        "end_time": {"type": "string", "pattern": r"^\d{2}:\d{2}$"},
        "no_of_slots": {"type": "integer"},
    },
)

SLOTS_SCHEMA = {
    "type": "object",
    "patternProperties": {
        DATE_KEY_SCHEMA["pattern"]: {"type": "array", "items": SLOT_SCHEMA}
    },
    "additionalProperties": False,
}

REMINDER_APPOINTMENT_SCHEMA = object_schema(
    required=[
        "formatted_date",
        "day",
        "email",
        "display_name",
        "location",
        "duration",
        "telephone",
        "service_email_paragraph",
        "office_email_paragraph",
        "service_name",
        "civic_address",
        "user_telephone",
    ],
    properties={
        "formatted_date": {"type": "string"},
        "day": nullable({"type": "string"}),
        "email": nullable({"type": "string"}),
        "display_name": {"type": "string"},
        "location": {"type": "string"},
        "duration": {"type": "integer"},
        "telephone": nullable({"type": "string"}),
        "service_email_paragraph": nullable({"type": "string"}),
        "office_email_paragraph": nullable({"type": "string"}),
        "service_name": {"type": "string"},
        "civic_address": nullable({"type": "string"}),
        "user_telephone": nullable({"type": "string"}),
    },
)

ERRORS_SCHEMA = {"type": "object"}

CITIZEN_RESPONSE_SCHEMA = object_schema(
    required=["citizen", "errors"],
    properties={"citizen": CITIZEN_SCHEMA, "errors": ERRORS_SCHEMA},
)

SERVICE_REQUEST_RESPONSE_SCHEMA = object_schema(
    required=["service_request", "errors"],
    properties={
        "service_request": SERVICE_REQUEST_SCHEMA,
        "errors": ERRORS_SCHEMA,
    },
)

SERVICE_REQUEST_LIST_RESPONSE_SCHEMA = object_schema(
    required=["service_requests", "errors"],
    properties={
        "service_requests": {"type": "array", "items": SERVICE_REQUEST_SCHEMA},
        "errors": ERRORS_SCHEMA,
    },
)

APPOINTMENT_RESPONSE_SCHEMA = object_schema(
    required=["appointment", "errors"],
    properties={"appointment": APPOINTMENT_SCHEMA, "errors": ERRORS_SCHEMA},
)

APPOINTMENT_LIST_RESPONSE_SCHEMA = object_schema(
    required=["appointments", "errors"],
    properties={
        "appointments": {"type": "array", "items": APPOINTMENT_SCHEMA},
        "errors": ERRORS_SCHEMA,
    },
)

BOOKING_RESPONSE_SCHEMA = object_schema(
    required=["booking", "errors"],
    properties={"booking": BOOKING_SCHEMA, "errors": ERRORS_SCHEMA},
)

BOOKING_LIST_RESPONSE_SCHEMA = object_schema(
    required=["bookings", "errors"],
    properties={
        "bookings": {"type": "array", "items": BOOKING_SCHEMA},
        "errors": ERRORS_SCHEMA,
    },
)

EXAM_RESPONSE_SCHEMA = object_schema(
    required=["exam", "errors"],
    properties={"exam": EXAM_SCHEMA, "errors": ERRORS_SCHEMA},
)

EXAM_LIST_RESPONSE_SCHEMA = object_schema(
    required=["exams", "errors"],
    properties={
        "exams": {"type": "array", "items": EXAM_SCHEMA},
        "errors": ERRORS_SCHEMA,
    },
)

CHANNEL_LIST_RESPONSE_SCHEMA = object_schema(
    required=["channels", "errors"],
    properties={
        "channels": {"type": "array", "items": CHANNEL_SCHEMA},
        "errors": ERRORS_SCHEMA,
    },
)

CATEGORY_LIST_RESPONSE_SCHEMA = object_schema(
    required=["categories", "errors"],
    properties={
        "categories": {"type": "array", "items": CATEGORY_SCHEMA},
        "errors": ERRORS_SCHEMA,
    },
)

SERVICE_LIST_RESPONSE_SCHEMA = object_schema(
    required=["services", "errors"],
    properties={
        "services": {"type": "array", "items": SERVICE_SCHEMA},
        "errors": ERRORS_SCHEMA,
    },
)

OFFICE_LIST_RESPONSE_SCHEMA = object_schema(
    required=["offices", "errors"],
    properties={
        "offices": {"type": "array", "items": OFFICE_SCHEMA},
        "errors": ERRORS_SCHEMA,
    },
)

ROOM_LIST_RESPONSE_SCHEMA = object_schema(
    required=["rooms", "errors"],
    properties={
        "rooms": {"type": "array", "items": ROOM_SCHEMA},
        "errors": ERRORS_SCHEMA,
    },
)

INVIGILATOR_LIST_RESPONSE_SCHEMA = object_schema(
    required=["invigilators", "errors"],
    properties={
        "invigilators": {"type": "array", "items": INVIGILATOR_SCHEMA},
        "errors": ERRORS_SCHEMA,
    },
)

EXAM_TYPE_LIST_RESPONSE_SCHEMA = object_schema(
    required=["exam_types", "errors"],
    properties={
        "exam_types": {"type": "array", "items": EXAM_TYPE_SCHEMA},
        "errors": ERRORS_SCHEMA,
    },
)

CSR_SCHEMA = object_schema(
    required=[
        "csr_id",
        "username",
        "office_id",
        "role_id",
        "csr_state_id",
        "counter_id",
        "counter",
        "role",
        "office",
        "finance_designate",
        "ita2_designate",
        "pesticide_designate",
        "qt_xn_csr_ind",
    ],
    properties={
        "csr_id": {"type": "integer"},
        "username": {"type": "string"},
        "office_id": {"type": "integer"},
        "role_id": {"type": "integer"},
        "receptionist_ind": nullable({"type": "integer"}),
        "deleted": nullable(ISO_DATETIME_SCHEMA),
        "csr_state_id": {"type": "integer"},
        "counter_id": {"type": "integer"},
        "counter": {"type": "integer"},
        "csr_state": nullable(CSR_STATE_SCHEMA),
        "office": OFFICE_SCHEMA,
        "role": ROLE_SCHEMA,
        "office_manager": nullable({"type": "integer"}),
        "pesticide_designate": nullable({"type": "integer"}),
        "qt_xn_csr_ind": nullable({"type": "integer"}),
        "finance_designate": nullable({"type": "integer"}),
        "ita2_designate": nullable({"type": "integer"}),
    },
)

CSR_LIST_ITEM_SCHEMA = object_schema(
    required=[field for field in CSR_SCHEMA["required"] if field != "office"],
    properties={
        key: value for key, value in CSR_SCHEMA["properties"].items() if key != "office"
    },
)

CSR_LIST_RESPONSE_SCHEMA = object_schema(
    required=["csrs", "errors"],
    properties={
        "csrs": {"type": "array", "items": CSR_LIST_ITEM_SCHEMA},
        "errors": ERRORS_SCHEMA,
    },
)

CSR_ME_RESPONSE_SCHEMA = object_schema(
    required=[
        "csr",
        "attention_needed",
        "active_citizens",
        "back_office_display",
        "recurring_feature_flag",
        "errors",
    ],
    properties={
        "csr": CSR_SCHEMA,
        "attention_needed": {"type": "boolean"},
        "active_citizens": {"type": "array", "items": CITIZEN_SCHEMA},
        "back_office_display": {},
        "recurring_feature_flag": {},
        "errors": ERRORS_SCHEMA,
    },
)

SMARTBOARD_SIDE_MENU_RESPONSE_SCHEMA = object_schema(
    required=["office"],
    properties={"office": OFFICE_SCHEMA},
)

PUBLIC_USER_LIST_SCHEMA = {"type": "array", "items": PUBLIC_USER_SCHEMA}

USER_APPOINTMENTS_RESPONSE_SCHEMA = object_schema(
    required=["appointments"],
    properties={"appointments": {"type": "array", "items": APPOINTMENT_SCHEMA}},
)

REMINDER_RESPONSE_SCHEMA = object_schema(
    required=["appointments"],
    properties={
        "appointments": {"type": "array", "items": REMINDER_APPOINTMENT_SCHEMA}
    },
)
