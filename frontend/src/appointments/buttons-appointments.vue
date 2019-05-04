<template>
  <fragment>
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
        <b-dropdown variant="primary" class="mr-3" :text="dropdownText">
          <b-dropdown-item @click="agendaWeek">
            Week View
          </b-dropdown-item>
          <b-dropdown-item @click="agendaDay">
            Day View
          </b-dropdown-item>
        </b-dropdown>
      </form>
    </div>
    <div>
      <span class="q-inline-title">{{ calendar_setup.title }}</span>
    </div>
  </fragment>

</template>

<script>
  import { createNamespacedHelpers } from 'vuex'
  const { mapActions, mapGetters, mapMutations, mapState } = createNamespacedHelpers('appointmentsModule')

  export default {
    name: 'ButtonsAppointments',
    computed: {
      ...mapGetters(['calendar_setup']),
      dropdownText() {
        if (this.calendar_setup.name === 'agendaDay') {
          return 'Day View'
        }
        if (this.calendar_setup.name === 'agendaWeek') {
          return 'Week View'
        }
        return 'Week View'
      },
    },
    methods: {
      ...mapMutations([]),
      ...mapActions('beginAppointment'),
      agendaDay() {
        this.$root.$emit('agendaDay')
      },
      agendaWeek() {
        this.$root.$emit('agendaWeek')
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