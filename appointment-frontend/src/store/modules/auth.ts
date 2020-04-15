import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators'
import ConfigHelper from '@/utils/config-helper'
import { SessionStorageKeys } from '@/utils/constants'

@Module({
  name: 'auth',
  namespaced: true
})
export default class AuthModule extends VuexModule {
  token: string = ''
  idToken: string = ''
  refreshToken: string = ''
  userFullName: string = ''
  kcGuid: string = ''
  loginSource: string = ''

  get isAuthenticated (): boolean {
    return !!this.token
  }

  @Mutation
  public setKCToken (token: string): void {
    this.token = token
    ConfigHelper.addToSession(SessionStorageKeys.KeyCloakToken, token)
  }

  @Mutation
  public setIDToken (idToken: string): void {
    this.idToken = idToken
    ConfigHelper.addToSession(SessionStorageKeys.KeyCloakIdToken, idToken)
  }

  @Mutation
  public setRefreshToken (refreshToken: string): void {
    this.refreshToken = refreshToken
    ConfigHelper.addToSession(SessionStorageKeys.KeyCloakRefreshToken, refreshToken)
  }

  @Mutation
  public setUserFullName (userFullName: string): void {
    this.userFullName = userFullName
    ConfigHelper.addToSession(SessionStorageKeys.UserFullName, userFullName)
  }

  @Mutation
  public setKCGuid (kcGuid: string): void {
    this.kcGuid = kcGuid
    ConfigHelper.addToSession(SessionStorageKeys.UserKcId, kcGuid)
  }

  @Mutation
  public setLoginSource (loginSource: string): void {
    this.loginSource = loginSource
    ConfigHelper.addToSession(SessionStorageKeys.UserAccountType, loginSource)
  }

  @Action({ rawError: true })
  public clearSession (): void {
    this.context.commit('setKCToken', '')
    this.context.commit('setIDToken', '')
    this.context.commit('setRefreshToken', '')
    this.context.commit('setUserFullName', '')
    this.context.commit('setKCGuid', '')
    this.context.commit('setLoginSource', '')
  }

  @Action({ rawError: true })
  public syncWithSessionStorage (): void {
    this.context.commit('setKCToken', ConfigHelper.getFromSession(SessionStorageKeys.KeyCloakToken) || '')
    this.context.commit('setIDToken', ConfigHelper.getFromSession(SessionStorageKeys.KeyCloakIdToken) || '')
    this.context.commit('setRefreshToken', ConfigHelper.getFromSession(SessionStorageKeys.KeyCloakRefreshToken) || '')
    this.context.commit('setUserFullName', ConfigHelper.getFromSession(SessionStorageKeys.UserFullName) || '')
    this.context.commit('setKCGuid', ConfigHelper.getFromSession(SessionStorageKeys.UserKcId) || '')
    this.context.commit('setLoginSource', ConfigHelper.getFromSession(SessionStorageKeys.UserAccountType) || '')
  }
}
