import Axios, { AxiosResponse } from 'axios'
import ConfigHelper from '@/utils/config-helper'
import { User } from '@/models/user'
import { addAxiosInterceptors } from '@/utils/interceptors'

const axios = addAxiosInterceptors(Axios.create())

export default class UserService {
  public static async getUser (): Promise<AxiosResponse<User[]>> {
    return axios.get(`${ConfigHelper.getAppAPIUrl()}/users/me/`)
  }

  public static async createUser (): Promise<AxiosResponse<User[]>> {
    return axios.post(`${ConfigHelper.getAppAPIUrl()}/users/`, {})
  }

  public static async updateUser (userId: number, updateBody): Promise<AxiosResponse<User[]>> {
    return axios.put(`${ConfigHelper.getAppAPIUrl()}/users/${userId}/`, updateBody)
  }
}
