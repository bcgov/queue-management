import { Office } from './office'
import { Service } from './service'

export interface AppointmentSlot {
  endTime: string
  startTime: string
}

export interface AppointmentRequestBody {
  startTime: string
  endTime: string
  serviceId: number
  comments: string
  officeId: number
  userId: number
  isDraft?:boolean
  appointmentDraftId?:number
}

export interface Appointment {
  appointmentId: number,
  blackoutFlag: string,
  checkedInTime: string,
  citizenId: number,
  citizenName: number,
  comments: string,
  contactInformation: string,
  endTime: string,
  office: number | Office,
  officeId: number,
  recurringUuid: string,
  service: number | Service,
  serviceId: number,
  startTime: string,
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
