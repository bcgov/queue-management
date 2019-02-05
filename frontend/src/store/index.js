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
import { Axios, searchNestedObject } from './helpers'
import moment from 'moment'

var flashInt

Vue.use(Vuex)

export const store = new Vuex.Store({
  
  state: {
    addIndITASteps: [
      {
        step: 1,
        title:'Exam Type',
        questions: [
          {
            key: 'exam_type_id',
            text: 'Exam Type ID / Colour',
            kind:'dropdown',
            minLength: 0,
            digit: false,
          }
        ]
      },
      {
        step: 2,
        title:'Exam Info',
        questions: [
          {
            key: 'event_id',
            text:'Event ID' ,
            kind: 'input',
            minLength: 6,
            digit: true,
          },
          {
            key: 'exam_name',
            text: 'Exam Name',
            kind: 'input',
            minLength: 6,
            digit: false
          },
          {
            key: 'examinee_name',
            text: `Exam Writer's Name`,
            minLength: 6,
            kind:'input',
            digit: false
          },
          {
            key: 'exam_method',
            text: 'Exam Method',
            minLength: 0,
            digit: false,
            kind:'select',
            options: [
              {text: 'paper', value: 'paper', id: 'exam_method'},
              {text: 'online', value: 'online', id: 'exam_method'}
            ]
          },
        ]
      },
      {
        step: 3,
        title: 'Exam Dates',
        questions: [
          {
            kind: 'exam_received',
            key: 'exam_received_date',
            text1:'Was the Exam Package Receieved Today?',
            text2: 'Date of Receipt of Exam Package',
            minLength: 0,
            digit: false,
          },
          {
            kind: 'date',
            key: 'expiry_date',
            text: 'Exam Expiry Date',
            minLength: 0,
            digit: false,
          },
          {
            kind: 'notes',
            key: 'notes',
            text: 'Additional Notes (optional)',
            minLength: 0,
            digit: false,
          },
        ]
      },
      {
        step: 4,
        title:'Summary',
        questions:
          [
            {
              kind: null,
              key: null,
              text1:null,
              text2: null,
              minLength: 0,
              digit: false,
            },
          ]
      },
    ],
    addGroupITASteps: [
      {
        step: 1,
        title:'Exam Type',
        questions:
        [
          {
            key: 'exam_type_id',
            text: 'Exam Type ID / Colour',
            kind:'dropdown',
            minLength: 0,
            digit: false,
          }
        ]
      },
      {
        step: 2,
        title: 'Basic Info',
        questions: [
          {
            key: 'office_id',
            text: 'Office',
            kind: 'office',
            minLength: 0,
            digit: false,
          },
          {
            key: 'event_id',
            text: 'Event ID',
            kind: 'input',
            minLength: 0,
            digit: false
          },
          {
            key: 'exam_name',
            text: 'Exam Name',
            kind: 'input',
            minLength: 0,
            digit: false,
          },
          {
            key: 'number_of_students',
            text: 'Number of Students',
            minLength: 0,
            kind: 'input',
            digit: false
          },
        ]
      },
      {
        step: 3,
        title: 'Date, Time & Format',
        questions: [
          {
            kind: 'date',
            key: 'expiry_date',
            text: 'Date and Time',
            minLength: 0,
            digit: false,
          },
          {
            kind: 'time',
            key: 'exam_time',
            text: 'Exam Time',
            minLength: 0,
            digit: false,
          },
          {
            kind: 'input',
            key: 'offsite_location',
            text: 'Location',
            type: 'input',
            minLength: 0,
            digit: false,
          },
          {
            key: 'exam_method',
            text: 'Exam Method',
            minLength: 0,
            digit: false,
            kind: 'select',
            options: [
              { text: 'paper', value: 'paper', id: 'exam_method' },
              { text: 'online', value: 'online', id: 'exam_method' }
            ]
          },
          {
            kind: 'notes',
            key: 'notes',
            text: 'Additional Notes (optional)',
            minLength: 0,
            digit: false,
          },
        ]
      },
      {
        step: 4,
        title:'Summary',
        questions:
        [
          {
            kind: null,
            key: null,
            text1:null,
            text2: null,
            minLength: 0,
            digit: false,
          },
        ]
      },
    ],
    addITAExamModal: {
      visible: false,
      setup: 'individual',
      step1MenuOpen: false,
    },
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
    nonITAExam: false,
    addNextService: false,
    adminNavigation: 'csr',
    alertMessage: '',
    allCitizens: [],
    bearer: '',
    bookings: [],
    calendarEvents: [],
    calendarSetup: null,
    capturedExam: {},
    captureITAExamTabSetup: {
      step: 1,
      highestStep: 1,
      stepsValidated: [],
      errors: [],
      showRadio: true,
      status: 'unknown',
      notes: false,
    },
    categories: [],
    channels: [],
    citizenInvited: false,
    citizens: [],
    clickedDate: '',
    csr_states: [],
    csrs: [],
    dismissCount: 0,
    editedBooking: null,
    editedBookingOriginal: null,
    editExamFailure: false,
    editExams: [],
    editExamSuccess: false,
    examAlertMessage: '',
    examEditSuccessMessage: '',
    examEditFailureMessage: '',
    examDismissCount: 0,
    examSuccessDismiss : 0,
    examMethods: [
      {text: 'paper', value: 'paper', id: 'exam_method'},
      {text: 'online', value: 'online', id: 'exam_method'}
    ],
    exams: [],
    examTypes: [],
    feedbackMessage: '',
    groupBookings: [],
    showGenFinReportModal: false,
    iframeLogedIn: false,
    invigilators: [],
    isLoggedIn: false,
    navigationVisible: true,
    nowServing: false,
    offices: [],
    officeFilter: null,
    officeType: null,
    performingAction: false,
    rescheduling: false,
    returnExams: [],
    rooms: [],
    roomResources: [],
    scheduling: false,
    schedulingOther: false,
    selectedBooking: {},
    selectedExam: {},
    selectedOffice: {},
    selectionIndicator: false,
    serveModalAlert: '',
    serveNowAltAction: false,
    serveNowStyle: 'btn-primary',
    serviceBegun: false,
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
    showBookingModal: false,
    showCalendarControls: true,
    showEditBookingModal: false,
    showEditExamModal: false,
    showExamInventoryModal: false,
    showFeedbackModal: false,
    showGAScreenModal: false,
    showSelectInvigilatorModal: false,
    showOtherBookingModal: false,
    showResponseModal: false,
    showReturnExamModalVisible: false,
    showSchedulingIndicator: false,
    showServiceModal: false,
    user: {
      csr_id: null,
      csr_state_id: null,
      csr_state: {
        csr_state_desc: null,
        csr_state_id: null,
        csr_state_name: null
      },
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
    userLoadingFail: false,
  },

  getters: {
    
    get_room_by_id: (state) => (id) => {
      return state.rooms.find(room => room.id == id)
    },
    
    get_exam_by_id: (state) => (id) => {
      return state.exams.find(exam => exam.id == id)
    },
    
    get_booking_by_id: (state) => (id) => {
      return state.bookings.find(booking => booking.id = id)
    },
  
    filtered_calendar_events: (state, getters) => (search) => {
      return state.calendarEvents.filter(event => searchNestedObject(event, search))
    },
    
    calendar_events(state) {
      if (state.bookings.length > 0) {
        let bookings = []
        state.bookings.forEach(booking => {
          let obj
          if (booking.room_id) {
            obj = {
              id: booking.booking_id,
              title: booking.booking_name,
              start: new moment(booking.start_time).utc(),
              end: new moment(booking.end_time).utc(),
              resourceId: booking.room_id,
              invigilator: booking.invigilator,
              room: booking.room,
            }
          }
          if (!booking.room_id) {
            obj = {
              id: booking.booking_id,
              title: booking.booking_name,
              start: new moment(booking.start_time).utc(),
              end: new moment(booking.end_time).utc(),
              resourceId: '_offsite',
            }
          }
          if (state.exams) {
            if (state.exams.find(ex => ex.booking_id == booking.booking_id)) {
              obj['exam'] = state.exams.find(ex => ex.booking_id == booking.booking_id)
            }
          }
          bookings.push(obj)
        })
        return bookings
      }
      return []
    },
    
    exam_inventory(state) {
      if (state.showExamInventoryModal) {
        return state.exams.filter(exam => exam.booking_id === null)
      }
      return state.exams
    },
    
    exam_object(state) {
      if (state.capturedExam && state.capturedExam.exam_type_id) {
        return state.examTypes.find(type => type.exam_type_id == state.capturedExam.exam_type_id)
      }
      return {
        exam_color: '',
        exam_type_name: '',
        exam_type_id: ''
      }
    },

    showExams(state) {
      if (state.user && state.user.office.exams_enabled_ind === 1) {
        return true
      }
      return false
    },

    add_exam_modal_navigation_buttons(state) {
      //controls disabled/enabled state of and current classes applied to the 'next' button in AddExamFormModal
      let setup = state.captureITAExamTabSetup
      if (setup.stepsValidated.indexOf(setup.step) === -1) {
        return {
          nextClass: 'btn-secondary disabled',
          nextDisabled: true
        }
      } else if (setup.step < setup.highestStep) {
        return {
          nextClass: 'btn-primary',
          nextDisabled: false
        }
      } else {
        return {
          nextClass: 'btn-primary',
          nextDisabled: false
        }
      }
    },

    role_code(state) {
      if (state.user && state.user.role && state.user.role.role_code) {
        return state.user.role.role_code
      }
      return ''
    },
    
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

    loginIframe(context) {
      Axios(context).get('/login/').then( () => {
        context.commit('setiframeLogedIn', true)
      })
    },

    changeAdminView(context, view) {
      if (view !== null) {
        context.commit("setNavigation", view)
      }
    },
  
    deleteBooking(context, id) {
      return new Promise((resolve, reject) => {
        Axios(context).delete(`/bookings/${id}/`).then(resp => {
          resolve(resp.data)
        })
          .catch(error => {
            reject(error)
          })
      })
    },
    
    putBooking(context, payload) {
      return new Promise((resolve, reject) => {
        Axios(context).put(`/bookings/${payload.id}/`, payload.changes).then(resp => {
          resolve(resp.data)
        })
          .catch(error => {
            reject(error)
          })
      })
    },

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

    getBookings(context) {
      return new Promise((resolve, reject) => {
        Axios(context).get('/bookings/')
        .then(resp => {
          context.commit('setBookings', resp.data.bookings)
          let calendarEvents = []
          
          resp.data.bookings.forEach(b => {
            let booking = {}
            if (b.room_id) {
              booking.resourceId = b.room_id
              booking.room = b.room
            }
            if (!b.room_id) {
              booking.resourceId = '_offsite'
            }
            if (b.invigilator_id) {
              booking.invigilator = b.invigilator
              booking.invigilator_id = b.invigilator_id
            }
            booking.start = b.start_time
            booking.end = b.end_time
            booking.title = b.booking_name
            booking.id = b.booking_id
            let exam = context.state.exams.find(ex => parseInt(ex.booking_id) == parseInt(b.booking_id)) || null
            if (exam !== null && exam.length >= 1) {
              booking.exam = exam
            }
          calendarEvents.push(booking)
          })
          context.commit('setEvents', calendarEvents)
          resolve()
        }).catch(() => { reject() })
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

    getCsrStateIDs(context) {
      Axios(context).get("/csr_states/")
        .then(resp => {
          var states = resp.data.csr_states;
          states.forEach(x => {
            context.state.csr_states[x.csr_state_name] = x.csr_state_id;
          });
        })
        .catch(error => {
          console.log("error @ store.actions.getCsrStateIDs");
          console.log(error.response);
          console.log(error.message);
        });
    },

    getCsrs(context) {
      Axios(context).get('/csrs/')
        .then(resp => {
          context.commit('setCsrs', resp.data.csrs)
        })
        .catch(error => {
          console.log('error @ store.actions.getCsrs')
          console.log(error.response)
          console.log(error.message)
        })
    },

    getExams(context) {
      return new Promise((resolve, reject) => {
        Axios(context).get('/exams/')
          .then(resp => {
            if (resp.data.exams.length > 0) {
              context.commit('setExams', resp.data.exams)
              let groupExams = resp.data.exams.filter(exm => exm.exam_type.exam_type_name.includes('Group'))
              let groupBookings = groupExams.map(ex =>
                ({
                  title: ex.exam_name,
                  start: new moment(ex.expiry_date).utc().local().toString(),
                  end: new moment(ex.expiry_date).add(ex.exam_type.number_of_hours, 'h').toString(),
                  resourceId: '_offsite',
                  exam: ex,
                })
              )
              context.commit('setGroupBookings', groupBookings)
            }
            resolve(resp)
          })
          .catch(error => {
            console.log(error)
            reject(error)
          })
      })
    },

    getExamsExport(context, url) {
      return new Promise((resolve, reject) => {
        Axios(context).get(url)
          .then(resp => {
            resolve(resp)
          })
          .catch(error => {
            console.log(error)
            reject(error)
          })
      })
    },

    getExamTypes(context) {
      return new Promise((resolve, reject) => {
        Axios(context).get('/exam_types/')
          .then(resp => {
            context.commit('setExamTypes', resp.data.exam_types)
            resolve(resp.data.exam_types)
          })
          .catch(error => {
            console.log(error)
            reject(error)
          })
      })
    },

    getInvigilators(context) {
      return new Promise ((resolve, reject) => {
        Axios(context).get('/invigilators/')
          .then(resp => {
            context.commit('setInvigilators', resp.data.invigilators)
            resolve(resp)
          })
          .catch(error => {
            console.log(error)
            reject(error)
          })
      })
    },
    
    getOffices(context, payload=null) {
      if (context.state.user.role.role_code === 'LIAISON' || payload === 'force') {
        return new Promise((resolve, reject) => {
          Axios(context).get('/offices/').then(resp => {
            context.commit('setOffices', resp.data.offices)
            resolve(resp.data.offices)
          })
            .then(error => {
              reject(error)
            })
        })
      }
    },

    getRooms(context) {
      return new Promise((resolve, reject) => {
        Axios(context).get('/rooms/')
          .then(resp => {
            let resources = []
            if (resp.data.rooms.length > 0) {
              resources = resp.data.rooms.map(room =>
                ({
                  id: room.room_id,
                  title: room.room_name,
                  eventColor: room.color
                })
              )
            }
            resources.push({
              id: '_offsite',
              title: 'Offsite',
              eventColor: '#82ff68'
            })
            context.commit('setRooms', resp.data.rooms)
            context.commit('setResources', resources)
            resolve(resources)
          })
          .catch( error => {
            reject(error)
          })
      })
    },

    getServices(context) {
      let office_id = context.state.user.office_id
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

          if (resp.data.group_exams > 0) {
            var groupExamBoolean = true
            context.commit('setGroupExam', groupExamBoolean)
          } else {
            var groupExamBoolean = false
            context.commit('setGroupExam', groupExamBoolean)
          }

          if (resp.data.individual_exams > 0) {
            var individualExamBoolean = true
            context.commit('setGroupExam', individualExamBoolean)
          } else {
            var individualExamBoolean = false
            context.commit('setGroupExam', individualExamBoolean)
          }

          if (groupExamBoolean && individualExamBoolean) {
            context.commit('setExamAlert', 'There are Individual Exams and Group Exams that require attention')
          }else if (groupExamBoolean) {
            context.commit('setExamAlert', 'There are Group Exams that require attention')
          }else if (individualExamBoolean) {
            context.commit('setExamAlert', 'There are Individual Exams that require attention')
          }

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

    clickAddExamSubmit(context, type) {
      return new Promise((resolve, reject) => {
        if (type === 'group') {
          context.dispatch('postITAGroupExam').then(() => {
            resolve('success')
          }).catch(() => { reject('failed') })
        }
        if (type === 'individual') {
          context.dispatch('postITAIndividualExam').then(() => {
            resolve('success')
          }).catch(() => { reject('failed') })
        }
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
          context.dispatch('postFinishService', {citizen_id}).then( () => {
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

    finishServiceFromGA(context, citizen_id) {
      context.dispatch('postFinishService', {citizen_id, inaccurate:'true'})
    },

    clickServiceModalClose(context) {
      context.commit('toggleServiceModal', false)
      context.commit('toggleInvitedStatus', true)
    },

    closeGAScreenModal(context) {
      context.commit('toggleGAScreenModal', false)
    },
    
    initializeAgenda(context) {
      return new Promise((resolve, reject) => {
        context.dispatch('getExams').then( () => {
          context.dispatch('getRooms').then( rooms => {
            resolve(rooms)
          })
        })
      })
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

    postFinishService(context, payload) {
      return new Promise((resolve, reject) => {
        let url = `/citizens/${payload.citizen_id}/finish_service/?inaccurate=${payload.inaccurate}`
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
    
    scheduleExam(context, payload) {
      context.dispatch('postBooking', payload).then(booking_id => {
        context.dispatch('putExam', booking_id).then( () => {
          context.dispatch('finishBooking')
        })
      })
    },
    
    putExam(context, payload) {
      let bookingId, examId
      if (typeof payload === 'object' && payload !== null) {
        bookingId = payload.bookingId
        examId = payload.examId
      } else {
        bookingId = payload
        examId = context.state.selectedExam.exam_id
      }
      return new Promise((resolve, reject) => {
        let url = `/exams/${examId}/`
        Axios(context).put(url, {booking_id: bookingId}).then( resp =>{
          resolve(resp)
        })
          .catch(error => {
            reject(error)
          })
      })
    },

    putExamInfo(context, payload) {
      return new Promise((resolve, reject) => {
        let url = `/exams/${context.state.selectedExam.exam_id}/`
        Axios(context).put(url, payload).then( resp =>{
          resolve(resp)
          context.commit('setEditExamSuccess', true)
          context.commit('setExamEditSuccessMessage', 'Success! Exam changes were committed.')
        })
          .catch(error => {
            context.commit('setEditExamFailure', true)
            context.commit('setExamEditFailureMessage', 'There was a problem submitting changes to your exam.')
            reject(error)
          })
      })
    },

    putBookingInfo(context, payload) {
      return new Promise((resolve, reject) => {
        let url = `/bookings/${context.state.selectedBooking.booking_id}/`
        Axios(context).put(url, payload).then( resp =>{
          resolve(resp)
        })
          .catch(error => {
            reject(error)
          })
      })
    },

    
    postBooking(context, payload) {
      if (!Object.keys(payload).includes('office_id')) {
        payload['office_id'] = context.state.user.office_id
      }
      return new Promise((resolve, reject) => {
        Axios(context).post('/bookings/', payload).then( resp => {
          resolve(resp.data.booking.booking_id)
        })
          .catch(error => {
            reject(error)
          })
      })
    },
    
    finishBooking(context) {
      context.dispatch('getBookings')
      context.commit('setSelectionIndicator', false)
      context.commit('navigationVisible', true)
      context.commit('toggleCalendarControls', true)
      context.commit('toggleScheduling', false)
      context.commit('toggleSchedulingOther', false)
      context.commit('toggleSchedulingIndicator', false)
      context.commit('toggleBookingModal', false)
      context.commit('toggleOtherBookingModal', false)
      context.commit('setClickedDate', null)
      context.commit('setSelectedExam', null)
      context.commit('setEditedBooking', null)
      context.commit('toggleEditBookingModal', false)
    },
    
    postITAGroupExam(context) {
      let responses = Object.assign( {}, context.state.capturedExam)
      let date = moment(responses.expiry_date).local().format('YYYY-MM-DD').toString()
      let time = moment(responses.exam_time).local().format('H:mm').toString()
      let datetime = date+'T'+time
      let start = moment(datetime).local()
      let length = context.state.examTypes.find(ex => ex.exam_type_id == responses.exam_type_id).number_of_hours
      let end = start.clone().add(length, 'hours')
      let booking = {
        start_time: start.clone().utc().format('YYYY-MM-DD[T]HH:mm:ssZ'),
        end_time: end.clone().utc().format('YYYY-MM-DD[T]HH:mm:ssZ'),
        fees: 'false',
        booking_name: responses.exam_name,
        office_id: responses.office_id,
      }
      
      let defaultValues = {
        exam_received: 0,
        exam_returned_ind: 0,
        examinee_name: 'group exam',
        expiry_date: new moment('2499-01-01T12:00:00-08:00').toString()
      }
      delete responses.exam_time
      if (responses.notes === null) {
        data.notes = ''
      }
      let postData = {...responses, ...defaultValues}
      
      return new Promise((resolve, reject) => {
        Axios(context).post('/exams/', postData)
        .then(examResp => {
            let { exam_id } = examResp.data.exam
            context.dispatch('postBooking', booking)
            .then( bookingResp => {
                let putObject = {
                  examId: exam_id,
                  bookingId: bookingResp,
                  officeId: responses.office_id
                }
                context.dispatch('putExam', putObject)
                .then( () => {
                    resolve()
                }).catch( () => { reject() })
            }).catch( () => { reject() })
        }).catch( () => { reject() })
      })
    },
  
    postITAIndividualExam(context) {
      let responses = Object.assign( {}, context.state.capturedExam)
      let defaultValues = {
        exam_received: 1,
        exam_returned_ind: 0,
        number_of_students: 1,
        office_id: context.state.user.office_id
      }
      responses.expiry_date = moment(responses.expiry_date).format('YYYY-MM-DD')
      if (responses.notes === null) {
        responses.notes = ''
      }
      let postData = {...responses, ...defaultValues}
  
      return new Promise((resolve, reject) => {
        Axios(context).post('/exams/', postData)
          .then(() => { resolve() })
          .catch(() => { reject() })
      })
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
    updateCSRCounterTypeState(context) {
      let csr_id = context.state.user.csr_id
      Axios(context).put(`/csrs/${csr_id}/`, {
        qt_xn_csr_ind: context.state.user.qt_xn_csr_ind,
        receptionist_ind: context.state.user.receptionist_ind
      })
        .then( resp => {
        })
    },

    updateCSRState(context) {
      let csr_id = context.state.user.csr_id
      Axios(context).put(`/csrs/${csr_id}/`, {
        csr_state_id: context.state.user.csr_state_id,
      })
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

    setSelectedOffice(state, payload) {
      state.selectedOffice = payload
    },

    setExamAlert(state, payload) {
      state.examAlertMessage = payload
      state.examDismissCount = 999
    },

    setExamEditSuccessMessage(state, payload) {
      state.examEditSuccessMessage = payload
    },

    setExamEditFailureMessage(state, payload) {
      state.examEditFailureMessage = payload
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

    setExams(state, payload) {
      state.exams = []
      state.exams = payload
    },

    setExamTypes(state, payload) {
      state.examTypes = []
      state.examTypes = payload
    },

    setInvigilators(state, payload){
      state.invigilators = []
      state.invigilators = payload
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

    examDismissCountDown(state, payload) {
      state.examDismissCount = payload
    },

    examSuccessCountDown(state, payload) {
      state.examSuccessDismiss = payload
    },

    toggleInvitedStatus: (state, payload) => state.citizenInvited = payload,

    toggleBegunStatus: (state, payload) => state.serviceBegun = payload,

    toggleGAScreenModal: (state,payload) => state.showGAScreenModal = payload,

    setQuickTransactionState: (state, payload) => state.user.qt_xn_csr_ind = payload,

    setReceptionistState: (state, payload) => state.user.receptionist_ind = payload,

    setCSRState: (state, payload) => state.user.csr_state_id = payload,

    setUserCSRStateName: (state, payload) => state.user.csr_state.csr_state_name = payload,

    setOffice: (state, officeType) => state.officeType = officeType,

    flashServeNow: (state, payload) => state.serveNowStyle = payload,

    setServeNowAction: (state, payload) => state.serveNowAltAction = payload,

    toggleFeedbackModal: (state, payload) => state.showFeedbackModal = payload,

    toggleAddNextService: (state, payload) => state.addNextService = payload,

    toggleShowAdmin: (state) => state.showAdmin = !state.showAdmin,

    setFeedbackMessage: (state, payload) => state.feedbackMessage = payload,

    setPerformingAction: (state, payload) => state.performingAction = payload,

    setUserLoadingFail: (state, payload) => state.userLoadingFail = payload,

    setGroupExam: (state, payload) => state.groupExam = payload,

    setIndividualExam: (state, payload) => state.individualExam = payload,

    showHideResponseModal(state) {
      state.showResponseModal = true
      setTimeout( ()=> {state.showResponseModal = false}, 3000)
    },

    hideResponseModal(state) {
      state.showResponseModal = false
    },

    setiframeLogedIn: (state, value) => state.iframeLogedIn = value,

    setNavigation: (state, value) => state.adminNavigation = value,
  
    toggleAddITAExamModal(state, payload) {
      if (typeof payload === 'object') {
        Object.keys(payload).forEach(key => {
          Vue.set(
            state.addITAExamModal,
            key,
            payload[key]
          )
        })
      } else {
        state.addITAExamModal.visible = payload
      }
    },

    toggleGenFinReport(state, payload) {
      state.showGenFinReportModal = payload
    },

    captureExamDetail(state, payload) {
      if (payload.key === 'exam_type_id') {
        payload.value = Number(payload.value)
      }
      if (payload.key === 'event_id') {
        payload.value = payload.value.toString()
      }
      Vue.set(
        state.capturedExam,
        payload.key,
        payload.value
      )
    },

    resetCaptureForm(state) {
      let keys = Object.keys(state.capturedExam)
      keys.forEach(key => {
        let value = null
        if (key === 'exam_method') {
          value = 'paper'
        }
        Vue.set(
          state.capturedExam,
          key,
          value
        )
      })
    },

    resetCaptureTab(state) {
      let initialState = {
        step: 1,
        highestStep: 1,
        stepsValidated: [],
        errors: [],
        showRadio: true,
        success: '',
        notes: false
      }
      let keys = Object.keys(initialState)
      keys.forEach(key => {
        Vue.set(
          state.captureITAExamTabSetup,
          key,
          initialState[key]
        )
      })
    },

    updateCaptureTab(state, payload) {
      let keys = Object.keys(payload)
      keys.forEach(key=>{
        Vue.set(
          state.captureITAExamTabSetup,
          key,
          payload[key]
        )
      })
    },

    toggleIndividualCaptureTabRadio(state, payload) {
      Vue.set(
        state.captureITAExamTabSetup,
        'showRadio',
        payload
      )
    },
  
    setBookings(state, payload) {
      state.bookings = payload
    },
    
    setRooms(state, payload) {
      state.rooms = payload
    },
  
    toggleBookingModal: (state, payload) => state.showBookingModal = payload,
    
    setClickedDate: (state, payload) => state.clickedDate = payload,
    
    toggleExamInventoryModal: (state, payload) => state.showExamInventoryModal = payload,

    toggleNonITAExamModal: (state, payload) => state.nonITAExam = payload,

    toggleEditExamModalVisible: (state, payload) => state.showEditExamModalVisible = payload,

    toggleReturnExamModalVisible: (state, payload) => state.showReturnExamModalVisible = payload,

    setEditExamInfo: (state, payload) => state.editExams = payload,

    setReturnExamInfo: (state, payload) => state.returnExams = payload,

    setExamMethods: (state, payload) => state.examMethods = payload,

    setSelectedExam: (state, payload) => state.selectedExam = payload,

    setSelectedBooking: (state, payload) => state.selectedBooking = payload,
  
    toggleScheduling: (state, payload) => state.scheduling = payload,
    
    toggleCalendarControls: (state, payload) => state.showCalendarControls = payload,
  
    navigationVisible: (state, payload) => state.navigationVisible = payload,
    
    setCalendarSetup: (state, payload) => state.calendarSetup = payload,
  
    toggleSchedulingOther: (state, payload) => state.schedulingOther = payload,
    
    toggleOtherBookingModal: (state, payload) => state.showOtherBookingModal = payload,
  
    toggleSchedulingIndicator: (state, payload) => state.showSchedulingIndicator= payload,

    setEditExamSuccess: (state, payload) => state.editExamSuccess = payload,

    setEditExamFailure: (state, payload) => state.editExamFailure = payload,
  
    toggleEditBookingModal: (state, payload) => state.showEditBookingModal = payload,
  
    setEditedBooking(state, payload) {
      if (payload) {
        let eventCopy = Object.assign({}, payload)
        state.editedBooking = eventCopy
      }
      if (!payload) {
        state.editedBooking = null
      }
    },
  
    toggleRescheduling: (state, payload) => state.rescheduling = payload,
  
    setEditedBookingOriginal: (state, payload) => state.editedBookingOriginal = payload,
    
    setOffices: (state, payload) => state.offices = payload,
    
    setOfficeFilter: (state, payload) => state.officeFilter = payload,
  
    setSelectionIndicator: (state, payload) => state.selectionIndicator = payload,
    
    toggleAddITAExamVisibility(state, payload) {
      Vue.set(
        state.addITAExamModal,
        'visible',
        payload
      )
    },
    setGroupBookings: (state, payload) => state.groupBookings = payload,
  
    setResources: (state, payload) => state.roomResources = payload,
    
    toggleSelectInvigilatorModal: (state, payload) => state.showSelectInvigilatorModal = payload,
    
    setEvents: (state, payload) => state.calendarEvents = payload,
  }
})
