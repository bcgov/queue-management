import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators'
import { Office } from '@/models/office'
import OfficeService from '@/services/office.services'
import { store } from '@/store'

@Module({
  name: 'office',
  namespaced: true,
  store,
  dynamic: true
})
export default class OfficeModule extends VuexModule {
  officeList: Office[] = []

  @Mutation
  public setOfficeList (officeList) {
    this.officeList = officeList
  }

  @Action({ commit: 'setOfficeList', rawError: true })
  public async getOffices () {
    const response = await OfficeService.getOffices()
    return response?.data?.offices || []
  }
}
