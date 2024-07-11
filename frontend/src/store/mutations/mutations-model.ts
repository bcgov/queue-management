/* eslint-disable */
/**
 *
 * Notes
 * JSTOTS - javascript to typescript Conversation
 * Just moved all mutstion from index.js to mutstion-madel file
 * No changes in functionality or any variables
 * this is just moving
 * in Future have to extract all functions and export Individually with typs defined
 * and import in index.ts
 *
 */

import { StateModelIF } from '@/interfaces'
import Vue from 'vue'
let _default_counter_id = null

export const commonMutation: any = {
  logIn: state => (state.isLoggedIn = true),
  logOut: state => (state.isLoggedIn = false),
  setBearer: (state, payload) => (state.bearer = payload),
  setUser: (state, payload) => (state.user = payload),
  updateQueue (state, payload) {
    state.citizens = []
    state.citizens = payload
  },
  setServices (state, payload) {
    state.services = {}
    state.services = payload
  },
  setChannels (state, payload) {
    state.channels = []
    state.channels = payload
  },
  setCategories (state, payload) {
    state.categories = []
    state.categories = payload
  },

  setReturnExamInfo: (state, payload) => (state.returnExam = payload),

  setManifestData (state, payload) {
    state.manifestdata = payload
  },

  setDiskSpace (state, payload) {
    state.diskspace = {}
    state.diskspace = payload
  },

  setIsUploadingFile (state, payload) {
    state.isUploadingFile = payload
  },

  setVideoFiles (state, payload) {
    state.videofiles = []
    state.videofiles = payload
  },

  toggleAddModal: (state, payload) => (state.showAddModal = payload),

  updateAddModalForm (state, payload) {
    Vue.set(state.addModalForm, payload.type, payload.value)
  },

  setAddModalSelectedItem (state, payload) {
    state.addModalForm.suspendFilter = true
    state.addModalForm.selectedItem = payload
  },

  resetAddModalForm (state) {
    const keys = Object.keys(state.addModalForm)
    keys.forEach(key => {
      switch (key) {
      case 'suspendFilter':
        Vue.set(state.addModalForm, key, false)
        break
      case 'priority':
        Vue.set(state.addModalForm, key, 2)
        break
      case 'counter':
        Vue.set(state.addModalForm, key, _default_counter_id)
        break
      default:
        Vue.set(state.addModalForm, key, '')
      }
    })
  },

  switchAddModalMode (state, payload) {
    state.addModalSetup = payload
  },

  setAddModalData (state, data) {
    const { citizen, active_service } = data

    const formData = {
      comments: citizen.citizen_comments,
      priority: citizen.priority,
      citizen: citizen,
      channel: active_service.channel_id,
      service: active_service.service_id,
      notification_phone: citizen.notification_phone,
      notification_email: citizen.notification_email,
      walkin_unique_id: citizen.walkin_unique_id
    }
    const keys = Object.keys(formData)
    keys.forEach(key => {
      Vue.set(state.addModalForm, key, formData[key])
    })
  },

  toggleServiceModal: (state, payload) => (state.showServiceModal = payload),

  setDisplayServices: (state, payload) => (state.displayServices = payload),

  setBackOfficeDisplay: (state, payload) =>
    (state.backOfficeDisplay = payload),

  setRecurringFeatureFlag: (state, payload) =>
    (state.recurringFeatureFlag = payload),

  toggleBookingBlackoutModal: (state, payload) =>
    (state.showBookingBlackoutModal = payload),

  toggleEditDeleteSeries: (state, payload) =>
    (state.editDeleteSeries = payload),

  setServiceModalForm (state, citizen) {
    const citizen_comments = citizen.citizen_comments
    const activeService = citizen.service_reqs.filter(sr =>
      sr.periods.some(p => p.time_end === null)
    )
    const activeQuantity = activeService[0].quantity
    const { citizen_id } = citizen
    const service_citizen = citizen
    const priority = citizen.priority
    const counter = citizen.counter_id

    const obj = {
      citizen_comments,
      activeQuantity,
      citizen_id,
      service_citizen,
      priority,
      counter
    }
    const keys = Object.keys(obj)

    keys.forEach(key => {
      Vue.set(state.serviceModalForm, key, obj[key])
    })
  },

  resetServiceModal (state) {
    const { serviceModalForm } = state
    const keys = Object.keys(serviceModalForm)
    Vue.set(state, 'serveModalAlert', '')

    keys.forEach(key => {
      if (key === 'activeQuantity') {
        Vue.set(state.serviceModalForm, key, 1)
      } else {
        Vue.set(state.serviceModalForm, key, null)
      }
    })
  },

  editServiceModalForm (state, payload) {
    Vue.set(state.serviceModalForm, payload.type, payload.value)
  },

  setDefaultChannel (state) {
    const channel = state.channels.filter(
      ch => ch.channel_name === 'In Person'
    )
    state.addModalForm.channel = channel[0].channel_id
  },

  setMainAlert (state, payload) {
    state.alertMessage = payload
    state.dismissCount = 5
  },

  setSelectedOffice (state, payload) {
    state.selectedOffice = payload
  },

  setExamAlert (state, payload) {
    state.examAlertMessage = payload
    if (payload) {
      state.examDismissCount = 999
    } else {
      state.examDismissCount = 0
    }
  },

  setLoginAlert (state, payload) {
    state.loginAlertMessage = payload
    state.loginDismissCount = 999
  },

  setExamEditSuccessCount (state, payload) {
    state.examEditSuccessCount = payload
  },

  setExamEditFailureCount (state, payload) {
    state.examEditFailCount = payload
  },

  setModalAlert (state, payload) {
    state.alertMessage = payload
  },

  setServeModalAlert (state, payload) {
    state.serveModalAlert = payload
  },

  setCsrs (state, payload) {
    state.csrs = []
    state.csrs = payload
  },

  setExams (state, payload) {
    state.exams = []
    state.exams = payload
  },

  setEventWarning (state, payload) {
    state.event_id_warning = payload
  },

  setExamEventIDs (state, payload) {
    state.event_ids = payload
  },

  setExamTypes (state, payload) {
    state.examTypes = []
    state.examTypes = payload
  },

  setInvigilators (state, payload) {
    state.invigilators = payload
  },

  setPesticideInvigilators (state, payload) {
    state.pesticide_invigilators = payload
  },

  setPesticideOffsiteInvigilators (state, payload) {
    state.pesticide_offsite_invigilators = payload
  },

  updateCitizen (state, payload) {
    Vue.set(state.citizens, payload.index, payload.citizen)
  },

  addCitizen (state, citizen) {
    state.citizens.push(citizen)
  },

  dismissCountDown (state, payload) {
    state.dismissCount = payload
  },

  examDismissCountDown (state, payload) {
    state.examDismissCount = payload
  },

  loginDismissCountDown (state, payload) {
    state.loginDismissCount = payload
  },

  examSuccessCountDown (state, payload) {
    state.examSuccessDismiss = payload
  },

  toggleInvitedStatus: (state, payload) => (state.citizenInvited = payload),

  toggleBegunStatus: (state, payload) => (state.serviceBegun = payload),

  toggleGAScreenModal: (state, payload) =>
    (state.showGAScreenModal = payload),

  toggleAgendaScreenModal: (state, payload) =>
    (state.showAgendaScreenModal = payload),

  setReceptionistState: (state, payload) => {
    state.user.receptionist_ind = payload
  },

  setCounterStatusState: (state, payload) => {
    state.user.counter_id = payload
  },

  setCSRState: (state, payload) => (state.user.csr_state_id = payload),

  setUserCSRStateName: (state, payload) =>
    (state.user.csr_state.csr_state_name = payload),

  setQuickList: (state, payload) => (state.user.office.quick_list = payload),

  setBackOfficeList: (state, payload) =>
    (state.user.office.back_office_list = payload),

  // Note: This method is for changing office TYPE, not office itself.
  // I'm leaving it in as-is as it was written this way.  I've
  // created a new mutation for changing offices themselves below.
  setOffice: (state, officeType) => (state.officeType = officeType),

  /**
   * Change the office a CSR is currently assigned to.
   */
  changeCSROffice: (state: StateModelIF, payload) => (state.user.office = payload),

  setDefaultCounter: (state, defaultCounter) => {
    state.addModalForm.counter = defaultCounter.counter_id
    state.serviceModalForm.counter = defaultCounter.counter_id
    _default_counter_id = defaultCounter.counter_id
  },

  flashServeNow: (state, payload) => (state.serveNowStyle = payload),

  setServeNowAction: (state, payload) => (state.serveNowAltAction = payload),

  toggleFeedbackModal: (state, payload) =>
    (state.showFeedbackModal = payload),

  toggleAddNextService: (state, payload) => (state.addNextService = payload),

  toggleShowAdmin: state => (state.showAdmin = !state.showAdmin),

  setFeedbackMessage: (state, payload) => (state.feedbackMessage = payload),

  setPerformingAction: (state, payload) => (state.performingAction = payload),

  setUserLoadingFail: (state, payload) => (state.userLoadingFail = payload),

  setGroupExam: (state, payload) => (state.groupExam = payload),

  setGroupIndividualExam: (state, payload) =>
    (state.groupIndividualExam = payload),

  setIndividualExam: (state, payload) => (state.individualExam = payload),

  showHideResponseModal (state) {
    state.showResponseModal = true
    setTimeout(() => {
      state.showResponseModal = false
    }, 3000)
  },

  hideResponseModal (state) {
    state.showResponseModal = false
  },

  setiframeLogedIn: (state, value) => (state.iframeLogedIn = value),

  setNavigation: (state, value) => (state.adminNavigation = value),

  setAddExamModalSetting (state, payload) {
    if (typeof payload === 'boolean') {
      state.addExamModal.visible = payload
      return
    }
    Object.keys(payload).forEach(key => {
      Vue.set(state.addExamModal, key, payload[key])
    })
  },

  resetAddExamModal: state => {
    state.addExamModal = {
      visible: false,
      setup: null,
      step1MenuOpen: false,
      office_number: null
    }
    state.addExamModule.candidates = []
  },

  resetLogAnotherExamModal: (state, setup) => {
    state.addExamModal = {
      visible: true,
      setup: setup,
      step1MenuOpen: true,
      office_number: null
    }
  },

  toggleGenFinReport (state, payload) {
    state.showGenFinReportModal = payload
  },

  captureExamDetail (state, payload) {
    if (payload.key === 'exam_type_id') {
      payload.value = Number(payload.value)
    }
    if (payload.key === 'event_id') {
      payload.value = payload.value.toString()
    }
    if (payload.value === null) {
      payload.value = ''
    }
    Vue.set(state.capturedExam, payload.key, payload.value)
  },

  resetCaptureForm (state) {
    state.capturedExam = {}
    state.addExamModule.candidates = []
    state.captureITAExamTabSetup.capturePayee = false
    state.captureITAExamTabSetup.payeeSentReceipt = false
    state.examBcmpJobId = null
  },

  resetCaptureTab (state) {
    Object.entries({
      step: 1,
      highestStep: 1,
      stepsValidated: [],
      errors: [],
      showRadio: true,
      success: '',
      notes: false
    }).forEach(entry => {
      Vue.set(state.captureITAExamTabSetup, entry[0], entry[1])
    })
  },

  updateCaptureTab (state, payload) {
    const keys = Object.keys(payload)
    keys.forEach(key => {
      Vue.set(state.captureITAExamTabSetup, key, payload[key])
    })
  },

  toggleIndividualCaptureTabRadio (state, payload) {
    Vue.set(state.captureITAExamTabSetup, 'showRadio', payload)
  },

  setBookings (state, payload) {
    state.bookings = payload
  },

  setRooms (state, payload) {
    state.rooms = payload
  },

  toggleBookingModal: (state, payload) => (state.showBookingModal = payload),

  setClickedDate: (state, payload) => (state.clickedDate = payload),

  toggleExamInventoryModal: (state, payload) =>
    (state.showExamInventoryModal = payload),

  toggleEditExamModal: (state, payload) =>
    (state.showEditExamModal = payload),

  toggleSelectInvigilatorModal: (state, payload) =>
    (state.showSelectInvigilatorModal = payload),

  toggleReturnExamModal: (state, payload) =>
    (state.showReturnExamModal = payload),

  toggleDeleteExamModalVisible: (state, payload) =>
    (state.showDeleteExamModal = payload),

  setSelectedExam (state, payload) {
    if (payload === 'clearGoto') {
      delete state.selectedExam.gotoDate
      return
    }
    state.selectedExam = payload
  },

  toggleScheduling: (state, payload) => {
    if (!payload) {
      state.scheduling = payload
      state.rescheduling = payload
      return
    }
    state.scheduling = payload
  },

  setCalendarSetup: (state, payload) => (state.calendarSetup = payload),

  toggleOtherBookingModal: (state, payload) =>
    (state.showOtherBookingModal = payload),

  setEditExamSuccess: (state, payload) =>
    (state.editExamSuccessCount = payload),

  setEditExamFailure: (state, payload) =>
    (state.editExamFailureCount = payload),

  toggleEditBookingModal: (state, payload) =>
    (state.showEditBookingModal = payload),

  toggleEditApptModal: (state, payload) =>
    (state.showEditBookingModal = payload),

  toggleApptEditMode: (state, payload) =>
    (state.isAppointmentEditMode = payload),

  setEditedBooking (state, payload) {
    if (typeof payload === 'object' && payload !== null) {
      state.editedBooking = Object.assign({}, payload)
    }
    if (!payload) {
      state.editedBooking = null
      state.editedBookingOriginal = null
    }
  },

  toggleRescheduling: (state, payload) => (state.rescheduling = payload),

  toggleApptRescheduleCancel: (state, payload) =>
    (state.apptRescheduleCancel = payload),

  setEditedBookingOriginal: (state, payload) =>
    (state.editedBookingOriginal = payload),

  setOffices: (state, payload) => (state.offices = payload),

  setOfficeFilter: (state, payload) => (state.officeFilter = payload),

  setSelectionIndicator: (state, payload) =>
    (state.selectionIndicator = payload),

  setResources: (state, payload) => (state.roomResources = payload),

  setEvents: (state, payload) => (state.calendarEvents = payload),

  setInventoryEditedBooking (state, booking) {
    const bookingCopy = Object.assign({}, booking)
    state.editedBooking = bookingCopy
  },

  toggleEditGroupBookingModal: (state, payload) =>
    (state.showEditGroupBookingModal = payload),

  setInventoryFilters (state, payload) {
    state.inventoryFilters[payload.type] = payload.value
  },

  setSelectedExamType: (state, payload) => (state.selectedExamType = payload),

  setSelectedExamTypeFilter: (state, payload) =>
    (state.selectedExamTypeFilter = payload),

  setSelectedQuickAction: (state, payload) =>
    (state.selectedQuickAction = payload),

  setSelectedQuickActionFilter: (state, payload) =>
    (state.selectedQuickActionFilter = payload),

  restoreSavedModal (state, payload) {
    Object.keys(payload.item).forEach(key => {
      Vue.set(state[payload.name], key, payload.item[key])
    })
  },

  toggleOffsiteVisible: (state, payload) => (state.offsiteVisible = payload),

  toggleExamsTrackingIP: (state, payload) =>
    (state.examsTrackingIP = payload),

  setAppointmentsStateInfo: (state, payload) =>
    (state.appointmentsStateInfo = payload),

  clearAddExamModalFromCalendarStatus: state =>
    Vue.delete(state.addExamModal, 'fromCalendar'),

  toggleServeCitizenSpinner (state, payload) {
    state.showServeCitizenSpinner = payload
  },
  toggleInviteCitizenSpinner (state, payload) {
    state.showInviteCitizenSpinner = payload
  },

  setOffsiteOnly: (state, payload) => (state.offsiteOnly = payload),
  
  setOfficeSwitcher: (state: StateModelIF, payload: boolean) => (state.showOfficeSwitcher = payload),

  toggleTimeTrackingIcon: (state, payload) =>
    (state.showTimeTrackingIcon = payload),

  deleteCapturedExamKey (state, payload) {
    Vue.delete(state.capturedExam, payload)
  },

  setBCMPJobId: (state, payload) => {
    state.capturedExam.bcmp_job_id = payload
    state.examBcmpJobId = payload
  },
}
