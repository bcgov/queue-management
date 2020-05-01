import { AccountModule, AppointmentModule, AuthModule, GeoModule, OfficeModule } from './modules'
// Libraries
import Vuex, { Store } from 'vuex'
import Vue from 'vue'

import VuexPersistence from 'vuex-persist'

// Mutations
// eslint-disable-next-line sort-imports
import { mutateName, mutateResource } from '@/store/mutations'

// State
import { resourceModel, stateModel } from './state'

// Actions
import { setName, setResource } from './actions'

Vue.use(Vuex)

const vuexLocal = new VuexPersistence({
  storage: window.localStorage
})

export const store: Store<any> = new Vuex.Store<any>({
  state: {
    stateModel,
    resourceModel,
    loading: true,
    refreshKey: 0,
    stepperCurrentStep: 1
  },
  getters: {
    loading: (state) => state.loading
  },
  mutations: {
    mutateName,
    mutateResource,
    loadComplete (state) {
      state.loading = false
    },
    updateHeader (state) {
      state.refreshKey++
    },
    stepperCurrentStep (state, step) {
      state.stepperCurrentStep = step
    },
    RESTORE_MUTATION: vuexLocal.RESTORE_MUTATION
  },
  actions: {
    setName,
    setResource
  },
  modules: {
    auth: AuthModule,
    account: AccountModule,
    geo: GeoModule,
    office: OfficeModule,
    appointment: AppointmentModule
  },
  plugins: [vuexLocal.plugin]
})
