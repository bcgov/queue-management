import { AxiosInstance } from 'axios'
import ConfigHelper from './config-helper'
import { SessionStorageKeys } from './constants'

export function addAxiosInterceptors (axiosInstance: AxiosInstance): AxiosInstance {
  axiosInstance.interceptors.request.use(config => {
    const token = ConfigHelper.getFromSession(SessionStorageKeys.KeyCloakToken)
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  err => {
    return Promise.reject(err)
  })
  return axiosInstance
}
