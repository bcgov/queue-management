import Axios, { AxiosResponse } from 'axios'
import { AppointmentRequestBody } from '@/models/appointment'
import ConfigHelper from '@/utils/config-helper'
import { addAxiosInterceptors } from '@/utils/interceptors'

const axios = addAxiosInterceptors(Axios.create())

export default class AppointmentService {
  public static async createAppointment (appointmentBody: AppointmentRequestBody): Promise<AxiosResponse<any>> {
    return axios.post(`${ConfigHelper.getAppAPIUrl()}/appoinments/`, appointmentBody)
  }
}
