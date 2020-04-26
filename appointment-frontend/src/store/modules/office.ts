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
  availableAppointmentSlots: Service[] = []
  categoryList = []
  currentOffice: Office
  currentService: Service

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
  public setAvailableAppointmentSlots (appointments) {
    this.availableAppointmentSlots = appointments
  }

  @Mutation
  public setCategoryList (categoryList) {
    this.categoryList = categoryList
  }

  @Mutation
  public setCurrentOffice (office: Office) {
    this.currentOffice = office
  }

  @Mutation
  public setCurrentService (service: Service) {
    this.currentService = service
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

  @Action({ commit: 'setAvailableAppointmentSlots', rawError: true })
  public async getAvailableAppointmentSlots (officeId: number) {
    const response = await OfficeService.getAvailableAppointmentSlots(officeId)
    return response?.data || []
  }

  @Action({ commit: 'setCategoryList', rawError: true })
  public async getCategories () {
    const response = await OfficeService.getCategories()
    return response?.data || []
  }

  @Action({ rawError: true })
  public async getCurrentOffice () {
    return this.currentOffice
  }

  @Action({ rawError: true })
  public async getCurrentService () {
    return this.currentService
  }
}
