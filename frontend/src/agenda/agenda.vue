<template>
  <div>
    <keep-alive>
      <full-calendar ref="agendacal"
                     key="agendacal"
                     class="q-calendar-margins"
                     @event-render="eventRender"
                     @view-render="viewRender"
                     :events="events"
                     :config="configuration"></full-calendar>
    </keep-alive>
  </div>
</template>

<script>
  import { mapState, mapMutations, mapActions, mapGetters } from 'vuex'
  import { FullCalendar } from 'vue-full-calendar'
  import 'fullcalendar/dist/fullcalendar.css'
  import 'fullcalendar-scheduler'

  export default {
    name: 'Agenda',
    components: { FullCalendar },
    mounted() {
      this.initialize()
      this.$root.$on('next', () => { this.next() })
      this.$root.$on('prev', () => { this.prev() })
      this.$root.$on('today', () => { this.today() })
      this.$root.$on('listWeek', () => { this.listWeek() })
      this.$root.$on('listDay', () => { this.listDay() })
    },
    destroyed() {
      this.setCalendarSetup(null)
    },
    data() {
      return {
        configuration: {
          timezone: 'local',
          schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
          showNonCurrentDates: false,
          fixedWeekCount: false,
          navLinks: true,
          defaultView: 'listWeek',
          resources: [],
          listDayFormat: 'dddd, MMM Do',
          views: {
            listDay: {
              allDaySlot: false,
              listDayAltFormat: '[Invigilator]',
            },
            listWeek: {
              allDaySlot: false,
              listDayAltFormat: null,
            },
          },
          height: 'auto',
          weekends: false,
          header: {
            left: null,
            center: null,
            right: null
          },
          groupByDateAndResource: true
        },
      }
    },
    computed: {
      ...mapGetters(['calendar_events', 'room_resources']),
      ...mapState(['exams', 'calendarSetup']),
      events() {
        if (this.calendar_events.length > 0) {
          return this.calendar_events
        }
        return []
      },
    },
    methods: {
      ...mapActions(['initializeAgenda', 'getBookings']),
      ...mapMutations([
        'setCalendarSetup',
        'toggleBookRoomModal',
      ]),
      initialize() {
        this.initializeAgenda().then( rooms => {
          rooms.forEach( room => {
            let roomObj = {
              id: room.room_id,
              title: room.room_name,
              eventColor: room.color
            }
            this.$refs.agendacal.fireMethod('addResource', roomObj)
          })
          this.getBookings()
        })
      },
      viewRender(view, el) {
        this.setCalendarSetup({ title: view.title, view: view.name })
      },
      eventRender(event, el, view) {
        let title = event.title
        let room = event.room.room_name
        let invig = '(none)'
        if (event.invigilator && event.invigilator.invigilator_name) {
          invig = event.invigilator.invigilator_name
        }
        el.find('td.fc-list-item-title.fc-widget-content').html(
          `<div style="display: flex; justify-content: space-between; width: 100%;">
             <div>${room} - <span style="font-weight: 600; font-size: .9rem">${title}</span></div>
             <div>${invig}</div>
           </div>
          `
        )
      },
      next() {
        this.$refs.agendacal.fireMethod('next')
      },
      prev() {
        this.$refs.agendacal.fireMethod('prev')
      },
      today() {
        this.$refs.agendacal.fireMethod('today')
      },
      listDay() {
        this.$refs.agendacal.fireMethod('changeView', 'listDay')
      },
      listWeek() {
        this.$refs.agendacal.fireMethod('changeView', 'listWeek')
      },
    }
  }
</script>

<style scoped>
  .exam-title {
    font-weight: 500 !important;
    font-size: 1rem !important;
  }
</style>