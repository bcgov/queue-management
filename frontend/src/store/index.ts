/* Copyright 2015 Province of British Columbia

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License. */

import 'es6-promise/auto'

import Vue from 'vue'
import Vuex from 'vuex'
import { addExamModule } from './modules/add-exam-module'
import appointmentsModule from './modules/appointments-module'
import { commonActions } from './actions'
import { commonGetters } from './getters'
import { commonMutation } from './mutations'
import { stateModel } from './state'

Vue.use(Vuex)

export const store = new Vuex.Store({
  modules: {
    addExamModule,
    appointmentsModule
  },
  state: {
    ...stateModel
  },

  getters: {
    ...commonGetters
  },

  actions: {
    ...commonActions
  },

  mutations: {
    ...commonMutation
  }
})

export default store
