/* eslint-disable camelcase */
export interface Office {
  appointment_duration: number
  appointments_days_limit: number
  appointments_enabled_ind: boolean
  exams_enabled_ind: boolean
  latitude: number
  longitude: number
  max_person_appointment_per_day: number
  office_appointment_message: string
  office_id: number
  office_name: string
  office_number: number
  sb_id: number
  timeslots: TimeSlots[]
  timezone: TimeZone
}

export interface Offices {
  offices: Office[]
}

export interface TimeSlots {
  day_of_week: number
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
