/* eslint-disable */
/**
 *
 * Notes
 * JSTOTS - javascript to typescript Conversation
 * Just moved all getter from index.js to getter-madel file
 * No changes in functionality or any variables
 * this is just moving
 * in Future have to extract all functions and export Individually with typs defined
 * and import in index.ts
 *
 */

import { searchNestedObject } from '../helpers'

export const commonGetters: any = {

  adminNavigationNonblank (state) {
    if (state.adminNavigation !== '') {
      return state.adminNavigation
    } else {
      //  Default navigation is to the GA Edit CSR screen.
      let nav = 'csrga'

      //  Calculate if it needs to be changed.
      if (
        state.user &&
        state.user.role &&
        state.user.role.role_code === 'SUPPORT'
      ) {
        nav = 'csr'
      }
      if (
        state.user &&
        state.user.role &&
        state.user.role.role_code === 'ANALYTICS'
      ) {
        nav = 'service'
      }

      //  Return the right option
      return nav
    }
  },

  commentsTooLong (state) {
    return state.addModalForm.comments.length > 1000
  },

  invigilatorDropdown (state) {
    const invigilators = [
      { value: null, text: 'unassigned', shadow_count: 2 },
      { value: 'sbc', text: 'SBC Staff', shadow_count: 2 }
    ]
    state.invigilators.forEach(i => {
      invigilators.push({
        value: i.invigilator_id,
        text: i.invigilator_name,
        shadow_count: i.shadow_count
      })
    })
    return invigilators.filter(i => i.shadow_count === 2)
  },

  shadowInvigilatorOptions (state) {
    const invigilators: any = []
    state.invigilators.forEach(i => {
      invigilators.push({
        id: i.invigilator_id,
        name: i.invigilator_name,
        shadow_count: i.shadow_count
      })
    })
    return invigilators.filter(i => i.shadow_count < 2)
  },

  shadowInvigilators (state) {
    const invigilators: any = []
    state.invigilators.forEach(i => {
      invigilators.push({
        id: i.invigilator_id,
        name: i.invigilator_name,
        shadow_count: i.shadow_count
      })
    })
    return invigilators
  },

  allInvigilatorOptions (state) {
    const invigilators: any = []
    state.invigilators.forEach(i => {
      invigilators.push({ id: i.invigilator_id, name: i.invigilator_name })
    })
    return invigilators
  },

  invigilatorMultiSelect (state) {
    const invigilators: any = []
    state.invigilators.forEach(i => {
      invigilators.push({
        value: i.invigilator_id,
        name: i.invigilator_name,
        shadow_count: i.shadow_count
      })
    })
    return invigilators.filter(i => i.shadow_count === 2)
  },

  showSchedulingIndicator: state => {
    if (state.scheduling || state.rescheduling) {
      if (
        !state.showOtherBookingModal &&
        !state.showBookingModal &&
        !state.showEditBookingModal &&
        !state.showEditApptModal
      ) {
        return true
      }
    }
    return false
  },

  filteredCalendarEvents: (state, getters) => search => {
    return state.calendarEvents.filter(event =>
      searchNestedObject(event, search)
    )
  },

  examInventory (state) {
    if (state.showExamInventoryModal) {
      return state.exams.filter(exam => exam.booking_id === null)
    }
    if (state.addExamModule.showAllPesticideExams) {
      if (Array.isArray(state.addExamModule.allPesticideExams)) {
        return state.addExamModule.allPesticideExams
      }
      return []
    }
    return state.exams
  },

  examObjectId: (state, getters) => examId => {
    return state.examTypes.find(type => type.exam_type_id === examId)
  },

  examObject (state) {
    if (state.capturedExam && state.capturedExam.exam_type_id) {
      return state.examTypes.find(
        type => type.exam_type_id === state.capturedExam.exam_type_id
      )
    }
    return {
      exam_color: '',
      exam_type_name: '',
      exam_type_id: ''
    }
  },

  showExams (state) {
    if (state.user && state.user.office.exams_enabled_ind === 1) {
      return true
    }
    return false
  },

  showAppointments (state) {
    if (state.user && state.user.office.appointments_enabled_ind === 1) {
      return true
    }
    return false
  },

  addExamModalNavigationButtons (state) {
    // controls disabled/enabled state of and current classes applied to the 'next' button in AddExamFormModal
    const setup = state.captureITAExamTabSetup
    if (setup.stepsValidated.indexOf(setup.step) === -1) {
      return {
        nextClass: 'btn-secondary disabled',
        nextDisabled: true
      }
    }
    return {
      nextClass: 'btn-primary',
      nextDisabled: false
    }
  },

  roleCode (state) {
    if (state.user && state.user.role && state.user.role.role_code) {
      return state.user.role.role_code
    }
    return ''
  },

  isPesticideDesignate (state) {
    if (state.user.pesticide_designate) {
      return true
    }
    return false
  },

  isFinancialDesignate (state) {
    if (state.user.finance_designate) {
      return true
    }
    return false
  },

  isIta2Designate (state) {
    if (state.user.ita2_designate) {
      return true
    }
    return false
  },

  isOfficeManager (state) {
    if (state.user.office_manager) {
      return true
    }
    return false
  },

  isRecurringEnabled (state) {
    if (state.recurringFeatureFlag === 'On') {
      return true
    }
    return false
  },

  reception (state) {
    if (state.user.office && state.user.office.sb) {
      if (
        state.user.office.sb.sb_type === 'callbyname' ||
        state.user.office.sb.sb_type === 'callbyticket'
      ) {
        return true
      }
      return false
    }
  },

  activeIndex (state, getters) {
    const { serviceCitizen } = state.serviceModalForm

    if (
      !serviceCitizen ||
      !serviceCitizen.service_reqs ||
      serviceCitizen.service_reqs.length === 0
    ) {
      return 0
    }
    return serviceCitizen.service_reqs.findIndex(sr =>
      sr.periods.some(p => p.time_end === null)
    )
  },

  activeService: (state, getters) => {
    const { serviceCitizen } = state.serviceModalForm
    if (
      !serviceCitizen ||
      !serviceCitizen.service_reqs ||
      serviceCitizen.service_reqs.length === 0
    ) {
      return null
    }
    return serviceCitizen.service_reqs.filter(sr =>
      sr.periods.some(p => p.time_end === null)
    )[0]
  },

  activeServiceId: state => citizen_id => {
    const { citizens } = state
    const citizen = citizens.find(c => c.citizen_id === citizen_id)

    return citizen.service_reqs.find(sr =>
      sr.periods.some(p => p.time_end === null)
    )
  },

  invitedServiceReqs: (state, getters) => {
    const { serviceCitizen } = state.serviceModalForm

    if (
      !serviceCitizen ||
      !serviceCitizen.service_reqs ||
      serviceCitizen.service_reqs.length === 0
    ) {
      return []
    }

    return serviceCitizen.service_reqs.sort((a, b) => {
      return b.sr_id - a.sr_id
    })
  },

  invitedCitizen: state => {
    const { serviceCitizen } = state.serviceModalForm
    return serviceCitizen
  },

  onHoldQueue (state) {
    const { citizens } = state
    if (!citizens || citizens.length === 0) {
      return []
    }

    const isCitizenOnHold = function (c) {
      const test = c.service_reqs.filter(sr =>
        sr.periods.some(p => p.time_end === null && p.ps.ps_name === 'On hold')
      )
      if (test.length > 0) {
        return true
      }
      return false
    }
    const filtered = citizens.filter(c => c.service_reqs.length > 0)
    const list = filtered.filter(isCitizenOnHold)
    return list
  },

  citizensQueue (state) {
    const { citizens } = state
    if (!citizens || citizens.length === 0) {
      return []
    }

    const isCitizenQueued = function (c) {
      const test = c.service_reqs.filter(sr =>
        sr.periods.some(p => p.time_end === null && p.ps.ps_name === 'Waiting')
      )
      if (test.length > 0) {
        return true
      }
      return false
    }
    const filtered = citizens.filter(c => c.service_reqs.length > 0)
    const list = filtered.filter(isCitizenQueued)
    return list
  },

  formData: state => {
    return state.addModalForm
  },

  channelOptions: state => {
    return state.channels.map(ch => ({
      value: ch.channel_id,
      text: ch.channel_name
    }))
  },

  categoriesOptions: (state, getters) => {
    let services = state.services
    if (state.displayServices === 'Dashboard') {
      services = getters.servicesDashboard
    }
    if (state.displayServices === 'BackOffice') {
      services = getters.servicesBackoffice
    }
    const opts = state.categories.filter(o =>
      services.some(s => s.parent_id === o.service_id)
    )

    const mappedOpts = opts.map(opt => ({
      value: opt.service_id,
      text: opt.service_name
    }))
    const blankOpt = [{ value: '', text: 'Categories' }]
    return blankOpt.concat(mappedOpts)
  },

  servicesDashboard: state => {
    let services = state.services
    services = services.filter(
      service => service.display_dashboard_ind === 1
    )
    return services
  },

  servicesBackoffice: state => {
    let services = state.services
    services = services.filter(
      service => service.display_dashboard_ind === 0
    )
    return services
  },

  filteredServices: (state, getters) => {
    let services = state.services
    if (state.displayServices === 'Dashboard') {
      services = services.filter(
        service => service.display_dashboard_ind === 1
      )
    }
    if (state.displayServices === 'BackOffice') {
      services = services.filter(
        service => service.display_dashboard_ind === 0
      )
    }

    if (getters.formData.category) {
      return services.filter(
        service => service.parent_id === getters.formData.category
      )
    } else {
      return services
    }
  },

  receptionistStatus (state) {
    if (state.user.receptionist_ind === 1) {
      return true
    } else if (state.user.receptionist_ind === 0) {
      return false
    } else {
      console.error('receptionist status: ', state.user.receptionist_ind)
    }
  }
}

export const mutateResource = (state: any, resource: object) => {
  state.resourceModel = resource
}
