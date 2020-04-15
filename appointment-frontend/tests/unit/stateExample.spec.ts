// Libraries
import Vue from 'vue'
import Vuetify from 'vuetify'
import { store } from '@/store'
import { shallowMount } from '@vue/test-utils'

// Components
import StateExample from '@/views/StateExample.vue'
import { ResourceExample } from '@/components/common'

Vue.use(Vuetify)
let vuetify = new Vuetify({})

describe('HelloWorld.vue', () => {
  let wrapper: any

  beforeEach(() => {
    // create wrapper for Dashboard
    // this stubs out the sub-component
    wrapper = shallowMount(StateExample, { store, vuetify })
  })

  afterEach(() => {
    wrapper.destroy()
  })

  it('renders the sub-components properly', () => {
    expect(wrapper.find(ResourceExample).exists()).toBe(true)
  })

  it('displays the appropriate welcome message', () => {
    expect(wrapper.vm.$el.querySelector('.stateExample').textContent)
      .toContain('Congratulations... it worked!')
  })
})
