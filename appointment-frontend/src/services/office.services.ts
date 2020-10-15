import Axios, { AxiosResponse } from 'axios'
import { Categories, Services } from '@/models/service'
import ConfigHelper from '@/utils/config-helper'
import { Offices } from '@/models/office'
import { addAxiosInterceptors } from '@/utils/interceptors'

const axios = addAxiosInterceptors(Axios.create())

export default class OfficeService {
  public static async getOffices (): Promise<AxiosResponse<Offices>> {
    return axios.get(`${ConfigHelper.getAppAPIUrl()}/offices/`)
  }

  public static async getServiceByOffice (officeId: number): Promise<AxiosResponse<Services>> {
    return axios.get(`${ConfigHelper.getAppAPIUrl()}/services/?office_id=${officeId}`)
  }

  public static async getServices (): Promise<AxiosResponse<Services>> {
    return axios.get(`${ConfigHelper.getAppAPIUrl()}/services/`)
  }

  public static async getCategories (): Promise<AxiosResponse<Categories>> {
    return axios.get(`${ConfigHelper.getAppAPIUrl()}/categories/`)
  }

  public static async getAvailableAppointmentSlots (officeId: number, serviceId: number): Promise<AxiosResponse<any>> {
    if (officeId === undefined || serviceId === undefined) throw Error('Missing required parameters')
    return axios.get(`${ConfigHelper.getAppAPIUrl()}/offices/${officeId}/slots/?service_id=${serviceId}`)
  }
}
