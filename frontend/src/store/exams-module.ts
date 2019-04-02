mport { Axios } from './helpers'
import { Module, VuexModule, Mutation, Action } from 'vuex-module-decorators'

@Module
export default class examsModule extends VuexModule {
    exams = []
    @Mutation
    setExams(p: any) {
        this.exams = p
    }
    @Action
    async getExams({commit, state}) {
        let p = await Axios({state}).get('/exams/')
        commit('setExams', p)
    }

    showReturnExamModal = false
    @Mutation
    toggleReturnExamModal(p: boolean) {
        this.showReturnExamModal = p
    }

    bookings = []
    @Mutation
    setBookings(p: any) {
        this.bookings = p
    }
    @Action
    async getBookings({commit, state}) {
        let p = await Axios({state}).get('/bookings/')
        commit('setBookings', p)
    }

    editExamSuccessCount = 0
    @Mutation
    setEditExamSuccessCount(p: number) {
        this.editExamSuccessCount = p
    }

    editExamFailureCount = 0
    @Mutation
    setEditExamFailureCount(p: number) {
        this.editExamFailureCount = p
    }

    showEditGroupBookingModal = false
    @Mutation
    toggleEditGroupBookingModal(p: boolean) {
        this.showEditGroupBookingModal = p
    }

    inventoryFilters = {
        returnedFilter: 'unreturned',
        groupFilter: 'both',
        officeFilter: 'default',
        bookedFilter: 'unbooked',
    }
    @Mutation
    setInventoryFilters(p: any) {
        this.inventoryFilters[p.key] = p.value
    }
    showEditExamModal = false
    @Mutation
    toggleEditExamModal(p: boolean) {


        this.showEditExamModal = p

        this.showReturnExamModal = p

        this.showDeleteExamModal = p
        this.editExamSuccessCount = p
        this.editExamFailureCount = p
        this.showEditGroupBookingModal = p
        this.inventoryFilters = p

}


export const examsModule {
    namespaced: true,
        state: {
        showExamInventoryModal,
            showEditExamModal,
            showReturnExamModal
        showDeleteExamModal
        editExamSuccessCount
        editExamFailureCount
        showEditGroupBookingModal
        inventoryFilters
    },
    getters: {

    },
    actions: {
        deleteExam(context, id) {
            return new Promise((resolve, reject) => {
                Axios(context).delete(`/exams/${id}/`).then(resp => {
                    resolve(resp.data)
                })
                    .catch(error => {
                        reject(error)
                    })
            })
        },
    },
    mutations: {
        setEditExamFailure: (state, payload) => state.editExamFailureCount = payload,

            setEditExamFailure: (state, payload) => state.editExamFailureCount = payload,

            setEditExamSuccess: (state, payload) => state.editExamSuccessCount = payload,

            setEditExamSuccess: (state, payload) => state.editExamSuccessCount = payload,

            setInventoryFilters(state, payload)
        state.inventoryFilters[payload.type] = payload.value
    },

    toggleDeleteExamModal: (state, payload) => state.showDeleteExamModal = payload,

        toggleDeleteExamModal: (state, payload) => state.showDeleteExamModal = payload,

        toggleEditBookingModal: (state, payload) => state.showEditBookingModal = payload,

        toggleEditExamModal: (state, payload) => state.showEditExamModal = payload,

        toggleEditExamModal: (state, payload) => state.showEditExamModal = payload,

        toggleEditGroupBookingModal: (state, payload) => state.showEditGroupBookingModal = payload,

        toggleExamInventoryModal: (state, payload) => state.showExamInventoryModal = payload,

        toggleReturnExamModal: (state, payload) => state.showReturnExamModal = payload,

        toggleReturnExamModal: (state, payload) => state.showReturnExamModal = payload,

},                                                                                           },
}
