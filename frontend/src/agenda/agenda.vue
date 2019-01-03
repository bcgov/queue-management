<template>
  <div>
    <keep-alive>
      <full-calendar ref="agendacal"
                     key="agendacal"
                     class="q-calendar-margins"
                     @view-render="viewRender"
                     @event-render="eventRender"
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
      this.setCalendarTitle(null)
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
          views: {
            listDay: {
              allDaySlot: false,
            },
            listWeek: {
              allDaySlot: false,
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
      ...mapState(['exams', 'viewPortSizes', 'calendarTitle']),
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
        'setCalendarTitle',
        'toggleBookRoomModal',
        'setCalendarView'
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
      eventRender(event, element, view) {
        if (view.name === 'listWeek' || view.name === 'listDay') {
          let resTitle = this.room_resources.find(res => res.id == event.resourceId).title
          let examObj = this.exams.find(exam => exam.booking_id == event.resourceId)
          let invigilator = 'none'
          if (examObj && examObj.invigilator&& examObj.invigilator.invigilator_name) {
            invigilator = examObj.invigilator.invigilator_name
          }
          element.find('.fc-list-item-marker').replaceWith(`<td>${resTitle} - ${event.title}</td>`)
          element.find('.fc-list-item-title').replaceWith(
            `<td style="text-align: right">Invigilator: ${invigilator}</td>`
          )
        }
      },
      viewRender(view, el) {
        this.setCalendarTitle({ title: view.title, view: view.name })
        if (view.name === 'basicDay') {
          this.$refs.agendacal.fireMethod('changeView', 'listDay')
        }
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