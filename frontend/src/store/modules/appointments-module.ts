/* eslint-disable */
/**
 *
 * Notes
 * JSTOTS - javascript to typescript Conversation
 * Just moved all module from store folder to to modules/* folder
 * No changes in functionality or any variables
 * this is just moving
 * in Future have to extract all functions and export Individually with typs defined
 * and import in index.ts
 *
 */

import { Axios, searchNestedObject } from './../helpers'

import moment from 'moment'

const serviceColor = (blackColor, serviceList, serviceId) => {
  if (blackColor) {
    return 'grey darken-1 white--text'
  }
  const serv = serviceList.find(service => service.service_id === serviceId)
  if (serv && serv.css_colour && serv.css_colour !== null) {
    return serv.css_colour
  }
  return 'cal-events-default'
}
const serviceName = (serviceList, serviceId) => {
  const serv = serviceList.find(service => service.service_id === serviceId)
  if (serv && serv.service_name) {
    return serv.service_name
  }
  return ''
}

export default {
  editing: false,
  namespaced: true,
  state: {
    appointments: [],
    apptRescheduling: false,
    calendarSetup: {
      title: null,
      name: null
    },
    checkInClicked: false,
    clickedAppt: null,
    clickedTime: null,
    editDeleteSeries: false,
    selectedService: null,
    showApptBookingModal: false,
    showAppointmentBlackoutModal: false,
    showCheckInModal: false,
    services: [],
    submitClicked: false,
    draftAppointment: {},
    toggleAppCalenderView: false,
    selected_office_id: null, // selected in the appointment page and reset based on the office_id each time we load appointment page

  },
  getters: {
    service_name: (state, getters, rootState) => {
      if (rootState.services && rootState.services.length > 0) {
        if (state.selectedService) {
          const { services } = rootState
          return services.find(srv => srv.service_id === state.selectedService).service_name
        }
      }
      return 'Please choose a service'
    },

    appointment_events (state, rootState) {
      if (state.appointments.length > 0) {
        return state.appointments.map(apt =>
          ({
            start: new Date(new Date(apt.start_time).toLocaleString('en-US', { timeZone: apt.office.timezone.timezone_name })),
            end: new Date(new Date(apt.end_time).toLocaleString('en-US', { timeZone: apt.office.timezone.timezone_name })),
            appointment_id: apt.appointment_id,
            service_id: parseInt(apt.service_id),
            citizen_id: apt.citizen_id,
            title: apt.citizen_name,
            name: apt.citizen_name,
            contact_information: apt.contact_information,
            comments: apt.comments,
            color: serviceColor(apt.is_draft || apt.blackout_flag === 'Y' || apt.stat_flag, rootState.services, parseInt(apt.service_id)), // apt.is_draft || apt.blackout_flag === 'Y' ? 'grey darken-1 white--text' : 'cal-events-default', //  apt.is_draft ? 'rgb(239, 212, 105)' : 'grey darken-1', // '#B5E0B8',
            blackout_flag: apt.blackout_flag,
            is_draft: apt.is_draft,
            recurring_uuid: apt.recurring_uuid,
            online_flag: apt.online_flag,
            timed: true,
            serviceName: serviceName(rootState.services, parseInt(apt.service_id)),
            stat_flag: apt.stat_flag,

          })
        )
      }
      return []
    },
    calendar_setup (state) {
      if ((state.calendarSetup || {}).name) {
        const { title, name, titleRef } = state.calendarSetup
        return {
          name,
          title,
          titleRef
        }
      }
      return {
        name: 'agendaWeek',
        title: 'Appointments',
        titleRef: null
      }
    },
    services (state, getters, rootState) {
      if (rootState.services) {
        return rootState.services
      }
      return []
    },
    is_GA (state, getters, rootState) {
      if (rootState.user && rootState.user.role && rootState.user.role.role_code === 'GA') {
        return true
      }
      return false
    },
    is_Support (state, getters, rootState) {
      if (rootState.user && rootState.user.role && rootState.user.role.role_code === 'SUPPORT') {
        return true
      }
      return false
    },
    is_recurring_enabled (state, getters, rootState) {
      if (rootState.recurringFeatureFlag === 'On') {
        return true
      }
      return false
    },

    filtered_appointment_events: (state, getters) => search => {
      return getters.appointment_events.filter(event => {
        return searchNestedObject(event, search)
      }
      )
    },
    getApiTotalCount (state) {
      return state.apiCallTotal
    },
    getSelectedOfficeId (state) {
      return state.selected_office_id
    }
  },
  actions: {
    clearAddModal ({ commit }) {
      commit('updateAddModalForm', { type: 'search', value: null }, { root: true })
      commit('setSelectedService', null)
    },

    deleteAppointment ({ dispatch, rootState }, payload) {
      const state = rootState
      return new Promise<void>((resolve, reject) => {
        Axios({ state }).delete(`/appointments/${payload}/`).then(() => {
          dispatch('getAppointments').then(() => {
            resolve()
          })
        })
      })
    },

    deleteRecurringAppointments ({ dispatch, rootState }, payload) {
      const state = rootState
      return new Promise<void>((resolve, reject) => {
        Axios({ state }).delete(`/appointments/recurring/${payload}`).then(() => {
          dispatch('getAppointments').then(() => {
            resolve()
          })
        })
      })
    },

    deleteRecurringStatAppointments ({ dispatch, rootState }, payload) {
      const state = rootState
      return new Promise<void>((resolve, reject) => {
        Axios({ state }).delete(`/appointments/all-stat/${payload}`).then(() => {
          dispatch('getAppointments').then(() => {
            resolve()
          })
        })
      })
    },

    getAppointments ({ commit, rootState }) {
      let output = []
      const state = rootState
      const office_id = state.appointmentsModule.selected_office_id
      return new Promise((resolve, reject) => {
        Axios({ state }).get(`/appointments/?office_id=${office_id}`).then(resp => {
          const appts = resp.data.appointments
          if (appts.length > 0) {
            output = appts.filter(ap => !ap.checked_in_time)
          }
          commit('setAppointments', output)
          resolve(output)
        })
      })
    },

    getChannels ({ dispatch }) {
      dispatch('getChannels', null, { root: true })
    },

    getServices ({ dispatch, commit }) {
      dispatch('getServices', null, { root: true })
      dispatch('getCategories', null, { root: true })
      dispatch('getChannels', null, { root: true })
    },

    postAddToQueue ({ rootState }, payload) {
      const state = rootState
      return new Promise((resolve, reject) => {
        const url = `/citizens/${payload}/add_to_queue/`
        Axios({ state }).post(url, {}).then(resp => {
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },
    postBeginService ({ rootState }, payload) {
      const state = rootState
      return new Promise((resolve, reject) => {
        const url = `/citizens/${payload}/begin_service/`
        Axios({ state }).post(url, {}).then(resp => {
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },

    postAppointment ({ rootState }, payload) {
      const state = rootState
      payload.office_id = state.appointmentsModule.selected_office_id
      payload.appointment_draft_id = 1
      return new Promise((resolve, reject) => {
        Axios({ state }).post('/appointments/', payload).then(resp => {
          resolve(resp)
        })
      })
    },

    async createAxioObject ({ rootState }, payload) {
      const state = rootState
      payload.office_id = rootState.user.office_id
      payload.appointment_draft_id = 1
      return Axios({ state }).post('/appointments/', payload)
    },

    async createStatAxioObject ({ rootState }, payload) {
      const state = rootState
      payload.appointment_draft_id = 1
      return Axios({ state }).post('/appointments/', payload)
    },

    async callBulkAxios({ rootState }, payload) {
      let flag =  false
      await Promise.all(payload.axiosArray).then(function() {
        flag = payload['flag']
      })
      return flag
    },
    postCheckIn ({ commit, dispatch, rootState }, payload) {
      const state = rootState
      const data = {
        checked_in_time: moment.utc().format(),
        appointment_id: payload.appointment_id,
        service_id: payload.service_id,
        citizen_name: payload.title 
      }
      if (!payload.hasOwnProperty('start_time'))
      {
        payload.start_time = data.checked_in_time
      }
      payload.snowplow_addcitizen = true
      return new Promise<void>((resolve, reject) => {
        Axios({ state }).put(`/appointments/${payload.appointment_id}/`, data).then(() => {
          if (state.officeType != 'nocallonsmartboard') {
            dispatch('sendToQueue', payload)
            setTimeout(() => { commit('toggleCheckInClicked', false) }, 2000)
            resolve()
          } else {
            dispatch('sendToService', payload)
            setTimeout(() => { commit('toggleCheckInClicked', false) }, 2000)
            resolve()
          }
        })
      })
    },

    postServiceReq ({ rootState }, { citizen_id, payload }) {
      const state = rootState
      const { channel_id } = rootState.channels.find(ch => ch.channel_name.includes('Person'))
      const service_request = {
        channel_id,
        citizen_id,
        priority: 1,
        quantity: 1,
        service_id: payload.service_id
      }
      return new Promise((resolve, reject) => {
        const url = '/service_requests/'
        Axios({ state }).post(url, { service_request }).then(resp => {
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },

    putAppointment ({ dispatch, rootState }, payload) {
      const state = rootState
      const { id } = payload
      return new Promise<void>((resolve, reject) => {
        Axios({ state }).put(`/appointments/${id}/`, payload.data).then(resp => {
          dispatch('getAppointments')
          resolve()
        })
      })
    },

    putRecurringAppointment ({ dispatch, rootState }, payload) {
      const state = rootState
      const uuid = payload.recurring_uuid

      return new Promise<void>((resolve, reject) => {
        Axios({ state }).put(`/appointments/recurring/${uuid}`, payload.data).then(resp => {
          dispatch('getAppointments')
          resolve()
        })
      })
    },

    putCitizen ({ rootState }, { citizen_id, payload }) {
      const start = moment(payload.start).clone().format('h:mm')
      if (!payload.comments) {
        payload.comments = ''
      }
      if (!payload.snowplow_addcitizen) {
        payload.snowplow_addcitizen = false
      }
      const data = {
        priority: 1,
        citizen_comments: `${start}|||${payload.comments}`,
        citizen_name: payload.title,
        start_time: payload.start_time.replace('+00:00', 'Z'),
        snowplow_addcitizen: payload.snowplow_addcitizen
      }

      return new Promise((resolve, reject) => {
        const state = rootState
        const url = `/citizens/${citizen_id}/`
        Axios({ state }).put(url, data).then(resp => {
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },

    resetAddModalForm ({ commit }) {
      commit('resetAddModalForm', null, { root: true })
    },

    sendToQueue ({ dispatch, commit, rootState }, payload) {
      const citizen_id = payload.citizen_id
      commit('setAppointmentsStateInfo', payload, { root: true })
      dispatch('putCitizen', { citizen_id, payload }).then(() => {
        dispatch('postServiceReq', { citizen_id, payload }).then(() => {
          dispatch('postAddToQueue', citizen_id).then(() => {
            dispatch('getAppointments').then(() => {
              commit('toggleCheckInModal', false)
            })
          })
        })
      })
    },
    sendToService ({ dispatch, commit, rootState }, payload) {
      const citizen_id = payload.citizen_id
      commit('setAppointmentsStateInfo', payload, { root: true })
      dispatch('putCitizen', { citizen_id, payload }).then(() => {
        dispatch('postServiceReq', { citizen_id, payload }).then(() => {
          dispatch('postBeginService', citizen_id).then(() => {
            dispatch('getAppointments').then(() => {
              commit('toggleCheckInModal', false)
            })
          })
        })
      })
    },

    toggleAddModal ({ commit }, payload) {
      commit('toggleAddModal', payload, { root: true })
    },

    async postDraftAppointment ({ rootState, commit }, payload) {
      const state = rootState
      // draftAppointments
      payload.office_id = state.appointmentsModule.selected_office_id
      return new Promise((resolve, reject) => {
        Axios({ state }).post('/appointments/draft', payload).then(resp => {
          commit('setDraftAppointments', resp.data)
          resolve(resp)
        })
      })
    },
    // need to set draft appointment id
    deleteDraftAppointment ({ dispatch, rootState, state, commit }) {

      const draftAppointmentId = state.draftAppointment.appointment && state.draftAppointment.appointment.appointment_id

      if (draftAppointmentId) {
        return new Promise((resolve, reject) => {
          Axios({ state: rootState }).delete(`/appointments/draft/${draftAppointmentId}/`).then((resp) => {
            commit('setDraftAppointments', {})
            resolve(resp)
          })
        })
      }
    },

    updateAppointments ({ commit, state, rootState }, data) {
      const { appointment, action = 'create' } = data

      const currentAppointment = state.appointments
      let output: any = currentAppointment
      if (action === 'create') {
        if (appointment.office_id === rootState.user.office_id) {
          output = [...currentAppointment, appointment]
        }
      } else if (action === 'update') {
        if (appointment.office_id === rootState.user.office_id) {
          const currentApp = currentAppointment.filter(app => {
            return app.appointment_id !== appointment.appointment_id
          })
          output = [...currentApp, appointment]
        }
      } else if (action === 'delete') {
        const currentApp = currentAppointment.filter(app => {
          return app.appointment_id !== appointment
        })
        output = currentApp
      }
      commit('setAppointments', output)
    }
  },
  mutations: {
    setEditedStatus: (state, payload) => state.editing = payload,
    setAppointments: (state, payload) => state.appointments = payload,
    setAppointmentsOfficeId: (state, payload) => {
      state.selected_office_id = payload;
    },
    setCalendarSetup: (state, payload) => {
      const { title, name, titleRef } = payload
      state.calendarSetup = { title, name, titleRef }
    },
    toggleApptBookingModal: (state, payload) => state.showApptBookingModal = payload,
    toggleCheckInClicked: (state, payload) => state.checkInClicked = payload,
    toggleCheckInModal: (state, payload) => state.showCheckInModal = payload,
    toggleEditDeleteSeries: (state, payload) => state.editDeleteSeries = payload,
    toggleSubmitClicked: (state, payload) => state.submitClicked = payload,
    setSelectedService: (state, payload) => {
      state.selectedService = null
      state.selectedService = payload
    },
    setRescheduling: (state, payload) => state.apptRescheduling = payload,
    toggleAppointmentBlackoutModal: (state, payload) => state.showAppointmentBlackoutModal = payload,
    setDraftAppointments: (state, payload) => state.draftAppointment = payload,
    setAgendaClickedAppt: (state, payload) => state.clickedAppt = payload,
    setAgendaClickedTime: (state, payload) => state.clickedTime = payload,
    setApiTotalCount: (state, payload) => {
      state.apiCallTotal = payload
    },
    setToggleAppCalenderView: (state, payload) => state.toggleAppCalenderView = payload,
  }
}
