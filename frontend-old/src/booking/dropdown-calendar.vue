<template>
  <b-dropdown variant="primary"
              class="mr-3"
              :text="view"
              id="view_select">
    <b-dropdown-item @click="month"
                     id="monthly_planner">Monthly Planner
    </b-dropdown-item>
    <b-dropdown-item @click="agendaWeek"
                     id="weekly_planner">Weekly Planner
    </b-dropdown-item>
    <b-dropdown-item @click="agendaDay"
                     id="single_day_planner">Single Day
    </b-dropdown-item>
  </b-dropdown>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    name: "DropdownCalendar",
    computed: {
      ...mapState(['calendarSetup']),
      view() {
        if (this.calendarSetup) {
          switch (this.calendarSetup.viewName) {
            case 'agendaDay':
              return 'Single Day'
            case 'agendaWeek':
              return 'Weekly Planner'
            case 'month':
              return 'Monthly Planner'
            case 'listYear':
              return 'Search Results'
            default:
              return 'Weekly Planner'
          }
        }
        return 'Weekly Schedule'
      }
    },
    methods: {
      month() {
        this.$root.$emit('month')
      },
      agendaWeek() {
        this.$root.$emit('agendaWeek')
      },
      agendaDay() {
        this.$root.$emit('agendaDay')
      },
    }
  }
</script>
