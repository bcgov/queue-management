import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators'
import { Appointment } from '@/models/appointment'
import AppointmentService from '@/services/appointment.services'
import CommonUtils from '@/utils/common-util'
import { store } from '@/store'

@Module({
  name: 'appointment',
  namespaced: true,
  store,
  dynamic: true
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
    return response?.data?.appointments || []
  }
}
