/*Copyright 2015 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.*/



import Vue from 'vue'
import 'es6-promise/auto'
import Vuex from 'vuex'
import { Axios } from './helpers'
var flashInt

Vue.use(Vuex)

export const store = new Vuex.Store({

  state: {
    addModalForm: {
      citizen:'',
      comments: '',
      channel: '',
      search: '',
      category: '',
      service:'',
      quick: 0,
      suspendFilter: false,
      selectedItem: ''
    },
    addModalSetup: null,
    alertMessage: '',
    allCitizens: [],
    bearer: '',
    categories: [],
    channels: [],
    citizens: [],
    citizenInvited: false,
    dismissCountDown: 0,
    isLoggedIn: false,
    nowServing: false,
    officeType: null,
    serveNowAltAction: false,
    serveNowStyle: 'btn-primary',
    serviceBegun: false,
    serviceModalForm: {
      citizen_id: null,
      service_citizen: null,
      citizen_comments: '',
      activeQuantity: 1
    },
    services: [],
    showAddModal: false,
    showServiceModal: false,
    user: {
      username: null,
      office: {
        office_id: null,
        office_name: null,
        sb: {
          sb_type: null,
        },
      },
      office_id: null,
      qt_xn_csr_ind: true,
      receptionist_ind: null,
      checkComplete: false
    },
  },

  getters: {
    reception(state) {
      if (state.user.office && state.user.office.sb)
        if (state.user.office.sb.sb_type === "callbyname" || state.user.office.sb.sb_type === "callbyticket") {
          return true
        }
        return false
    },

    active_index(state, getters) {
      let { service_citizen } = state.serviceModalForm

      if (!service_citizen || !service_citizen.service_reqs || service_citizen.service_reqs.length === 0) {
        return 0
      }
      return service_citizen.service_reqs.findIndex(sr => sr.periods.some(p => p.time_end == null))
    },

    active_service: (state, getters) => {
      let { service_citizen } = state.serviceModalForm
      if (!service_citizen || !service_citizen.service_reqs || service_citizen.service_reqs.length === 0) {
        return null
      }
      return service_citizen.service_reqs.filter(sr => sr.periods.some(p => p.time_end == null))[0]
    },

    active_service_id: (state) => (citizen_id) => {
      let { citizens } = state
      let citizen = citizens.find(c => c.citizen_id === citizen_id)

      return citizen.service_reqs.find(sr=>sr.periods.some(p=>p.time_end === null))
    },

    invited_service_reqs: (state, getters) => {
      let { service_citizen } = state.serviceModalForm

      if (!service_citizen || !service_citizen.service_reqs || service_citizen.service_reqs.length === 0) {
        return []
      }

      return service_citizen.service_reqs.sort((a,b) => { return b.sr_id - a.sr_id })
    },

    invited_citizen: (state) => {
      let { service_citizen } = state.serviceModalForm
      return service_citizen
    },

    on_hold_queue(state) {
      let { citizens } = state
      if (!citizens || citizens.length===0) {
        return []
      }

      let isCitizenOnHold = function(c) {
        let test = c.service_reqs.filter(sr=>sr.periods.some(p=>p.time_end == null && p.ps.ps_name === 'On hold'))
        if (test.length > 0) {
          return true
        } else {
          return false
        }
      }
      let filtered = citizens.filter(c=>c.service_reqs.length > 0)
      let list = filtered.filter(isCitizenOnHold)
      return list
    },

    citizens_queue(state) {
      let { citizens } = state
      if (!citizens || citizens.length===0) {
        return []
      }

      let isCitizenQueued = function(c) {
        let test = c.service_reqs.filter(sr=>sr.periods.some(p=>p.time_end == null && p.ps.ps_name === 'Waiting'))
        if (test.length > 0) {
          return true
        } else {
          return false
        }
      }
      let filtered = citizens.filter(c=>c.service_reqs.length > 0)
      let list = filtered.filter(isCitizenQueued)
      return list
    },

    form_data: state => {
      return state.addModalForm
    },

    channel_options: state => {
      return state.channels.map(ch=>({value: ch.channel_id, text: ch.channel_name}))
    },

    categories_options: (state, getters) => {
      let opts = state.categories
      let mappedOpts = opts.map(opt =>
          ({value: opt.service_id, text: opt.service_name})
        )
      let blankOpt = [{value:'', text:'Categories'}]
      return blankOpt.concat(mappedOpts)
    },

    filtered_services: (state, getters) => {
      let services = state.services

      if (getters.form_data.category) {
        return services.filter(service=>service.parent.service_id === getters.form_data.category)
      } else {
        return services
      }
    },

    quick_trans_status(state) {
      if (state.user.qt_xn_csr_ind == 1) {
        return true
      } else if (state.user.qt_xn_csr_ind == 0) {
        return false
      }
    }
  },

  actions: {
    flashServeNow(context, payload) {
      let flash = () => {
        if ( context.state.serveNowStyle === 'btn-primary' ) {
          context.commit('flashServeNow', 'btn-highlighted')
        } else if ( context.state.serveNowStyle === 'btn-highlighted' ) {
          context.commit('flashServeNow', 'btn-primary')
        }
      }
      if (payload === 'start') {
        flashInt = setInterval( ()=>{ flash() }, 800)
        return
      }
      if (payload === 'stop') {
        clearInterval(flashInt)
        context.commit('flashServeNow', 'btn-primary')
      }
    },

    logIn(context, payload) {
      context.commit('setBearer', payload)
      context.commit('logIn')
      context.dispatch('getUser')
    },

    getAllCitizens(context) {
      let url = '/citizens/'
      Axios(context).get(url).then( resp => {
        if (!resp.data.citizens) {
          context.commit('updateQueue', [])
          return
        }
        context.commit('updateQueue', resp.data.citizens)
        if (!context.state.checkComplete) {
          context.dispatch('checkForUnfinishedService', resp.data.citizens).then(()=>{
            context.commit('logCheckComplete', true)
          })

        }
      })
    },

    getCategories(context) {
      Axios(context).get('/categories/')
        .then( resp => {
          context.commit('setCategories', resp.data.categories)
        })
        .catch(error => {
          console.log('error @ store.actions.getCategories')
          console.log(error.response)
          console.log(error.message)
        })
    },

    getChannels(context) {
      return new Promise((resolve, reject) => {
        let url = `/channels/`
        Axios(context).get(url).then(resp=>{
          context.commit('setChannels', resp.data.channels)
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },

    getCitizen(context, citizen_id) {
      return new Promise((resolve, reject) => {
        let url = `/citizens/${citizen_id}/`
        Axios(context).get(url).then(resp=>{
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },

    getServices(context) {
      let office_id = context.state.user.office.office_id
      Axios(context).get(`/services/?office_id=${office_id}`)
        .then( resp => {
          let services = resp.data.services.filter(service => service.actual_service_ind === 1)
          context.commit('setServices', services)
        })
        .catch(error => {
          console.log('error @ store.actions.getServices')
          console.log(error.response)
          console.log(error.message)
        })
    },

    getUser(context) {
      return new Promise((resolve, reject) => {
        let url = '/csrs/me/'
        Axios(context).get(url).then(resp=>{
          context.commit('setUser', resp.data.csr)
          let officeType = resp.data.csr.office.sb.sb_type
          context.commit('setOffice', officeType)
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },

    getOffice(context) {

    },

    cancelAddCitizensModal(context) {
      let { citizen_id } = context.getters.form_data.citizen

      context.dispatch('postCitizenLeft', citizen_id)
        .then( () => {
          context.commit('toggleAddModal', false)
          context.commit('resetAddModalForm')
        })
    },

    clickAddCitizen(context) {
      context.dispatch('toggleModalBack')
      Axios(context).post('/citizens/', {})
        .then(resp => {
          let value = resp.data.citizen
          context.commit('updateAddModalForm', {type:'citizen',value})
          context.commit('toggleAddModal', true)
          context.commit('resetServiceModal')
        })
      if (context.state.categories.length === 0) {
        context.dispatch('getCategories')
      }
      if (context.state.channels.length === 0) {
        context.dispatch('getChannels').then( () => {
          context.commit('setDefaultChannel')
        })
      }
      if (context.state.channels.length > 0) {
        context.commit('setDefaultChannel')
      }
      if (context.state.services.length === 0) {
        context.dispatch('getServices')
      }
    },

    clickAddService(context) {
      if (context.state.channels.length === 0) {
        context.dispatch('getCategories')
        context.dispatch('getChannels')
        context.dispatch('getServices')
      }

      context.dispatch('putServiceRequest').then(() => {
        context.dispatch('putCitizen').then(() => {
          context.commit('switchAddModalMode', 'add_mode')
          context.commit('updateAddModalForm', {
            type: 'citizen',
            value: context.getters.invited_citizen
          })
          context.commit('updateAddModalForm', {
            type: 'channel',
            value: context.getters.active_service.channel_id
          })
          context.commit('updateAddModalForm', {
            type: 'quick',
            value: context.getters.invited_citizen.qt_xn_citizen_ind
          })
          context.commit('toggleAddModal', true)
          context.commit('toggleServiceModal', false)
        })
      })
  },

    clickAddServiceApply(context) {
      context.dispatch('postServiceReq').then(() => {
        context.dispatch('putCitizen').then(() => {
          context.commit('toggleAddModal', false)
          context.commit('toggleServiceModal', true)
          context.dispatch('toggleModalBack')
          context.commit('resetAddModalForm')
        })
      })
  },

    clickAddToQueue(context) {
      let { citizen_id } = context.getters.form_data.citizen

      context.dispatch('putCitizen').then( () => {
        context.dispatch('postServiceReq').then( () => {
          context.dispatch('postAddToQueue', citizen_id).then( resp => {
            context.dispatch('resetAddCitizenModal')
            context.commit('toggleBegunStatus', false)
            context.commit('toggleInvitedStatus', false)

          })
        })
      })
    },

    clickBeginService(context) {
      let {citizen_id} = context.getters.form_data.citizen

      context.dispatch('putCitizen').then( () => {
        context.dispatch('postServiceReq').then( () => {
          context.dispatch('postBeginService', citizen_id).then( () => {
            context.commit('toggleAddModal', false)
            context.commit('toggleBegunStatus', true)
            context.commit('toggleInvitedStatus', false)
            context.commit('toggleServiceModal', true)
            context.commit('resetAddModalForm')
          })
        })
      })
    },

    clickBackOffice(context) {
      context.dispatch('toggleModalBack')
      Axios(context).post('/citizens/', {})
        .then(resp => {
          let value = resp.data.citizen
          context.commit('updateAddModalForm', {type:'citizen',value})
          let chanopts = context.getters.channel_options
          let index = chanopts.findIndex(co=>co.text === 'back office')
          context.commit('updateAddModalForm', {type:'channel', value:chanopts[index].value})
          context.commit('toggleAddModal', true)
        })
      if (context.state.categories.length == 0) {
        context.dispatch('getCategories')
      }
      if (context.state.channels.length == 0) {
        context.dispatch('getChannels')
      }
      if (context.state.services.length == 0) {
        context.dispatch('getServices')
      }
    },

    clickCitizenLeft(context) {
      let {citizen_id} = context.getters.invited_citizen
      context.dispatch('postCitizenLeft', citizen_id)
      context.commit('toggleServiceModal', false)
      context.commit('toggleBegunStatus', false)
      context.commit('toggleInvitedStatus', false)
      context.commit('resetServiceModal')

    },

    clickDashTableRow(context, citizen_id) {
      context.dispatch('postInvite', citizen_id).then( () => {
        context.commit('toggleBegunStatus', false)
        context.commit('toggleInvitedStatus', true)
        context.commit('toggleServiceModal', true)
      })
    },

    clickEdit(context) {
      if (context.state.channels.length === 0) {
        context.dispatch('getCategories')
        context.dispatch('getChannels')
        context.dispatch('getServices')
      }
      context.dispatch('putServiceRequest').then(() => {
        context.dispatch('putCitizen').then(() => {
          context.commit('switchAddModalMode', 'edit_mode')
          context.dispatch('setAddModalData')
          context.commit('toggleAddModal', true)
          context.commit('toggleServiceModal', false)
        })
      })
    },

    clickEditApply(context) {
      context.dispatch('putServiceRequest').then( () => {
        context.dispatch('putCitizen').then(() => {
          context.commit( 'toggleAddModal', false )
          context.dispatch( 'toggleModalBack' )
          context.commit( 'resetAddModalForm' )
          context.commit( 'toggleServiceModal', true )
        })
      })
    },

    clickEditCancel(context) {
      context.commit('toggleAddModal', false)
      context.dispatch('toggleModalBack')
      context.commit('resetAddModalForm')
      context.commit('toggleServiceModal', true)
    },

    clickHold(context) {
      let { citizen_id } = context.state.serviceModalForm
      context.dispatch('putCitizen').then(() => {
        context.dispatch('putServiceRequest').then(() => {
          context.dispatch('postHold', citizen_id).then(() => {
            context.commit('toggleBegunStatus', false)
            context.commit('toggleInvitedStatus', false)
            context.commit('toggleServiceModal', false)
          })
        })
      })
    },

    clickInvite(context) {
      context.dispatch('postInvite', 'next').then(() => {
        context.commit('toggleInvitedStatus', true)
        context.commit('toggleServiceModal', true)
      }).catch(() => {
        context.commit('setMainAlert', 'There are no citizens waiting.')
      })
    },

    checkForUnfinishedService(context, citizens) {

      if (context.state.serviceBegun || context.state.citizenInvited) {
        clearInterval(flashInt)
        context.commit('flashServeNow', 'btn-primary')
        return
      }
      if ( !( context.state.serviceBegun && context.state.citizenInvited ) ) {
        let citizenFound = false
        citizens.forEach(citizen => {
          if ( citizen.service_reqs.length > 0 ) {
            let activeService = citizen.service_reqs.filter(sr => sr.periods.some(p => p.time_end === null))
            if ( activeService[0].periods.length > 0 ) {
              let activePeriod = activeService[0].periods[activeService[0].periods.length - 1]
              if ( ( ['Invited', 'Being Served'].indexOf(activePeriod.ps.ps_name) > -1 )
                && activePeriod.csr.username === this.state.user.username ) {
                citizenFound = true

                if ( activePeriod.ps.ps_name === 'Invited' ) {
                  context.commit('setServiceModalForm', citizen)
                  context.commit('toggleInvitedStatus', true)
                  context.commit('toggleBegunStatus', false)
                  context.dispatch('flashServeNow', 'start')
                  context.commit('resetAddModalForm')
                } else if ( activePeriod.ps.ps_name === 'Being Served' ) {
                  context.commit('setServiceModalForm', citizen)
                  context.commit('toggleInvitedStatus', true)
                  context.commit('setServeNowAction', true)
                  context.dispatch('flashServeNow', 'start')
                  context.commit('resetAddModalForm')
                } else {
                  context.commit('toggleServiceModal', false)
                  context.commit('toggleBegunStatus', false)
                  context.commit('toggleInvitedStatus', false)
                  context.commit('resetAddModalForm')
                }
              }
            }
          }
        })

        if ( !citizenFound ) {
          context.commit('resetServiceModal')
          context.commit('toggleServiceModal', false)
          context.commit('toggleBegunStatus', false)
          context.commit('toggleInvitedStatus', false)
        }
      }
    },

    clickMakeActive(context, sr_id) {
      context.dispatch('putServiceRequest').then(() => {
        context.dispatch('putCitizen').then(() => {
          context.dispatch('postActivateServiceReq', sr_id)
        })
      })
    },

    clickReturnToQueue(context) {
     let {citizen_id} = context.getters.invited_citizen
     context.dispatch('putCitizen').then( () => {
       context.dispatch('putServiceRequest').then( () => {
         context.dispatch('postAddToQueue', citizen_id).then( () => {
           context.commit('toggleInvitedStatus', false)
           context.commit('toggleServiceModal', false)
           context.commit('resetServiceModal')

         })
       })
     })
    },

    clickRowHoldQueue(context, citizen_id) {
      context.dispatch('postBeginService', citizen_id).then( () => {
        context.commit('toggleBegunStatus', true)
        context.commit('toggleInvitedStatus', false)
        context.commit('toggleServiceModal', true)
      })
    },

    toggleBegunStatus(context, payload) {
      context.commit('toggleBegunStatus', payload)
    },

    toggleInvitedStatus(context, payload) {
      context.commit('toggleInvitedStatus', payload)
    },

    clickServeNow(context) {
      if (context.state.serveNowAltAction) {
        context.commit('toggleBegunStatus', true)
        context.commit('toggleInvitedStatus', false)
      }
      context.commit('toggleServiceModal', true)
      context.dispatch('flashServeNow', 'stop')
    },

    clickServiceBeginService(context) {
      let { citizen_id } = context.state.serviceModalForm

      context.dispatch('putCitizen').then( () => {
        context.dispatch('putServiceRequest').then( () => {
          context.dispatch('postBeginService', citizen_id)
          context.commit('toggleBegunStatus', true)
        })
      })
    },

    clickServiceFinish(context) {
      let { citizen_id } = context.state.serviceModalForm

      context.dispatch('putCitizen').then( (resp) => {
        context.dispatch('putServiceRequest').then( () => {
          context.dispatch('postFinishService', citizen_id).then( () => {
            context.commit('toggleServiceModal', false)
            context.commit('toggleBegunStatus', false)
            context.commit('toggleInvitedStatus', false)

          })
        })
      })
    },

    clickServiceModalClose(context) {
      context.commit('toggleServiceModal', false)
      context.commit('toggleInvitedStatus', true)
    },

    messageSlack(context, payload) {
      let slackObject = {
        slack_message: payload.slack_message
      }
      let url = "/slack/"
      Axios.post(url, slackObject)
    },

    postActivateServiceReq(context, sr_id) {
      return new Promise((resolve, reject) => {
        let url = `/service_requests/${sr_id}/activate/`
        Axios(context).post(url).then(resp=>{
            resolve(resp)
          }, error => {
            reject(error)
          })
        })
    },

    postAddToQueue(context, citizen_id) {
      return new Promise((resolve, reject) => {
        let url = `/citizens/${citizen_id}/add_to_queue/`
        Axios(context).post(url,{}).then(resp=>{
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },

    postBeginService(context, citizen_id) {
      return new Promise((resolve, reject) => {
        let url = `/citizens/${citizen_id}/begin_service/`
        Axios(context).post(url,{}).then(resp=>{
          resolve(resp)
        }, error => {
          if (error.response.status === 400) {
              context.commit('setMainAlert', error.response.data.message)
          } else {
            reject(error)
          }
        })
      })
    },

    postCitizenLeft(context, citizen_id) {
      return new Promise((resolve, reject) => {
        let url = `/citizens/${citizen_id}/citizen_left/`
        Axios(context).post(url).then(resp=>{
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },

    postFinishService(context, citizen_id) {
      return new Promise((resolve, reject) => {
        let url = `/citizens/${citizen_id}/finish_service/`
        Axios(context).post(url).then(resp=>{
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },

    postHold(context, citizen_id) {
      return new Promise((resolve, reject) => {
        let url = `/citizens/${citizen_id}/place_on_hold/`
        Axios(context).post(url).then(resp=>{
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },

    postInvite(context, payload) {
      let { qt_xn_csr_ind } = context.state.user
      let data = { qt_xn_csr_ind }
      if (payload==='next') {
        return new Promise((resolve, reject) => {
          let url = `/citizens/invite/`
          Axios(context).post(url, data).then(resp=>{
            resolve(resp)
          }, error => {
            reject(error)
          })
        })
      } else {
        return new Promise((resolve, reject) => {
          let url = `/citizens/${payload}/invite/`
          Axios(context).post(url, data).then(resp=>{
            resolve(resp)
          }, error => {
            if (error.response.status === 400) {
              context.commit('setMainAlert', error.response.data.message)
            } else {
              reject(error)
            }
          })
        })
      }
    },

    postServiceReq(context) {
      let { form_data } = context.getters
      let { citizen_id } = form_data.citizen
      let service_request = {
        service_id: form_data.service,
        citizen_id: citizen_id,
        quantity: 1,
        channel_id: form_data.channel
      }

      return new Promise((resolve, reject) => {
        let url = `/service_requests/`
        Axios(context).post(url, {service_request}).then(resp=>{
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },

    putCitizen(context) {
      let data = {}
      let citizen_id
      let quick

      if (context.state.serviceModalForm.citizen_id) {
        let { citizen_comments } = context.state.serviceModalForm
        citizen_id = context.state.serviceModalForm.citizen_id
        let prevCitizen = context.getters.invited_citizen

        if (context.state.showAddModal) {
          quick = context.getters.form_data.quick
          if (prevCitizen.qt_xn_citizen_ind !== quick) {
            data.qt_xn_citizen_ind = quick
          }
        }
        if (!context.state.showAddModal) {
          if ( citizen_comments !== prevCitizen.citizen_comments ) {
            data.citizen_comments = citizen_comments
          }
        }
      } else {
        let { form_data } = context.getters
        citizen_id = form_data.citizen.citizen_id
        data.qt_xn_citizen_ind = form_data.quick
        if (!form_data.quick) {
          data.qt_xn_citizen_ind = 0
        }
        data.citizen_comments = form_data.comments
      }

      if (Object.keys(data).length === 0) {
        return new Promise((resolve, reject) => { resolve(' ') })
      }


      return new Promise((resolve, reject) => {
        let url = `/citizens/${citizen_id}/`

        Axios(context).put(url, data).then(resp => { resolve(resp) },
          error => { reject(error) })
      })
    },

    putInaccurateIndicator(context) {
      let { citizen_id } = context.getters.invited_citizen
      let { sr_id } = context.getters.active_service

      return new Promise((resolve, reject) => {
        let url = `/service_requests/${sr_id}/`

        Axios(context).put(url, {accurate_time_ind: 0}).then(resp=>{
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },

    putServiceRequest(context) {
      let { citizen_id, activeQuantity } = context.state.serviceModalForm
      let compareService = context.getters.active_service
      let { sr_id } = compareService
      let index = context.getters.active_index

      let data = {}
      if (activeQuantity != compareService.quantity) {
        data.quantity = activeQuantity
      }

      let setup = context.state.addModalSetup
      let { form_data } = context.getters
      if ( setup === 'add_mode' || setup === 'edit_mode') {
        if (form_data.channel != compareService.channel_id) {
          data.channel_id = form_data.channel
        }
        if (form_data.service != compareService.service_id) {
          data.service_id = form_data.service
        }
      }
      if (Object.keys(data).length === 0) {
        return new Promise((resolve, reject) => { resolve(' ') })
      }

      return new Promise((resolve, reject) => {
        let url = `/service_requests/${sr_id}/`
        Axios(context).put(url,data).then(resp=>{
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },

    resetAddCitizenModal(context) {
      context.commit('toggleAddModal', false)
      context.dispatch('toggleModalBack')
      context.commit('resetAddModalForm')
    },

    screenIncomingCitizen(context, citizen) {
      console.log(citizen)
      let { csr_id } = context.state.user
      if (citizen.service_reqs.length > 0) {
        if ( citizen.service_reqs[0].periods) {
          let filteredService = citizen.service_reqs.filter(sr => sr.periods.some(p => p.time_end === null))
          if (filteredService.length > 0) {
            let activeService = filteredService[0]
            if ( activeService.periods.length > 0 ) {
              let l = activeService.periods.length - 1
              let activePeriod = activeService.periods[l]
              if ( activePeriod.csr_id === csr_id ) {
                if (activePeriod.ps.ps_name === 'Invited') {
                  context.commit('setServiceModalForm', citizen)
                  context.commit('toggleServiceModal', true)
                  context.commit('toggleInvitedStatus', true)
                  context.commit('setServeNowAction', true)
                  context.dispatch('flashServeNow', 'start')
                  context.commit('resetAddModalForm')
                } else if (activePeriod.ps.ps_name === 'Being Served') {
                  context.commit('setServiceModalForm', citizen)
                  context.commit('toggleServiceModal', true)
                  context.commit('toggleBegunStatus', true)
                  context.commit('toggleInvitedStatus', false)
                  context.commit('setServeNowAction', false)
                  context.dispatch('flashServeNow', 'stop')
                  context.commit('resetAddModalForm')
                } else {
                  context.commit('resetServiceModal')
                  context.commit('toggleServiceModal', false)
                  context.commit('toggleInvitedStatus', false)
                  context.commit('toggleBegunStatus', false)
                  context.dispatch('flashServeNow', 'stop')
                  context.commit('resetAddModalForm')
                }
              }
            }
            //Citizen is completed or left
          } else {

            //Ensure that we only close serve citizen if it's the citizen _we're_ editing that was finished
            let mostRecentActivePeriod = citizen.service_reqs[0].periods[0]
            citizen.service_reqs.forEach((request) => {
              request.periods.forEach((period) => {
                if (period.time_end > mostRecentActivePeriod.time_end) {
                  mostRecentActivePeriod = period
                }
              })
            })

            if (mostRecentActivePeriod.csr_id === csr_id) {
              context.commit('resetServiceModal')
              context.commit('toggleServiceModal', false)
              context.commit('toggleInvitedStatus', false)
              context.commit('toggleBegunStatus', false)
              context.dispatch('flashServeNow', 'stop')
            }
          }
        }
      }
    },

    setAddModalData(context) {
      let data = {
        citizen: context.getters.invited_citizen,
        active_service: context.getters.active_service
      }
      context.commit('setAddModalData', data)
    },

    toggleModalBack(context) {
      if (context.state.user.office.sb.sb_type === "nocallonsmartboard") {
        context.commit('switchAddModalMode', 'non_reception')
      } else {
        context.commit('switchAddModalMode', 'reception')
      }
    }
  },

  mutations: {
    logIn: state => state.isLoggedIn = true,
    logOut: state => state.isLoggedIn = false,
    setBearer: (state, payload) => state.bearer = payload,
    setUser: (state, payload) => state.user = payload,
    updateQueue(state, payload) {
      state.citizens = []
      state.citizens = payload
    },
    setServices(state, payload) {
      state.services = {}
      state.services = payload
    },
    setChannels(state, payload) {
      state.channels = []
      state.channels = payload
    },
    setCategories(state, payload) {
      state.categories = []
      state.categories = payload
    },

    toggleAddModal: (state, payload) => state.showAddModal = payload,

    updateAddModalForm(state, payload) {
      Vue.set(
        state.addModalForm,
        payload.type,
        payload.value
      )
    },

    setAddModalSelectedItem(state, payload) {
      state.addModalForm.suspendFilter = true
      state.addModalForm.selectedItem = payload
    },

    resetAddModalForm(state) {
      let keys = Object.keys(state.addModalForm)

      keys.forEach(key => {
        if ( key !== 'quick' && key !== 'suspendFilter' ) Vue.set(
          state.addModalForm,
          key,
          ''
        )
        if ( key === 'quick' ) Vue.set(
          state.addModalForm,
          key,
          0
        )
        if ( key === 'suspendFilter' ) Vue.set(
          state.addModalForm,
          key,
          false
        )
      })
    },

    switchAddModalMode(state, payload) {
      state.addModalSetup = payload
    },

    setAddModalData(state, data) {
      let { citizen, active_service } = data

      let formData = {
        comments: citizen.citizen_comments,
        quick: citizen.qt_xn_citizen_ind,
        citizen: citizen,
        channel: active_service.channel_id,
        service: active_service.service_id
      }
      let keys = Object.keys(formData)
      keys.forEach(key => {
        Vue.set(
          state.addModalForm,
          key,
          formData[ key ]
        )
      })
    },

    toggleServiceModal: (state, payload) => state.showServiceModal = payload,

    setServiceModalForm(state, citizen) {
      let citizen_comments = citizen.citizen_comments
      let activeService = citizen.service_reqs.filter(sr => sr.periods.some(p => p.time_end === null))
      let activeQuantity = activeService[0].quantity
      let { citizen_id } = citizen
      let service_citizen = citizen

      let obj = { citizen_comments, activeQuantity, citizen_id, service_citizen }
      let keys = Object.keys(obj)

      keys.forEach(key => {
        Vue.set(
          state.serviceModalForm,
          key,
          obj[ key ]
        )
      })
    },

    resetServiceModal(state) {
      let { serviceModalForm } = state
      let keys = Object.keys(serviceModalForm)

      keys.forEach(key => {
        if ( key === 'activeQuantity' ) {
          Vue.set(
            state.serviceModalForm,
            key,
            1
          )
        } else {
          Vue.set(
            state.serviceModalForm,
            key,
            null
          )
        }
      })
    },

    editServiceModalForm(state, payload) {
      Vue.set(
        state.serviceModalForm,
        payload.type,
        payload.value
      )
    },

    setDefaultChannel(state) {
      let channel = state.channels.filter(ch => ch.channel_name === 'In Person')
      state.addModalForm.channel = channel[ 0 ].channel_id
    },

    setMainAlert(state, payload) {
      state.alertMessage = payload
      state.dismissCountDown = 5
    },

    setModalAlert(state, payload) {
      state.alertMessage = payload
    },

    dismissCountDown(state, payload) {
      state.dismissCountDown = payload
    },

    toggleInvitedStatus: (state, payload) => state.citizenInvited = payload,

    toggleBegunStatus: (state, payload) => state.serviceBegun = payload,

    setQuickTransactionState: (state, payload) => state.user.qt_xn_csr_ind = payload,

    setOffice: (state, officeType) => state.officeType = officeType,

    flashServeNow: (state, payload) => state.serveNowStyle = payload,

    setServeNowAction: (state, payload) => state.serveNowAltAction = payload,

    logCheckComplete: (state, payload) => state.checkComplete = payload
  }
})

