import Vue from 'vue'
import { Axios } from './helpers'

//question definition mixins
const addExamCounterQ = {
  digit: false,
  key: 'add_exam_counter',
  kind: 'add_exam_counter',
  minLength: 1,
}
const dateTimeQ = {
  digit: false,
  key: 'expiry_date',
  kind: 'date',
  minLength: 1,
  text: 'Date and Time',
}
const eventIdQ = {
  digit: true,
  key: 'event_id',
  kind: 'input',
  minLength: 4,
  text: 'Event ID',
}
const examineeEmailQ = {
  digit: false,
  key: 'examinee_email',
  kind: 'input',
  minLength: 0,
  text: `Candidate's Email`,
}
const examineeNameQ = {
  digit: false,
  key: 'examinee_name',
  kind: 'input',
  minLength: 2,
  text: `Candidate's Name`,
}
const examineePhoneQ = {
  digit: false,
  key: 'examinee_phone',
  kind: 'input',
  minLength: 0,
  text: `Candidate's Phone`,
}
const examMethodQ = {
  digit: false,
  key: 'exam_method',
  kind: 'select',
  minLength: 1,
  options: [
    { text: 'paper', value: 'paper', id: 'exam_method' },
    { text: 'online', value: 'online', id: 'exam_method' }
  ],
  text: 'Exam Method',
}
const examNameQ = {
  digit: false,
  key: 'exam_name',
  kind: 'input',
  minLength: 2,
  text: 'Exam Name',
}
const examReceivedQ = {
  digit: false,
  key: 'exam_received_date',
  kind: 'exam_received',
  minLength: 1,
  text1: 'Was the Exam Package Receieved Today?',
  text2: 'Date of Receipt of Exam Package',
}
const examTypeQ = {
  digit: false,
  key: 'exam_type_id',
  kind: 'dropdown',
  minLength: 1,
  text: 'Exam Type ID / Colour',
}
const expiryQ = {
  digit: false,
  key: 'expiry_date',
  kind: 'date',
  minLength: 1,
  text: 'Exam Expiry Date',
}
const indOrGroupQ = {
  digit: false,
  key: 'ind_or_group',
  kind: 'select',
  minLength: 1,
  options: [
    { text: 'Individual', value: 'individual' },
    { text: 'Group', value: 'group' }
  ],
  text: 'Individual or Group Exam?',
}
const notesQ = {
  digit: false,
  key: 'notes',
  kind: 'notes',
  minLength: 0,
  text: 'Additional Notes (optional)',
}
const numberStudentsQ = {
  digit: true,
  key: 'number_of_students',
  kind: 'input',
  minLength: 1,
  text: 'Number of Students',
}
const officeSelectQ =  {
  digit: true,
  key: 'office_id',
  kind: 'office',
  minLength: 1,
  text: 'Office',
}
const offsiteQ = {
  digit: false,
  key: 'offsite_location',
  kind: 'locationInput',
  minLength: 2,
  text: 'Location',
  type: 'input',
}
const onOrOffQ = {
  digit: false,
  key: 'on_or_off',
  kind: 'offsiteSelect',
  minLength: 1,
  options: [
    { text: 'Offsite: Exam will be held at an external location', value: 'off', },
    { text: 'Onsite: Exam will be held at SBC Office', value: 'on', }
  ],
  text: 'Exam Location',
}
const payeeEmailQ = {
  digit: false,
  key: 'payee_email',
  kind: 'input',
  minLength: 0,
  text: `Payee's Email`,
}
const payeeNameQ = {
  digit: false,
  key: 'payee_name',
  kind: 'input',
  minLength: 0,
  text: `Payee's Name`,
}
const payeePhoneQ = {
  digit: false,
  key: 'payee_phone',
  kind: 'input',
  minLength: 0,
  text: `Payee's Phone`,
}
const pesticideFeesQ = {
  digit: false,
  key: 'fees',
  kind: 'pesticideFees',
  minLength: 0,
  options: [
    { text: 'Collect', value: 'collect' },
    { text: 'Paid', value: 'paid' }
  ],
  text: 'Fees',
}
const pesticideGroupTypesQ = {
  digit: false,
  key: 'group_exam_types',
  kind: 'group_exam_types',
  minLength: 0,
  text: 'Number of Candidates',
}
// pesticide Exam Type defined in step1 getter since requires state.pesticideExamTypes
const sbcManagedQ = {
  digit: false,
  key: 'sbc_managed',
  kind: 'offsiteSelect',
  minLength: 1,
  options: [
    { text: 'Non-SBC (Invigilator) Managed Exam', value: 'non-sbc', },
    { text: 'SBC Managed Exam', value: 'sbc', }
  ],
  text: 'SBC or Invigilator Managed?',
}
const summaryQ = {
  digit: false,
  key: null,
  kind: null,
  minLength: 0,
  text1: null,
  text2: null,
}
const timeQ = {
  digit: false,
  key: 'exam_time',
  kind: 'time',
  minLength: 1,
  text: 'Exam Time',
}

