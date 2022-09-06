import { AxiosInstance } from 'axios'
import ConfigHelper from './config-helper'
import { SessionStorageKeys } from './constants'
import humps from 'humps'

export function addAxiosInterceptors (axiosInstance: AxiosInstance): AxiosInstance {
  axiosInstance.interceptors.request.use(config => {
    const token = ConfigHelper.getFromSession(SessionStorageKeys.KeyCloakToken)
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return { ...config, data: humps.decamelizeKeys(config.data) }
  },
  err => {
    return Promise.reject(err)
  })
  axiosInstance.interceptors.response.use(
    response => {
      return { ...response, data: humps.camelizeKeys(response.data) }
    },
    error => Promise.reject(error)
  )
  return axiosInstance
}
