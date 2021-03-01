import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators'
import { AppointmentRequestBody, AppointmentSlot } from '@/models/appointment'
import { Appointment } from './../../models/appointment'
import AppointmentService from '@/services/appointment.services'
import CommonUtils from '@/utils/common-util'
import { Office } from '@/models/office'
import OfficeService from '@/services/office.services'
import { Service } from '@/models/service'
import { Snowplow } from '@/models/global'
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
  spLastStep: number = 0

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
    this.currentOfficeTimezone = office?.timezone?.timezone_name || undefined
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
        return (service.actual_service_ind &&
          service.display_dashboard_ind &&
          service.online_availability !== ServiceAvailability.HIDE)
      })
      // Sort alphabetically on displayed external_service_name
      services = services.sort((a, b) => {
        // If external_service_name is null, sort it to last of list.
        let aName = a.external_service_name || 'zzz'
        let bName = b.external_service_name || 'zzz'
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
        return services.some(s => s.parent_id === cat.service_id)
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
      start_time: this.context.state['currentAppointmentSlot'].start_time,
      end_time: this.context.state['currentAppointmentSlot'].end_time,
      service_id: this.context.state['currentService'].service_id,
      comments: this.context.state['additionalNotes'],
      office_id: this.context.state['currentOffice'].office_id,
      user_id: userId,
      appointment_draft_id: this.context.state['currentDraftAppointment'].appointment_id
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
      start_time: appointment?.start_time,
      end_time: appointment?.end_time
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
      start_time: this.context.state['currentAppointmentSlot'].start_time,
      end_time: this.context.state['currentAppointmentSlot'].end_time,
      service_id: this.context.state['currentService'].service_id,
      comments: this.context.state['additionalNotes'],
      office_id: this.context.state['currentOffice'].office_id,
      user_id: userId,
      is_draft: true
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
    // eslint-disable-next-line no-console
    console.log('snowplow.appointment_step', mySP.step)
    // eslint-disable-next-line no-console
    console.log('snowplow.status', this.context.state['spStatus'])
    // eslint-disable-next-line no-console
    console.log('snowplow.logged_in', mySP.loggedIn)
    // eslint-disable-next-line no-console
    console.log('snowplow.appointment_id', mySP.apptID)
    // eslint-disable-next-line no-console
    console.log('snowplow.client_id', mySP.clientID)
    // eslint-disable-next-line no-console
    console.log('snowplow.location', mySP.loc)
    // eslint-disable-next-line no-console
    console.log('snowplow.service', mySP.serv)
  }
}
