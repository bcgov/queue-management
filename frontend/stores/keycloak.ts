import { defineStore } from 'pinia';
import Keycloak from 'keycloak-js';

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
        clientId: config.resource
      });

      return new Promise((resolve, reject) => {
        if (this.keycloak) {
          this.keycloak.init({ onLoad: 'login-required',
            redirectUri: 'http://localhost:8080/queue'
           })
            .then((authenticated) => {
              this.authenticated = authenticated;
              resolve(authenticated);
            })
            .catch((error) => {
              reject(error);
            });
        } else {
          reject(new Error('Keycloak instance is null'));
        }
      });
    },
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
      return this.keycloak?.logout();
    },
  },
});
