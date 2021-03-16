<template>
  <b-dropdown variant="primary" class="mr-3" :text="view" id="view_select">
    <b-dropdown-item @click="month" id="monthly_planner"
      >Monthly Planner
    </b-dropdown-item>
    <b-dropdown-item @click="agendaWeek" id="weekly_planner"
      >Weekly Planner
    </b-dropdown-item>
    <b-dropdown-item @click="agendaDay" id="single_day_planner"
      >Single Day
    </b-dropdown-item>
  </b-dropdown>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import { State } from 'vuex-class'

@Component({})
export default class DropdownCalendar extends Vue {
  @State('calendarSetup') private calendarSetup!: any

  get view () {
    if (this.calendarSetup) {
      switch (this.calendarSetup.viewName) {
      case 'agendaDay':
        return 'Single Day'
      case 'week':
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

  month () {
    this.$root.$emit('month')
  }

  agendaWeek () {
    this.$root.$emit('agendaWeek')
  }

  agendaDay () {
    this.$root.$emit('agendaDay')
  }
}
</script>
