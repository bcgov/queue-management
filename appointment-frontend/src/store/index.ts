// Libraries
import Vuex, { Store } from 'vuex'
import Vue from 'vue'

// Mutations
// eslint-disable-next-line sort-imports
import { mutateName, mutateResource } from '@/store/mutations'

// State
import { resourceModel, stateModel } from './state'

// Actions
import { setName, setResource } from './actions'

Vue.use(Vuex)

export const store: Store<any> = new Vuex.Store<any>({
  state: {
    stateModel,
    resourceModel,
    loading: true,
    refreshKey: 0
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
    }
  },
  actions: {
    setName,
    setResource
  }
})
