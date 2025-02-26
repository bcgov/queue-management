import Keycloak, { KeycloakInitOptions } from 'keycloak-js'
import AuthModule from '@/store/modules/auth'
import ConfigHelper from '@/utils/config-helper'
import { SessionStorageKeys } from '@/utils/constants'
import { Store } from 'vuex'
import { getModule } from 'vuex-module-decorators'

class TokenServices {
  private kc: Keycloak | undefined
  private counter = 0
  private REFRESH_ATTEMPT_INTERVAL = 10 // in seconds
  private timerId = 0
  private store: Store<any> | null = null

  initUsingKc (kcInstance: Keycloak) {
    this.kc = kcInstance
  }

  // Fallback function just to not break the legacy versions
  // Should be removed once the coops consumes the service using the init() function
  async initUsingUrl (keyCloakConfigurl: string) {
    ConfigHelper.setKeycloakConfigUrl(keyCloakConfigurl)
    await this.init()
  }

  async init (store?: Store<any>) {
    this.store = store
    const kcOptions: KeycloakInitOptions = {
      onLoad: 'check-sso',
      checkLoginIframe: false,
      timeSkew: 0,
      token: ConfigHelper.getFromSession(SessionStorageKeys.KeyCloakToken) || undefined,
      refreshToken: ConfigHelper.getFromSession(SessionStorageKeys.KeyCloakRefreshToken) || undefined,
      idToken: ConfigHelper.getFromSession(SessionStorageKeys.KeyCloakIdToken) || undefined
    }

    return new Promise((resolve, reject) => {
      this.kc = Keycloak(ConfigHelper.getKeycloakConfigUrl())
      this.kc.init(kcOptions)
        .then(authenticated => {
          // eslint-disable-next-line no-console
          console.info('[TokenServices] is User Authenticated?: Syncing ' + authenticated)
          if (this.kc && authenticated) {
            this.syncSessionStorage()
            resolve(this.kc.token)
          } else {
            // If not authenticated that means token is invalid
            // Clear out session storage and go to auth home
            this.clearSession()
          }
        })
        .catch(error => {
          reject(new Error('Could not Initialize KC' + error))
        })
    })
  }

  scheduleRefreshTimer (refreshEarlyTime = 0) {
    const refreshEarlyTimeinMilliseconds = Math.max(this.REFRESH_ATTEMPT_INTERVAL, refreshEarlyTime) * 1000
    this.scheduleRefreshToken(refreshEarlyTimeinMilliseconds)
  }

  refreshToken () {
    // eslint-disable-next-line no-console
    console.log('[TokenServices] One time Token Refreshing ')
    return new Promise<void>((resolve, reject) => {
      if (this.kc) {
        this.kc.updateToken(-1)
          .then(refreshed => {
            if (refreshed) {
              // eslint-disable-next-line no-console
              console.log('[TokenServices] One time Token Refreshed ')
              this.syncSessionStorage()
              resolve()
            }
          })
          .catch(() => {
            reject(new Error('Could not refresh Token'))
          })
      } else {
        reject(new Error('Could not refresh Token:No Kc Instance'))
      }
    })
  }

  stopRefreshTimer () {
    // eslint-disable-next-line no-console
    console.info('[TokenServices Stopping the timer] ')
    clearTimeout(this.timerId)
  }

  private scheduleRefreshToken (refreshEarlyTimeinMilliseconds: number) {
    let refreshTokenExpiresIn = -1
    // check if refresh token is still valid . Or else clear all timers and throw errors
    if (this.kc && this.kc.timeSkew !== undefined && this.kc.refreshTokenParsed) {
      refreshTokenExpiresIn = this.kc.refreshTokenParsed['exp']! - Math.ceil(new Date().getTime() / 1000) + this.kc.timeSkew
    }
    if (refreshTokenExpiresIn < 0) {
      throw new Error('Refresh Token Expired. No more token refreshes')
    }
    let expiresIn = -1
    if (this.kc && this.kc.tokenParsed && this.kc.tokenParsed['exp'] && this.kc.timeSkew !== undefined) {
      expiresIn = this.kc.tokenParsed['exp'] - Math.ceil(new Date().getTime() / 1000) + this.kc.timeSkew
    }
    if (expiresIn < 0) {
      throw new Error('Refresh Token Expired. No more token refreshes')
    }
    const refreshInMilliSeconds = (expiresIn * 1000) - refreshEarlyTimeinMilliseconds // in milliseconds
    // eslint-disable-next-line no-console
    console.info('[TokenServices] Token Refresh Scheduled in %s Seconds', (refreshInMilliSeconds / 1000))
    this.timerId = setTimeout(() => {
      // eslint-disable-next-line no-console
      console.log('[TokenServices] Refreshing Token Attempt: %s ', ++this.counter)
      this.kc.updateToken(-1)
        .then(refreshed => {
          if (refreshed) {
            // eslint-disable-next-line no-console
            console.log('Token successfully refreshed')
            this.syncSessionStorage()
            this.scheduleRefreshToken(refreshEarlyTimeinMilliseconds)
          }
        })
        .catch(() => {
          clearTimeout(this.timerId)
        })
    }, refreshInMilliSeconds)
  }

  private syncSessionStorage () {
    if (this.kc) {
      if (this.kc.token) {
        ConfigHelper.addToSession(SessionStorageKeys.KeyCloakToken, this.kc.token)
      }
      if (this.kc.refreshToken) {
        ConfigHelper.addToSession(SessionStorageKeys.KeyCloakRefreshToken, this.kc.refreshToken)
      }
      if (this.kc.idToken) {
        ConfigHelper.addToSession(SessionStorageKeys.KeyCloakIdToken, this.kc.idToken)
      }
    }
  }

  private async clearSession () {
    if (this.store) {
      const authModule = getModule(AuthModule, this.store)
      authModule.clearSession()
    } else {
      ConfigHelper.removeFromSession(SessionStorageKeys.KeyCloakToken)
      ConfigHelper.removeFromSession(SessionStorageKeys.KeyCloakIdToken)
      ConfigHelper.removeFromSession(SessionStorageKeys.KeyCloakRefreshToken)
      ConfigHelper.removeFromSession(SessionStorageKeys.UserFullName)
      ConfigHelper.removeFromSession(SessionStorageKeys.UserKcId)
      ConfigHelper.removeFromSession(SessionStorageKeys.UserAccountType)
    }
  }

  decodeToken () {
    try {
      const token = ConfigHelper.getFromSession(SessionStorageKeys.KeyCloakToken)
      if (token) {
        const base64Url = token.split('.')[1]
        const base64 = decodeURIComponent(window.atob(base64Url).split('').map(function (c) {
          return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
        }).join(''))
        return JSON.parse(base64)
      } else {
        throw new Error('null JWT')
      }
    } catch (error) {
      throw new Error('Error parsing JWT - ' + error)
    }
  }
}

export default TokenServices
