import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators'
import { KCUserProfile } from '@/models/KCUserProfile'
import KeyCloakService from '@/services/keycloak.services'
import { store } from '@/store'

@Module({
  name: 'account',
  namespaced: true
})
export default class AccountModule extends VuexModule {
  currentUser: KCUserProfile | null = null

  @Mutation
  public setCurrentUser (currentUser: KCUserProfile) {
    this.currentUser = currentUser
  }

  get username (): string {
    return `${this.currentUser?.firstName || '-'} ${this.currentUser?.lastName || ''}`
  }

  @Action({ rawError: true, commit: 'setCurrentUser' })
  public loadUserInfo () {
    // Load User Info
    return KeyCloakService.getUserInfo()
  }
}
