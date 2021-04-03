import Axios, { AxiosResponse } from 'axios'
import ConfigHelper from '@/utils/config-helper'
import { WalkinQModel } from '@/models/walkin'
import { addAxiosInterceptors } from '@/utils/interceptors'
const axios = addAxiosInterceptors(Axios.create())

export default class WalkinService {
  public static async getWalkin (walkinUniqueId: string): Promise<AxiosResponse<WalkinQModel>> {
    return axios.get(`${ConfigHelper.getAppAPIUrl()}/citizen/all-walkin/${walkinUniqueId}/`)
  }
}
