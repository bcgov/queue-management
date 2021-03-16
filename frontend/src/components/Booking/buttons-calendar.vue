<template>
  <!--this outer div is necessary because this file will be rendered inside a flex-div box and so the direct child of
  that flex-div must also be div in order for it to be subject to the flex settings (see layout/nav.vue)-->
  <div>
    <form inline>
      <b-button class="btn-primary" @click="prev" id="previous">
        <font-awesome-icon
          icon="angle-left"
          class="m-0 p-0"
          style="font-size: 1rem"
      /></b-button>
      <b-button class="btn-primary ml-1" @click="next" id="next">
        <font-awesome-icon
          icon="angle-right"
          class="m-0 p-0"
          style="font-size: 1rem"
      /></b-button>
      <b-button class="btn-primary mx-2" @click="today">Today</b-button>
      <DropdownCalendar class="mr-3" />
      <b-dropdown
        variant="primary"
        v-if="!scheduling && !rescheduling"
        class="mr-3 ml-3"
        text="Schedule an Event..."
      >
        <b-dropdown-item @click="showExamModal"> Exam Event </b-dropdown-item>
        <b-dropdown-item @click="scheduleOtherEvent">
          Non-Exam Event
        </b-dropdown-item>
      </b-dropdown>
      <b-button
        variant="primary"
        @click="clickBlackout"
      >
        Create Blackout
      </b-button>
    </form>
  </div>
</template>

<script lang="ts">
// /* eslint-disable */
import { Mutation, State } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'

import DropdownCalendar from './dropdown-calendar.vue'

@Component({
  components: {
    DropdownCalendar
  }
})
export default class ButtonsCalendar extends Vue {
  @State('scheduling') private scheduling!: any
  @State('rescheduling') private rescheduling!: any
  @State('showBookingBlackoutModal') private showBookingBlackoutModal!: any

  // @Getter('role_code') private role_code!: any;

  @Mutation('setSelectedExam') public setSelectedExam: any
  @Mutation('toggleExamInventoryModal') public toggleExamInventoryModal: any
  @Mutation('toggleScheduling') public toggleScheduling: any
  @Mutation('toggleBookingBlackoutModal') public toggleBookingBlackoutModal: any

  showExamModal () {
    this.toggleExamInventoryModal(true)
  }

  scheduleOtherEvent () {
    this.setSelectedExam(null)
    this.toggleScheduling(true)
  }

  next () {
    this.$root.$emit('next')
  }

  prev () {
    this.$root.$emit('prev')
  }

  today () {
    this.$root.$emit('today')
  }

  clickBlackout () {
    this.toggleBookingBlackoutModal(!this.showBookingBlackoutModal)
  }
}
</script>
