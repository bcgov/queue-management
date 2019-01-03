<template>
  <b-dropdown variant="primary" class="mr-3" :text="view">
    <b-dropdown-item @click="month">
      Monthly Planner
    </b-dropdown-item>
    <b-dropdown-item @click="agendaWeek">
      Weekly Planner
    </b-dropdown-item>
    <b-dropdown-item @click="agendaDay">
      Single Day
    </b-dropdown-item>
  </b-dropdown>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    name: "DropdownCalendar",
    computed: {
      ...mapState(['calendarTitle']),
      view() {
        if (this.calendarTitle) {
          switch (this.calendarTitle.view) {
            case 'agendaDay':
              return 'Single Day'
            case 'agendaWeek':
              return 'Weekly Planner'
            case 'month':
              return 'Monthly Planner'
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