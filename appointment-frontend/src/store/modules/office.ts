import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators'
import { Appointment, AppointmentRequestBody, AppointmentSlot } from '@/models/appointment'
import AppointmentService from '@/services/appointment.services'
import CommonUtils from '@/utils/common-util'
import { Office } from '@/models/office'
import OfficeService from '@/services/office.services'
import { Service } from '@/models/service'
import { ServiceAvailability } from '@/utils'

@Module({
  name: 'office',
  namespaced: true
})
export default class OfficeModule extends VuexModule {
  officeList: Office[] = []
  serviceList: Service[] = []
  availableAppointmentSlots = []
  categoryList: Service[] = [] // category and service shares similar data model
  additionalNotes: string
  currentOffice: Office
  currentOfficeTimezone: string
  currentService: Service
  currentAppointmentSlot: AppointmentSlot
  currentAppointment: Appointment
  currentDraftAppointment: Appointment
  spStatus: string
  spLastStep: number

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
    this.currentOfficeTimezone = office?.timezone?.timezoneName || undefined
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

  @Mutation
  public setACurrentAppointment (appointment: Appointment) {
    this.currentAppointment = appointment
  }

  @Mutation
  public setCurrentDraftAppointment (appointment: Appointment) {
    this.currentDraftAppointment = appointment
  }

  @Mutation
  public setSPStatus (status: string) {
    this.spStatus = status
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
    let services = response?.data?.services || []
    if (services.length) {
      services = response.data.services.filter(service => {
        return (service.actualServiceInd &&
          service.displayDashboardInd &&
          service.onlineAvailability !== ServiceAvailability.HIDE)
      })
      // Sort alphabetically on displayed external_service_name
      services = services.sort((a, b) => {
        // If external_service_name is null, sort it to last of list.
        const aName = a.externalServiceName || 'zzz'
        const bName = b.externalServiceName || 'zzz'
        return aName.localeCompare(bName)
      })
    }
    return services
  }

  @Action({ commit: 'setAvailableAppointmentSlots', rawError: true })
  public async getAvailableAppointmentSlots (input: {officeId: number, serviceId: number}) {
    const response = await OfficeService.getAvailableAppointmentSlots(input.officeId, input.serviceId)
    return response?.data || []
  }

  @Action({ commit: 'setCategoryList', rawError: true })
  public async getCategories () {
    const response = await OfficeService.getCategories()
    let categories = response?.data?.categories || []
    if (categories.length) {
      const services = this.context.state['serviceList'] || []
      categories = response.data.categories.filter(cat => {
        return services.some(s => s.parent_id === cat.serviceId)
      })
    }
    return categories
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
    // Don't make changes here, instead make changes to slot where end_time is set
    const userId = this.context.rootState.auth.currentUserProfile?.user_id || null
    const appointmentBody: AppointmentRequestBody = {
      startTime: this.context.state['currentAppointmentSlot'].start_time,
      endTime: this.context.state['currentAppointmentSlot'].end_time,
      serviceId: this.context.state['currentService'].service_id,
      comments: this.context.state['additionalNotes'],
      officeId: this.context.state['currentOffice'].office_id,
      userId: userId,
      appointmentDraftId: this.context.state['currentDraftAppointment'].appointment_id
    }
    let response
    if (this.context.rootState.isAppointmentEditMode) {
      if (this.context.state['currentAppointment']?.appointment_id) {
        response = await AppointmentService.updateAppointment(this.context.state['currentAppointment'].appointment_id, appointmentBody)
        this.context.commit('setCurrentDraftAppointment', {})
      }
    } else {
      response = await AppointmentService.createAppointment(appointmentBody)
      this.context.commit('setCurrentDraftAppointment', {})
    }
    return response?.data?.appointment || {}
  }

  @Action({ rawError: true })
  public clearSelectedValues (): void {
    this.context.commit('setCurrentOffice', undefined)
    this.context.commit('setCurrentService', undefined)
    this.context.commit('setCurrentAppointmentSlot', undefined)
    this.context.commit('setAdditionalNotes', undefined)
    this.context.rootState.stepperCurrentStep = 1
    this.context.rootState.isAppointmentEditMode = false
  }

  @Action({ rawError: true })
  public setAppointmentValues (appointment: Appointment): void {
    const apppointmentSlot: AppointmentSlot = {
      startTime: appointment?.startTime,
      endTime: appointment?.endTime
    }
    this.context.commit('setCurrentOffice', appointment?.office)
    this.context.commit('setCurrentService', appointment?.service)
    this.context.commit('setCurrentAppointmentSlot', apppointmentSlot)
    this.context.commit('setAdditionalNotes', appointment?.comments)
    this.context.commit('setACurrentAppointment', appointment)
  }

  @Action({ rawError: true })
  public async createDraftAppointment () {
    // Don't make changes here, instead make changes to slot where end_time is set
    const userId = this.context.rootState.auth.currentUserProfile?.user_id || null
    const appointmentBody: AppointmentRequestBody = {
      startTime: this.context.state['currentAppointmentSlot'].start_time,
      endTime: this.context.state['currentAppointmentSlot'].end_time,
      serviceId: this.context.state['currentService'].service_id,
      comments: this.context.state['additionalNotes'],
      officeId: this.context.state['currentOffice'].office_id,
      userId: userId,
      isDraft: true
    }
    let response
    let deleteResponse

    if (this.context.state['currentDraftAppointment']?.appointment_id) {
    //   // deleteResponse =
      try {
        deleteResponse = await AppointmentService.deleteDraftAppointment(this.context.state['currentDraftAppointment'].appointment_id)
        if (deleteResponse.data) {
          this.context.commit('setCurrentDraftAppointment', {})
        }
      } catch (error) {
        // console.log('error', error)
      }
    }

    // } else {
    response = await AppointmentService.createDraftAppointment(appointmentBody)
    // }
    return response?.data?.appointment || {}
  }

  @Action({ rawError: true })
  public callSnowplowClick (mySP: any): void {
    if (!mySP.loggedIn) {
      mySP.clientID = null
    }
    if (!mySP.url) {
      mySP.url = null
    }
    (window as any).snowplow('trackSelfDescribingEvent', {
      schema: 'iglu:ca.bc.gov.cfmspoc/appointment_click/jsonschema/1-0-0',
      data: {
        label: mySP.label,
        appointment_step: mySP.step,
        logged_in: mySP.loggedIn,
        appointment_id: mySP.apptID,
        client_id: mySP.clientID,
        location: mySP.loc,
        service: mySP.serv,
        url: mySP.url
      }
    }
    )
  }

  @Action({ rawError: true })
  public callSnowplow (mySP: any): void {
    if (!mySP.loggedIn) {
      mySP.clientID = null
    }
    (window as any).snowplow('trackSelfDescribingEvent', {
      schema: 'iglu:ca.bc.gov.cfmspoc/appointment_step/jsonschema/1-0-0',
      data: {
        appointment_step: mySP.step,
        status: this.context.state['spStatus'],
        logged_in: mySP.loggedIn,
        appointment_id: mySP.apptID,
        client_id: mySP.clientID,
        location: mySP.loc,
        service: mySP.serv
      }
    }
    )
  }
}
