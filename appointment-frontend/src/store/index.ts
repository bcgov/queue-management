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
    resourceModel
  },
  mutations: {
    mutateName,
    mutateResource
  },
  actions: {
    setName,
    setResource
  }
})
