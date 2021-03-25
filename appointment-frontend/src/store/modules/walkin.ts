import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators'
import { WalkinQModel } from '@/models/walkin'
import WalkinService from '@/services/walkin.service'

@Module({
  name: 'walkin',
  namespaced: true
})
export default class WalkinModule extends VuexModule {
  walkinList: WalkinQModel[] = []

  /**
    Mutations in this Module
  **/

  @Mutation
  public setwalkinList (walkinList: any) {
    this.walkinList = walkinList
  }
  /**
    Actions in this Module
  **/

  @Action({ rawError: true })
  public async getAllWalkin (walkinUniqueId: string) {
    const response = await WalkinService.getWalkin(walkinUniqueId)
    return response || {}
  }
}
