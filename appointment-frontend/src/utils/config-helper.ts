import Axios from 'axios'
import { SessionStorageKeys } from './constants'

/**
 * the configs are used since process.env doesnt play well when we hae only one build config and multiple deployments..so going for this
 */
const url = `${process.env.VUE_APP_PATH}config/configuration.json`

export default class ConfigHelper {
  static keycloakConfigUrl: string = ''
  static mapConfiguration = {
    zoomControl: false,
    mapTypeControl: false,
    scaleControl: false,
    streetViewControl: false,
    rotateControl: false,
    fullscreenControl: false,
    disableDefaultUi: false
  }

  static async fetchConfig () {
    const response = await Axios.get(url)
    sessionStorage.setItem(SessionStorageKeys.ApiConfigKey, JSON.stringify(response.data))
  }

  /**
 * this will run everytime when vue is being loaded..so do the call only when session storage doesnt have the values
 */
  static saveConfigToSessionStorage () {
    if (sessionStorage.getItem(SessionStorageKeys.ApiConfigKey)) {
      return Promise.resolve()
    } else {
      return this.fetchConfig()
    }
  }

  static getSelfURL () {
    // this is without a trailing slash
    return `${window.location.origin}${process.env.VUE_APP_PATH}`.replace(/\/$/, '') // remove the slash at the end
  }

  static getAppAPIUrl () {
    // return ConfigHelper.getValue('VUE_APP_ROOT_API')
    // Temporarily commented out above line for demo.
    // TODO - Restore above
    return 'https://dev-theq.pathfinder.gov.bc.ca/api/v1'
  }

  static getValue (key: String) {
    // @ts-ignore
    return JSON.parse(sessionStorage.getItem(SessionStorageKeys.ApiConfigKey))[key]
  }

  static addToSession (key:string, value:any) {
    sessionStorage.setItem(key, value)
  }

  static getFromSession (key:string):any {
    return sessionStorage.getItem(key)
  }

  static removeFromSession (key:string) {
    sessionStorage.removeItem(key)
  }

  static clearSession () {
    sessionStorage.clear()
  }

  static setKeycloakConfigUrl (keycloakConfigUrl: string) {
    this.keycloakConfigUrl = keycloakConfigUrl
  }

  static getKeycloakConfigUrl (): string {
    return this.keycloakConfigUrl
  }

  static getMapConfigurations () {
    return this.mapConfiguration
  }
}
