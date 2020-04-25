import Axios, { AxiosResponse } from 'axios'
import ConfigHelper from '@/utils/config-helper'
import { Offices } from '@/models/office'
import { addAxiosInterceptors } from '@/utils/interceptors'

const axios = addAxiosInterceptors(Axios.create())

export default class OfficeService {
  public static async getOffices (): Promise<AxiosResponse<Offices>> {
    return axios.get(`${ConfigHelper.getAppAPIUrl()}/offices/`)
  }
}
