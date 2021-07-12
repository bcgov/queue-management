/* eslint-disable */
/**
 *
 * Notes
 * JSTOTS - javascript to typescript Conversation
 * Just moved all action from index.js to action-madel file
 * No changes in functionality or any variables
 * this is just moving
 * in Future have to extract all functions and export Individually with typs defined
 * and import in index.ts
 *
 */

// import { ActionIF } from '@/interfaces/action-interface'

import { Axios, searchNestedObject } from './../helpers'

import AppointmentsModule from '../modules/appointments-module';
import { makeBookingReqObj } from '../helpers/makeBookingReqObj'
import moment from 'moment'

const DEFAULT_COUNTER_NAME = 'Counter'
const getEventColor = (isBlackout, room, isStat) => {
  if (isBlackout && isBlackout === 'Y' || isStat) {
    return 'grey darken-1 white--text'
  }
  return room && room.color ? room.color : 'cal-events-default'
}

let flashInt

export const commonActions: any = {

  loginIframe (context) {
    Axios(context)
      .get('/login/')
      .then(() => {
        context.commit('setiframeLogedIn', true)
      })
  },

  clickUploadFile (context, payload) {
    context.commit('setIsUploadingFile', true)
    const formData = new FormData()
    if (payload.file) {
      formData.append('file', payload.file)
      if (payload.newname) {
        formData.append('newname', payload.newname)
      }
    }
    formData.append('manifest', payload.data)
    var contenttype = {
      headers: {
        'content-type': 'multipart/form-data'
      }
    }

    // Post the data to the back end.
    Axios(context)
      .post('/upload/', formData, contenttype)
      .then(
        resp => {
          context.commit('setMainAlert', 'File uploaded successfully.')
          context.dispatch('requestVideoFileInfo')
        },
        error => {
          context.commit(
            'setMainAlert',
            'An error occurred uploading your file.'
          )
        }
      )
      .catch(() => {
        context.commit(
          'setMainAlert',
          'An exceptoin occurred uploading your file.'
        )
      })
      .finally(() => {
        context.commit('setIsUploadingFile', false)
      })
  },

  clickDeleteFile (context, payload) {
    // Post the file name to delete to the back end.
    Axios(context)
      .delete('/videofiles/', { data: payload })
      .then(
        resp => {
          context.commit('setMainAlert', 'File deleted successfully.')
          context.dispatch('requestVideoFileInfo')
        },
        error => {
          context.commit('setMainAlert', 'File could not be deleted.')
        }
      )
    // .catch(() => {
    //   context.commit('setMainAlert', 'An exception occurred trying to delete file.')
    // })
  },

  requestVideoFileInfo (context) {
    // Get video file info from the back end.
    Axios(context)
      .get('/videofiles/')
      .then(resp => {
        const videofiles = resp.data.videofiles
        const manifestdata = resp.data.manifest
        const diskspace = resp.data.space
        context.commit('setVideoFiles', videofiles)
        context.commit('setManifestData', manifestdata)
        context.commit('setDiskSpace', diskspace)
      })
      .catch(error => {
        console.log('error in requestVideoFileInfo')
        console.log(error.response)
        console.log(error.message)
      })
  },

  changeAdminView (context, view) {
    if (view !== null) {
      context.commit('setNavigation', view)
    }
  },

  deleteBooking (context, id) {
    return new Promise((resolve, reject) => {
      Axios(context)
        .delete(`/bookings/${id}/`)
        .then(resp => {
          resolve(resp.data)
        })
        .catch(error => {
          reject(error)
        })
    })
  },

  deleteRecurringBooking (context, id) {
    return new Promise((resolve, reject) => {
      Axios(context)
        .delete(`/bookings/recurring/${id}`)
        .then(resp => {
          resolve(resp.data)
        })
        .catch(error => {
          reject(error)
        })
    })
  },

  deleteRecurringStatBooking (context, id) {
    return new Promise((resolve, reject) => {
      Axios(context)
        .delete(`/bookings/recurring/current-office/${id}`)
        .then(resp => {
          resolve(resp.data)
        })
        .catch(error => {
          reject(error)
        })
    })
  },

  deleteRecurringStatAllOfficeBooking (context, id) {
    return new Promise((resolve, reject) => {
      Axios(context)
        .delete(`/bookings/recurring/stat/${id}`)
        .then(resp => {
          resolve(resp.data)
        })
        .catch(error => {
          reject(error)
        })
    })
  },

  deleteExam (context, id) {
    return new Promise((resolve, reject) => {
      Axios(context)
        .delete(`/exams/${id}/`)
        .then(resp => {
          resolve(resp.data)
        })
        .catch(error => {
          reject(error)
        })
    })
  },

  putRequest (context, payload) {
    return new Promise<void>((resolve, reject) => {
      Axios(context)
        .put(payload.url, payload.data)
        .then(() => {
          resolve()
        })
        .catch(() => {
          reject()
        })
    })
  },

  putBooking (context, payload) {
    return new Promise((resolve, reject) => {
      Axios(context)
        .put(`/bookings/${payload.id}/`, payload.changes)
        .then(resp => {
          resolve(resp.data)
        })
        .catch(error => {
          reject(error)
        })
    })
  },

  putRecurringBooking (context, payload) {
    return new Promise((resolve, reject) => {
      Axios(context)
        .put(`/bookings/recurring/${payload.recurring_uuid}`, payload.changes)
        .then(resp => {
          resolve(resp.data)
        })
        .catch(error => {
          reject(error)
        })
    })
  },

  putInvigilatorShadow (context, payload) {
    return new Promise((resolve, reject) => {
      Axios(context)
        .put(`/invigilator/${payload.id}/${payload.params}`)
        .then(resp => {
          resolve(resp.data)
        })
        .catch(error => {
          reject(error)
        })
    })
  },

  flashServeNow (context, payload) {
    const flash = () => {
      if (!context.state.showServiceModal) {
        if (context.state.serveNowStyle === 'btn-primary') {
          context.commit('flashServeNow', 'btn-highlighted')
        } else if (context.state.serveNowStyle === 'btn-highlighted') {
          context.commit('flashServeNow', 'btn-primary')
        }
      }
    }
    if (payload === 'start') {
      clearInterval(flashInt)
      flashInt = setInterval(() => {
        flash()
      }, 800)
      return
    }
    if (payload === 'stop') {
      clearInterval(flashInt)
      context.commit('flashServeNow', 'btn-primary')
    }
  },

  logIn (context, payload) {
    context.commit('setBearer', payload)
    context.commit('logIn')
    context.dispatch('getUser').catch(() => {
      context.commit('setUserLoadingFail', true)
    })
  },

  getBookings (context) {
    return new Promise<void>((resolve, reject) => {
      Axios(context)
        .get('/bookings/')
        .then(resp => {
          context.commit('setBookings', resp.data.bookings)
          const calendarEvents: any = []
          resp.data.bookings.forEach(b => {
            const booking: any = {}

            if (b.room_id) {
              booking.resourceId = b.room_id
              booking.room = b.room

              // With Vuetify calendar, if the bookings aren't deleted
              // the room calenar will be created.  This hides it
              // entirely from the frontend UI.
              if (booking.room && booking.room.deleted) {
                return;
              }
            }
            if (!b.room_id) {
              booking.resourceId = '_offsite'
            }
            if (b.invigilator_id) {
              booking.invigilator = b.invigilator
              booking.invigilator_id = b.invigilator_id
            }
            booking.start = new Date(new Date(b.start_time).toLocaleString('en-US', { timeZone: b.office.timezone.timezone_name }))
            booking.end = new Date(new Date(b.end_time).toLocaleString('en-US', { timeZone: b.office.timezone.timezone_name }))
            if ( b.stat_flag && b.blackout_notes) {
              booking.name = b.blackout_notes
            } else {
              booking.name = b.booking_name
            }
            booking.id = b.booking_id
            booking.category = b.room ? b.room.room_name : 'Offsite'// 'Boardroom 1'// b.room.room_name
            booking.exam =
              context.state.exams.find(ex => ex.booking_id == b.booking_id) ||
              false
            booking.booking_contact_information =
              b.booking_contact_information
            booking.fees = b.fees
            booking.shadow_invigilator_id = b.shadow_invigilator_id
            booking.blackout_flag = b.blackout_flag
            booking.is_draft = b.is_draft
            booking.blackout_notes = b.blackout_notes
            booking.recurring_uuid = b.recurring_uuid
            booking.color = getEventColor(b.blackout_flag, b.room, b.stat_flag)
            booking.timed = true
            booking.stat_flag = b.stat_flag
            calendarEvents.push(booking)
          })

          context.commit('setEvents', calendarEvents)
          resolve()
        })
        .catch(() => {
          reject()
        })
    })
  },

  getAllCitizens (context) {
    const url = '/citizens/'
    return new Promise<void>((resolve, reject) => {
      Axios(context)
        .get(url)
        .then(resp => {
          if (!resp.data.citizens) {
            context.commit('updateQueue', [])
            resolve()
            return
          }
          context.commit('updateQueue', resp.data.citizens)
          resolve()
        })
    })
  },

  getCategories (context) {
    Axios(context)
      .get('/categories/')
      .then(resp => {
        context.commit('setCategories', resp.data.categories)
      })
      .catch(error => {
        console.log('error @ store.actions.getCategories')
        console.log(error.response)
        console.log(error.message)
      })
  },

  getChannels (context) {
    return new Promise((resolve, reject) => {
      const url = '/channels/'
      Axios(context)
        .get(url)
        .then(
          resp => {
            context.commit('setChannels', resp.data.channels)
            resolve(resp)
          },
          error => {
            reject(error)
          }
        )
    })
  },

  getCitizen (context, citizen_id) {
    return new Promise((resolve, reject) => {
      const url = `/citizens/${citizen_id}/`
      Axios(context)
        .get(url)
        .then(
          resp => {
            resolve(resp)
          },
          error => {
            reject(error)
          }
        )
    })
  },

  getCsrStateIDs (context) {
    Axios(context)
      .get('/csr_states/')
      .then(resp => {
        var states = resp.data.csr_states
        states.forEach(x => {
          context.state.csr_states[x.csr_state_name] = x.csr_state_id
        })
      })
      .catch(error => {
        console.log('error @ store.actions.getCsrStateIDs')
        console.log(error.response)
        console.log(error.message)
      })
  },

  getCsrs (context) {
    Axios(context)
      .get('/csrs/')
      .then(resp => {
        context.commit('setCsrs', resp.data.csrs)
      })
      .catch(error => {
        console.log('error @ store.actions.getCsrs')
        console.log(error.response)
        console.log(error.message)
      })
  },

  getExams (context) {
    return new Promise((resolve, reject) => {
      let url = '/exams/'
      const filter = context.state.inventoryFilters.office_number

      if (filter === 'default') {
        url += `?office_number=${context.state.user.office.office_number}`
      } else {
        url += `?office_number=${filter}`
      }

      Axios(context)
        .get(url)
        .then(resp => {
          context.commit('setExams', resp.data.exams)
          // console.log('==> getExams(context), exams are:')
          // console.log(resp.data.exams)
          resolve(resp)
        })
        .catch(error => {
          console.log(error)
          reject(error)
        })
    })
  },

  getExamEventIDs (context, id) {
    return new Promise((resolve, reject) => {
      const url = `/exams/event_id/${id}/`
      Axios(context)
        .get(url)
        .then(
          resp => {
            context.commit('setExamEventIDs', resp.data.message)
            resolve(resp.data)
          },
          error => {
            reject(error)
          }
        )
    })
  },

  getExamsForOffice (context, office_number) {
    return new Promise((resolve, reject) => {
      let url = '/exams/'

      if (office_number === 'default') {
        url += `?office_number=${context.state.user.office.office_number}`
      } else {
        url += `?office_number=${office_number}`
      }

      Axios(context)
        .get(url)
        .then(resp => {
          context.commit('setExams', resp.data.exams)
          resolve(resp)
        })
        .catch(error => {
          console.log(error)
          reject(error)
        })
    })
  },

  getExamsExport (context, url) {
    return new Promise((resolve, reject) => {
      Axios(context)
        .get(url)
        .then(resp => {
          resolve(resp)
        })
        .catch(error => {
          console.log(error)
          reject(error)
        })
    })
  },

  getExamTypes (context) {
    return new Promise((resolve, reject) => {
      Axios(context)
        .get('/exam_types/')
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

  getInvigilators (context) {
    return new Promise((resolve, reject) => {
      Axios(context)
        .get('/invigilators/')
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

  getPesticideOfficeInvigilators (context) {
    return new Promise((resolve, reject) => {
      Axios(context)
        .get('/invigilators/')
        .then(resp => {
          context.commit('setPesticideInvigilators', resp.data.invigilators)
          resolve(resp)
        })
        .catch(error => {
          console.log(error)
          reject(error)
        })
    })
  },

  getPesticideOffsiteInvigilators (context) {
    return new Promise((resolve, reject) => {
      Axios(context)
        .get('/invigilators/offsite/')
        .then(resp => {
          context.commit(
            'setPesticideOffsiteInvigilators',
            resp.data.invigilators
          )
          resolve(resp)
        })
        .catch(error => {
          console.log(error)
          reject(error)
        })
    })
  },

  getInvigilatorsWithShadowFlag (context) {
    return new Promise((resolve, reject) => {
      Axios(context)
        .get('/invigilators/')
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

  emailInvigilator (context, payload) {
    console.log(payload)
    const invigilator = payload.invigilator
    const postData = {
      invigilator_id: invigilator.invigilator_id,
      invigilator_name: invigilator.invigilator_name,
      invigilator_email: invigilator.contact_email,
      invigilator_phone: invigilator.contact_phone
    }
    const exam = payload.exam

    return new Promise((resolve, reject) => {
      Axios(context)
        .post(`/exams/${exam.exam_id}/email_invigilator/`, postData)
        .then(resp => {
          resolve(resp.data)
        })
        .catch(error => {
          console.log(error)
          reject(error)
        })
    })
  },

  getOffices (context, payload = null) {
    if (
      context.state.user.ita2_designate === 1 ||
      payload === 'force' ||
      context.state.user.pesticide_designate === 1
    ) {
      return new Promise((resolve, reject) => {
        Axios(context)
          .get('/offices/')
          .then(resp => {
            context.commit('setOffices', resp.data.offices)
            resolve(resp.data.offices)
          })
          .then(error => {
            reject(error)
          })
      })
    }
  },

  getRooms (context) {
    return new Promise((resolve, reject) => {
      Axios(context)
        .get('/rooms/')
        .then(resp => {
          let resources: any = []
          if (resp.data.rooms.length > 0) {
            resources = resp.data.rooms.map(room => ({
              id: room.room_id,
              title: room.room_name,
              eventColor: room.color
            }))
          }
          resources.push({
            id: '_offsite',
            title: 'Offsite',
            eventColor: '#F58B4C'
          })
          context.commit('setRooms', resp.data.rooms)
          context.commit('setResources', resources)
          resolve(resources)
        })
        .catch(error => {
          reject(error)
        })
    })
  },

  getOfficeRooms (context, data) {
    return new Promise((resolve, reject) => {
    Axios(context)
      .get(`/rooms/?office_id=${data['office_id']}`)
      .then(resp => {
        let resources: any = []
          if (resp.data.rooms.length > 0) {
            resources = resp.data.rooms.map(room => ({
              id: room.room_id,
              title: room.room_name,
              eventColor: room.color
            }))
          }
          resources.push({
            id: '_offsite',
            title: 'Offsite',
            eventColor: '#F58B4C'
          })
          resolve(resources)
      })
      .catch(error => {
        reject(error)
      })
      })
  },

  getServices (context) {
    const office_id = context.state.user.office_id
    Axios(context)
      .get(`/services/?office_id=${office_id}`)
      .then(resp => {
        const services = resp.data.services.filter(
          service => service.actual_service_ind === 1
        )
        context.commit('setServices', services)
      })
      .catch(error => {
        console.log('error @ store.actions.getServices')
        console.log(error.response)
        console.log(error.message)
      })
  },

  updateExamStatus (context) {
    return new Promise((resolve, reject) => {
      Axios(context)
        .post('/exams/bcmp_status/')
        .then(
          resp => {
            context.dispatch('getExams')
            resolve(resp.data)
          },
          err => {
            reject(err)
          }
        )
        .catch(err => {
          reject(err)
        })
    })
  },

  getUser (context) {
    return new Promise((resolve, reject) => {
      const url = '/csrs/me/'
      Axios(context)
        .get(url)
        .then(
          resp => {
            context.commit('setUser', resp.data.csr)
            const officeType = resp.data.csr.office.sb.sb_type
            context.commit('setOffice', officeType)
            context.commit(
              'setDefaultCounter',
              resp.data.csr.office.counters.filter(
                c => c.counter_name === DEFAULT_COUNTER_NAME
              )[0]
            )
            context.commit(
              'setBackOfficeDisplay',
              resp.data.back_office_display
            )
            context.commit(
              'setRecurringFeatureFlag',
              resp.data.recurring_feature_flag
            )
            const examManagerBoolean = resp.data.attention_needed

            if (examManagerBoolean === true) {
              context.commit(
                'setExamAlert',
                'Office Exam Manager Action Items are present'
              )
            } else {
              context.commit('setExamAlert', '')
            }

            if (
              resp.data.active_citizens &&
              resp.data.active_citizens.length > 0
            ) {
              context.dispatch(
                'checkForUnfinishedService',
                resp.data.active_citizens
              )
            }
            resolve(resp)
          },
          error => {
            context.commit(
              'setLoginAlert',
              'You are not setup in TheQ, please contact RMSHelp to be setup.'
            )
            reject(error)
          }
        )
    })
  },

  getUserAttentionForExam (context) {
    return new Promise((resolve, reject) => {
      const url = '/csrs/me/'
      Axios(context)
        .get(url)
        .then(
          resp => {
            const examManagerBoolean = resp.data.attention_needed            
            if (examManagerBoolean === true) {
              context.commit(
                'setExamAlert',
                'Office Exam Manager Action Items are present'
              )
            } else {
              context.commit('setExamAlert', '')
            }
 
            resolve(resp)
          },
          error => {
            context.commit(
              'setExamAlert',
              'There is an error while setting an exam alert'
            )
            reject(error)
          }
        )
    })
  },

  cancelAddCitizensModal (context) {
    const { citizen_id } = context.getters.form_data.citizen

    context.dispatch('postCitizenLeft', citizen_id).then(() => {
      context.commit('toggleAddModal', false)
      context.commit('resetAddModalForm')
    })
  },

  clickAddCitizen (context) {
    context.commit('setDisplayServices', 'Dashboard')
    context.commit('setPerformingAction', true)
    context.dispatch('toggleModalBack')
    context.commit('toggleAddModal', true)

    Axios(context)
      .post('/citizens/', {})
      .then(
        resp => {
          const value = resp.data.citizen
          context.commit('updateAddModalForm', { type: 'citizen', value })
          context.commit('resetServiceModal')
        },
        error => {
          context.commit('toggleAddModal', false)
          context.commit(
            'setMainAlert',
            'An error occurred adding a citizen.'
          )
          context.commit('toggleServeCitizenSpinner', false)
        }
      )
      .finally(() => {
        context.commit('setPerformingAction', false)
      })
    if (context.state.categories.length === 0) {
      context.dispatch('getCategories')
    }
    if (context.state.channels.length === 0) {
      context.dispatch('getChannels').then(() => {
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

  clickAddService (context) {
    context.commit('setDisplayServices', 'All')
    context.commit('setPerformingAction', true)

    if (context.state.channels.length === 0) {
      context.dispatch('getCategories')
      context.dispatch('getChannels')
      context.dispatch('getServices')
    }

    context.commit('toggleAddNextService', true)

    context.dispatch('putServiceRequest').then(
      response => {
        context
          .dispatch('putCitizen')
          .then(() => {
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
              type: 'counter',
              value: context.getters.invited_citizen.counter_id
            })
            context.commit('updateAddModalForm', {
              type: 'priority',
              value: context.getters.invited_citizen.priority
            })
            context.commit('toggleAddModal', true)
            context.commit('toggleServiceModal', false)
          })
          .finally(() => {
            context.commit('setPerformingAction', false)
          })
      },
      error => {
        console.log(error)
        context.commit('setPerformingAction', false)
      }
    )
  },

  clickAddServiceApply (context) {
    context.commit('setPerformingAction', true)

    context
      .dispatch('postServiceReq')
      .then(() => {
        context
          .dispatch('putCitizen')
          .then(resp => {
            context.commit('toggleAddModal', false)
            context.commit('toggleAddNextService', false)
            context.commit('toggleServiceModal', true)
            context.dispatch('toggleModalBack')
            context.commit('resetAddModalForm')
          })
          .finally(() => {
            context.commit('setPerformingAction', false)
          })
      })
      .catch(() => {
        context.commit('setPerformingAction', false)
      })
  },

  clickAddToQueue (context) {
    const { citizen_id } = context.getters.form_data.citizen
    context.commit('setPerformingAction', true)
    context
      .dispatch('putCitizen')
      .then(() => {
        context
          .dispatch('postServiceReq')
          .then(() => {
            context
              .dispatch('postAddToQueue', citizen_id)
              .then(resp => {
                context.dispatch('resetAddCitizenModal')
                context.commit('toggleBegunStatus', false)
                context.commit('toggleInvitedStatus', false)
              })
              .finally(() => {
                context.commit('setPerformingAction', false)
              })
          })
          .catch(() => {
            context.commit('setPerformingAction', false)
            context.commit('toggleServeCitizenSpinner', false)
          })
      })
      .catch(() => {
        context.commit('setPerformingAction', false)
      })
  },

  clickAddExamSubmit (context, type) {
    return new Promise((resolve, reject) => {
      if (type === 'challenger') {
        context
          .dispatch('postITAChallengerExam')
          .then(() => {
            resolve('success')
          })
          .catch(() => {
            reject('failed')
          })
      }
      if (type === 'group') {
        context
          .dispatch('postITAGroupExam')
          .then(() => {
            resolve('success')
          })
          .catch(() => {
            reject('failed')
          })
      }
      if (type === 'individual') {
        context
          .dispatch('postITAIndividualExam')
          .then(
            () => {
              resolve('success')
            },
            err => {
              reject(err)
            }
          )
          .catch(err => {
            reject(err)
          })
      }
    })
  },

  clickRequestExam (context, type) {
    return new Promise((resolve, reject) => {
      context
        .dispatch('postRequestExam')
        .then(() => {
          resolve('success')
        })
        .catch(() => {
          reject('failed')
        })
    })
  },

  clickPesticideRequestExam (context) {
    return new Promise((resolve, reject) => {
      context
        .dispatch('postITAIndividualExam', true)
        .then(resp => {
          if (resp && resp.data && resp.data.bcmp_job_id) {
            resolve(resp.data.bcmp_job_id)
          } else {
            reject(resp)
          }
        })
        .catch(err => {
          reject(err)
        })
    })
  },

  clickAdmin (context) {
    context.commit('toggleShowAdmin')
  },

  clickBeginService (context, payload) {
    context.commit('setPerformingAction', true)
    context.commit('toggleServeCitizenSpinner', true)
    const { citizen_id } = context.getters.form_data.citizen
    context
      .dispatch('putCitizen')
      .then(() => {
        context
          .dispatch('postServiceReq')
          .then(() => {
            context
              .dispatch('postBeginService', citizen_id)
              .then(() => {
                context.commit('toggleAddModal', false)
                context.commit('toggleBegunStatus', true)
                context.commit('toggleInvitedStatus', false)
                if (!payload.simple) {
                  context.commit('toggleServiceModal', true)
                }
                context.commit('resetAddModalForm')
              })
              .finally(() => {
                context.commit('setPerformingAction', false)
              })
          })
          .catch(() => {
            context.commit('setPerformingAction', false)
            context.commit('toggleServeCitizenSpinner', false)
          })
      })
      .catch(() => {
        context.commit('setPerformingAction', false)
        context.commit('toggleServeCitizenSpinner', false)
      })
  },

  clickQuickServe (context) {
    context.commit('setPerformingAction', true)

    if (context.state.channels.length === 0) {
      context.dispatch('getChannels').then(() => {
        context.commit('setDefaultChannel')
      })
    }
    if (context.state.channels.length > 0) {
      context.commit('setDefaultChannel')
    }

    Axios(context)
      .post('/citizens/', {})
      .then(
        resp => {
          const value = resp.data.citizen
          context.commit('updateAddModalForm', { type: 'citizen', value })
          context.commit('resetServiceModal')
          context
            .dispatch('putCitizen')
            .then(() => {
              context
                .dispatch('postServiceReq')
                .then(() => {
                  context
                    .dispatch('postBeginService', value.citizen_id)
                    .then(() => {
                      context.commit('toggleAddModal', false)
                      context.commit('toggleBegunStatus', true)
                      context.commit('toggleInvitedStatus', false)
                      context.commit('toggleServiceModal', true)
                      context.commit('resetAddModalForm')
                    })
                    .finally(() => {
                      context.commit('setPerformingAction', false)
                    })
                })
                .catch(() => {
                  context.commit('setPerformingAction', false)
                })
            })
            .catch(() => {
              context.commit('setPerformingAction', false)
            })
        },
        error => {
          context.commit(
            'setMainAlert',
            'An error occurred adding a citizen.'
          )
          context.commit('toggleServeCitizenSpinner', false)
        }
      )

    if (context.state.channels.length === 0) {
      context.dispatch('getChannels').then(() => {
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

  clickBackOffice (context) {
    context.commit('setDisplayServices', context.state.backOfficeDisplay)
    context.commit('setPerformingAction', true)
    context.dispatch('toggleModalBack')

    Axios(context)
      .post('/citizens/', {})
      .then(resp => {
        const value = resp.data.citizen
        context.commit('updateAddModalForm', { type: 'citizen', value })
        context.commit('toggleAddModal', true)
        context.commit('resetServiceModal')
      })
      .finally(() => {
        context.commit('setPerformingAction', false)
      })

    const setupChannels = () => {
      let index = -1
      const { channel_options } = context.getters
      channel_options.forEach((opt, i) => {
        if (opt.text.toLowerCase() === 'back office') {
          index = i
        }
      })
      if (index >= 0) {
        context.commit('updateAddModalForm', {
          type: 'channel',
          value: channel_options[index].value
        })
      } else {
        context.commit('setDefaultChannel')
      }
    }

    if (context.state.channels.length === 0) {
      context.dispatch('getChannels').then(() => {
        setupChannels()
      })
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

  clickQuickBackOffice (context) {
    context.commit('setPerformingAction', true)
    context.dispatch('toggleModalBack')

    Axios(context)
      .post('/citizens/', {})
      .then(resp => {
        const value = resp.data.citizen
        context.commit('updateAddModalForm', { type: 'citizen', value })
        context.commit('resetServiceModal')
        context
          .dispatch('putCitizen')
          .then(() => {
            context
              .dispatch('postServiceReq')
              .then(() => {
                context
                  .dispatch('postBeginService', value.citizen_id)
                  .then(() => {
                    context.commit('toggleAddModal', false)
                    context.commit('toggleBegunStatus', true)
                    context.commit('toggleInvitedStatus', false)
                    context.commit('toggleServiceModal', true)
                    context.commit('resetAddModalForm')
                  })
                  .finally(() => {
                    context.commit('setPerformingAction', false)
                  })
              })
              .catch(() => {
                context.commit('setPerformingAction', false)
              })
          })
          .catch(() => {
            context.commit('setPerformingAction', false)
          })
      })

    const setupChannels = () => {
      let index = -1
      const { channel_options } = context.getters
      channel_options.forEach((opt, i) => {
        if (opt.text.toLowerCase() === 'back office') {
          index = i
        }
      })
      if (index >= 0) {
        context.commit('updateAddModalForm', {
          type: 'channel',
          value: channel_options[index].value
        })
      } else {
        context.commit('setDefaultChannel')
      }
    }

    if (context.state.channels.length === 0) {
      context.dispatch('getChannels').then(() => {
        setupChannels()
      })
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

  clickRefresh (context) {
    context.commit('setPerformingAction', true)
    const office_id = context.state.user.office_id
    Axios(context)
      .get(`/services/refresh/?office_id=${office_id}`)
      .then(resp => {
        context.commit('setQuickList', resp.data.quick_list)
        context.commit('setBackOfficeList', resp.data.back_office_list)
      })
      .finally(() => {
        context.commit('setPerformingAction', false)
      })
  },

  clickCitizenLeft (context) {
    const { citizen_id } = context.getters.invited_citizen
    context.commit('setPerformingAction', true)

    context.dispatch('postCitizenLeft', citizen_id).finally(() => {
      // send reminder for nth citizen in line
      context
      .dispatch('sendWalkinLineReminder', {
        citizen_id: citizen_id
      })
      .then(() => {
        context.dispatch('getAllCitizens')
      })
      context.commit('setPerformingAction', false)
    })
    context.commit('toggleServiceModal', false)
    context.commit('toggleBegunStatus', false)
    context.commit('toggleInvitedStatus', false)
    context.commit('resetServiceModal')
  },

  clickDashTableRow (context, citizen_id) {
    context.commit('toggleServeCitizenSpinner', true)
    context.commit('setPerformingAction', true)

    context
      .dispatch('postInvite', citizen_id)
      .then(() => {
        context.commit('toggleBegunStatus', false)
        context.commit('toggleInvitedStatus', true)
        context.commit('toggleServiceModal', true)
      })
      .finally(() => {
        context.commit('setPerformingAction', false)
      })
  },

  clickEdit (context) {
    context.commit('setDisplayServices', 'All')
    context.commit('setPerformingAction', true)

    if (context.state.channels.length === 0) {
      context.dispatch('getCategories')
      context.dispatch('getChannels')
      context.dispatch('getServices')
    }

    context
      .dispatch('putServiceRequest')
      .then(() => {
        context
          .dispatch('putCitizen')
          .then(() => {
            context.commit('switchAddModalMode', 'edit_mode')
            context.dispatch('setAddModalData')
            context.commit('toggleAddModal', true)
            context.commit('toggleServiceModal', false)
            context.commit('setPerformingAction', false)
          })
          .finally(() => {
            context.commit('setPerformingAction', false)
          })
      })
      .catch(() => {
        context.commit('setPerformingAction', false)
      })
  },

  clickEditApply (context) {
    context.commit('setPerformingAction', true)

    context
      .dispatch('putServiceRequest')
      .then(() => {
        context
          .dispatch('putCitizen')
          .then(() => {
            context.commit('toggleAddModal', false)
            context.dispatch('toggleModalBack')
            context.commit('resetAddModalForm')
            context.commit('toggleServiceModal', true)
          })
          .finally(() => {
            context.commit('setPerformingAction', false)
          })
      })
      .catch(() => {
        context.commit('setPerformingAction', false)
      })
  },

  clickEditCancel (context) {
    context.commit('toggleAddModal', false)
    context.dispatch('toggleModalBack')
    context.commit('resetAddModalForm')
    context.commit('toggleServiceModal', true)
  },

  clickGAScreen (context) {
    context.dispatch('getCsrs').then(() => {
      context.commit('toggleGAScreenModal', !context.state.showGAScreenModal)
    })
  },

  clickAgendaScreen (context) {
    context.commit('toggleAgendaScreenModal', !context.state.showAgendaScreenModal)
  },

  clickHold (context) {
    const { citizen_id } = context.state.serviceModalForm
    context.commit('setPerformingAction', true)

    context
      .dispatch('putServiceRequest')
      .then(() => {
        context
          .dispatch('putCitizen')
          .then(() => {
            context
              .dispatch('postHold', citizen_id)
              .then(() => {
                context.commit('toggleBegunStatus', false)
                context.commit('toggleInvitedStatus', false)
                context.commit('toggleServiceModal', false)
                context.commit('resetServiceModal')
              })
              .finally(() => {
                context.commit('setPerformingAction', false)
              })
          })
          .catch(() => {
            context.commit('setPerformingAction', false)
          })
      })
      .catch(() => {
        context.commit('setPerformingAction', false)
      })
  },

  clickInvite (context) {
    context.commit('toggleInviteCitizenSpinner', true)
    context.commit('setPerformingAction', true)

    context
      .dispatch('postInvite', 'next')
      .then(() => {
        context.commit('toggleInvitedStatus', true)
        context.commit('toggleServiceModal', true)
      })
      .catch(() => {
        // context.commit('setMainAlert', '(index) There are no citizens waiting.')
        context.commit('toggleInviteCitizenSpinner', false)
      })
      .finally(() => {
        context.commit('setPerformingAction', false)
        context.commit('toggleInviteCitizenSpinner', false)
      })
    context.dispatch('flashServeNow', 'stop')
  },

  checkForUnfinishedService (context, citizens) {
    if (context.state.serviceBegun || context.state.citizenInvited) {
      clearInterval(flashInt)
      context.commit('flashServeNow', 'btn-primary')
      return
    }
    if (!(context.state.serviceBegun && context.state.citizenInvited)) {
      let citizenFound = false
      citizens.forEach(citizen => {
        if (citizen.service_reqs.length > 0) {
          const activeService = citizen.service_reqs.filter(sr =>
            sr.periods.some(p => p.time_end === null)
          )
          if (activeService[0].periods.length > 0) {
            const activePeriod =
              activeService[0].periods[activeService[0].periods.length - 1]
            if (
              ['Invited', 'Being Served'].indexOf(activePeriod.ps.ps_name) >
              -1 &&
              activePeriod.csr.username === this.state.user.username
            ) {
              citizenFound = true

              if (activePeriod.ps.ps_name === 'Invited') {
                context.commit('setServiceModalForm', citizen)
                context.commit('toggleInvitedStatus', true)
                context.commit('toggleBegunStatus', false)
                context.dispatch('flashServeNow', 'start')
                context.commit('resetAddModalForm')
              } else if (activePeriod.ps.ps_name === 'Being Served') {
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

      if (!citizenFound) {
        context.commit('resetServiceModal')
        context.commit('toggleServiceModal', false)
        context.commit('toggleBegunStatus', false)
        context.commit('toggleInvitedStatus', false)
      }
    }
  },

  clickMakeActive (context, sr_id) {
    context.commit('setPerformingAction', true)

    context
      .dispatch('putServiceRequest')
      .then(() => {
        context
          .dispatch('putCitizen')
          .then(() => {
            context
              .dispatch('postActivateServiceReq', sr_id)
              .finally(() => {
                context.commit('setPerformingAction', false)
              })
              .finally(() => {
                context.commit('setPerformingAction', false)
              })
          })
          .catch(() => {
            context.commit('setPerformingAction', false)
          })
      })
      .catch(() => {
        context.commit('setPerformingAction', false)
      })
  },

  clickReturnToQueue (context) {
    const { citizen_id } = context.getters.invited_citizen
    context.commit('setPerformingAction', true)

    context
      .dispatch('putServiceRequest')
      .then(() => {
        context
          .dispatch('putCitizen')
          .then(() => {
            context
              .dispatch('postAddToQueue', citizen_id)
              .then(() => {
                context.commit('toggleInvitedStatus', false)
                context.commit('toggleServiceModal', false)
                context.commit('resetServiceModal')
              })
              .finally(() => {
                context.commit('setPerformingAction', false)
              })
          })
          .catch(() => {
            context.commit('setPerformingAction', false)
          })
      })
      .catch(() => {
        context.commit('setPerformingAction', false)
      })
  },

  clickUnCheckIn (context) {
    const { citizen_id } = context.getters.invited_citizen
    context.commit('setPerformingAction', true)

    Axios(context)
      .post(`/citizens/${citizen_id}/remove_from_queue/`, {})
      .then((res) => {
        context.commit('toggleInvitedStatus', false)
        context.commit('setPerformingAction', false)
        context.commit('toggleServiceModal', false)
        context.commit('resetServiceModal')
        context.dispatch('flashServeNow', 'stop')
        context.dispatch('appointmentsModule/getAppointments')
      })
      .catch(() => {
        context.commit('setPerformingAction', false)
      })
  },

  clickRowHoldQueue (context, citizen_id) {
    context.commit('toggleServeCitizenSpinner', true)
    context.commit('setPerformingAction', true)

    context
      .dispatch('postBeginService', citizen_id)
      .then(() => {
        context.commit('toggleBegunStatus', true)
        context.commit('toggleInvitedStatus', false)
        context.commit('toggleServiceModal', true)
      })
      .finally(() => {
        context.commit('setPerformingAction', false)
      })
  },
  // JSTOTS added payload as param
  toggleBegunStatus ({ commit }, payload) {
    commit('toggleBegunStatus', payload)
  },

  toggleInvitedStatus (context, payload) {
    context.commit('toggleInvitedStatus', payload)
  },

  clickServeNow (context) {
    if (context.state.serveNowAltAction) {
      context.commit('toggleBegunStatus', true)
      context.commit('toggleInvitedStatus', false)
    }
    context.commit('toggleServiceModal', true)
    context.dispatch('flashServeNow', 'stop')
  },

  clickServiceBeginService (context) {
    context.commit('setPerformingAction', true)
    context.commit('toggleServeCitizenSpinner', true)
    const { citizen_id } = context.state.serviceModalForm

    context
      .dispatch('putServiceRequest')
      .then(() => {
        context
          .dispatch('putCitizen')
          .then(() => {
            context
              .dispatch('postBeginService', citizen_id)
              .then(() => {
                context.commit('toggleBegunStatus', true)
                // send reminder for nth citizen in line
                context
                .dispatch('sendWalkinLineReminder', {
                  citizen_id: citizen_id
                })
                .then(() => {
                  context.dispatch('getAllCitizens')
                })
              })
              .finally(() => {
                context.commit('setPerformingAction', false)
              })
          })
          .catch(() => {
            context.commit('setPerformingAction', false)
            context.commit('toggleServeCitizenSpinner', false)
          })
      })
      .catch(() => {
        context.commit('setPerformingAction', false)
        context.commit('toggleServeCitizenSpinner', false)
      })
  },

  clickServiceFinish (context) {
    const { citizen_id } = context.state.serviceModalForm
    const { accurate_time_ind } = context.state.serviceModalForm
    let inaccurate_flag = 'true'
    if (accurate_time_ind === null || accurate_time_ind === 1) {
      inaccurate_flag = 'false'
    }
    context.commit('setPerformingAction', true)
    context.commit('toggleServeCitizenSpinner', true)

    context
      .dispatch('putServiceRequest')
      .then(resp => {
        context
          .dispatch('putCitizen')
          .then(() => {
            context
              .dispatch('postFinishService', {
                citizen_id,
                inaccurate: inaccurate_flag
              })
              .then(() => {
                context.commit('toggleServiceModal', false)
                context.commit('toggleBegunStatus', false)
                context.commit('toggleInvitedStatus', false)
                context.commit('resetServiceModal')
              })
              .finally(() => {
                context.commit('setPerformingAction', false)
              })
          })
          .catch(() => {
            context.commit('setPerformingAction', false)
            context.commit('toggleServeCitizenSpinner', false)
          })
      })
      .catch(() => {
        context.commit('setPerformingAction', false)
        context.commit('toggleServeCitizenSpinner', false)
      })
  },

  finishServiceFromGA (context, citizen_id) {
    context.dispatch('postFinishService', { citizen_id, inaccurate: 'true' })
  },

  clickServiceModalClose (context) {
    context.commit('toggleServiceModal', false)
    context.commit('toggleInvitedStatus', true)
  },

  closeGAScreenModal (context) {
    context.commit('toggleGAScreenModal', false)
  },

  initializeAgenda (context) {
    return new Promise<void>((resolve, reject) => {
      context.dispatch('getExams').then(() => {
        context.dispatch('getBookings').then(() => resolve())
      })
    })
  },

  messageFeedback (context) {
    const messageParts: any = []
    messageParts.push(`Username: ${context.state.user.username}`)
    messageParts.push(`Office: ${context.state.user.office.office_name}`)

    const activeCitizen = context.state.serviceModalForm.service_citizen

    if (activeCitizen) {
      const activeService = activeCitizen.service_reqs.filter(sr =>
        sr.periods.some(p => p.time_end === null)
      )[0]
      const activePeriod = activeService.periods.filter(
        p => p.time_end === null
      )[0]

      messageParts.push(`Ticket Number: ${activeCitizen.ticket_number}`)
      messageParts.push(`Citizen ID: ${activeCitizen.citizen_id}`)
      messageParts.push(`Active SR ID: ${activeService.sr_id}`)
      messageParts.push(`Active Period ID: ${activePeriod.period_id}`)
    } else {
      messageParts.push('Ticket Number: not available')
    }
    messageParts.push('')
    messageParts.push(`Message: ${context.state.feedbackMessage}`)

    const feedbackObject = {
      feedback_message: messageParts.join('\n')
    }

    const url = '/feedback/'
    Axios(context)
      .post(url, feedbackObject)
      .then(() => {
        context.commit('setFeedbackMessage', '')
      })
  },

  postActivateServiceReq (context, sr_id) {
    return new Promise((resolve, reject) => {
      const url = `/service_requests/${sr_id}/activate/`
      Axios(context)
        .post(url)
        .then(
          resp => {
            resolve(resp)
          },
          error => {
            reject(error)
          }
        )
    })
  },

  postAddToQueue (context, citizen_id) {
    return new Promise((resolve, reject) => {
      const url = `/citizens/${citizen_id}/add_to_queue/`
      Axios(context)
        .post(url, {})
        .then(
          resp => {
            resolve(resp)
          },
          error => {
            reject(error)
          }
        )
    })
  },

  postBeginService (context, citizen_id) {
    return new Promise((resolve, reject) => {
      const url = `/citizens/${citizen_id}/begin_service/`
      Axios(context)
        .post(url, {})
        .then(
          resp => {
            resolve(resp)
          },
          error => {
            if (error.response.status === 400) {
              context.commit('setMainAlert', error.response.data.message)
            }
            reject(error)
          }
        )
    })
  },

  postCitizenLeft (context, citizen_id) {
    return new Promise((resolve, reject) => {
      const url = `/citizens/${citizen_id}/citizen_left/`
      Axios(context)
        .post(url)
        .then(
          resp => {
            resolve(resp)
          },
          error => {
            reject(error)
          }
        )
    })
  },

  postFinishService (context, payload) {
    return new Promise((resolve, reject) => {
      const url = `/citizens/${payload.citizen_id}/finish_service/?inaccurate=${payload.inaccurate}`
      Axios(context)
        .post(url)
        .then(
          resp => {
            resolve(resp)
          },
          error => {
            reject(error)
          }
        )
    })
  },

  postHold (context, citizen_id) {
    return new Promise((resolve, reject) => {
      const url = `/citizens/${citizen_id}/place_on_hold/`
      Axios(context)
        .post(url)
        .then(
          resp => {
            resolve(resp)
          },
          error => {
            reject(error)
          }
        )
    })
  },

  postInvite (context, payload) {
    const { counter_id } = context.state.user

    const data = { counter_id }
    if (payload === 'next') {
      return new Promise((resolve, reject) => {
        const url = '/citizens/invite/'
        Axios(context)
          .post(url, data)
          .then(
            resp => {
              resolve(resp)
            },
            error => {
              reject(error)
            }
          )
      })
    } else {
      return new Promise((resolve, reject) => {
        const url = `/citizens/${payload}/invite/`
        Axios(context)
          .post(url, data)
          .then(
            resp => {
              resolve(resp)
            },
            error => {
              if (error.response.status === 400) {
                context.commit('setMainAlert', error.response.data.message)
              }
              reject(error)
            }
          )
      })
    }
  },

  scheduleExam (context, payload) {
    return new Promise<void>((resolve, reject) => {
      context.dispatch('postBooking', payload).then(booking_id => {
        context.dispatch('putExam', booking_id).then(() => {
          resolve()
        })
      })
    })
  },

  putExam (context, payload) {
    let bookingId, examId
    if (typeof payload === 'object' && payload !== null) {
      bookingId = payload.bookingId
      examId = payload.examId
    } else {
      bookingId = payload
      examId = context.state.selectedExam.exam_id
    }
    return new Promise((resolve, reject) => {
      const url = `/exams/${examId}/`
      Axios(context)
        .put(url, { booking_id: bookingId })
        .then(resp => {
          resolve(resp)
        })
        .catch(error => {
          reject(error)
        })
    })
  },

  putExamInfo (context, payload) {
    const id = payload.exam_id.valueOf()
    delete payload.exam_id
    return new Promise<void>((resolve, reject) => {
      const url = `/exams/${id}/`
      Axios(context)
        .put(url, payload)
        .then(() => {
          context.dispatch('getExams').then(() => {
            context.commit('setEditExamSuccess', 3)
            context.dispatch('getUserAttentionForExam')
            resolve()
          })
        })
    })
  },

  postBooking (context, payload) {
    if (!Object.keys(payload).includes('office_id')) {
      payload.office_id = context.state.user.office_id
    }
    return new Promise((resolve, reject) => {
      Axios(context)
        .post('/bookings/', payload)
        .then(resp => {
          resolve(resp.data.booking.booking_id)
        })
        .catch(error => {
          reject(error)
        })
    })
  },

  postBookingStat (context, payload) {
    return Axios(context).post('/bookings/', payload)
  },

  finishBooking (context) {
    context.dispatch('getBookings')
    context.commit('setSelectionIndicator', false)
    context.commit('toggleScheduling', false)
    context.commit('toggleBookingModal', false)
    context.commit('toggleOtherBookingModal', false)
    context.commit('setClickedDate', null)
    context.commit('setSelectedExam', null)
    context.commit('setEditedBooking', null)
    context.commit('toggleEditBookingModal', false)
    context.commit('toggleEditGroupBookingModal', false)
    context.dispatch('getUserAttentionForExam')
  },
  finishAppointment (context) {
    context.commit('setSelectionIndicator', false)
    context.commit('toggleRescheduling', false)
    context.commit('toggleApptRescheduleCancel', true)
    context.commit('toggleApptEditMode', false)
    context.commit('toggleEditApptModal', false)
  },

  postITAChallengerExam (context) {
    // JSOTOTS added data variable
    let data: any
    const responses = Object.assign({}, context.state.capturedExam)
    // JSTOTS TOCHECK removed new from moment. no need to use new with moment
    const date = moment(responses.expiry_date).local().format('YYYY-MM-DD')
    // JSTOTS TOCHECK removed new from moment. no need to use new with moment
    const time = moment(responses.exam_time).local().format('HH:mm:ss')
    const datetime = date + 'T' + time
    // JSTOTS TOCHECK removed new from moment. no need to use new with moment
    const start = moment(datetime).local()
    const end = start.clone().add(4, 'hours')
    const booking: any = {
      start_time: start
        .clone()
        .utc()
        .format('YYYY-MM-DD[T]HH:mm:ssZ'),
      end_time: end
        .clone()
        .utc()
        .format('YYYY-MM-DD[T]HH:mm:ssZ'),
      fees: 'false',
      booking_name: responses.exam_name,
      office_id: context.state.user.office_id
    }
    if (responses.on_or_off === 'on') {
      booking.room_id = responses.offsite_location.id.valueOf()
      delete responses.offsite_location
    }
    if (responses.invigilator) {
      if (responses.invigilator === 'sbc') {
        booking.invigilator_id = null
        booking.sbc_staff_invigilated = true
      } else {
        booking.invigilator_id = responses.invigilator.invigilator_id.valueOf()
      }
      delete responses.invigilator
    }
    const exam_type = context.state.examTypes.find(
      ex => ex.exam_type_name === 'Monthly Session Exam'
    )
    const defaultValues = {
      exam_returned_ind: 0,
      examinee_name: 'Monthly Session',
      exam_type_id: exam_type.exam_type_id,
      office_id: context.state.user.office_id,
      exam_method: 'paper'
    }
    delete responses.exam_time
    delete responses.expiry_date
    if (responses.notes === null) {
      data.notes = ''
    }
    const postData = { ...responses, ...defaultValues }

    return new Promise<void>((resolve, reject) => {
      Axios(context)
        .post('/exams/', postData)
        .then(examResp => {
          const { exam_id } = examResp.data.exam
          context
            .dispatch('postBooking', booking)
            .then(bookingResp => {
              const putObject = {
                examId: exam_id,
                bookingId: bookingResp,
                officeId: responses.office_id
              }
              context
                .dispatch('putExam', putObject)
                .then(() => {
                  resolve()
                })
                .catch(() => {
                  reject()
                })
            })
            .catch(() => {
              reject()
            })
        })
        .catch(() => {
          reject()
        })
    })
  },

  postITAGroupExam (context) {
    // JSOTOTS added data variable
    let data: any
    const responses = Object.assign({}, context.state.capturedExam)
    const booking = makeBookingReqObj(context, responses)
    const defaultValues: any = {
      exam_returned_ind: 0,
      examinee_name: 'group exam'
    }
    delete responses.exam_time
    delete responses.expiry_date
    if (responses.notes === null) {
      data.notes = ''
    }
    const postData = { ...responses, ...defaultValues }

    return new Promise<void>((resolve, reject) => {
      Axios(context)
        .post('/exams/', postData)
        .then(examResp => {
          const { exam_id } = examResp.data.exam
          context
            .dispatch('postBooking', booking)
            .then(bookingResp => {
              const putObject = {
                examId: exam_id,
                bookingId: bookingResp,
                officeId: responses.office_id
              }
              context
                .dispatch('putExam', putObject)
                .then(() => {
                  resolve()
                })
                .catch(() => {
                  reject()
                })
            })
            .catch(() => {
              reject()
            })
        })
        .catch(() => {
          reject()
        })
    })
  },

  postITAIndividualExam (context, isRequestExam) {
    const isRequestExamReq = isRequestExam || false
    const responses = Object.assign({}, context.state.capturedExam)
    console.log('====>  requesting BCMP exam',responses)
    if (responses.on_or_off) {
      if (responses.on_or_off === 'off') {
        responses.offsite_location = '_offsite'
      }
      delete responses.on_or_off
    }
    responses.office_id = responses.office_id
      ? responses.office_id
      : context.state.user.office_id

    const defaultValues = {
      exam_returned_ind: 0,
      number_of_students: 1
    }
    defaultValues.number_of_students =
      responses.ind_or_group === 'group'
        ? responses.number_of_students
        : 1
    // JSTOTS TOCHECK removed new from moment. no need to use new with moment
    const exp = moment(responses.expiry_date)
      .format('YYYY-MM-DD')
      .toString()
    // JSTOTS TOCHECK removed new from moment. no need to use new with moment
    responses.expiry_date = moment(exp)
      .utc()
      .format('YYYY-MM-DD[T]HH:mm:ssZ')
    if (responses.exam_received_date) {
      // JSTOTS TOCHECK removed new from moment. no need to use new with moment
      responses.exam_received_date = moment(responses.exam_received_date)
        .utc()
        .format('YYYY-MM-DD[T]HH:mm:ssZ')
    }
    if (responses.notes === null) {
      responses.notes = ''
    }
    if (context.state.addExamModal.setup === 'other') {
      if (context.state.captureITAExamTabSetup.showRadio === true) {
        delete responses.exam_received_date
      }
    }

    if (context.state.addExamModal.setup === 'pesticide') {
      responses.exam_name = 'Environment'
      responses.is_pesticide = 1
    }

    responses.receipt = responses.receipt_number
    responses.payee_ind = context.state.captureITAExamTabSetup.capturePayee ? 1 : 0
    responses.receipt_sent_ind =
      context.state.captureITAExamTabSetup.payeeSentReceipt ? 1 : 0
    responses.sbc_managed_ind = responses.sbc_managed === 'sbc' ? 1 : 0

    const postData = { ...responses, ...defaultValues }

    if (responses.ind_or_group === 'group') {
      const examType = context.state.examTypes.find(
        type =>
          type.group_exam_ind && !type.ita_ind && !type.pesticide_exam_ind
      )
      postData.exam_type_id = responses.exam_type_id = examType.exam_type_id
      postData.candidates =
        context.state.addExamModule && context.state.addExamModule.candidates
          ? context.state.addExamModule.candidates
          : []
    }

    const booking = makeBookingReqObj(context, responses)

    if ((postData.ind_or_group === 'group') && (postData.is_pesticide === 1)) {
      postData.bookdata = booking
    }

    const apiUrl = isRequestExamReq ? '/exams/bcmp/' : '/exams/'

    return new Promise((resolve, reject) => {
      Axios(context)
        .post(apiUrl, postData)
        .then(examResp => {
          if (
            (responses.ind_or_group === 'group' ||
              responses.sbc_managed === 'non-sbc') &&
            !isRequestExamReq
          ) {
            const { exam_id } = examResp.data.exam
            context
              .dispatch('postBooking', booking)
              .then(bookingResp => {
                const putObject = {
                  examId: exam_id,
                  bookingId: bookingResp,
                  officeId: responses.office_id
                }
                context
                  .dispatch('putExam', putObject)
                  .then(examResp => {
                    if (responses.sbc_managed === 'non-sbc') {
                      if (
                        examResp.data &&
                        examResp.data.exam &&
                        examResp.data.exam.invigilator
                      ) {
                        context
                          .dispatch('emailInvigilator', {
                            invigilator: examResp.data.exam.invigilator,
                            exam: examResp.data.exam
                          })
                          .then(emailResp => {
                            resolve(examResp)
                          })
                          .catch(() => {
                            console.log('EMAIL_FAILED')
                            reject('EMAIL_FAILED')
                          })
                      }
                    } else {
                      resolve(examResp)
                    }
                  })
                  .catch(() => {
                    reject()
                  })
              })
              .catch(() => {
                reject()
              })
          } else {
            resolve(examResp)
          }
        })
        .catch(err => {
          console.log(err)
          reject(err)
        })
    })
  },

  postRequestExam (context) {
    const responses = Object.assign({}, context.state.requestExam)
    console.log(responses)
    const postData = { ...responses }

    return new Promise<void>((resolve, reject) => {
      Axios(context)
        .post('/exams/request', postData)
        .then(examResp => {
          resolve()
        })
        .catch(err => {
          console.log(err)
          reject()
        })
    })
  },

  postServiceReq (context) {
    const { form_data } = context.getters
    const { citizen_id } = form_data.citizen
    const { priority } = form_data.priority
    const service_request = {
      service_id: form_data.service,
      citizen_id: citizen_id,
      quantity: 1,
      channel_id: form_data.channel,
      priority: priority
    }

    return new Promise((resolve, reject) => {
      const url = '/service_requests/'
      Axios(context)
        .post(url, { service_request })
        .then(
          resp => {
            resolve(resp)
          },
          error => {
            reject(error)
          }
        )
    })
  },

  putCitizen (context) {
    const data: any = {}
    let citizen_id
    let priority
    let counter
    let notification_phone
    let notification_email
    let walkin_unique_id

    if (context.state.serviceModalForm.citizen_id) {
      const {
        accurate_time_ind,
        citizen_comments
      } = context.state.serviceModalForm
      counter = context.state.serviceModalForm.counter
      priority = context.state.serviceModalForm.priority
      citizen_id = context.state.serviceModalForm.citizen_id
      const prevCitizen = context.getters.invited_citizen
      notification_phone = context.state.serviceModalForm.notification_phone
      notification_email = context.state.serviceModalForm.notification_email
      walkin_unique_id =  context.state.serviceModalForm.walkin_unique_id

      if (!context.state.showAddModal) {
        if (citizen_comments !== prevCitizen.citizen_comments) {
          data.citizen_comments = citizen_comments
        }
        if (counter !== prevCitizen.counter_id) {
          data.counter_id = counter
        }
        if (priority !== prevCitizen.priority) {
          data.priority = priority
        }
        if (
          accurate_time_ind != null &&
          accurate_time_ind !== prevCitizen.accurate_time_ind
        ) {
          data.accurate_time_ind = accurate_time_ind
        }
        if (notification_phone !== prevCitizen.notification_phone) {
          data.notification_phone = notification_phone
        }
        if (notification_email !== prevCitizen.notification_email) {
          data.notification_email = notification_email
        }
        if (walkin_unique_id !== prevCitizen.walkin_unique_id) {
          data.walkin_unique_id = walkin_unique_id
        }
      }
    } else {
      const { form_data } = context.getters
      citizen_id = form_data.citizen.citizen_id
      data.counter_id = form_data.counter
      data.priority = form_data.priority
      data.citizen_comments = form_data.comments
      data.notification_phone = form_data.notification_phone
      data.notification_email = form_data.notification_email
      data.walkin_unique_id = form_data.walkin_unique_id
    }

    if (Object.keys(data).length === 0) {
      return new Promise((resolve, reject) => {
        resolve(' ')
      })
    }
    return new Promise((resolve, reject) => {
      const url = `/citizens/${citizen_id}/`

      Axios(context)
        .put(url, data)
        .then(
          resp => {
            resolve(resp)
          },
          error => {
            reject(error)
          }
        )
    })
  },

  sentNotificationReminder (context, payload) {
    return new Promise((resolve, reject) => {
      const url = `/citizens/${payload['citizen_id']}/`
      Axios(context)
        .put(url, payload)
        .then(
          resp => {
            resolve(resp)
          },
          error => {
            reject(error)
          }
        )
    })
  },

  putServiceRequest (context) {
    const { activeQuantity } = context.state.serviceModalForm
    const compareService = context.getters.active_service
    const { sr_id } = compareService

    const data: any = {}
    if (activeQuantity != compareService.quantity) {
      data.quantity = activeQuantity
    }

    // Make sure quantity is position
    if (!/^\+?\d+$/.test(activeQuantity)) {
      context.commit(
        'setServeModalAlert',
        'Quantity must be a number and greater than 0'
      )
      return Promise.reject('Quantity must be a number and greater than 0')
    } else {
      context.commit('setServeModalAlert', '')
    }

    const setup = context.state.addModalSetup
    const { form_data } = context.getters
    if (setup === 'add_mode' || setup === 'edit_mode') {
      if (form_data.channel === '') {
        form_data.channel = compareService.channel_id
      }
      if (form_data.channel != compareService.channel_id) {
        data.channel_id = form_data.channel
      }
      if (form_data.service != compareService.service_id) {
        data.service_id = form_data.service
      }
    }
    if (Object.keys(data).length === 0) {
      return new Promise((resolve, reject) => {
        resolve(' ')
      })
    }
    
    return new Promise((resolve, reject) => {
      const url = `/service_requests/${sr_id}/`
      Axios(context)
        .put(url, data)
        .then(
          resp => {
            resolve(resp)
          },
          error => {
            reject(error)
          }
        )
    })
  },

  resetAddCitizenModal (context) {
    context.commit('toggleAddModal', false)
    context.dispatch('toggleModalBack')
    context.commit('resetAddModalForm')
    context.commit('toggleServeCitizenSpinner', false)
  },

  screenAllCitizens (context, route) {
    context.state.citizens.forEach(citizen => {
      const payload = {
        citizen,
        route
      }
      context.dispatch('screenIncomingCitizen', payload)
    })
  },

  screenIncomingCitizen (context, payload) {
    console.log('screenIncomingCitizen start', { payload })
    const { addNextService } = context.state
    const { csr_id } = context.state.user
    const { citizen, route } = payload
    function checkPath () {
      if (route && route.path && route.path === '/queue') {
        return true
      }
      return false
    }
    if (citizen.service_reqs.length > 0) {
      if (citizen.service_reqs[0].periods) {
        const filteredService = citizen.service_reqs.filter(sr =>
          sr.periods.some(p => p.time_end === null)
        )
        if (filteredService.length > 0) {
          const activeService = filteredService[0]
          if (activeService.periods.length > 0) {
            const l = activeService.periods.length - 1
            const activePeriod = activeService.periods[l]
            if (activePeriod.csr_id === csr_id) {
              if (activePeriod.ps.ps_name === 'Invited') {
                context.commit('setServiceModalForm', citizen)
                context.commit('toggleBegunStatus', false)
                context.commit('toggleInvitedStatus', true)
                context.commit('setServeNowAction', true)
                console.log('screenIncomingCitizen is starting flashServeNow')
                context.dispatch('flashServeNow', 'start')

                if (!addNextService && checkPath()) {
                  context.commit('toggleServiceModal', true)
                  context.commit('resetAddModalForm')
                }
              } else if (activePeriod.ps.ps_name === 'Being Served') {
                context.commit('setServiceModalForm', citizen)
                context.commit('toggleBegunStatus', true)
                context.commit('toggleInvitedStatus', false)
                context.commit('setServeNowAction', false)
                context.dispatch('flashServeNow', 'stop')

                if (!addNextService && checkPath()) {
                  context.commit('toggleServiceModal', true)
                  context.commit('resetAddModalForm')
                }
              } else {
                if (checkPath()) {
                  context.commit('resetServiceModal')
                  context.commit('toggleServiceModal', false)
                }
                context.commit('toggleInvitedStatus', false)
                context.commit('toggleBegunStatus', false)
                context.dispatch('flashServeNow', 'stop')
                context.commit('resetAddModalForm')
              }
            }
          }
          // Citizen is completed or left
        } else {
          // Ensure that we only close serve citizen if it's the citizen _we're_ editing that was finished
          let mostRecentActivePeriod = citizen.service_reqs[0].periods[0]
          citizen.service_reqs.forEach(request => {
            request.periods.forEach(period => {
              if (period.time_end > mostRecentActivePeriod.time_end) {
                mostRecentActivePeriod = period
              }
            })
          })

          if (mostRecentActivePeriod.csr_id === csr_id) {
            if (checkPath()) {
              context.commit('resetServiceModal')
              context.commit('toggleServiceModal', false)
            }
            context.commit('toggleInvitedStatus', false)
            context.commit('toggleBegunStatus', false)
            context.dispatch('flashServeNow', 'stop')
          }
        }
      }
    }
    const index = context.state.citizens
      .map(c => c.citizen_id)
      .indexOf(citizen.citizen_id)

    if (index >= 0) {
      context.commit('updateCitizen', { citizen, index })
      context.commit('toggleServeCitizenSpinner', false)
    } else {
      if (citizen.service_reqs && citizen.service_reqs.length > 0) {
        if (
          citizen.service_reqs[0].periods &&
          citizen.service_reqs[0].periods.length > 0
        ) {
          context.commit('addCitizen', citizen)
        }
      }
    }
  },

  setAddModalData (context) {
    const data = {
      citizen: context.getters.invited_citizen,
      active_service: context.getters.active_service
    }
    context.commit('setAddModalData', data)
  },

  toggleModalBack (context) {
    if (context.state.user.office.sb.sb_type === 'nocallonsmartboard') {
      context.commit('switchAddModalMode', 'non_reception')
    } else {
      context.commit('switchAddModalMode', 'reception')
    }
  },

  updateCSRCounterTypeState (context) {
    const csr_id = context.state.user.csr_id
    Axios(context).put(`/csrs/${csr_id}/`, {
      counter_id: context.state.user.counter_id,
      receptionist_ind: context.state.user.receptionist_ind ? 1 : 0
    })
  },

  updateCSRState (context) {
    const csr_id = context.state.user.csr_id
    Axios(context).put(`/csrs/${csr_id}/`, {
      csr_state_id: context.state.user.csr_state_id
    })
  },

  updateCSROffice (context, newOffice) {
    const csr_id = context.state.user.csr_id
    const { office_id } = newOffice;
    return Axios(context).put(`/csrs/${csr_id}/`, { office_id })
    .then(() => {
      console.log('Axios complete. commiting changeCSROffice w/', { newOffice });
      context.commit('changeCSROffice', newOffice)
    })

  },

  restoreSavedModalAction ({ commit }, payload) {
    commit('restoreSavedModal', payload)
  },

  sendWalkinLineReminder (context, payload) {
    return new Promise((resolve, reject) => {
      Axios(context)
        .post(`/send-reminder/line-walkin/`, {'previous_citizen_id':payload.citizen_id})
        .then(
          resp => {
            console.log('send reminder')
            resolve(resp)
          },
          error => {
            reject(error)
          }
        )
      })
  },
}
