import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators'
import { KCUserProfile } from '@/models/KCUserProfile'
import KeyCloakService from '@/services/keycloak.services'
import { store } from '@/store'

@Module({
  name: 'account',
  namespaced: true,
  store,
  dynamic: true
})
export default class AccountModule extends VuexModule {
  currentUser: KCUserProfile | null = null

  @Mutation
  public setCurrentUser (currentUser: KCUserProfile) {
    this.currentUser = currentUser
  }

  @Action({ rawError: true, commit: 'setCurrentUser' })
  public loadUserInfo () {
    // Load User Info
    return KeyCloakService.getUserInfo()
  }
}
