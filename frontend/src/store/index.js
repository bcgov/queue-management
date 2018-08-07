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


Vue.use(Vuex)

export const store = new Vuex.Store({

  state: {
    isLoggedIn: false,
    bearer: '',
    user: {
      username: null,
      office: {
        office_name: null
      },
      receptionist_ind: null
    },
    serviceModalForm: {
      citizen_id: null,
      service_citizen: null,
      citizen_comments: '',
      activeQuantity: 1
    },
    addModalSetup: 'reception',
    addModalForm: {
        citizen:'',
        comments: '',
        channel: '',
        search: '',
        category: '',
        service:'',
        quick: 0,
        setup: ''
    },
    showAddModal: false,
    showServiceModal: false,
    citizens: [],
    services: [],
    categories: [],
    channels: [],
    alertMessage: '',
    dismissCountDown: 0,
    citizenInvited: false,
    serviceBegun: false
  },

  getters: {
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

      return service_citizen.service_reqs.find(sr => sr.periods.some(p => p.time_end == null))
    },

    active_service_id: (state) => (citizen_id) => {
      let { citizens } = state
      let citizen = citizens.find(c => c.citizen_id === citizen_id)

      return citizen.service_reqs.find(sr=>sr.periods.some(p=>p.time_end === null))
    },

    invited_service_reqs: (state, getters) => {
      let { service_citizen } = state.serviceModalForm
      console.log(service_citizen)

      if (!service_citizen || !service_citizen.service_reqs || service_citizen.service_reqs.length === 0) {
        return []
      }

      return service_citizen.service_reqs.sort((a,b) => { return b.sr_id - a.sr_id })
    },

    invited_citizen: (state) => {
      let { service_citizen } = state.serviceModalForm
      console.log(service_citizen)
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
      let qry = getters.form_data.search.toUpperCase()
      let filteredOpts

      if (getters.form_data.search.length > 1) {
        filteredOpts = opts.filter(opt =>
          opt.service_name.toUpperCase().search(qry) != -1)
      } else {
        filteredOpts = opts
      }
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

    logIn(context, payload) {
      context.commit('setBearer', payload)
      context.commit('logIn')
      context.dispatch('getUser')
    },

    getAllCitizens(context) {
      console.log("getAllCitizens")
      let url = "/citizens/"
      Axios(context).get(url)
        .then( resp => {
          context.commit('updateQueue', resp.data.citizens)

          //Find the csr's active citizen
          let citizenFound = false;
          resp.data.citizens.forEach((citizen) => {
            if (citizen.service_reqs.length > 0) {
              if (citizen.service_reqs[0].periods.length > 0) {
                let activePeriod = citizen.service_reqs[0].periods[citizen.service_reqs[0].periods.length - 1]
                console.log(activePeriod.time_end)
                console.log(activePeriod.ps.ps_name)

                if (["Invited", "Being Served"].includes(activePeriod.ps.ps_name)
                  && activePeriod.csr.username === this.state.user.username) {
                  citizenFound = true
                  console.log("Found citizen")
                  console.log(this.state.serviceModalForm.service_citizen)

                  if (activePeriod.ps.ps_name === "Invited") {
                    context.commit('setServiceModalForm', citizen)
                    context.commit('toggleServiceModal', true)
                    context.commit('toggleBegunStatus', false)
                    context.commit('toggleInvitedStatus', true)
                    context.commit('resetAddModalForm')
                  } else if (activePeriod.ps.ps_name === "Being Served") {
                    context.commit('setServiceModalForm', citizen)
                    context.commit('toggleServiceModal', true)
                    context.commit('toggleBegunStatus', true)
                    context.commit('toggleInvitedStatus', false)
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

          if (!citizenFound) {
            console.log("No citizen found")
            context.commit('setServiceModalForm', {
              citizen_id: null,
              service_citizen: null,
              citizen_comments: '',
              activeQuantity: 1
            })
            context.commit('toggleServiceModal', false)
            context.commit('toggleBegunStatus', false)
            context.commit('toggleInvitedStatus', false)
          }
        })
        .catch(error => {
          console.log('error @ store.actions.getAllCitizens')
          console.log(error.response)
          console.log(error.message)
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
      Axios(context).get('/channels/')
        .then( resp => {
          context.commit('setChannels', resp.data.channels)
        })
        .catch(error => {
          console.log('error @ store.actions.getChannels')
          console.log(error.response)
          console.log(error.message)
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

    getUser(context) {
      Axios(context).get('/csrs/me/')
        .then( resp => {
          context.commit('setUser', resp.data.csr)
        })
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

    clickAddService(context) {
      if (context.state.channels.length === 0) {
        context.dispatch('getCategories')
        context.dispatch('getChannels')
        context.dispatch('getServices')
      }

        context.dispatch('putCitizen').then( () => {
          context.dispatch('putServiceRequest').then( () => {
            context.commit('updateAddModalForm',{
              type: 'citizen',
              value: context.getters.invited_citizen
            })
            context.commit('updateAddModalForm',{
              type: 'channel',
              value: context.getters.active_service.channel_id
            })
            context.commit('updateAddModalForm',{
              type: 'quick',
              value: context.getters.invited_citizen.qt_xn_citizen_ind
            })
            context.commit('switchAddModalMode', 'add_mode')
            context.commit('toggleAddModal', true)
            context.commit('toggleServiceModal', false)
          })
        })

    },

    clickAddServiceApply(context) {
      context.dispatch('putCitizen').then( () => {
        context.dispatch('postServiceReq').then( () => {
          context.commit('toggleAddModal', false)
          context.commit('toggleServiceModal', true)
          context.dispatch('toggleModalBack')
          context.commit('resetAddModalForm')
          context.commit('editServiceModalForm', {
            type: 'activeQuantity',
            value: 1
          })
        })
      })
    },

    clickBeginService(context) {
      let {citizen_id} = context.getters.form_data.citizen

      context.dispatch('putCitizen').then( () => {
        context.dispatch('postServiceReq').then( () => {
          context.dispatch('setServedCitizenId', citizen_id).then( () => {
            context.dispatch('postBeginService', citizen_id).then( () => {
              context.commit('toggleAddModal', false)
              context.commit('toggleServiceModal', true)
              context.commit('toggleBegunStatus', true)
              context.commit('toggleInvitedStatus', false)
              context.commit('resetAddModalForm')
            })
          })
        })
      })
    },

    clickBackOffce(context) {
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
      context.dispatch('postInvite', citizen_id).then( resp => {
        context.commit('setServiceModalForm', resp.data.citizen)
        context.commit('toggleServiceModal', true)
        context.commit('toggleBegunStatus', false)
        context.commit('toggleInvitedStatus', true)
        context.dispatch('resetQuantity')
      })
    },

    clickEdit(context) {
      if (context.state.channels.length === 0) {
        context.dispatch('getCategories')
        context.dispatch('getChannels')
        context.dispatch('getServices')
      }
      context.dispatch('putCitizen').then( () => {
        context.dispatch('putServiceRequest').then( () => {
          context.dispatch('setAddModalData')
          context.commit('switchAddModalMode', 'edit_mode')
          context.commit('toggleAddModal', true)
          context.commit('toggleServiceModal', false)
        })
      })
    },

    clickEditApply(context) {

      context.dispatch('putCitizen').then( () => {
        context.dispatch('putServiceRequest').then( () => {
          context.commit('toggleAddModal', false)
          context.dispatch('toggleModalBack')
          context.commit('resetAddModalForm')
          context.commit('toggleServiceModal', true)
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
      context.dispatch('putCitizen').then( () => {
        context.dispatch('putServiceRequest').then( () => {
          context.dispatch('postHold', citizen_id).then( resp=> {
            context.commit('toggleServiceModal', false)
            context.commit('toggleBegunStatus', false)
            context.commit('toggleInvitedStatus', false)
          })
        })
      })
    },

    clickInvite(context) {
      context.dispatch('postInvite', 'next').then( resp => {
        context.commit('setServiceModalForm', resp.data.citizen)
        context.commit('toggleServiceModal', true)
        context.commit('toggleInvitedStatus', true)
        context.dispatch('resetQuantity')
      })
      .catch(error=> {
        context.commit('setMainAlert', 'There are currently not citizens to invite.')
      })
    },

    clickMakeActive(context, sr_id) {
      let { citizen_id } = context.getters.invited_citizen
      context.dispatch('putCitizen').then( () => {
        context.dispatch('putServiceRequest').then( () => {
          context.dispatch('postActivateServiceReq', sr_id).then( () => {
            context.dispatch('resetQuantity')
          })
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
      context.dispatch('postBeginService', citizen_id).then( resp => {
        context.commit('setServiceModalForm', resp.data.citizen)
        context.commit('toggleServiceModal', true)
        context.commit('toggleBegunStatus', true)
        context.commit('toggleInvitedStatus', false)
        context.dispatch('resetQuantity')
      })
    },

    clickServeNow(context) {
      context.commit('toggleServiceModal', true)
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

      context.dispatch('putCitizen').then( () => {
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
        let compareCitizen = context.getters.invited_citizen

        if (context.state.showAddModal===true) {
          quick = context.getters.form_data.quick

          if (compareCitizen.qt_xn_citizen_ind != quick) {
            data.qt_xn_citizen_ind = quick
          }
        }
        if (compareCitizen.citizen_comments != citizen_comments) {
          data.citizen_comments = citizen_comments
        }
      } else {
        let { form_data } = context.getters
        citizen_id = form_data.citizen.citizen_id

        data.qt_xn_citizen_ind = form_data.quick
        data.citizen_comments = form_data.comments
      }
      if (Object.keys(data).length === 0) {
        return new Promise((resolve, reject) => { resolve(' ') })
      }

      return new Promise((resolve, reject) => {
        let url = `/citizens/${citizen_id}/`
        Axios(context).put(url,data).then(resp=>{
          resolve(resp)
        }, error => {
          reject(error)
        })
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

    messageSlack(context, payload) {
      let slackObject = {
        slack_message: payload.slack_message
      }
      let url = "/slack/"
      Axios.post(url, slackObject)
    },

    resetAddCitizenModal(context) {
      context.commit('toggleAddModal', false)
      context.dispatch('toggleModalBack')
      context.commit('resetAddModalForm')
    },

    resetQuantity(context) {
      let { quantity } = context.getters.active_service
      context.commit('editServiceModalForm', {
        type: 'activeQuantity',
        value: quantity
      })
    },

    setAddModalData(context) {
      let data = {
        citizen: context.getters.invited_citizen,
        active_service: context.getters.active_service
      }
      context.commit('setAddModalData', data)
    },

    setServedCitizenId(context, payload) {
      let data = {
        type: 'citizen_id',
        value: payload
      }
      context.commit('editServiceModalForm', data)
    },

    toggleModalBack(context) {
      if (context.state.user.receptionist_ind === 0) {
        context.commit('switchAddModalMode', 'non-reception')
      }
      if (context.state.user.receptionist_ind === 1) {
        context.commit('switchAddModalMode', 'reception')
      }
    },

    updateAddModalForm(context, payload) {
      context.commit('updateAddModalForm', payload)
    },
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

    resetAddModalForm(state) {
      let form_data = state.addModalForm

      let keys = Object.keys(form_data)
      keys.forEach( key => {
        Vue.set(
          state.addModalForm,
          key,
          ''
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
      keys.forEach(key=>{
        Vue.set(
          state.addModalForm,
          key,
          formData[key]
        )
      })
    },

    toggleServiceModal: (state,payload)=>state.showServiceModal=payload,

    setServiceModalForm(state, payload) {

      let current_comments = state.serviceModalForm.citizen_comments
      let current_citizen_comments = ''
      let citizen_comments = ''


      if (state.serviceModalForm.service_citizen) {
        current_citizen_comments = state.serviceModalForm.service_citizen.citizen_comments
      }

      //If we've updated the comments, keep our changes on refresh
      if (current_citizen_comments !== current_comments) {
        citizen_comments = current_comments
      } else {
        citizen_comments = payload.citizen_comments
      }

      let data = {
        citizen_comments: citizen_comments,
        citizen_id: payload.citizen_id,
        quick: payload.qt_xn_citizen_ind,
        service_citizen: payload
      }

      let keys = Object.keys(data)
      keys.forEach( key => {
        Vue.set(
          state.serviceModalForm,
          key,
          data[key]
        )
      })
    },

    resetServiceModal(state) {
      let { serviceModalForm } = state
      let keys = Object.keys(serviceModalForm)

      keys.forEach( key => {
        Vue.set(
          state.serviceModalForm,
          key,
          null
        )
      })
    },

    editServiceModalForm(state, payload) {
      Vue.set(
        state.serviceModalForm,
        payload.type,
        payload.value
      )
    },

    setMainAlert(state, payload) {
      state.alertMessage = payload
      state.dismissCountDown = 5
    },

    setModalAlert(state, payload) {
      state.alertMessage = payload
    },

    dismissCountDown(state,payload) {
      state.dismissCountDown = payload
    },

    toggleInvitedStatus: (state, payload) => state.citizenInvited = payload,

    toggleBegunStatus: (state, payload) => state.serviceBegun = payload
  }
})