export const addExamModule = {
  actions: {
    clearChallengerBooking({ commit }) {
      commit('clearChallengerBooking')
      commit('clearAddExamModalFromCalendarStatus')
    },
    getAllPesticideExams({ commit, rootState }) {
      return new Promise((resolve, reject) => {
        let url = "/exams/"

        Axios(rootState.bearer).get(url)
          .then(resp => {
            let pesticideExams = resp.data.exams.filter(exam => exam.exam_type.pesticide_exam_ind)
            commit('setAllPesticideExams', pesticideExams)
            commit('toggleShowAllPesticideExams', true)
            resolve()
          })
          .catch(error => {
            console.log(error)
            reject(error)
          })
      })
    },
    getBCMPlusExamStatus({ commit, rootState, dispatch }) {
      //TO-DO
    },
    getBCMPlusID({ commit, dispatch }) {
      Axios.get().then(resp => {

      })
    },
    getPesticideExamTypes({ commit, dispatch }) {
      //TO-DO.  Make this work with the actual end point
      let response = {}
      response.data = [
        { examName: `Industrial Vegetation`, examTypeId: 1, numberOfHours: 3, numberOfMinutes: 0 },
        { examName: `Landscape`, examTypeId: 2, numberOfHours: 3, numberOfMinutes: 0 },
        { examName: `Structural - General`, examTypeId: 3, numberOfHours: 3, numberOfMinutes: 0 },
        { examName: `Dispenser - Commercial`, examTypeId: 4, numberOfHours: 3, numberOfMinutes: 0 },
        { examName: `Dispenser - Domestic`, examTypeId: 5, numberOfHours: 3, numberOfMinutes: 0 },
        { examName: `Agriculture - Greenhouse`, examTypeId: 6, numberOfHours: 3, numberOfMinutes: 0 },
        { examName: `Agriculture - Field Crop & Orchard`, examTypeId: 7, numberOfHours: 3, numberOfMinutes: 0 },
        { examName: `Forestry - General`, examTypeId: 8, numberOfHours: 3, numberOfMinutes: 0 },
        { examName: `Forestry - Seed Orchard`, examTypeId: 9, numberOfHours: 3, numberOfMinutes: 0 },
        { examName: `Forestry - Seedling Nursery`, examTypeId: 10, numberOfHours: 3, numberOfMinutes: 0 },
        { examName: `Forestry - Non-broadcast`, examTypeId: 11, numberOfHours: 3, numberOfMinutes: 0 },
        { examName: `Act and Regulation - Forestry/Mosquito`, examTypeId: 12, numberOfHours: 1, numberOfMinutes: 0 },
        { examName: `Act and Regulation - Landscape/Structural`, examTypeId: 13, numberOfHours: 1, numberOfMinutes: 0 },
        { examName: `Act and Regulation - Industrial VegJNox ous Weed`, examTypeId: 14, numberOfHours: 1 },
        { examName: `Mosquito and Biting Fly`, examTypeId: 15, numberOfHours: 3, numberOfMinutes: 0 },
        { examName: `Mosquito - Aerial - Granular`, examTypeId: 16, numberOfHours: 1, numberOfMinutes: 30 },
        { examName: `Mosquito - Ground Application`, examTypeId: 17, numberOfHours: 1, numberOfMinutes: 30 },
        { examName: `Structural - Wood Preservation`, examTypeId: 18, numberOfHours: 3, numberOfMinutes: 0 },
        { examName: `Fumigation - C02`, examTypeId: 19, numberOfHours: 3, numberOfMinutes: 0 },
        { examName: `Dispenser - C02 - Fumigant`, examTypeId: 20, numberOfHours: 3, numberOfMinutes: 0 },
        { examName: `Aquaculture - Marine, Hydrogen Peroxide`, examTypeId: 21, numberOfHours: 3, numberOfMinutes: 0 },
        { examName: `Fumigation - Ship & Structure`, examTypeId: 22, numberOfHours: 3, numberOfMinutes: 0 },
        { examName: `Fumigation - Container`, examTypeId: 23, numberOfHours: 3, numberOfMinutes: 0 },
        { examName: `Aircraft - Disinsection`, examTypeId: 24, numberOfHours: 2, numberOfMinutes: 0 },
      ]
      commit('setPesticideExamTypes', response.data)
    },
    submitExam() {

    }
  },
  getters: {
    add_modal_steps(state, getters, rootState) {
      if ( rootState.addExamModal && rootState.addExamModal.setup ) {
        let { capturedExam } = rootState
        switch ( rootState.addExamModal.setup ) {
          case 'challenger':
            return state.addChallengerSteps
          case 'group':
            return state.addGroupSteps
          case 'individual':
            return state.addIndividualSteps
          case 'pesticide':
            return getters.addPesticideSteps
          case 'other':
            return state.addOtherSteps
          default:
            return []
        }
      }
    },
    addPesticideSteps(state, getters) {
      return [
        ...getters.pesticideStep1,
        ...getters.pesticideStep2,
        ...getters.pesticideStep3,
        ...[{
          step: 4,
          title: 'Summary',
          questions: [summaryQ]
        }],
      ]
    },
    pesticideStep1(state, getters, rootState) {
      let { capturedExam } = rootState
      let pesticideTypeQ = {
        key: 'pesticide_type',
        text: 'Type of Pesticide Exam',
        kind: 'select',
        options: state.pesticideExamTypes.map(type => ({ text: type.examName, value: type.examTypeId })),
        minLength: 1,
        digit: false,
      }

      let step1 = { ...state.pesticideStep1 }
      if ( capturedExam.sbc_managed === 'sbc' ) {
        step1.questions = [...step1.questions, officeSelectQ]
      }

      if ( capturedExam.ind_or_group === 'individual' ) {
        if ( step1.questions.findIndex(step => step.key === 'pesticide_type') === -1 ) {
          step1.questions = [...step1.questions, pesticideTypeQ]
          return [step1]
        }
      }
      return [step1]
    },
    pesticideStep2(state, getters, rootState) {
      let { capturedExam } = rootState
      let step2

      if ( capturedExam.ind_or_group === 'individual' ) {
        let nameQ = { ...examineeNameQ }
        nameQ.minLength = 0
        step2 = { ...state.pesticideStep2_individual }
        step2.questions[0] = nameQ
        if (capturedExam.fees === 'paid') {
          step2.questions[4] = {
            key: 'receipt_number',
            minLength: 0,
          }
        }
      }
      if ( capturedExam.ind_or_group === 'group' ) {
        step2 = { ...state.pesticideStep2_group }
      }
      return [step2]
    },
    pesticideStep3(state, getters, rootState) {
      if ( rootState.captureITAExamTabSetup.capturePayee ) {
        return [ state.pesticideStep3_payee ]
      }
      return [ state.pesticideStep3 ]
    },
  },
  mutations: {
    clearChallengerBooking(state) {
      Vue.delete(
        state,
        'challengerBooking'
      )
    },
    saveChallengerBooking(state, payload) {
      Object.keys(payload).forEach(key => {
        if ( payload[key] ) {
          Vue.set(
            state.challengerBooking,
            key,
            payload[key]
          )
        }
      })
    },
    setAllPesticideExams: (state, payload) => state.allPesticideExams = payload,
    setPesticideExamTypes: (state, payload) => state.pesticideExamTypes = payload,
    setSelectedExams: (state, payload) => state.candidates = payload,
    toggleShowAllPesticideExams: (state, payload) => state.showAllPesticideExams = payload,
    toggleUploadExamModal: (state, payload) => state.uploadPesticideModalVisible = payload,
  },
  state: {
    addChallengerSteps: [
      {
        step: 1,
        title:'Exam Details',
        questions: [
          examNameQ,
          onOrOffQ,
          {...eventIdQ, ...{minLength: 0, digit: false}},
          {...numberStudentsQ, ...{minLength: 0, digit: false}},
        ]
      },
      {
        step: 2,
        title: 'Exam Dates',
        questions: [ dateTimeQ, timeQ, offsiteQ, ]
      },
      {
        step: 3,
        title:'Summary',
        questions: [ summaryQ ]
      },
    ],
    addGroupSteps: [
      {
        step: 1,
        title:'Exam Type',
        questions: [ examTypeQ ]
      },
      {
        step: 2,
        title: 'Basic Info',
        questions: [ officeSelectQ, eventIdQ, examNameQ, numberStudentsQ, ]
      },
      {
        step: 3,
        title: 'Date, Time & Format',
        questions: [ dateTimeQ, timeQ, examMethodQ, offsiteQ, notesQ ]
      },
      {
        step: 4,
        title:'Summary',
        questions: [ summaryQ ]
      },
    ],
    addIndividualSteps: [
      {
        step: 1,
        title:'Exam Type',
        questions: [ examTypeQ ]
      },
      {
        step: 2,
        title:'Exam Info',
        questions: [ eventIdQ, examNameQ, examineeNameQ, examMethodQ ]
      },
      {
        step: 3,
        title: 'Exam Dates',
        questions: [ examReceivedQ, expiryQ, notesQ ]
      },
      {
        step: 4,
        title:'Summary',
        questions: [ summaryQ ]
      },
    ],
    addOtherSteps: [
      {
        step: 1,
        title:'Exam Type',
        questions: [ examTypeQ ]
      },
      {
        step: 2,
        title:'Exam Info',
        questions: [ eventIdQ, examNameQ, examineeNameQ, examMethodQ ]
      },
      {
        step: 3,
        title: 'Exam Dates',
        questions: [ examReceivedQ, expiryQ, onOrOffQ, notesQ ]
      },
      {
        step: 4,
        title:'Summary',
        questions: [ summaryQ ]
      },
    ],
    allPesticideExams: null,
    candidates: [],
    challengerBooking: {},
    pesticideExamTypes: [],
    pesticideGroupStep3: {
      step: 3,
      title: 'Notes',
      questions: [ notesQ ]
    },
    pesticideStep1: {
      step: 1,
      title:'Exam Type',
      questions: [ indOrGroupQ, sbcManagedQ, ]
    },
    pesticideStep2_group: {
      step: 2,
      title: 'Candidates',
      questions: [ numberStudentsQ, pesticideGroupTypesQ, addExamCounterQ ]
    },
    pesticideStep2_individual: {
      step: 2,
      title: 'Candidate Info',
      questions: [ examineeNameQ, examineePhoneQ, examineeEmailQ, pesticideFeesQ, ]
    },
    pesticideStep3: {
      step: 3,
      title: 'Notes',
      questions: [ offsiteQ, notesQ ]
    },
    pesticideStep3_payee: {
      step: 3,
      title: 'Payee/Notes',
      questions: [ payeeNameQ, payeeEmailQ, payeePhoneQ, offsiteQ, notesQ ]
    },
    showAllPesticideExams: false,
    uploadPesticideModalVisible: false,
  },
}
