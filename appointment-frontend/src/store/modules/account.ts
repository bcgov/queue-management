import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators'
import { KCUserProfile } from '@/models/KCUserProfile'
import KeyCloakService from '@/services/keycloak.services'
import UserService from '@/services/user.services'
import { UserUpdateBody } from '@/models/user'

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
    return this.currentUser?.displayName || this.context.rootState.auth.userFullName || ''
  }

  @Action({ rawError: true, commit: 'setCurrentUser' })
  public loadUserInfo () {
    // Load User Info
    return KeyCloakService.getUserInfo()
  }

  @Action({ rawError: true })
  public async updateUserAccount (userUpdateBody: UserUpdateBody) {
    const userId = this.context.rootState.auth.currentUserProfile?.user_id || null
    const response = await UserService.updateUser(userId, userUpdateBody)
    const returnData = response?.data?.length ? response.data[0] : {}
    this.context.commit('auth/setUserProfile', returnData, { root: true })
    return returnData
  }

  @Action({ rawError: true })
  public async getUser () {
    const response = await UserService.getUser()
    const returnData = response?.data?.length ? response.data[0] : {}
    this.context.commit('auth/setUserProfile', returnData, { root: true })
    return returnData
  }
}
