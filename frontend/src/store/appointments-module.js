import Vue from 'vue'
import { Axios } from './helpers'
import moment from 'moment'

export default {
  editing: false,
  rescheduling: false,
  namespaced: true,
  state: {
    appointments: [],
    calendarSetup: {
      title: null,
      name: null
    },
    selectedService: null,
    showApptBookingModal: false,
    showCheckInModal: false,
    services: [],
  },
  getters: {
    service_name: (state, getters, rootState) => {
      if (rootState.services && rootState.services.length > 0) {
        if (state.selectedService) {
          let { services } = rootState
          return services.find(srv => srv.service_id === state.selectedService).service_name
        }
      }
      return 'Please choose a service'
    },

    appointment_events(state) {
      if (state.appointments.length > 0) {
        return state.appointments.map(apt =>
          ({
            start: apt.start_time,
            end: apt.end_time,
            appointment_id: apt.appointment_id,
            service_id: parseInt(apt.service_id),
            title: apt.citizen_name,
            contact_information: apt.contact_information,
            comments: apt.comments,
            color: '#B5E0B8',
          })
        )
      }
      return []
    },
    calendar_setup(state) {
      if ((state.calendarSetup || {}).name) {
        let { title, name } = state.calendarSetup
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
    services(state, getters, rootState) {
      if (rootState.services) {
        return rootState.services
      }
      return []
    }
  },
  actions: {
    clearAddModal({commit}) {
      commit('updateAddModalForm', { type: 'search', value: null}, {root: true})
      commit('setSelectedService', null)
    },
  
    resetAddModalForm({commit}) {
      commit('resetAddModalForm', null, {root: true})
    },
    
    getAppointments({commit, rootState}) {
      let state = rootState
      let output = []
      return new Promise((resolve, reject) => {
        Axios({state}).get('/appointments/').then( resp => {
          let appts = resp.data.appointments
          if (appts.length > 0) {
            output = appts.filter(ap => !ap.checked_in_time)
          }
          commit('setAppointments', output)
          resolve()
        })
      })
    },
    
    getChannels({dispatch}) {
      dispatch('getChannels', null, {root: true})
    },
    
    putAppointment({dispatch, rootState}, payload) {
      let state = rootState
      let { id } = payload
      return new Promise((resolve, reject) => {
        Axios({state}).put(`/appointments/${id}/`, payload.data).then( resp => {
          dispatch('getAppointments')
          resolve()
        })
      })
    },
    
    getServices({dispatch, commit}) {
      dispatch('getServices', null, {root: true})
      dispatch('getCategories', null, {root: true})
      dispatch('getChannels', null, {root: true})
    },
    
    postAddToQueue({rootState}, payload) {
      let state = rootState
      return new Promise((resolve, reject) => {
        let url = `/citizens/${payload}/add_to_queue/`
        Axios({state}).post(url,{}).then(resp=>{
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },
  
    postAppointment({rootState}, payload) {
      let state = rootState
      payload.office_id = rootState.user.office_id
      return new Promise((resolve, reject) => {
        Axios({state}).post('/appointments/', payload).then( resp => {
          resolve(resp)
        })
      })
    },
    
    postCheckIn({ dispatch, rootState }, payload) {
      let state = rootState
      let data = {
        checked_in_time: moment.utc().format(),
        appointment_id: payload.appointment_id,
        service_id: payload.service_id,
        citizen_name: payload.title,
      }
      return new Promise((resolve, reject) => {
        Axios({state}).put(`/appointments/${payload.appointment_id}/`, data).then( () => {
          dispatch('sendToQueue', payload)
        })
      })
    },
    
    postServiceReq({rootState}, payload) {
      let state = rootState
      let service_request = {
        service_id: payload.service_id,
        citizen_id: payload.citizen_id,
        quantity: payload.quantity,
        channel_id: payload.channel_id,
        priority: payload.priority,
      }
      return new Promise((resolve, reject) => {
        let url = `/service_requests/`
        Axios({state}).post(url, {service_request}).then(resp=>{
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },
  
    putCitizen({rootState}, payload) {
      let state = rootState
      let {
        citizen_id
      } = payload
      let data = {
        priority: 1,
        citizen_comments: `APPOINTMENT: ${payload.citizen_name}`,
      }
      return new Promise((resolve, reject) => {
        let url = `/citizens/${citizen_id}/`
        Axios({state}).put(url, data).then(resp => {
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },
    
    deleteAppointment({dispatch, rootState}, payload) {
      let state = rootState
      return new Promise((resolve, reject) => {
        Axios({state}).delete(`/appointments/${payload}/`).then( () => {
          dispatch('getAppointments').then( () => {
            resolve()
          })
        })
      })
    },
  
    sendToQueue({dispatch, commit, rootState}, payload) {
      let state = rootState
      Axios({state}).post('/citizens/', {}).then(resp => {
        let { citizen_id } = resp.data.citizen
        let { channel_id } = rootState.channels.find(ch => ch.channel_name.includes('Person'))
        let { service_id } = payload
        let citizen_name = payload.title
        let quantity = 1
        let priority  = 1
        let data = { service_id, citizen_id, channel_id, quantity, priority, citizen_name }
        commit('setAppointmentsStateInfo', data, { root: true })
        dispatch('putCitizen', data).then( () => {
          dispatch('postServiceReq', data).then( () => {
            dispatch('postAddToQueue', data.citizen_id).then( () => {
              dispatch('getAppointments').then( () => {
                commit('toggleCheckInModal', false)
              })
            })
          })
        })
      })
    },
    toggleAddModal({commit}, payload) {
      commit('toggleAddModal', payload, {root: true})
      if (payload) {
        commit('switchAddModalMode', 'add_mode', {root: true})
      }
    },
  },
  mutations: {
    setEditedStatus: (state, payload) => state.editing = payload,
    setAppointments: (state, payload) => state.appointments = payload,
    setCalendarSetup: (state, payload) => {
      let { title, name } = payload
      state.calendarSetup = { title, name }
    },
    toggleApptBookingModal: (state, payload) => state.showApptBookingModal = payload,
    toggleCheckInModal: (state, payload) => state.showCheckInModal = payload,
    setSelectedService: (state, payload) => {
      state.selectedService = null
      state.selectedService = payload
    },
    setRescheduling: (state, payload) => state.reschedulinng = payload,
  },
}