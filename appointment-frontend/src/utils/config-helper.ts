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
    // NOTE: Problem -> this caches sessions for ever, would never update with new build.
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
    return ConfigHelper.getValue('VUE_APP_ROOT_API')
    // return process.env.VUE_APP_ROOT_API
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

  static isEmsEnabled () {
    let smsEnabled:boolean = true
    if (this.getValue('disableSms') === true) {
      smsEnabled = false
    }
    return smsEnabled
  }

  static getFeedbackURL () {
    return ConfigHelper.getValue('VUE_APP_FEEDBACK_API')
  }

  static getFeedbackServiceChannel () {
    return ConfigHelper.getValue('FEEDBACK_SERVICE_CHANNEL')
  }

  static isFeedbackEnabled () {
    return ConfigHelper.getValue('FEEDBACK_ENABLED')
  }

  static getHeaderText () {
    return ConfigHelper.getValue('VUE_APP_HEADER_MSG')
  }

  static getHeaderLinks () {
    return ConfigHelper.getValue('VUE_APP_HEADER_LINKS')
  }

  static getFooterText () {
    return ConfigHelper.getValue('VUE_APP_FOOTER_MSG')
  }

  static getFooterLinks () {
    return ConfigHelper.getValue('VUE_APP_FOOTER_LINKS')
  }
}
