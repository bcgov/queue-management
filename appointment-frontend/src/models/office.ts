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
}

export interface Offices {
  offices: Office[]
}
