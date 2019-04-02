import Vue from 'vue/types/vue'

export const examsModule = {
  state: {
    addExamModal: {
      office_number: null,
      setup: 'individual',
      step1MenuOpen: false,
      visible: false,
    },
    bookings: [],
    calendarEvents: [],
    calendarSetup: null,
    capturedExam: {},
    captureITAExamTabSetup: {
      errors: [],
      highestStep: 1,
      notes: false,
      showRadio: true,
      status: 'unknown',
      step: 1,
      stepsValidated: [],
    },
    clickedDate: '',
    editedBooking: null,
    editedBookingOriginal: null,
    editExamFailureCount: 0,
    editExamSuccessCount: 0,
    examAlertMessage: '',
    examDismissCount: 0,
    exams: [],
    inventoryFilters: {
      expiryFilter: 'current',
      groupFilter: 'both',
      office_number: 'default',
      returnedFilter: 'unreturned',
      scheduledFilter: 'both',
    },
    invigilators: [],
    examsTrackingIP: false,
    examTypes: [],
    rescheduling: false,
    roomResources: [],
    rooms: [],
    scheduling: false,
    selectedExam: {},
    selectedOffice: {},
    selectionIndicator: false,
    showBookingModal: false,
    showDeleteExamModal: false,
    showEditBookingModal: false,
    showEditExamModal: false,
    showEditGroupBookingModal: false,
    showExamInventoryModal: false,
    showOtherBookingModal: false,
    showReturnExamModal: false,
    offsiteVisible: true,
    officeFilter: null,
    offices: [],
    showGenFinReportModal: false,
  },
  getters: {
  
  },
  actions: {
  
  },
  mutations: {
    setExams(state, payload) {
      state.exams = []
      state.exams = payload
    },
    setExamTypes(state, payload) {
      state.examTypes = []
      state.examTypes = payload
    },
    setInvigilators(state, payload) {
      state.invigilators = payload
    },
    setGroupExam: (state, payload) => state.groupExam = payload,
    setIndividualExam: (state, payload) => state.individualExam = payload,
    setAddExamModalSetting(state, payload) {
      if (typeof payload === 'boolean') {
        state.addExamModal.visible = payload
        return
      }
      Object.keys(payload).forEach(key => {
        Vue.set(
          state.addExamModal,
          key,
          payload[key]
        )
      })
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
      if (payload.value === null) {
        payload.value = ''
      }
      Vue.set(
        state.capturedExam,
        payload.key,
        payload.value
      )
    },
    resetCaptureForm(state) {
      state.capturedExam = {}
    },
    resetCaptureTab(state) {
      Object.entries({
        step: 1,
        highestStep: 1,
        stepsValidated: [],
        errors: [],
        showRadio: true,
        success: '',
        notes: false
      }).forEach(entry => {
        Vue.set(
          state.captureITAExamTabSetup,
          entry[0],
          entry[1]
        )
      })
    },
    updateCaptureTab(state, payload) {
      let keys = Object.keys(payload)
      keys.forEach(key => {
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
    toggleEditExamModal: (state, payload) => state.showEditExamModal = payload,
    toggleReturnExamModal: (state, payload) => state.showReturnExamModal = payload,
    toggleDeleteExamModal: (state, payload) => state.showDeleteExamModal = payload,
    setSelectedExam(state, payload) {
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
    setCalendarSetup: (state, payload) => state.calendarSetup = payload,
    toggleOtherBookingModal: (state, payload) => state.showOtherBookingModal = payload,
    setEditExamSuccess: (state, payload) => state.editExamSuccessCount = payload,
    setEditExamFailure: (state, payload) => state.editExamFailureCount = payload,
    toggleEditBookingModal: (state, payload) => state.showEditBookingModal = payload,
    setEditedBooking(state, payload) {
      if (typeof payload === 'object' && payload !== null) {
        state.editedBooking = Object.assign({}, payload)
      }
      if (!payload) {
        state.editedBooking = null
        state.editedBookingOriginal = null
      }
    },
    toggleRescheduling: (state, payload) => state.rescheduling = payload,
    setEditedBookingOriginal: (state, payload) => state.editedBookingOriginal = payload,
    setOffices: (state, payload) => state.offices = payload,
    setOfficeFilter: (ste, payload) => state.officeFilter = payload,
    setSelectionIndicator: (state, payload) => state.selectionIndicator = payload,
    setResources: (state, payload) => state.roomResources = payload,
    setEvents: (state, payload) => state.calendarEvents = payload,
    toggleEditGroupBookingModal: (state, payload) => state.showEditGroupBookingModal = payload,
    setInventoryFilters(state, payload) {
      state.inventoryFilters[payload.type] = payload.value
    },
    restoreSavedModal(state, payload) {
      Object.keys(payload.item).forEach(key => {
        Vue.set(
          state[payload.name],
          key,
          payload.item[key]
        )
      })
    },
    toggleOffsiteVisible: (state, payload) => state.offsiteVisible = payload,
    toggleExamsTrackingIP: (state, payload) => state.examsTrackingIP = payload,
    setSelectedOffice(state, payload) {
      state.selectedOffice = payload
    },
    setExamEditSuccessCount(state, payload) {
      state.examEditSuccessCount = payload
    },
    setExamEditFailureCount(state, payload) {
      state.examEditFailCount = payload
    },
  
  }
}