import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators'
import { FeedbackRequestObject, FeedbackResponseObject } from '@/models/feedback'
import { Appointment } from '@/models/appointment'
import AppointmentService from '@/services/appointment.services'
import CommonUtils from '@/utils/common-util'
import FeedbackService from '@/services/feedback.service'
import OfficeService from '@/services/office.services'

@Module({
  name: 'appointment',
  namespaced: true
})
export default class AppointmentModule extends VuexModule {
  appointmentList: Appointment[] = []

  /**
    Mutations in this Module
  **/

  @Mutation
  public setAppointmentList (appointmentList) {
    this.appointmentList = appointmentList
  }

  /**
    Actions in this Module
  **/

  @Action({ commit: 'setAppointmentList', rawError: true })
  public async getAppointmentList () {
    const response = await AppointmentService.getAppointments()
    const serviceResponse = await OfficeService.getServices()
    const officeResponse = await OfficeService.getOffices()
    let appointmentsList = response?.data?.appointments || []
    if (appointmentsList?.length) {
      const serviceList = serviceResponse?.data?.services || []
      const officeList = officeResponse?.data?.offices || []
      appointmentsList = appointmentsList.map(appointment => {
        appointment.office = officeList.find(office => (office.office_id === appointment.office_id))
        appointment.service = serviceList.find(service => (service.service_id === appointment.service_id))
        const timezone = appointment.office?.timezone?.timezone_name
        appointment.appointmentDate = CommonUtils.getUTCToTimeZoneTime(appointment.start_time, timezone, 'MMM dd, yyyy')
        appointment.appointmentStartTime = CommonUtils.getUTCToTimeZoneTime(appointment.start_time, timezone, 'hh:mmaaaa')
        appointment.appointmentEndTime = CommonUtils.getUTCToTimeZoneTime(appointment.end_time, timezone, 'hh:mmaaaa')
        return appointment
      })
    }
    return appointmentsList
  }

  // @Action({ rawError: true })
  // public async updateAppointments () {
  //   const response = await AppointmentService.updateAppointment()
  //   return response?.data || []
  // }

  @Action({ rawError: true })
  public async deleteAppointment (appointmentId: number) {
    const response = await AppointmentService.deleteAppointment(appointmentId)
    return response || {}
  }

  @Action({ rawError: true })
  public async submitFeedback (feedbackRequest: FeedbackRequestObject) {
    const response = await FeedbackService.submitFeedback(feedbackRequest)
    return response || {}
  }
}
