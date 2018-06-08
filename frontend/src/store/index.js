/*Copyright 2015 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.*/



import Vue from 'vue'
import 'es6-promise/auto'
import axios from 'axios'
import Vuex from 'vuex'

var axiosInstance = axios.create({
  baseURL: process.env.API_URL,
  withCredentials: true
})

Vue.use(Vuex)

export const store = new Vuex.Store({

  state: {
    isLoggedIn: false,
    items: [],
    user: null,
  },
  actions: {
    getAllClients(context) {
      let url = "/clients/"
      axiosInstance.get(url, { headers: {
        "Accept": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      }})
        .then( response => {
          let list = response.data.map(d=>
            ({name:d.name, id:d.id})
          )
        context.commit('updateList', list)
        })
    },
    postClient(context, payload) {
      let clientObject = {
        name: payload.name
      }
      let url = "/clients/"
      axiosInstance.post(url, clientObject, { headers: {
        "Accept": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      }})
    }
  },
  mutations: {
    logIn: state => state.isLoggedIn = true,

    logOut: state => state.isLoggedIn = false,

    updateList(state, payload) {
      state.items = []
      state.items = payload
      },

    setUser(state, payload) {
      state.user = payload
    }
}
  })
