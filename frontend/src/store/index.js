import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

const axiosInst = axios.create({
    baseURL: process.env.API_URL,
    withCredentials: true
})

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    isLoggedIn: false,
    items: [{name:''}],
    user: ''
  },
  actions: {
    getClients(context) {
      let url = "/clients/"
      axiosInst.get(url)
        .then( response => {
          let names = response.data.map(n => 
            ({name: n.name })
          )
          context.commit('updateList', names)
        })
    },
    postClient(context, payload) {
      let clientObject = {
        name: payload.name
      }
      let url = "/clients/"
      axiosInst.post(url, clientObject)
    }
  },
  mutations: {
    logIn: state => state.isLoggedIn = true,
    logOut: state => state.isLoggedIn = false,
    setUser(state, payload) {
      state.user = payload
    },
    updateList(state, payload) {
      state.items.push({name: payload.client})
    }
  }
})
