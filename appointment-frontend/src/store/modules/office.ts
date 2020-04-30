import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators'
import { AppointmentRequestBody, AppointmentSlot } from '@/models/appointment'
import CommonUtils, { Days } from '@/utils/common-util'
import AppointmentService from '@/services/appointment.services'
import { Office } from '@/models/office'
import OfficeService from '@/services/office.services'
import { Service } from '@/models/service'
import { ServiceAvailability } from '@/utils'
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
  additionalNotes: string
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

  @Mutation
  public setAdditionalNotes (notes: string) {
    this.additionalNotes = notes
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
          office.timeslots = CommonUtils.getFormattedTimeslots(office.timeslots)
        }
      })
    }
    return offices
  }

  @Action({ commit: 'setServiceList', rawError: true })
  public async getServiceByOffice (officeId: number) {
    const response = await OfficeService.getServiceByOffice(officeId)
    let services = []
    if (response?.data?.services?.length) {
      services = response.data.services.filter(service => {
        return service.online_availability !== ServiceAvailability.HIDE
      })
    }
    return services
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

  @Action({ rawError: true })
  public async createAppointment () {
    const userId = this.context.rootState.auth.currentUserProfile?.user_id || null
    const appointmentBody: AppointmentRequestBody = {
      start_time: this.context.state['currentAppointmentSlot'].start_time,
      end_time: this.context.state['currentAppointmentSlot'].end_time,
      service_id: this.context.state['currentService'].service_id,
      comments: this.context.state['additionalNotes'],
      office_id: this.context.state['currentOffice'].office_id,
      user_id: userId
    }
    const response = await AppointmentService.createAppointment(appointmentBody)
    return response?.data?.appointment || {}
  }
}
