import Axios, { AxiosResponse } from 'axios'
import ConfigHelper from '@/utils/config-helper'
import { User } from '@/models/user'
import { addAxiosInterceptors } from '@/utils/interceptors'

const axios = addAxiosInterceptors(Axios.create())

export default class UserService {
  public static async createUser (): Promise<AxiosResponse<User[]>> {
    return axios.post(`${ConfigHelper.getAppAPIUrl()}/users/`, {})
  }
}
