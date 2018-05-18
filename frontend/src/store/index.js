import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    isLoggedIn: false
  },
  mutations: {
  	increment: state => state.count++,
    decrement: state => state.count--,
    logIn: state => state.isLoggedIn = true
  }
})
