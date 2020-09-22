<template>
  <!--this outer div is necessary because this file will be rendered inside a flex-div box and so the direct child of
  that flex-div must also be div in order for it to be subject to the flex settings (see layout/nav.vue)-->
  <div>
    <form inline>
      <b-button class="btn-primary"
                @click="prev"
                id="previous">
        <font-awesome-icon icon="angle-left"
                           class="m-0 p-0"
                           style="font-size: 1rem;"/></b-button>
      <b-button class="btn-primary"
                @click="next"
                id="next">
        <font-awesome-icon icon="angle-right"
                           class="m-0 p-0"
                           style="font-size: 1rem;"/></b-button>
      <b-button class="btn-primary mx-2" @click="today">Today</b-button>
      <DropdownCalendar class="mr-3" />
      <b-dropdown variant="primary"
                  v-if="!scheduling && !rescheduling"
                  class="mr-3 ml-3"
                  text="Schedule an Event...">
        <b-dropdown-item @click="showExamModal">
          Exam Event
        </b-dropdown-item>
        <b-dropdown-item @click="scheduleOtherEvent">
          Non-Exam Event
        </b-dropdown-item>
      </b-dropdown>
      <b-button v-if="role_code === 'GA'"
                variant="primary"
                @click="clickBlackout">
        Create Blackout
      </b-button>
    </form>
  </div>
</template>

<script>
  import { mapMutations, mapState, mapGetters } from 'vuex'
  import DropdownCalendar from './dropdown-calendar'

  export default {
    name: 'ButtonsCalendar',
    components: { DropdownCalendar },
    computed: {
      ...mapState([
        'scheduling',
        'rescheduling',
        'showBookingBlackoutModal',
      ]),
      ...mapGetters([
        'role_code',
      ])
    },
    methods: {
      ...mapMutations([
        'setSelectedExam',
        'toggleExamInventoryModal',
        'toggleScheduling',
        'toggleBookingBlackoutModal',
      ]),
      showExamModal() {
        this.toggleExamInventoryModal(true)
      },
      scheduleOtherEvent() {
        this.setSelectedExam(null)
        this.toggleScheduling(true)
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
      clickBlackout(){
        this.toggleBookingBlackoutModal(!this.showBookingBlackoutModal)
      }
    }
  }
</script>
