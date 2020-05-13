<template>
  <v-card>
    <div class="stateExample">
      <h1>This is an about page that contains an example for state</h1>
      <p>{{ stateModel.stateText }}</p>
    </div>

    <!-- Resourced Component example #1 -->
    <ResourceExample
      :name="getName(1)"
      :message="getMessage(1)"
    />

    <!-- Resourced Component example #2-->
    <ResourceExample
      :name="getName(2)"
      :message="getMessage(2)"
    />
  </v-card>
</template>
<script lang="ts">
// Interfaces
import { Action, State } from 'vuex-class'
import { ActionBindingIF, StateModelIF } from '@/interfaces'
// Libraries
import { Component, Mixins } from 'vue-property-decorator'

// Resources
import { ExternalResource } from '@/resources'

// Components
import { ResourceExample } from '@/components/common'

// Mixins
import { ResourceLookupMixin } from '@/mixins'

@Component({
  components: {
    ResourceExample
  }
})
export default class StateExample extends Mixins(ResourceLookupMixin) {
  // Initialize State
  @State stateModel!: StateModelIF

  // Initialize Actions
  @Action setName!: ActionBindingIF
  @Action setResource!: ActionBindingIF

  created () {
    // Example of setting the State of a string
    this.setName('Testing My Actions and Mutations: Congratulations... it worked!')

    // Example of setting the State of a Resource
    this.setResource(ExternalResource)
  }
}
</script>
