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
}
