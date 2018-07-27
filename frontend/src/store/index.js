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
import axios from 'axios'
import Vuex from 'vuex'
import { Axios } from './helpers'

import { formData, invitedCitizen } from './helpers'

Vue.use(Vuex)

export const store = new Vuex.Store({

  state: {
    isLoggedIn: false,
    bearer: '',
    user: {
      username: null,
      office: {
        office_name: null
      }
    },
    invitedCitizen: {
      ticket_number: null,
      service_reqs: [
        {
          start_time: null,
          channel: {
            channel_name: null,
            channel_id: null
          }
        }
      ]
    },
    servedCitizen: {
      ticket_number: null,
      service_reqs: [
        {
          start_time: null,
          channel: {
            channel_name: null,
            channel_id: null
          }
        }
      ]
    },
    searchScreenNextService: false,
    serviceCommentsEdited: false,
    addCitizenModal: {
      visible: false,
      formData: {
        citizen:'',
        comments: '',
        channel: '',
        search: '',
        category: '',
        service:'',
        quick: false,
        setup: ''
      },
    },
    showAddModal: false,
    showServiceModal: false,
    citizens: [],
    services: null,
    categories: [],
    channels: [],
    serveNowDisabled: true,
    alertMessage: '',
    inviteButtonDisabled: false,
    serveButtonDisabled: true,
    addCitizenDisabled: false,
    backOfficeDisabled: false,
    dismissCountDown: 0,
    serveBeginServiceDisabled: false,
    serveCitizenLeftDisabled: false,
    serveReturnQueueDisabled: false,
    finishDisabled: false
  },

  getters: {
    filtered_citizens(state) {
      let { citizens } = state
      
      if (citizens.length === 0) {
        return []
      }
      console.log('cit')
      console.log(citizens)
      let filter0 = citizens.filter(c=>c.service_reqs.length >= 1)
      console.log('0')
      console.log(filter0)
      return filter0.filter(c=>c.service_reqs[0].periods.some(p=>p.time_end == null && p.ps.ps_name === 'Waiting'))
    },
    
    search_screen_setup(state) {
      let indicator = state.user.receptionist_ind
      let nextService = state.searchScreenNextService
     
      if (indicator === 0) {
        return 'non_reception'
      }
      else if (indicator === 1) {
        if (nextService === false) {
          return 'reception'
        }
        else if (nextService === true) {
          return "serve_now"
        }
      }
    },
    form_data: state => {
      return state.addCitizenModal.formData
    },
    channel_options: state => {
      return(
        state.channels.map(ch=>
          ({value: ch.channel_id, text: ch.channel_name})
        )
      )
    },
    categories_options: (state, getters) => {
      let opts = state.categories 
      let qry = getters.form_data.search.toUpperCase()
      let filteredOpts
      
      if (getters.form_data.search.length > 1) {
        filteredOpts = opts.filter(opt => 
          opt.service_name.toUpperCase().search(qry) != -1)
      } else {
        filteredOpts = opts
      }
      console.log(filteredOpts)
      let mappedOpts = filteredOpts.map(opt =>
          ({value: opt.service_id, text: opt.service_name})
        )
      let blankOpt = [{value:'', text:''}]
      let finalOpts = blankOpt.concat(mappedOpts)
      return finalOpts
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
    getUser(context) {
      Axios(context).get('/csrs/me/')
        .then( resp => {
          context.commit('setUser', resp.data.csr)
        })
    },
    
    getServices(context) {
      Axios(context).get('/services/')
        .then( resp => {
          context.commit('setServices', resp.data.services)
        })
        .catch(error => {
          console.log('error @ store.actions.getServices')
          console.log(error.response)
          console.log(error.message)
        })
    },
    
    getCategories(context) {
      Axios(context).get('/categories/')
        .then( resp => {
          context.commit('setCategories', resp.data.categories)
          console.log('categories set')          
        })
        .catch(error => {
          console.log('error @ store.actions.getCategories')
          console.log(error.response)
          console.log(error.message)
        })
    },
    
    getChannels(context) {
      Axios(context).get('/channels/')
        .then( resp => {
          context.commit('setChannels', resp.data.channels)
          console.log('channels set')          
        })
        .catch(error => {
          console.log('error @ store.actions.getChannels')
          console.log(error.response)
          console.log(error.message)
        })
    },
    
    getAllCitizens(context) {
      let url = "/citizens/"
      Axios(context).get(url)
        .then( response => {
          context.commit('updateQueue', response.data.citizens)
        })
        .catch(error => {
          console.log('error @ store.actions.getAllCitizens')
          console.log(error.response)
          console.log(error.message)
        })
    },
    
    clickBeginService(context) {
      let {citizen_id} = context.getters.form_data.citizen
      
      context.dispatch('putCitizen').then( resp => {
        context.dispatch('postServiceReq').then( resp => {
          context.dispatch('postBeginService', citizen_id).then( resp => {
            context.commit('setInvitedCitizen', resp.data.citizen)
            context.commit('resetAddCitizen')
            context.commit('toggleAddCitizen', false)
            context.commit('toggleServiceModal', true)
            context.commit('disableServiceButtons')
            context.commit('enableFinish')
          })
        })
      })
    },
  
    clickAddToQueue(context) {
      let { citizen_id } = context.getters.form_data.citizen
      
      context.dispatch('putCitizen').then( resp => {
        context.dispatch('postServiceReq').then( resp => {
          context.dispatch('postAddToQueue', citizen_id).then( resp => {
            context.dispatch('closeAddCitizenModal')
          })
        })
      })
    },
    
    cancelAddCitizensModal(context) {
      let { citizen_id } = context.getters.form_data.citizen
      
      context.dispatch('postCitizenLeft', citizen_id)
        .then( () => {
          context.commit('toggleAddCitizen', false)
          context.commit('resetAddCitizen')
        })
    },
    
    clickServiceBeginService(context) {
      let {citizen_id} = context.state.invitedCitizen
      
      context.dispatch('putCitizenService').then( () => {
        context.dispatch('postBeginService', citizen_id)
        context.commit('disableServiceButtons')
        context.commit('enableFinish')
      })
    },
    
    clickInvite(context) {
      context.dispatch('postInvite', 'next').then( resp => {
        context.commit('setInvitedCitizen', resp.data.citizen)
        context.commit('toggleServiceModal', true)
        context.commit('disableFinish')
      })
      .catch(error=> {
        context.commit('setAlert', 'There are currently not citizens to invite.')
      })  
    },
    
    clickServeNow(context) {
      context.commit('toggleServiceModal', true)
      context.commit('enableButtons')
    },
    
    clickCitizenLeft(context) {
      let {citizen_id} = context.state.invitedCitizen
      context.dispatch('postCitizenLeft', citizen_id)
      context.dispatch('closeServeCitizenModal')
    },
    
    clickReturnToQueue(context) {
      let {citizen_id} = context.state.invitedCitizen
      context.dispatch('postAddToQueue', citizen_id).then( () => {
        context.commit('toggleServiceModal', false)
        context.commit('resetInvitedCitizen')
      })
    },
    
    clickServiceModalClose(context) {
      context.commit('toggleServiceModal', false)
      context.commit('disableButtons')
    },
    
    clickDashTableRow(context, citizen_id) {
      context.dispatch('postInvite', citizen_id).then( resp => {
        context.commit('setInvitedCitizen', resp.data.citizen)
        context.commit('toggleServiceModal', true)
        context.commit('disableFinish')
      })
    },
    
    clickFinishService(context) {
      let { citizen_id } = context.state.invitedCitizen
      
      context.dispatch('postFinishService', citizen_id).then( () => {
        context.commit('toggleServiceModal', false)
        context.commit('resetInvitedCitizen')
        context.commit('enableServiceButtons')
      })
    },
    
    logIn(context, payload) {
      context.commit('setBearer', payload)
      context.commit('logIn')
      context.dispatch('getUser')
      context.dispatch('getAllCitizens')
    },
    
    addCitizen(context) {
      Axios(context).post('/citizens/', {})
        .then(resp => {
          let value = resp.data.citizen
          context.commit('updateModalForm', {type:'citizen',value})
          context.commit('toggleAddCitizen', true)
        })
      context.dispatch('getCategories')
      context.dispatch('getChannels')
      context.dispatch('getServices')
    },
    
    dashTableRow(context, payload) {
      let { citizen_id } = payload.citizen
      Axios(context).get(`/citizens/${citizen_id}/`)
    },

    putCitizen(context) {
      let { formData } = context.state.addCitizenModal
      let { citizen_id } = formData.citizen
      
      let qt_xn_citizen_ind 
      formData.quick ? qt_xn_citizen_ind=1 : qt_xn_citizen_ind = 0
      
      let citizen = {
        citizen_comments: formData.comments,
        qt_xn_citizen_ind 
      }
      
      return new Promise((resolve, reject) => { 
        let url = `/citizens/${citizen_id}/`
        Axios(context).put(url,citizen).then(resp=>{ 
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },
    
    putCitizenService(context) {
      let {citizen_id} = context.state.invitedCitizen
      
      let citizen = {
        citizen_comments: context.state.invitedCitizen.citizen_comments
      }
      
      return new Promise((resolve, reject) => { 
        let url = `/citizens/${citizen_id}/`
        Axios(context).put(url,citizen).then(resp=>{ 
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },
    
    postServiceReq(context) {
      let { formData } = context.state.addCitizenModal
      let { citizen_id } = formData.citizen
      let service_request = {
        service_id: formData.service,
        citizen_id,
        quantity: formData.quantity,
        channel_id: formData.channel
      }
      
      return new Promise((resolve, reject) => { 
        let url = `/service_requests/`
        Axios(context).post(url,{service_request}).then(resp=>{ 
          resolve(resp)
        }, error => {
          reject(error)
        })
      })
    },
    
    postInvite(context, payload) {
      if (payload==='next') {
        return new Promise((resolve, reject) => { 
          let url = `/citizens/invite/`
          Axios(context).post(url).then(resp=>{ 
            resolve(resp)
          }, error => {
            reject(error)
          })
        })
      } else {
        return new Promise((resolve, reject) => { 
          let url = `/citizens/${payload}/invite/`
          Axios(context).post(url).then(resp=>{ 
            resolve(resp)
          }, error => {
            reject(error)
          })
        })
      }
    },
    
    postBeginService(context, citizen_id) {
      return new Promise((resolve, reject) => { 
        let url = `/citizens/${citizen_id}/begin_service/`
        Axios(context).post(url,{}).then(resp=>{ 
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
    
    editServiceButton(context) {
      let citizen = context.state.invitedCitizen
      let quick 
      citizen.qt_xn_citizen_indr===1 ? quick=true : quick=false
      
      let formData = {
        comments: citizen.citizen_comments,
        quick,
        citizen,
        channel: citizen.service_reqs[0].channel_id,
        service: citizen.service_reqs[0].service_id,
        category: '',
        search: ''
      }
  
      Axios(context).put(`/citizens/${citizen_id}/`, citizen)
        .then( resp => {
          context.commit('setInvitedCitizen',resp.data.citizen)
          let payload = resp.data.citizen.citizen_id
          context.dispatch('postBeginService',payload)
            .then( resp => {
              context.commit('setInvitedCitizen', resp.data.citizen)
            })
          })
        },
    
    closeAddCitizenModal(context) {
      context.commit('toggleAddCitizen', false)
      context.commit('resetAddCitizen')
    },
    
    closeServeCitizenModal(context) {
      context.commit('toggleServiceModal', false)
    },
    
    messageSlack(context, payload) {
      let slackObject = {
        slack_message: payload.slack_message
      }
      let url = "/slack/"
      Axios.post(url, slackObject)
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
    
    updateModalForm(state, payload) {
      Vue.set(
        state.addCitizenModal.formData, 
        payload.type,
        payload.value 
      )
    },
    
    toggleAddCitizen(state, payload) {
        Vue.set(
          state,
          'showAddModal',
          payload
        )
    },

    resetAddCitizen(state) {
      let { formData } = state.addCitizenModal
      
      let keys = Object.keys(formData)
      keys.forEach( key => {
        Vue.set(
          state.addCitizenModal.formData,
          key,
          ''
        )
      })
    }, 
    
    editInvitedCitizen(state,payload) {
      Vue.set(
        state.invitedCitizen,
        payload.type,
        payload.value
      )
    },
    
    setInvitedCitizen(state, payload) {
      Vue.set(
        state,
        'invitedCitizen',
        payload
      )
    },
    
    resetInvitedCitizen(state) {
      let { invitedCitizen } = state 
      Vue.set(
        state,
        'invitedCitizen',
        invitedCitizen
      )
    },
     
    toggleServiceModal: (state,payload)=>state.showServiceModal=payload,
    
    toggleServeNow: (state,payload) => state.serveNowDisabled = payload,
        
    editServicesFromServe(state) {
      let citizen = state.invitedCitizen
      let { citizen_id } = citizen
      let { formData } = state.addCitizenModal
      let srv = citizen.service_reqs[0]
      let quick
      citizen.qt_xn_csr_ind===1 ? quick = true : quick = false
      
      formData.comments = citizen.citizen_comments
      formData.service = srv.service.service_id
      formData.channel = srv.channel.channel_id
      
      formData.quick = quick
      formData.citizen = citizen
      state.addCitizenModal.visible = true
    },
    setAlert(state, payload) {
      state.alertMessage = payload
      state.dismissCountDown = 5
    },
    disableButtons(state) {
      state.inviteButtonDisabled = true
      state.serveButtonDisabled = false
      state.addCitizenDisabled = true
      state.backOfficeDisabled = true  
    },
    enableButtons(state) {
      state.inviteButtonDisabled = false
      state.serveButtonDisabled = true
      state.addCitizenDisabled = false
      state.backOfficeDisabled = false  
    },
    dismissCountDown(state,payload) {
      state.dismissCountDown = payload
    },
    setModalAlert(state, payload) {
      state.alertMessage = payload
    },
    disableServiceButtons(state) {
      state.serveBeginServiceDisabled = true
      state.serveCitizenLeftDisabled = true
      state.serveReturnQueueDisabled = true
    },
    enableServiceButtons(state) {
      state.serveBeginServiceDisabled = false
      state.serveCitizenLeftDisabled = false
      state.serveReturnQueueDisabled = false
    },
    disableFinish(state) {
      state.finishDisabled = true
    },
    enableFinish(state) {
      state.finishDisabled = false
    }
  }
})

