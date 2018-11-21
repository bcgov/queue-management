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
      selectedItem: '',
      priority: 2
    },
    addModalSetup: null,
    alertMessage: '',
    allCitizens: [],
    bearer: '',
    categories: [],
    channels: [],
    citizens: [],
    citizenInvited: false,
    csrs: [],
    dismissCount: 0,
    feedbackMessage: '',
    isLoggedIn: false,
    nowServing: false,
    officeType: null,
    performingAction: false,
    serveNowAltAction: false,
    serveNowStyle: 'btn-primary',
    serviceBegun: false,
    serveModalAlert: '',
    serviceModalForm: {
      citizen_id: null,
      service_citizen: null,
      citizen_comments: '',
      activeQuantity: 1,
      accurate_time_ind: 1,
      quick: 0,
      priority: 2
    },
    services: [],
    showAddModal: false,
    showAdmin: false,
    showFeedbackModal: false,
    showGAScreenModal: false,
    showResponseModal: false,
    showServiceModal: false,
    addNextService: false,
    user: {
      csr_id: null,
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
      receptionist_ind: null
    },
    userLoadingFail: false
  },

  getters: {
    reception(state) {
      if (state.user.office && state.user.office.sb) {
        if (state.user.office.sb.sb_type === "callbyname" || state.user.office.sb.sb_type === "callbyticket") {
          return true
        }
        return false
      }
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
      let opts = state.categories.filter(o => state.services.some(s => s.parent_id === o.service_id))

      let mappedOpts = opts.map(opt =>
          ({value: opt.service_id, text: opt.service_name})
        )
      let blankOpt = [{value:'', text:'Categories'}]
      return blankOpt.concat(mappedOpts)
    },

    filtered_services: (state, getters) => {
      let services = state.services

      if (getters.form_data.category) {
        return services.filter(service=>service.parent_id === getters.form_data.category)
      } else {
        return services
      }
    },

    quick_trans_status(state) {
      if (state.user.qt_xn_csr_ind == 1) {
        return true
      } else if (state.user.qt_xn_csr_ind == 0) {
        return false
      } else {
        console.error('quick trans status: ', state.user.qt_xn_csr_ind)
      }
    },

    receptionist_status(state) {
      if (state.user.receptionist_ind == 1) {
        return true
      } else if (state.user.receptionist_ind == 0) {
        return false
      } else {
        console.error('receptionist status: ', state.user.qt_xn_csr_ind)
      }
    }
  },

  actions: {
    flashServeNow(context, payload) {
      let flash = () => {
        if (!context.state.showServiceModal) {
          if ( context.state.serveNowStyle === 'btn-primary' ) {
            context.commit('flashServeNow', 'btn-highlighted')
          } else if ( context.state.serveNowStyle === 'btn-highlighted' ) {
            context.commit('flashServeNow', 'btn-primary')
          }
        }
      }
      if (payload === 'start') {
        clearInterval(flashInt)
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
      context.dispatch('getUser').catch(() => {
        context.commit('setUserLoadingFail', true)
      })
    },

    getAllCitizens(context) {
      let url = '/citizens/'
      Axios(context).get(url).then( resp => {
        if (!resp.data.citizens) {
          context.commit('updateQueue', [])
          return
        }
        context.commit('updateQueue', resp.data.citizens)
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

    getCsrs(context) {
      //We only need to get the CSRs once
      if (context.state.csrs === null || context.state.csrs.length === 0) {
        Axios(context).get('/csrs/')
        .then( resp => {
          context.commit('setCsrs', resp.data.csrs)
        })
        .catch(error => {
          console.log('error @ store.actions.getCsrs')
          console.log(error.response)
          console.log(error.message)
        })
      }
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

          if (resp.data.active_citizens && resp.data.active_citizens.length > 0) {
            context.dispatch('checkForUnfinishedService', resp.data.active_citizens)
          }
          resolve(resp)
        }, error => {
          reject(error)
        })
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
      context.commit('setPerformingAction', true)
      context.dispatch('toggleModalBack')
      context.commit('toggleAddModal', true)

      Axios(context).post('/citizens/', {})
      .then(resp => {
        let value = resp.data.citizen
        context.commit('updateAddModalForm', {type:'citizen',value})
        context.commit('resetServiceModal')
      },
      error => {
        context.commit('toggleAddModal', false)
        context.commit('setMainAlert', 'An error occurred adding a citizen.')
      }).finally(() => {
        context.commit('setPerformingAction', false)
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
      context.commit('setPerformingAction', true)

      if (context.state.channels.length === 0) {
        context.dispatch('getCategories')
        context.dispatch('getChannels')
        context.dispatch('getServices')
      }

      context.commit('toggleAddNextService', true)

      context.dispatch('putServiceRequest').then(response => {
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
          context.commit('updateAddModalForm', {
            type: 'priority',
            value: context.getters.invited_citizen.priority
          })
          context.commit('toggleAddModal', true)
          context.commit('toggleServiceModal', false)
        }).finally(() => {
          context.commit('setPerformingAction', false)
        })
      }, error => {
        console.log(error)
        context.commit('setPerformingAction', false)
      })
    },

    clickAddServiceApply(context) {
      context.commit('setPerformingAction', true)

      context.dispatch('postServiceReq').then(() => {
        context.dispatch('putCitizen').then((resp) => {
          context.commit('toggleAddModal', false)
          context.commit('toggleAddNextService', false)
          context.commit('toggleServiceModal', true)
          context.dispatch('toggleModalBack')
          context.commit('resetAddModalForm')
        }).finally(() => {
          context.commit('setPerformingAction', false)
        })
      }).catch(() => {
        context.commit('setPerformingAction', false)
      })
  },

    clickAddToQueue(context) {
      let { citizen_id } = context.getters.form_data.citizen
      context.commit('setPerformingAction', true)

      context.dispatch('putCitizen').then( () => {
        context.dispatch('postServiceReq').then( () => {
          context.dispatch('postAddToQueue', citizen_id).then( resp => {
            context.dispatch('resetAddCitizenModal')
            context.commit('toggleBegunStatus', false)
            context.commit('toggleInvitedStatus', false)
          }).finally(() => {
            context.commit('setPerformingAction', false)
          })
        }).catch(() => {
          context.commit('setPerformingAction', false)
        })
      }).catch(() => {
        context.commit('setPerformingAction', false)
      })
    },

    clickAdmin(context) {
      context.commit('toggleShowAdmin')
    },

    clickBeginService(context) {
      let {citizen_id} = context.getters.form_data.citizen
      context.commit('setPerformingAction', true)

      context.dispatch('putCitizen').then( () => {
        context.dispatch('postServiceReq').then( () => {
          context.dispatch('postBeginService', citizen_id).then( () => {
            context.commit('toggleAddModal', false)
            context.commit('toggleBegunStatus', true)
            context.commit('toggleInvitedStatus', false)
            context.commit('toggleServiceModal', true)
            context.commit('resetAddModalForm')
          }).finally(() => {
            context.commit('setPerformingAction', false)
          })
        }).catch(() => {
          context.commit('setPerformingAction', false)
        })
      }).catch(() => {
        context.commit('setPerformingAction', false)
      })
    },

    clickBackOffice(context) {
      context.commit('setPerformingAction', true)
      context.dispatch('toggleModalBack')

      Axios(context).post('/citizens/', {})
      .then(resp => {
        let value = resp.data.citizen
        context.commit('updateAddModalForm', {type:'citizen',value})
        context.commit('toggleAddModal', true)
        context.commit('resetServiceModal')
      }).finally(() => {
        context.commit('setPerformingAction', false)
      })

      let setupChannels = () => {
        let index = -1
        let { channel_options } = context.getters
        channel_options.forEach((opt,i) => {
          if (opt.text.toLowerCase() === 'back office') {
            index = i
          }
        })
        if (index >= 0) {
          context.commit('updateAddModalForm', {type:'channel', value:channel_options[index].value})
        } else {
          context.commit('setDefaultChannel')
        }
      }

      if (context.state.channels.length === 0) {
        context.dispatch('getChannels').then( () => { setupChannels() })
      } else {
        setupChannels()
      }
      if (context.state.categories.length === 0) {
        context.dispatch('getCategories')
      }
      if (context.state.services.length === 0) {
        context.dispatch('getServices')
      }
    },

    clickCitizenLeft(context) {
      let {citizen_id} = context.getters.invited_citizen
      context.commit('setPerformingAction', true)

      context.dispatch('postCitizenLeft', citizen_id).finally(() => {
        context.commit('setPerformingAction', false)
      })
      context.commit('toggleServiceModal', false)
      context.commit('toggleBegunStatus', false)
      context.commit('toggleInvitedStatus', false)
      context.commit('resetServiceModal')
    },

    clickDashTableRow(context, citizen_id) {
      context.commit('setPerformingAction', true)

      context.dispatch('postInvite', citizen_id).then( () => {
        context.commit('toggleBegunStatus', false)
        context.commit('toggleInvitedStatus', true)
        context.commit('toggleServiceModal', true)
      }).finally(() => {
        context.commit('setPerformingAction', false)
      })
    },

    clickEdit(context) {
      context.commit('setPerformingAction', true)

      if (context.state.channels.length === 0) {
        context.dispatch('getCategories')
        context.dispatch('getChannels')
        context.dispatch('getServices')
      }
      context.dispatch('putServiceRequest').then(() => {
        context.commit('switchAddModalMode', 'edit_mode')
        context.dispatch('setAddModalData')
        context.commit('toggleAddModal', true)
        context.commit('toggleServiceModal', false)
        context.commit('setPerformingAction', false)
      }).catch(() => {
        context.commit('setPerformingAction', false)
      })
    },

    clickEditApply(context) {
      context.commit('setPerformingAction', true)

      context.dispatch('putServiceRequest').then( () => {
        context.dispatch('putCitizen').then(() => {
          context.commit('toggleAddModal', false )
          context.dispatch('toggleModalBack' )
          context.commit('resetAddModalForm' )
          context.commit('toggleServiceModal', true )
        }).finally(() => {
          context.commit('setPerformingAction', false)
        })
      }).catch(() => {
        context.commit('setPerformingAction', false)
      })
    },

    clickEditCancel(context) {
      context.commit('toggleAddModal', false)
      context.dispatch('toggleModalBack')
      context.commit('resetAddModalForm')
      context.commit('toggleServiceModal', true)
    },

    clickGAScreen(context) {
      context.dispatch('getCsrs').then( () => {
        context.commit('toggleGAScreenModal', !context.state.showGAScreenModal)
      })
    },

    clickHold(context) {
      let { citizen_id } = context.state.serviceModalForm
      context.commit('setPerformingAction', true)

      context.dispatch('putCitizen').then(() => {
        context.dispatch('putServiceRequest').then(() => {
          context.dispatch('postHold', citizen_id).then(() => {
            context.commit('toggleBegunStatus', false)
            context.commit('toggleInvitedStatus', false)
            context.commit('toggleServiceModal', false)
            context.commit('resetServiceModal')
          }).finally(() => {
            context.commit('setPerformingAction', false)
          })
        }).catch(() => {
          context.commit('setPerformingAction', false)
        })
      }).catch(() => {
        context.commit('setPerformingAction', false)
      })
    },

    clickInvite(context) {
      context.commit('setPerformingAction', true)

      context.dispatch('postInvite', 'next').then(() => {
        context.commit('toggleInvitedStatus', true)
        context.commit('toggleServiceModal', true)
      }).catch(() => {
        context.commit('setMainAlert', 'There are no citizens waiting.')
      }).finally(() => {
        context.commit('setPerformingAction', false)
      })
      context.dispatch('flashServeNow', 'stop')
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
      context.commit('setPerformingAction', true)

      context.dispatch('putServiceRequest').then(() => {
        context.dispatch('putCitizen').then(() => {
          context.dispatch('postActivateServiceReq', sr_id).finally(() => {
            context.commit('setPerformingAction', false)
          }).finally(() => {
            context.commit('setPerformingAction', false)
          })
        }).catch(() => {
          context.commit('setPerformingAction', false)
        })
      }).catch(() => {
        context.commit('setPerformingAction', false)
      })
    },

    clickReturnToQueue(context) {
      let {citizen_id} = context.getters.invited_citizen
      context.commit('setPerformingAction', true)

      context.dispatch('putCitizen').then( () => {
        context.dispatch('putServiceRequest').then( () => {
          context.dispatch('postAddToQueue', citizen_id).then( () => {
            context.commit('toggleInvitedStatus', false)
            context.commit('toggleServiceModal', false)
            context.commit('resetServiceModal')
          }).finally(() => {
            context.commit('setPerformingAction', false)
          })
        }).catch(() => {
          context.commit('setPerformingAction', false)
        })
      }).catch(() => {
        context.commit('setPerformingAction', false)
      })
    },

    clickRowHoldQueue(context, citizen_id) {
      context.commit('setPerformingAction', true)

      context.dispatch('postBeginService', citizen_id).then( () => {
        context.commit('toggleBegunStatus', true)
        context.commit('toggleInvitedStatus', false)
        context.commit('toggleServiceModal', true)
      }).finally(() => {
        context.commit('setPerformingAction', false)
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
      context.commit('setPerformingAction', true)

      context.dispatch('putCitizen').then( () => {
        context.dispatch('putServiceRequest').then( () => {
          context.dispatch('postBeginService', citizen_id).then(() => {
            context.commit('toggleBegunStatus', true)
          }).finally(() => {
            context.commit('setPerformingAction', false)
          })
        }).catch(() => {
          context.commit('setPerformingAction', false)
        })
      }).catch(() => {
        context.commit('setPerformingAction', false)
      })
    },

    clickServiceFinish(context) {
      let { citizen_id } = context.state.serviceModalForm
      context.commit('setPerformingAction', true)

      context.dispatch('putCitizen').then( (resp) => {
        context.dispatch('putServiceRequest').then( () => {
          context.dispatch('postFinishService', citizen_id).then( () => {
            context.commit('toggleServiceModal', false)
            context.commit('toggleBegunStatus', false)
            context.commit('toggleInvitedStatus', false)
            context.commit('resetServiceModal')
          }).finally(() => {
            context.commit('setPerformingAction', false)
          })
        }).catch(() => {
          context.commit('setPerformingAction', false)
        })
      }).catch(() => {
        context.commit('setPerformingAction', false)
      })
    },

    clickServiceModalClose(context) {
      context.commit('toggleServiceModal', false)
      context.commit('toggleInvitedStatus', true)
    },

    closeGAScreenModal(context) {
      context.commit('toggleGAScreenModal', false)
    },

      messageFeedback(context) {
      let messageParts = []
      messageParts.push(`Username: ${context.state.user.username}`)
      messageParts.push(`Office: ${context.state.user.office.office_name}`)

      let activeCitizen = context.state.serviceModalForm.service_citizen

      if (activeCitizen) {
        let activeService = activeCitizen.service_reqs.filter(sr => sr.periods.some(p => p.time_end === null))[0]
        let activePeriod = activeService.periods.filter(p => p.time_end === null)[0]

        messageParts.push(`Ticket Number: ${activeCitizen.ticket_number}`)
        messageParts.push(`Citizen ID: ${activeCitizen.citizen_id}`)
        messageParts.push(`Active SR ID: ${activeService.sr_id}`)
        messageParts.push(`Active Period ID: ${activePeriod.period_id}`)
      } else {
        messageParts.push(`Ticket Number: not available`)
      }
      messageParts.push("")
      messageParts.push(`Message: ${context.state.feedbackMessage}`)

      let feedbackObject = {
        feedback_message: messageParts.join("\n")
      }

      let url = "/feedback/"
      Axios(context).post(url, feedbackObject).then(()=> {
        context.commit('setFeedbackMessage', '')
      })
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
        Axios(context).post(url,{})
        .then(resp => {
          resolve(resp)
        },
        error => {
          if (error.response.status === 400) {
            context.commit('setMainAlert', error.response.data.message)
          }

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
            }

            reject(error)
          })
        })
      }
    },

    postServiceReq(context) {
      let { form_data } = context.getters
      let { citizen_id } = form_data.citizen
      let { priority } = form_data.priority
      let service_request = {
        service_id: form_data.service,
        citizen_id: citizen_id,
        quantity: 1,
        channel_id: form_data.channel,
        priority: priority
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
      let priority

      if (context.state.serviceModalForm.citizen_id) {
        let { accurate_time_ind, citizen_comments } = context.state.serviceModalForm
        quick = context.state.serviceModalForm.quick
        priority = context.state.serviceModalForm.priority
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
          if ( quick !== prevCitizen.qt_xn_citizen_ind ) {
            data.qt_xn_citizen_ind = quick
          }
          if ( priority !== prevCitizen.priority ) {
            data.priority = priority
          }
          if ( accurate_time_ind != null && accurate_time_ind !== prevCitizen.accurate_time_ind ) {
            data.accurate_time_ind = accurate_time_ind
          }
        }
      } else {
        let { form_data } = context.getters
        citizen_id = form_data.citizen.citizen_id
        data.qt_xn_citizen_ind = form_data.quick
        if (!form_data.quick) {
          data.qt_xn_citizen_ind = 0
        }
        data.priority = form_data.priority
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

    putServiceRequest(context) {
      let { activeQuantity } = context.state.serviceModalForm
      let compareService = context.getters.active_service
      let { sr_id } = compareService

      let data = {}
      if (activeQuantity != compareService.quantity) {
        data.quantity = activeQuantity
      }

      // Make sure quantity is position
      if (!/^\+?\d+$/.test(activeQuantity)) {
        context.commit("setServeModalAlert", "Quantity must be a number and greater than 0")
        return Promise.reject('Quantity must be a number and greater than 0')
      } else {
        context.commit("setServeModalAlert", "")
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

    screenAllCitizens(context) {
      context.state.citizens.forEach(citizen => {
        context.dispatch('screenIncomingCitizen', citizen)
      })
    },

    screenIncomingCitizen(context, citizen) {
      let { addNextService } = context.state

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
                  context.commit('toggleBegunStatus', false)
                  context.commit('toggleInvitedStatus', true)
                  context.commit('setServeNowAction', true)
                  context.dispatch('flashServeNow', 'start')

                  if (!addNextService) {
                    context.commit('toggleServiceModal', true)
                    context.commit('resetAddModalForm')
                  }

                } else if (activePeriod.ps.ps_name === 'Being Served') {
                  context.commit('setServiceModalForm', citizen)
                  context.commit('toggleBegunStatus', true)
                  context.commit('toggleInvitedStatus', false)
                  context.commit('setServeNowAction', false)
                  context.dispatch('flashServeNow', 'stop')

                  if (!addNextService) {
                    context.commit('toggleServiceModal', true)
                    context.commit('resetAddModalForm')
                  }
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

      const index = context.state.citizens.map(c => c.citizen_id).indexOf(citizen.citizen_id);

      if (index >= 0) {
        context.commit('updateCitizen', {citizen, index})
      } else {
        if (citizen.service_reqs && citizen.service_reqs.length > 0) {
          if (citizen.service_reqs[0].periods && citizen.service_reqs[0].periods.length > 0) {
            console.log("Adding citizen")
            context.commit('addCitizen', citizen)
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
    },

    //Updates the counter's type from the state after selecting from the dropdown (regular counter, quick transaction, or receptionist)
      updateCSRState(context) {
      let csr_id = context.state.user.csr_id
      Axios(context).put(`/csrs/${csr_id}/`, {
        qt_xn_csr_ind: context.state.user.qt_xn_csr_ind,
        receptionist_ind: context.state.user.receptionist_ind
      })
      .then( resp => {
      })
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
        if ( key === 'priority' ) Vue.set(
          state.addModalForm,
          key,
          2
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
        priority: citizen.priority,
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
      let quick = citizen.qt_xn_citizen_ind
      let priority = citizen.priority

      let obj = { citizen_comments, activeQuantity, citizen_id, service_citizen, quick, priority }
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
      Vue.set(
        state,
        "serveModalAlert",
        ""
      )

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
      state.dismissCount = 5
    },

    setModalAlert(state, payload) {
      state.alertMessage = payload
    },

    setServeModalAlert(state, payload) {
      state.serveModalAlert = payload
    },

    setCsrs(state, payload) {
      state.csrs = []
      state.csrs = payload
    },

    updateCitizen(state, payload) {
      Vue.set(state.citizens, payload.index, payload.citizen)
    },

    addCitizen(state, citizen) {
      state.citizens.push(citizen)
    },

    dismissCountDown(state, payload) {
      state.dismissCount = payload
    },

    toggleInvitedStatus: (state, payload) => state.citizenInvited = payload,

    toggleBegunStatus: (state, payload) => state.serviceBegun = payload,

    toggleGAScreenModal: (state,payload) => state.showGAScreenModal = payload,

    setQuickTransactionState: (state, payload) => state.user.qt_xn_csr_ind = payload,

    setReceptionistState: (state, payload) => state.user.receptionist_ind = payload,

    setOffice: (state, officeType) => state.officeType = officeType,

    flashServeNow: (state, payload) => state.serveNowStyle = payload,

    setServeNowAction: (state, payload) => state.serveNowAltAction = payload,

    toggleFeedbackModal: (state, payload) => state.showFeedbackModal = payload,

    toggleAddNextService: (state, payload) => state.addNextService = payload,

    toggleShowAdmin: (state) => state.showAdmin = !state.showAdmin,

    setFeedbackMessage: (state, payload) => state.feedbackMessage = payload,

    setPerformingAction: (state, payload) => state.performingAction = payload,

    setUserLoadingFail: (state, payload) => state.userLoadingFail = payload,

    showHideResponseModal(state) {
      state.showResponseModal = true
      setTimeout( ()=> {state.showResponseModal = false}, 3000)
    },

    hideResponseModal(state) {
      state.showResponseModal = false
    }
  }
})
