
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
import { Axios } from './../helpers'
import moment from 'moment'

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
    editDeleteSeries: false,
    selectedService: null,
    showApptBookingModal: false,
    showAppointmentBlackoutModal: false,
    showCheckInModal: false,
    services: [],
    submitClicked: false,
    draftAppointment: {}

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

    appointment_events (state) {
      if (state.appointments.length > 0) {
        return state.appointments.map(apt =>
          ({
            start: apt.start_time,
            end: apt.end_time,
            appointment_id: apt.appointment_id,
            service_id: parseInt(apt.service_id),
            citizen_id: apt.citizen_id,
            title: apt.citizen_name,
            contact_information: apt.contact_information,
            comments: apt.comments,
            color: '#B5E0B8',
            blackout_flag: apt.blackout_flag,
            is_draft: apt.is_draft,
            recurring_uuid: apt.recurring_uuid,
            online_flag: apt.online_flag
          })
        )
      }
      return []
    },
    calendar_setup (state) {
      if ((state.calendarSetup || {}).name) {
        const { title, name } = state.calendarSetup
        return {
          name,
          title
        }
      }
      return {
        name: 'agendaWeek',
        title: 'Appointments'
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
    is_recurring_enabled (state, getters, rootState) {
      if (rootState.recurringFeatureFlag === 'On') {
        return true
      }
      return false
    }
  },
  actions: {
    clearAddModal ({ commit }) {
      commit('updateAddModalForm', { type: 'search', value: null }, { root: true })
      commit('setSelectedService', null)
    },

    deleteAppointment ({ dispatch, rootState }, payload) {
      const state = rootState
      return new Promise((resolve, reject) => {
        Axios({ state }).delete(`/appointments/${payload}/`).then(() => {
          dispatch('getAppointments').then(() => {
            resolve()
          })
        })
      })
    },

    deleteRecurringAppointments ({ dispatch, rootState }, payload) {
      const state = rootState
      return new Promise((resolve, reject) => {
        Axios({ state }).delete(`/appointments/recurring/${payload}`).then(() => {
          dispatch('getAppointments').then(() => {
            resolve()
          })
        })
      })
    },

    getAppointments ({ commit, rootState }) {
      const state = rootState
      let output = []
      return new Promise((resolve, reject) => {
        Axios({ state }).get('/appointments/').then(resp => {
          const appts = resp.data.appointments
          if (appts.length > 0) {
            output = appts.filter(ap => !ap.checked_in_time)
          }
          commit('setAppointments', output)
          resolve()
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
      payload.office_id = rootState.user.office_id
      payload.appointment_draft_id = 1
      return new Promise((resolve, reject) => {
        Axios({ state }).post('/appointments/', payload).then(resp => {
          resolve(resp)
        })
      })
    },

    postCheckIn ({ commit, dispatch, rootState }, payload) {
      const state = rootState
      const data = {
        checked_in_time: moment.utc().format(),
        appointment_id: payload.appointment_id,
        service_id: payload.service_id,
        citizen_name: payload.title
      }
      payload.start_time = data.checked_in_time
      payload.snowplow_addcitizen = true
      return new Promise((resolve, reject) => {
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
      return new Promise((resolve, reject) => {
        Axios({ state }).put(`/appointments/${id}/`, payload.data).then(resp => {
          dispatch('getAppointments')
          resolve()
        })
      })
    },

    putRecurringAppointment ({ dispatch, rootState }, payload) {
      const state = rootState
      const uuid = payload.recurring_uuid

      return new Promise((resolve, reject) => {
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
        start_time: payload.start_time,
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
      if (payload) {
        commit('switchAddModalMode', 'add_mode', { root: true })
      }
    },

    // toggleApptBookingModalWithDraft ({ commit }, payload) {
    //   commit('toggleApptBookingModal', payload, { root: true })
    //   if (payload) {
    //     // commit('switchAddModalMode', 'add_mode', { root: true })
    //   }
    // },
    async postDraftAppointment ({ rootState, commit }, payload) {
      const state = rootState
      // console.log('currentState', currentState)
      // draftAppointments
      payload.office_id = rootState.user.office_id
      return new Promise((resolve, reject) => {
        Axios({ state }).post('/appointments/draft', payload).then(resp => {
          commit('setDraftAppointments', resp.data)
          resolve(resp)
        })
      })
    },
    // need to set draft appointment id
    deleteDraftAppointment ({ dispatch, rootState, state, commit }) {
      // const state = rootState

      const draftAppointmentId = state.draftAppointment.appointment && state.draftAppointment.appointment.appointment_id

      if (draftAppointmentId) {
        return new Promise((resolve, reject) => {
          Axios({ state: rootState }).delete(`/appointments/draft/${draftAppointmentId}/`).then((resp) => {
            commit('setDraftAppointments', {})
            resolve(resp)
            // dispatch('getAppointments').then(() => {
            //   resolve()
            // })
          })
        })
      }
    },

    updateAppointments ({ commit, state }, data ) {

      const { appointment, action='create' } = data
      let output:any = []

      const currentAppointment = state.appointments
    
      if (action==='create') {
        output = [...currentAppointment, appointment]
      } else if (action==='update') {
        const  currentApp = currentAppointment.filter(app  => {
          return app.appointment_id !== appointment.appointment_id
        })
        output = [...currentApp, appointment]
      } else if (action==='delete') {
       const  currentApp = currentAppointment.filter(app  => {
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
    setCalendarSetup: (state, payload) => {
      const { title, name } = payload
      state.calendarSetup = { title, name }
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
    setDraftAppointments: (state, payload) => state.draftAppointment = payload
  }
}
