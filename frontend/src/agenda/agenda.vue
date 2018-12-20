<template>
  <div>
    <div class="inline-title">{{ title }}</div>
    <keep-alive>
      <full-calendar ref="qcalendar"
                     key="qcalendar"
                     class="calendar-margins"
                     @view-render="viewRender"
                     @event-render="eventRender"
                     :events="calendar_events"
                     :config="configuration"></full-calendar>
    </keep-alive>
  </div>

</template>

<script>
  import { mapState, mapMutations, mapActions, mapGetters } from 'vuex'
  import 'fullcalendar/dist/fullcalendar.css'
  import 'fullcalendar-scheduler'

  export default {
    name: 'Agenda',
    created() {
      this.initializeAgenda()
    },
    mounted() {
      this.$root.$on('next', () => { this.next() })
      this.$root.$on('prev', () => { this.prev() })
      this.$root.$on('today', () => { this.today() })
      this.$root.$on('listWeek', () => { this.listWeek() })
      this.$root.$on('listDay', () => { this.listDay() })
    },
    data() {
      return {
        config: {
          schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
          showNonCurrentDates: false,
          fixedWeekCount: false,
          navLinks: true,
          defaultView: 'listWeek',
          views: {
            listDay: {
              allDaySlot: false,
            },
            listWeek: {
              allDaySlot: false,
            },
          },
          contentHeight() {
            return window.innerHeight - 240
          },
          weekends: false,
          maxTime: '18:00:00',
          minTime: '8:00:00',
          header: {
            left: null,
            center: null,
            right: null
          },
          groupByDateAndResource: true
        },
        title: '',
      }
    },
    computed: {
      ...mapGetters(['room_resources', 'calendar_events']),
      ...mapState(['exams']),
      configuration() {
        let configuration = this.config
        configuration['resources'] = this.room_resources
        return configuration
      },
    },
    methods: {
      ...mapActions(['initializeAgenda']),
      ...mapMutations([
        'toggleBookRoomModal',
        'setCalendarView'
      ]),
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
        this.title = view.title
      },
      next() {
        this.$refs.qcalendar.fireMethod('next')
      },
      prev() {
        this.$refs.qcalendar.fireMethod('prev')
      },
      today() {
        this.$refs.qcalendar.fireMethod('today')
      },
      listDay() {
        this.$refs.qcalendar.fireMethod('changeView', 'listDay')
      },
      listWeek() {
        this.$refs.qcalendar.fireMethod('changeView', 'listWeek')
      },
    }
  }
</script>

<style scoped>
  .inline-title {
    display: inline;
    margin: 0px 0px -30px 20px;
    font-size: 2rem;
    font-weight: 600;
  }
  .calendar-margins {
    margin-top: -35px;
    margin-left: 20px;
    padding: 0px;
  }
</style>