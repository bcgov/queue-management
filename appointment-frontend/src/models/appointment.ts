import { Office } from './office'
import { Service } from './service'
// Do not remove the eslint-disable camelcase below as the Python data model uses
// snake_case and Vue can't translate it to camelCase easily.
/* eslint-disable camelcase */

export interface AppointmentSlot {
  end_time: string
  start_time: string
}

export interface AppointmentRequestBody {
  start_time: string
  end_time: string
  service_id: number
  comments: string
  office_id: number
  user_id: number
  is_draft?:boolean
  appointment_draft_id?:number
}

export interface Appointment {
  appointment_id: number,
  blackout_flag: string,
  checked_in_time: string,
  citizen_id: number,
  citizen_name: number,
  comments: string,
  contact_information: string,
  end_time: string,
  office: number | Office,
  office_id: number,
  recurring_uuid: string,
  service: number | Service,
  service_id: number,
  start_time: string,
  appointmentDate?: string,
  appointmentStartTime?: string
  appointmentEndTime?: string
}

export interface AppointmentResponse {
  appointment: Appointment
}

export interface Appointments {
  appointments: Appointment[]
}
