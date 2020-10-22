import { AppointmentRequestBody, AppointmentResponse, Appointments } from '@/models/appointment'
import Axios, { AxiosResponse } from 'axios'
import ConfigHelper from '@/utils/config-helper'
import { addAxiosInterceptors } from '@/utils/interceptors'

const axios = addAxiosInterceptors(Axios.create())

export default class AppointmentService {
  public static async createAppointment (appointmentBody: AppointmentRequestBody): Promise<AxiosResponse<AppointmentResponse>> {
    return axios.post(`${ConfigHelper.getAppAPIUrl()}/appointments/`, appointmentBody)
  }
  public static async createDraftAppointment (appointmentBody: AppointmentRequestBody): Promise<AxiosResponse<AppointmentResponse>> {
    return axios.post(`${ConfigHelper.getAppAPIUrl()}/appointments/draft`, appointmentBody)
  }

  public static async updateAppointment (appointmentId: number, appointmentBody: AppointmentRequestBody): Promise<AxiosResponse<AppointmentResponse>> {
    return axios.put(`${ConfigHelper.getAppAPIUrl()}/appointments/${appointmentId}/`, appointmentBody)
  }

  public static async deleteAppointment (appointmentId: number): Promise<AxiosResponse<any>> {
    return axios.delete(`${ConfigHelper.getAppAPIUrl()}/appointments/${appointmentId}/`)
  }

  public static async getAppointments (): Promise<AxiosResponse<Appointments>> {
    return axios.get(`${ConfigHelper.getAppAPIUrl()}/users/appointments/`)
  }
}
