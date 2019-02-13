<template>
  <!--this outer div is necessary because this file will be rendered inside a flex-div box and so the direct child of
  that flex-div must also be div in order for it to be subject to the flex settings (see layout/nav.vue)-->
  <div>
    <form inline>
      <b-button class="btn-primary" @click="prev">
        <font-awesome-icon icon="angle-left"
                           class="m-0 p-0"
                           style="font-size: 1rem;"/></b-button>
      <b-button class="btn-primary" @click="next">
        <font-awesome-icon icon="angle-right"
                           class="m-0 p-0"
                           style="font-size: 1rem;"/></b-button>
      <b-button class="btn-primary mx-2" @click="today">Today</b-button>
      <DropdownCalendar class="mr-3" />
      <b-dropdown variant="primary"
                  v-if="showCalendarControls"
                  class="mr-3 ml-3"
                  text="Schedule an Event...">
        <b-dropdown-item @click="showExamModal">
          ITA Exam
        </b-dropdown-item>
        <b-dropdown-item @click="scheduleOtherEvent">
          Non-exam/Other Event
        </b-dropdown-item>
      </b-dropdown>
    </form>
  </div>
</template>

<script>
  import { mapMutations, mapState } from 'vuex'
  import DropdownCalendar from './dropdown-calendar'

  export default {
    name: 'ButtonsCalendar',
    components: { DropdownCalendar },
    computed: {
      ...mapState(['showCalendarControls',])
    },
    methods: {
      ...mapMutations([
        'toggleExamInventoryModal',
        'toggleScheduling',
        'toggleCalendarControls',
        'toggleSchedulingIndicator',
        'toggleSchedulingOther',
        'navigationVisible'
      ]),
      showExamModal() {
        this.toggleExamInventoryModal(true)
      },
      scheduleOtherEvent() {
        this.$root.$emit('toggleOffsite', false)
        this.navigationVisible(false)
        this.toggleCalendarControls(false)
        this.toggleSchedulingOther(true)
        this.toggleSchedulingIndicator(true)
        this.$root.$emit('options', {name: 'selectable', value: true})
      },
      next() {
        this.$root.$emit('next')
      },
      prev() {
        this.$root.$emit('prev')
      },
      today() {
        this.$root.$emit('today')
      },
    }
  }
</script>