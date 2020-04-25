import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators'
import { Office } from '@/models/office'
import OfficeService from '@/services/office.services'
import { Service } from '@/models/service'
import { store } from '@/store'

@Module({
  name: 'office',
  namespaced: true,
  store,
  dynamic: true
})
export default class OfficeModule extends VuexModule {
  officeList: Office[] = []
  serviceList: Service[] = []
  currentOffice: Office

  /**
    Mutations in this Module
  **/

  @Mutation
  public setOfficeList (officeList) {
    this.officeList = officeList
  }

  @Mutation
  public setServiceList (serviceList) {
    this.serviceList = serviceList
  }

  @Mutation
  public setcurrentOffice (office: Office) {
    this.currentOffice = office
  }

  /**
    Actions in this Module
  **/

  @Action({ commit: 'setOfficeList', rawError: true })
  public async getOffices () {
    const response = await OfficeService.getOffices()
    return response?.data?.offices || []
  }

  @Action({ commit: 'setServiceList', rawError: true })
  public async getServiceByOffice (officeId: number) {
    const response = await OfficeService.getServiceByOffice(officeId)
    return response?.data?.services || []
  }

  @Action({ rawError: true })
  public async getCurrentOffice () {
    return this.currentOffice
  }
}
