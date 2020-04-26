import Axios, { AxiosResponse } from 'axios'
import ConfigHelper from '@/utils/config-helper'
import { Offices } from '@/models/office'
import { Services } from '@/models/service'
import { addAxiosInterceptors } from '@/utils/interceptors'

const axios = addAxiosInterceptors(Axios.create())

export default class OfficeService {
  public static async getOffices (): Promise<AxiosResponse<Offices>> {
    return axios.get(`${ConfigHelper.getAppAPIUrl()}/offices/`)
  }

  public static async getServiceByOffice (officeId: number): Promise<AxiosResponse<Services>> {
    return axios.get(`${ConfigHelper.getAppAPIUrl()}/services/?office_id=${officeId}`)
  }

  public static async getCategories (): Promise<AxiosResponse<any>> {
    return axios.get(`${ConfigHelper.getAppAPIUrl()}/categories/`)
  }

  public static async getAvailableAppointmentSlots (officeId: number): Promise<AxiosResponse<any>> {
    return axios.get(`${ConfigHelper.getAppAPIUrl()}/offices/${officeId}/slots/`)
  }
}
