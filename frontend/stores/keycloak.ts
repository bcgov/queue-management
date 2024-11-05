import { defineStore } from 'pinia'
import Keycloak from 'keycloak-js'
import { SessionStorageKeyE } from '~/enums/session-storage-e'

const DEFAULT_REFRESH_CHECK_INTERVAL = 60000
const DEFAULT_REFRESH_MIN_VALIDITY = 120

export const useKeycloakStore = defineStore('keycloak', {
  state: () => ({
    keycloak: null as Keycloak | null,
    authenticated: false,
  }),
  actions: {
    async initKeycloak() {
      const config = await this.fetchKeycloakConfig();
      this.keycloak = new Keycloak({
        url: config['auth-server-url'],
        realm: config.realm,
        clientId: config.resource,
      });
    
      try {
        console.log("Keycloak instance created");
        const authenticated = await this.keycloak.init({
          onLoad: 'login-required',
          redirectUri: window.location.origin + '/queue',
        });
    
        this.authenticated = authenticated;
        console.log("User authenticated")
        await this.storeKeycloakToken()
        this.scheduleRefreshToken()
      } catch (error) {
        console.error("Keycloak init error:", error);
      }
    }
    ,
    
    async fetchKeycloakConfig() {
      const response = await fetch('/static/keycloak/keycloak.json');
      if (!response.ok) {
        throw new Error('Failed to load Keycloak configuration');
      }
      return await response.json();
    },
    
    async login() {
      if (!this.keycloak) {
        await this.initKeycloak();
      }
      return this.keycloak?.login();
    },
    
    logout() {
      this.clearSessionStorage();
      return this.keycloak?.logout();
    },
    
    storeKeycloakToken() {
      if (this.keycloak) {
        sessionStorage.setItem(SessionStorageKeyE.KEYCLOAK_TOKEN, this.keycloak.token || '')
        sessionStorage.setItem(SessionStorageKeyE.KEYCLOAK_TOKEN_ID, this.keycloak.idToken || '')
        sessionStorage.setItem(SessionStorageKeyE.KEYCLOAK_TOKEN_REFRESH, this.keycloak.refreshToken || '')
        sessionStorage.setItem(SessionStorageKeyE.KEYCLOAK_SYNCED, 'true');
      }
    },
    
    clearSessionStorage() {
      sessionStorage.removeItem(SessionStorageKeyE.KEYCLOAK_TOKEN)
      sessionStorage.removeItem(SessionStorageKeyE.KEYCLOAK_TOKEN_ID)
      sessionStorage.removeItem(SessionStorageKeyE.KEYCLOAK_TOKEN_REFRESH)
      sessionStorage.removeItem(SessionStorageKeyE.KEYCLOAK_SYNCED)
    },
    
    syncSessionStorage() {
      if (this.keycloak) {
        sessionStorage.setItem(SessionStorageKeyE.KEYCLOAK_TOKEN, this.keycloak.token || '')
        sessionStorage.setItem(SessionStorageKeyE.KEYCLOAK_TOKEN_REFRESH, this.keycloak.refreshToken || '')
        sessionStorage.setItem(SessionStorageKeyE.KEYCLOAK_TOKEN_ID, this.keycloak.idToken || '')
        sessionStorage.setItem(SessionStorageKeyE.KEYCLOAK_SYNCED, 'true');
      }
    },
    
    async refreshToken() {
      if (this.keycloak) {
        try {
          await this.keycloak.updateToken(DEFAULT_REFRESH_CHECK_INTERVAL)
          this.syncSessionStorage();
          console.info('Token refreshed successfully')
        } catch (error) {
          console.error('Failed to refresh token:', error)
          this.logout()
        }
      }
    },
    
    scheduleRefreshToken() {
      setInterval(() => {
        if (this.keycloak && this.keycloak.isTokenExpired(DEFAULT_REFRESH_MIN_VALIDITY)) {
          this.refreshToken()
        }
      }, DEFAULT_REFRESH_CHECK_INTERVAL)
    },
  },
});
