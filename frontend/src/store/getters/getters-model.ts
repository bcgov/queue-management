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

enum UserRole {
  PesticideDesignate = 'pesticide_designate',
  FinanceDesignate = 'finance_designate',
  Ita2Designate = 'ita2_designate',
  OfficeManager = 'office_manager'
}

function isDesignate(state: any, role: UserRole): boolean {
    return Boolean(state.user[role]);
}

export const commonGetters: any = {

  admin_navigation_nonblank (state) {
    if (state.adminNavigation != '') {
      return state.adminNavigation
    } else {
      //  Default navigation is to the GA Edit CSR screen.
      let nav = 'csrga'

      //  Calculate if it needs to be changed.
      if (
        state.user &&
        state.user.role &&
        state.user.role.role_code == 'SUPPORT'
      ) {
        nav = 'csr'
      }
      if (
        state.user &&
        state.user.role &&
        state.user.role.role_code == 'ANALYTICS'
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

  invigilator_dropdown (state) {
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
    return invigilators.filter(i => i.shadow_count == 2)
  },

  shadow_invigilator_options (state) {
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

  shadow_invigilators (state) {
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

  all_invigilator_options (state) {
    const invigilators: any = []
    state.invigilators.forEach(i => {
      invigilators.push({ id: i.invigilator_id, name: i.invigilator_name })
    })
    return invigilators
  },

  invigilator_multi_select (state) {
    const invigilators: any = []
    state.invigilators.forEach(i => {
      invigilators.push({
        value: i.invigilator_id,
        name: i.invigilator_name,
        shadow_count: i.shadow_count,
        contact_phone: i.contact_phone || '',
        contact_email: i.contact_email || '',
        invigilator_notes: i.invigilator_notes || ''
      })
    })
    return invigilators.filter(i => i.shadow_count == 2)
  },

  show_scheduling_indicator: state => {
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

  filtered_calendar_events: (state, getters) => search => {
    return state.calendarEvents.filter(event =>
      searchNestedObject(event, search)
    )
  },

  exam_inventory (state) {
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

  exam_object_id: (state, getters) => examId => {
    return state.examTypes.find(type => type.exam_type_id == examId)
  },

  exam_object (state) {
    if (state.capturedExam && state.capturedExam.exam_type_id) {
      return state.examTypes.find(
        type => type.exam_type_id == state.capturedExam.exam_type_id
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

  add_exam_modal_navigation_buttons (state) {
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

  role_code (state) {
    if (state.user && state.user.role && state.user.role.role_code) {
      return state.user.role.role_code
    }
    return ''
  },

  is_pesticide_designate (state) {
    return isDesignate(state, UserRole.PesticideDesignate)
  },

  is_financial_designate (state) {
    return isDesignate(state, UserRole.FinanceDesignate)
  },

  is_ita2_designate (state) {
    return isDesignate(state, UserRole.Ita2Designate)
  },

  is_office_manager (state) {
    return isDesignate(state, UserRole.OfficeManager)
  },

  is_recurring_enabled (state) {
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

  active_index (state, getters) {
    const { service_citizen } = state.serviceModalForm

    if (
      !service_citizen ||
      !service_citizen.service_reqs ||
      service_citizen.service_reqs.length === 0
    ) {
      return 0
    }
    return service_citizen.service_reqs.findIndex(sr =>
      sr.periods.some(p => p.time_end == null)
    )
  },

  active_service: (state, getters) => {
    const { service_citizen } = state.serviceModalForm
    if (
      !service_citizen ||
      !service_citizen.service_reqs ||
      service_citizen.service_reqs.length === 0
    ) {
      return null
    }
    return service_citizen.service_reqs.filter(sr =>
      sr.periods.some(p => p.time_end == null)
    )[0]
  },

  active_service_id: state => citizen_id => {
    const { citizens } = state
    const citizen = citizens.find(c => c.citizen_id === citizen_id)

    return citizen.service_reqs.find(sr =>
      sr.periods.some(p => p.time_end === null)
    )
  },

  invited_service_reqs: (state, getters) => {
    const { service_citizen } = state.serviceModalForm

    if (
      !service_citizen ||
      !service_citizen.service_reqs ||
      service_citizen.service_reqs.length === 0
    ) {
      return []
    }

    return service_citizen.service_reqs.sort((a, b) => {
      return b.sr_id - a.sr_id
    })
  },

  invited_citizen: state => {
    const { service_citizen } = state.serviceModalForm
    return service_citizen
  },

  on_hold_queue (state) {
    const { citizens } = state
    if (!citizens || citizens.length === 0) {
      return []
    }

    const isCitizenOnHold = function (c) {
      const test = c.service_reqs.filter(sr =>
        sr.periods.some(p => p.time_end == null && p.ps.ps_name === 'On hold')
      )
      if (test.length > 0) {
        return true
      }
      return false
    }
    const filtered = citizens.filter(c => c.service_reqs.length > 0)
    return filtered.filter(isCitizenOnHold)
  },

  citizens_queue (state) {
    const { citizens } = state
    if (!citizens || citizens.length === 0) {
      return []
    }

    const isCitizenQueued = function (c) {
      const test = c.service_reqs.filter(sr =>
        sr.periods.some(p => p.time_end == null && p.ps.ps_name === 'Waiting')
      )
      if (test.length > 0) {
        return true
      }
      return false
    }
    const filtered = citizens.filter(c => c.service_reqs.length > 0)
    return filtered.filter(isCitizenQueued)
  },

  form_data: state => {
    return state.addModalForm
  },

  channel_options: state => {
    return state.channels.map(ch => ({
      value: ch.channel_id,
      text: ch.channel_name
    }))
  },

  categories_options: (state, getters) => {
    let services = state.services
    if (state.displayServices === 'Dashboard') {
      services = getters.services_dashboard
    }
    if (state.displayServices === 'BackOffice') {
      services = getters.services_backoffice
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

  services_dashboard: state => {
    let services = state.services
    services = services.filter(
      service => service.display_dashboard_ind === 1
    )
    return services
  },

  services_backoffice: state => {
    let services = state.services
    services = services.filter(
      service => service.display_dashboard_ind === 0
    )
    return services
  },

  filtered_services: (state, getters) => {
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

    if (getters.form_data.category) {
      return services.filter(
        service => service.parent_id === getters.form_data.category
      )
    } else {
      return services
    }
  },

  receptionist_status (state) {
    if (state.user.receptionist_ind == 1) {
      return true
    } else if (state.user.receptionist_ind == 0) {
      return false
    } else {
      console.error('receptionist status: ', state.user.receptionist_ind)
    }
  }
}

export const mutateResource = (state: any, resource: object) => {
  state.resourceModel = resource
}
