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
import { Axios } from './../helpers'

Vue.use(Vuex)

export const store = new Vuex.Store({

  state: {
    isLoggedIn: false,
    dash: {
      sortby:'',
      page:'',
      descending:false,
      perpage:''
    },
    citizens: [],
    user: null,
    addCitizenModal: {
      visible: false,
      showAlert: true,
      formData: {
        allowClose: false,
        citizen:'',
        comments: '',
        channel: '',
        search: '',
        category: '',
        service:'',
        quick: false
      },
    },
    userOfficeType:1,
    newCitizen: null,
    services: null,
    categories: [],
    channels: [],
    bearer: ''
  },
/////////////////////////////////////////////////
/////////////////////////////////////////////////
  getters: {
    add_citizen_form_ready: state => {
      let { formData } = state.addCitizenModal
      let reqs = ['service', 'channel', 'citizen']
      
      if (reqs.every(req=>formData[req]!=='')) {
        return true
      } else {
        return false 
      }
    },
    missing_items: (state, getters) => {
      if (getters.add_citizen_form_ready) {
        return null
      }
      let { formData } = state.addCitizenModal
      let reqs = ['service', 'channel', 'citizen']
      let missing = []
    
      reqs.forEach(req=>{
        if (!state.addCitizenModal.formData[req]) {
          missing.push(req)
        }
      })
        return missing
      },
    dash_status: state => {
      return state.dash
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
    categories_options: state => {
      let blankOpt = [{value:'', text:''}]
      let mappedOpts = state.categories.map(ctg=>
          ({value: ctg.service_id, text: ctg.service_name})
        )
      let finalOpts = blankOpt.concat(mappedOpts)
      return finalOpts
    },
    index: state => {
      return state.addCitizenModal.formData.index
    }
  },
/////////////////////////////////////////////////
/////////////////////////////////////////////////
  actions: {
    putCitizenInQueue(context, payload=1) {
      let { formData } = context.state.addCitizenModal
      let { citizen_id } = formData.citizen
      
      let qt_xn_citizen_ind
      if (formData.quick) {
        qt_xn_citizen_ind = 1
      } else {
        qt_xn_citizen_ind = 0
      }
      
      let citizen = {
        citizen_comments: formData.comments
      }
      let service_request = {
        service_id: formData.service,
        citizen_id,
        quantity: payload,
        channel_id: formData.channel,
        qt_xn_citizen_ind
      }
    
      Axios(context).put(`/citizens/${citizen_id}/`,citizen)
      Axios(context).post(`/service_requests/`,{service_request})
        .then( () => {
          Axios(context).post(`/citizens/${citizen_id}/add_to_queue/`)  
            .then( () => {
              context.commit('resetFormData')
          })
      })
    },
    putCitizenInService(context, payload=1) {
      let { formData } = context.state.addCitizenModal
      let { citizen_id } = formData.citizen
      
      let citizen = {
        citizen_comments: formData.comments
      }
      let service_request = {
        service_id: formData.service,
        citizen_id,
        quantity: payload,
        channel_id: formData.channel
      }
    
      Axios(context).put(`/citizens/${citizen_id}/`,citizen)
      Axios(context).post(`/service_requests/`,{service_request})
        .then( () => {
          Axios(context).post(`/citizens/${citizen_id}/invite/`)  
            .then( () => {
              context.commit('resetFormData')
            })
        })
    },
    addCitizen(context) {
      let emptyObj = {}
      Axios(context).post('/citizens/', emptyObj)
        .then(resp => {
          let value = resp.data.citizen
          context.commit('updateModalForm', {type:'citizen',value})
        })
        .catch(error => {
          console.log('error @ store.actions.addCitizen')
          console.log(error.response)
          console.log(error.message)
        })
      context.commit('toggleAddCitizen', true)
      context.dispatch('getCategories')
      context.dispatch('getChannels')
      context.dispatch('getServices')
    },
    getServices(context) {
      Axios(context).get('/services/')
        .then( resp => {
          context.commit('setServices', resp.data.services)
          console.log('services set')          
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
    getAllClients(context) {
      let url = "/citizens/"
      Axios(context).get(url)
        .then( response => {
          console.log(response.data.citizens)
        context.commit('updateList', response.data.citizens)
        })
        .catch(error => {
          console.log('error @ store.actions.getAllClients')
          console.log(error.response)
          console.log(error.message)
        })
    },
    postClient(context, payload) {
      let clientObject = {
        name: payload.name
      }
      let url = "/citizens/"
      Axios(context).post(url, clientObject)
    },
    deleteClient(context, payload) {
      let url = `/citizens/${payload}/`
      Axios(context).delete(url)
        .then( resp => {
          console.log(resp)
          context.commit('getAllClients')
        })
        .catch( error => {
          console.log(error.status)
          context.commit('getAllClients')
        })
    },
    getUser(context) {
      Axios(context).get('/services/')
        .then( resp => {
          console.log('getUser .thens!')
          console.log(resp.data)
        })
        .catch( () => {
          console.log('it got caught')
        })
    },
    messageSlack(context, payload) {
      let slackObject = {
        slack_message: payload.slack_message
      }
      let url = "/slack/"
      Axios.post(url, slackObject)
    },
    handleServiceClick(context, payload) {
      console.log(context)
    }
  },
/////////////////////////////////////////////////
/////////////////////////////////////////////////  
  mutations: {
    updateModalForm(state, payload) {
      Vue.set(
        state.addCitizenModal.formData, 
        payload.type,
        payload.value 
      )
    },
    resetFormData(state) {
      let addCitizenModal = {
        visible: false,
        formData: {
          allowClose: false,
          citizen:'',
          comments: '',
          channel: '',
          search: '',
          category: '',
          service:'',
          quick: false
        }
      }
      state.addCitizenModal = addCitizenModal
    },
    toggleAlert(state, payload) {
      state.addCitizenModal.showAlert = payload
    },
    reconForm(state, payload) {
      state.userOfficeType = payload
    },
    setNewCitizen(state, newCitizen) {
      state.newCitizen = payload
    },
    setServices(state, payload) {
      state.services = {}
      state.services = payload
    },
    setCategories(state, payload) {
      state.categories = []
      state.categories = payload
    },
    setChannels(state, payload) {
      state.channels = []
      state.channels = payload
    },
    logIn: state => state.isLoggedIn = true,
    logOut: state => state.isLoggedIn = false,
    toggleAddCitizen(state, payload) {
      state.addCitizenModal.visible = payload
    },
    updateList(state, payload) {
      state.citizens = []
      state.citizens = payload
    },
    updateDash(state, payload) {
      Vue.set(
        state.dash,
        payload.type,
        payload.value
      )
    },
    setUser(state, payload) {
      state.user = payload
    },
    setBearer: (state, payload) => state.bearer = payload
  }

  })
