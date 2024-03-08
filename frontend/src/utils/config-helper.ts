import Axios from 'axios'

/**
 * the configs are used since process.env doesnt play well when we hae only one build config and multiple deployments..so going for this
 */
const url = 'config/configuration.json'

export default class ConfigHelper {
  static config: any = '';

  static async fetchConfig () {
    // if (this.config === '') {
    //   const a = document.createElement('a')
    //   a.href = window.location.href
    //   const configUrl = a.protocol + '//' + a.host + '/' + url
    //   const response = await Axios.get(configUrl)
    //   this.config = response.data
    // }
    return {
      BPM_URL: "https://dev-sbc-ffa-bpm.apps.silver.devops.gov.bc.ca/camunda",
      FORM_IO_USER_ROLES: "formsflow-reviewer",
      FORM_IO_API_URL: "https://dev-sbc-ffa-forms.apps.silver.devops.gov.bc.ca",
      FORM_IO_RESOURCE_ID: "6078c70bdb2a9c357e91ba44",
      FORM_IO_REVIEWER_ID: "6078c79cdb2a9c5ce791ba51",
      FORM_IO_REVIEWER: "formsflow-reviewer",
      FORM_FLOW_API_URL : "https://dev-sbc-ffa-api.apps.silver.devops.gov.bc.ca",
      FORM_FLOW_URL : "https://dev-sbc-serviceflow.apps.silver.devops.gov.bc.ca",
      SERVICEFLOW_ENABLED: true,
      WEBSOCKET_ENCRYPT_KEY: "123455",
      SOCKET_TIMEOUT: 30000,
      SOCKET_DELAY_MAX : 3000,
      FORMIO_JWT_SECRET: "12345"
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
