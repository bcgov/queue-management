<template>
  <div>
    <form inline>
      <b-button class="btn-primary" @click="prev">
        <font-awesome-icon icon="angle-left"
                           class="m-0 p-0"
                           style="font-size: 1rem;"/>
      </b-button>
      <b-button class="btn-primary" @click="next">
        <font-awesome-icon icon="angle-right"
                           class="m-0 p-0"
                           style="font-size: 1rem;"/>
      </b-button>
      <b-button class="btn-primary mx-2" @click="today">Today</b-button>
      <b-dropdown variant="primary" class="mr-3" :text="view">
        <b-dropdown-item @click="listDay">
          Daily List
        </b-dropdown-item>
        <b-dropdown-item @click="listWeek">
          Weekly List
        </b-dropdown-item>
      </b-dropdown>
    </form>
  </div>
</template>

<script>
  import { mapMutations, mapState } from 'vuex'

  export default {
    name: 'ButtonsAgenda',
    computed: {
      ...mapState(['calendarSetup']),
      view() {
        if (this.calendarSetup) {
          switch (this.calendarSetup.viewName) {
            case 'listDay':
              return 'Daily List'
            case 'listWeek':
              return 'Weekly List'
            default:
              return 'Weekly List'
          }
        }
        return 'Weekly List'
      }
    },
    methods: {
      ...mapMutations([
        'toggleBookRoomModal',
        'toggleCalendarScheduleMode',
        'toggleInventoryModal',
        'toggleNavigation',
        'toggleSchedulerModal',
      ]),
      next() {
        this.$root.$emit('next')
      },
      prev() {
        this.$root.$emit('prev')
      },
      today() {
        this.$root.$emit('today')
      },
      listDay() {
        this.$root.$emit('listDay')
      },
      listWeek() {
        this.$root.$emit('listWeek')
      },
    }
  }
</script>