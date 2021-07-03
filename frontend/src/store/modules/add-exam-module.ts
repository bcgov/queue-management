
/**
 *
 * Notes
 * JSTOTS - javascript to typescript Conversation
 * Just moved all module from store folder to to modules/* folder
 * No changes in functionality or any variables
 * this is just moving
 * in Future have to extract all functions and export Individually with typs defined
 * and import in index.ts
 *
 */

import { Axios } from './../helpers'
import Vue from 'vue'
import axios from 'axios'
import config from './../../../config'

// question definition mixins
const addExamCounterQ = {
  digit: false,
  key: 'add_exam_counter',
  kind: 'add_exam_counter',
  minLength: 1
}
const dateTimeQ = {
  digit: false,
  key: 'expiry_date',
  kind: 'date',
  minLength: 1,
  text: 'Date and Time'
}
const eventIdQ = {
  digit: true,
  key: 'event_id',
  kind: 'input',
  minLength: 4,
  text: 'Event ID'
}
const examineeEmailQ = {
  digit: false,
  key: 'examinee_email',
  kind: 'input',
  minLength: 0,
  text: 'Candidate\'s Email'
}
const examineeNameQ = {
  digit: false,
  key: 'examinee_name',
  kind: 'input',
  minLength: 2,
  text: 'Candidate\'s Name'
}
const examineePhoneQ = {
  digit: false,
  key: 'examinee_phone',
  kind: 'input',
  minLength: 0,
  text: 'Candidate\'s Phone'
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
  text: 'Exam Method'
}
const examNameQ = {
  digit: false,
  key: 'exam_name',
  kind: 'input',
  minLength: 2,
  maxLength: 50,
  text: 'Exam Name'
}
const examReceivedQ = {
  digit: false,
  key: 'exam_received_date',
  kind: 'exam_received',
  minLength: 1,
  text1: 'Was the Exam Package Receieved Today?',
  text2: 'Date of Receipt of Exam Package'
}
const examTypeQ = {
  digit: false,
  key: 'exam_type_id',
  kind: 'dropdown',
  minLength: 1,
  text: 'Exam Type ID / Colour'
}
const expiryQ = {
  digit: false,
  key: 'expiry_date',
  kind: 'date',
  minLength: 1,
  text: 'Exam Expiry Date'
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
  text: 'Individual or Group Exam?'
}
const notesQ = {
  digit: false,
  key: 'notes',
  kind: 'notes',
  minLength: 0,
  text: 'Additional Notes (optional)'
}
const numberStudentsQ = {
  digit: true,
  key: 'number_of_students',
  kind: 'input',
  minLength: 1,
  text: 'Number of Students'
}
const officeSelectQ = {
  digit: true,
  key: 'office_id',
  kind: 'office',
  minLength: 1,
  text: 'Office'
}
const offsiteQ = {
  digit: false,
  key: 'offsite_location',
  kind: 'locationInput',
  minLength: 2,
  text: 'Location',
  type: 'input'
}
const onOrOffQ = {
  digit: false,
  key: 'on_or_off',
  kind: 'offsiteSelect',
  minLength: 1,
  options: [
    { text: 'Offsite: Exam will be held at an external location', value: 'off' },
    { text: 'Onsite: Exam will be held at SBC Office', value: 'on' }
  ],
  text: 'Exam Location'
}
const payeeEmailQ = {
  digit: false,
  key: 'payee_email',
  kind: 'input',
  minLength: 0,
  text: 'Payee\'s Email'
}
const payeeNameQ = {
  digit: false,
  key: 'payee_name',
  kind: 'input',
  minLength: 0,
  text: 'Payee\'s Name'
}
const payeePhoneQ = {
  digit: false,
  key: 'payee_phone',
  kind: 'input',
  minLength: 0,
  text: 'Payee\'s Phone'
}
const pesticideFeesQ = {
  digit: false,
  key: 'fees',
  kind: 'pesticideFees',
  minLength: 0,
  options: [
    { text: 'Collect at Exam Time', value: 'collect' },
    { text: 'Paid with Liasion', value: 'paid' }
  ],
  text: 'Fees'
}
const pesticideGroupTypesQ = {
  digit: false,
  key: 'group_exam_types',
  kind: 'group_exam_types',
  minLength: 0,
  text: 'Number of Candidates'
}
// pesticide Exam Type defined in step1 getter since requires state.pesticideExamTypes
const sbcManagedQ = {
  digit: false,
  key: 'sbc_managed',
  kind: 'offsiteSelect',
  minLength: 1,
  options: [
    { text: 'Non-SBC (Invigilator) Managed Exam', value: 'non-sbc' },
    { text: 'SBC Managed Exam', value: 'sbc' }
  ],
  text: 'SBC or Invigilator Managed?'
}
const summaryQ = {
  digit: false,
  key: null,
  kind: null,
  minLength: 0,
  text1: null,
  text2: null
}
const timeQ = {
  digit: false,
  key: 'exam_time',
  kind: 'time',
  minLength: 1,
  text: 'Exam Time'
}

