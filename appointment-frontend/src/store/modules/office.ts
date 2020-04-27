import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators'
import { AppointmentSlot } from '@/models/appointment'
import CommonUtils from '@/utils/common-util'
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
  categoryList: Service[] = [] // category and service shares similar data model
  currentOffice: Office
  currentService: Service
  currentAppointmentSlot: AppointmentSlot

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

  @Mutation
  public setCurrentAppointmentSlot (slots: AppointmentSlot) {
    this.currentAppointmentSlot = slots
  }

  /**
    Actions in this Module
  **/

  @Action({ commit: 'setOfficeList', rawError: true })
  public async getOffices () {
    const response = await OfficeService.getOffices()
    let offices = []
    if (response?.data?.offices) {
      offices = response.data.offices
      offices.forEach(office => {
        if (office?.timeslots) {
          office.timeslots = office.timeslots.map(timeslot => {
            return {
              ...timeslot,
              day_str: CommonUtils.getDayOfWeek(timeslot.day_of_week),
              end_time_str: CommonUtils.get12HTimeString(timeslot.end_time),
              start_time_str: CommonUtils.get12HTimeString(timeslot.start_time)
            }
          })
        }
      })
    }
    return offices
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
    return response?.data?.categories || []
  }

  @Action({ rawError: true })
  public async getCurrentOffice () {
    return this.currentOffice
  }

  @Action({ rawError: true })
  public async getCurrentService () {
    return this.currentService
  }

  @Action({ rawError: true })
  public async getCurrentAppointmentSlot () {
    return this.currentAppointmentSlot
  }
}
