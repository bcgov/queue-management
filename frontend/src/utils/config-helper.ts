import Axios from 'axios'

/**
 * the configs are used since process.env doesnt play well when we hae only one build config and multiple deployments..so going for this
 */
const url = 'config/configuration.json'

export default class ConfigHelper {
  static config: any = '';

  static async fetchConfig () {
    if (this.config === '') {
      const a = document.createElement('a')
      a.href = window.location.href
      const configUrl = a.protocol + '//' + a.host + '/' + url
      const response = await Axios.get(configUrl)
      this.config = response.data
    }
  }

  static getValue (key: any) {
    // @ts-ignore
    if (this.config === '') {
      this.fetchConfig()
    }
    return this.config[key] || false
  }

  static isServiceFLowEnabled () {
    return this.getValue('SERVICEFLOW_ENABLED') || false
  }

  static getSocketTimeout () {
    return this.getValue('SOCKET_TIMEOUT') || 20000
  }

  static getSocketDelayMax () {
    return this.getValue('SOCKET_DELAY_MAX') || 5000
  }

  static getconfig () {
    return this.config
  }
}