export const addExamModule = {
  actions: {
    clearChallengerBooking ({ commit }) {
      commit('clearChallengerBooking')
      commit('clearAddExamModalFromCalendarStatus')
    },
    downloadExam (context, payload) {
      return new Promise((resolve, reject) => {
        const url = `/exams/${payload.exam_id}/download/`
        axios({
          baseURL: config.APP_API_URL,
          url: url,
          withCredentials: true,
          headers: {
            Accept: 'application/pdf',
            Authorization: `Bearer ${context.rootState.bearer}`
          },
          method: 'GET',
          responseType: 'blob' // important
        })
          .then(resp => {
            resolve(resp)
          })
          .catch(error => {
            console.log(error)
            reject(error)
          })
      })
    },
    getAllPesticideExams ({ commit, rootState }) {
      return new Promise<void>((resolve, reject) => {
        const url = '/exams/'

        Axios(rootState.bearer).get(url)
          .then(resp => {
            const pesticideExams = resp.data.exams.filter(exam => exam.is_pesticide)
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
    getPesticideExamTypes ({ commit, rootState }) {
      return new Promise<void>((resolve, reject) => {
        const url = '/exam_types/'

        Axios(rootState.bearer).get(url)
          .then(resp => {
            const pesticideExams = resp.data.exam_types.filter(exam_type => exam_type.pesticide_exam_ind)
            console.log('pesticideExams', pesticideExams)
            commit('setPesticideExamTypes', pesticideExams)
            resolve()
          })
          .catch(error => {
            console.log(error)
            reject(error)
          })
      })
    },
    submitExam (context, payload) {
      console.log(context)
      console.log(payload)
      return new Promise((resolve, reject) => {
        const url = `/exams/${payload.exam.exam_id}/upload/`

        Axios(context.rootState.bearer).get(url)
          .then((resp) => {
            console.log(resp)
            const putUrl = resp.data.url

            const config = {
              headers: {
                'Content-Type': payload.file.type
              },
              transformRequest: (data, headers) => {
                // delete Authorization header for file upload requests (credentials are via a presigned link)
                delete headers.common.Authorization
                return data
              }
            }

            axios.put(putUrl, payload.file, config)
              .then((putResponse) => {
                console.log(putResponse)
                const bcmpUrl = `/exams/${payload.exam.exam_id}/transfer/`

                Axios(context.rootState.bearer).post(bcmpUrl)
                  .then((transferResponse) => {
                    console.log(transferResponse)
                    resolve(transferResponse)
                  })
                  .catch((error) => {
                    console.error(error)
                  })
              })
              .catch((error) => {
                console.error(error)
              })
          })
          .catch((error) => {
            console.error(error)
            reject(error)
          })
      })
    }
  },
  getters: {
    add_modal_steps (state, getters, rootState) {
      if (rootState.addExamModal && rootState.addExamModal.setup) {
        const { capturedExam } = rootState
        switch (rootState.addExamModal.setup) {
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
    addPesticideSteps (state, getters) {
      return [
        ...getters.pesticideStep1,
        ...getters.pesticideStep2,
        ...getters.pesticideStep3,
        ...getters.pesticideStep4
      ]
    },
    pesticideStep1 (state, getters, rootState) {
      const { capturedExam, pesticide_invigilators, pesticide_offsite_invigilators } = rootState
      const pesticideTypeQ = {
        key: 'exam_type_id',
        text: 'Type of Environment Exam',
        kind: 'select',
        options: state.pesticideExamTypes.map(type => ({ text: type.exam_type_name, value: type.exam_type_id })),
        minLength: 1,
        digit: false
      }

      const step1 = { ...state.pesticideStep1 }

      if (capturedExam.ind_or_group === 'individual') {
        if (step1.questions.findIndex(step => step.key === 'pesticide_type') === -1) {
          step1.questions = [...step1.questions, pesticideTypeQ]
        }
      }
      if (capturedExam.sbc_managed === 'sbc') {
        step1.questions = [...step1.questions, officeSelectQ]
        if (capturedExam.ind_or_group === 'group') {
          step1.questions.push(offsiteQ)
        }
      }
      if (capturedExam.sbc_managed === 'non-sbc') {
        const invigilatorQ = {
          key: 'invigilator_id',
          text: 'Invigilator',
          kind: 'select',
          options: pesticide_offsite_invigilators.map(invigilator => ({ text: invigilator.invigilator_name, value: parseInt(invigilator.invigilator_id) })),
          minLength: 1,
          digit: true
        }
        step1.questions = [...step1.questions, offsiteQ, invigilatorQ]
      }
      return [step1]
    },
    pesticideStep2 (state, getters, rootState) {
      const { capturedExam } = rootState
      let step2

      if (capturedExam.ind_or_group === 'individual') {
        const nameQ = { ...examineeNameQ }
        nameQ.minLength = 0
        step2 = { ...state.pesticideStep2_individual }
        step2.questions[0] = nameQ
        if (capturedExam.fees === 'paid') {
          step2.questions[4] = {
            key: 'receipt_number',
            minLength: 0
          }
        }
      }
      if (capturedExam.ind_or_group === 'group') {
        step2 = { ...state.pesticideStep2_group }
      }
      return [step2]
    },
    pesticideStep3 (state, getters, rootState) {
      const { capturedExam } = rootState

      if (capturedExam.ind_or_group === 'individual') {
        if (rootState.captureITAExamTabSetup.capturePayee) {
          return [state.pesticideStep3_payee]
        }
      }
      if (capturedExam.ind_or_group === 'group') {
        return [state.pesticideStep3_group]
      }
      return [state.pesticideStep3]
    },
    pesticideStep4 (state, getters, rootState) {
      const { capturedExam } = rootState

      const step4 = { ...state.pesticideStep4_summary }

      return [step4]
    }
  },
  mutations: {
    clearChallengerBooking (state) {
      Vue.delete(
        state,
        'challengerBooking'
      )
    },
    saveChallengerBooking (state, payload) {
      Object.keys(payload).forEach(key => {
        if (payload[key]) {
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
    setCandidateTableData: (state, payload) => state.candidateTableData = payload,
    toggleShowAllPesticideExams: (state, payload) => state.showAllPesticideExams = payload,
    toggleUploadExamModal: (state, payload) => state.uploadPesticideModalVisible = payload
  },
  state: {
    addChallengerSteps: [
      {
        step: 1,
        title: 'Exam Details',
        questions: [
          examNameQ,
          onOrOffQ,
          { ...eventIdQ, ...{ minLength: 0, digit: false } },
          { ...numberStudentsQ, ...{ minLength: 0, digit: false } }
        ]
      },
      {
        step: 2,
        title: 'Exam Dates',
        questions: [dateTimeQ, timeQ, offsiteQ]
      },
      {
        step: 3,
        title: 'Summary',
        questions: [summaryQ]
      }
    ],
    addGroupSteps: [
      {
        step: 1,
        title: 'Exam Type',
        questions: [examTypeQ]
      },
      {
        step: 2,
        title: 'Basic Info',
        questions: [officeSelectQ, eventIdQ, examNameQ, numberStudentsQ]
      },
      {
        step: 3,
        title: 'Date, Time & Format',
        questions: [dateTimeQ, timeQ, examMethodQ, offsiteQ, notesQ]
      },
      {
        step: 4,
        title: 'Summary',
        questions: [summaryQ]
      }
    ],
    addIndividualSteps: [
      {
        step: 1,
        title: 'Exam Type',
        questions: [examTypeQ]
      },
      {
        step: 2,
        title: 'Exam Info',
        questions: [eventIdQ, examNameQ, examineeNameQ, examMethodQ]
      },
      {
        step: 3,
        title: 'Exam Dates',
        questions: [examReceivedQ, expiryQ, notesQ]
      },
      {
        step: 4,
        title: 'Summary',
        questions: [summaryQ]
      }
    ],
    addOtherSteps: [
      {
        step: 1,
        title: 'Exam Type',
        questions: [examTypeQ]
      },
      {
        step: 2,
        title: 'Exam Info',
        questions: [eventIdQ, examNameQ, examineeNameQ, examMethodQ]
      },
      {
        step: 3,
        title: 'Exam Dates',
        questions: [examReceivedQ, expiryQ, onOrOffQ, notesQ]
      },
      {
        step: 4,
        title: 'Summary',
        questions: [summaryQ]
      }
    ],
    allPesticideExams: null,
    candidates: [],
    candidateTableData: [],
    challengerBooking: {},
    pesticideExamTypes: [],
    invigilators: [],
    pesticideGroupStep3: {
      step: 3,
      title: 'Notes',
      questions: [notesQ]
    },
    pesticideStep1: {
      step: 1,
      title: 'Exam Type',
      questions: [indOrGroupQ, sbcManagedQ]
    },
    pesticideStep2_group: {
      step: 2,
      title: 'Candidates',
      questions: [numberStudentsQ, pesticideGroupTypesQ, addExamCounterQ]
    },
    pesticideStep2_individual: {
      step: 2,
      title: 'Candidate Info',
      questions: [examineeNameQ, examineePhoneQ, examineeEmailQ, pesticideFeesQ]
    },
    pesticideStep3: {
      step: 3,
      title: 'Notes',
      questions: [notesQ]
    },
    pesticideStep3_payee: {
      step: 3,
      title: 'Payee/Notes',
      questions: [payeeNameQ, payeeEmailQ, payeePhoneQ, notesQ]
    },
    pesticideStep3_group: {
      step: 3,
      title: 'Date, Time & Format',
      questions: [dateTimeQ, timeQ, notesQ]
    },
    pesticideStep4_summary: {
      step: 4,
      title: 'Summary',
      questions: [summaryQ]
    },
    showAllPesticideExams: false,
    uploadPesticideModalVisible: false
  }
}
