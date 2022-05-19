// Do not remove the eslint-disable camelcase below as the Python data model uses
// snake_case and Vue can't translate it to camelCase easily.
/* eslint-disable camelcase */
export interface TimeSlots {
  day_of_week: string[]
  end_time: string
  start_time: string
  no_of_slots: number
  day_str?: string
  end_time_str?: string
  start_time_str?: string
}

export interface TimeZone {
  timezone_id: number
  timezone_name: string
}

export interface Office {
  appointment_duration: number
  appointments_days_limit: number
  appointments_enabled_ind: boolean
  civic_address: string
  disable_online_appointment: boolean
  exams_enabled_ind: boolean
  latitude: number
  longitude: number
  max_person_appointment_per_day: number
  office_appointment_message: string
  office_id: number
  office_name: string
  office_number: number
  sb_id: number
  telephone: string
  timeslots: TimeSlots[]
  timezone: TimeZone
  online_status: string
  external_map_link: string,
  check_in_notification: number,
  check_in_reminder_msg: Text,
  automatic_reminder_at: number,
  currently_waiting: number,
  digital_signage_message: number,
  digital_signage_message_1: Text,
  digital_signage_message_2: Text,
  digital_signage_message_3: Text,
  show_currently_waiting_bottom: number,
}

export interface Offices {
  offices: Office[]
}
