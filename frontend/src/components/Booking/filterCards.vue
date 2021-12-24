<template>
  <div fluid class="container-fluid">
    <div class="fc-view-container">
      <div class="fc-view fc-listYear-view fc-list-view fc-widget-content">
        <div class="fc-scroller" style="overflow: hidden auto; height: auto">
          <div v-if="events.length === 0" class="my-5 mx-3">
            No events found
          </div>
          <table class="fc-list-table" aria-hidden=true  v-else>
            <tbody>
              <template v-for="(eventDetails, date) in getEvents">
                <tr
                  class="fc-list-heading"
                  :key="eventDetails.id"
                  @click="showDayView(eventDetails[0] && eventDetails[0].start)"
                >
                  <td class="fc-widget-header" colspan="3">
                    <a class="fc-list-heading-main">
                      {{ moment(date).format('MMMM DD, YYYY') }}</a
                    >
                  </td>
                </tr>
                <tr
                  class="fc-list-item"
                  style="max-width: 85%"
                  v-for="event in eventDetails"
                  :key="event.id"
                >
                  <td class="fc-list-item-time fc-widget-content">
                    {{ moment(event.start).format('hh:mm') }} -
                    {{ moment(event.end).format('hh:mm') }}
                  </td>
                  <td class="fc-list-item-marker fc-widget-content">
                    <span
                      class="fc-event-dot"
                      :style="eventColor(event.color)"
                    ></span>
                  </td>
                  <td class="fc-list-item-title fc-widget-content">
                    <div
                      style="display: flex; justify-content: left; width: 100%"
                      v-if="event.exam"
                    >
                      <div class="ft-wt-600 mr-1"><strong>Exam:</strong></div>

                      <div class="ft-wt-400 mr-3">{{ event.title }}</div>

                      <div class="ft-wt-600 mx-1"><strong>Event ID:</strong></div>

                      <div class="ft-wt-400 mr-3">
                        {{ event.exam.event_id }}
                      </div>

                      <div class="ft-wt-600 mx-1"><strong>Writer:</strong></div>

                      <div class="ft-wt-400 mr-3">
                        {{ event.exam.examinee_name }}
                      </div>

                      <div class="ft-wt-600 mx-1"><strong>Received:</strong></div>

                      <div class="ft-wt-400 mr-3">
                        {{
                          moment(event.exam.exam_received_date).format(
                            'MMM Do, YYYY'
                          )
                        }}
                      </div>

                      <div class="ft-wt-600 mx-1"><strong>Expiry:</strong></div>

                      <div class="ft-wt-400 mr-3">
                        {{
                          moment(event.exam.exam_expiry).format('MMM Do, YYYY')
                        }}
                      </div>

                      <div class="ft-wt-600 mx-1"><strong>Method:</strong></div>

                      <div class="ft-wt-400 mr-3">
                        {{ event.exam.exam_method }}
                      </div>

                      <div class="ft-wt-600 mx-1"><strong>Invigilator:</strong></div>

                      <div class="ft-wt-400 mr-3">
                        {{
                          event.exam.invigilator &&
                          event.exam.invigilator.invigilator_name
                        }}
                      </div>
                    </div>

                    <div
                      style="
                        display: flex;
                        justify-content: flex-center;
                        width: 100%;
                      "
                      v-else
                    >
                      <div class="ft-wt-400 mr-3">{{ event.title }}</div>
                      <div>Non-Exam / Other Event</div>
                    </div>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">

import { Component, Prop, Vue } from 'vue-property-decorator'

import moment from 'moment'

@Component
export default class FilterCards extends Vue {
  @Prop({ default: {} })
  events: any

  get getEvents () {
    const filterEvents = {}
    const eventsList: any = [...this.events]
    eventsList.sort(function (a: any, b: any) {
      return (new Date(a.start) as any) - (new Date(b.start) as any)
    })

    eventsList.forEach((event) => {
      const date = moment(event.start).format('YYYY-MM-DD')
      if (filterEvents[date]) {
        filterEvents[date].push(event)
      } else {
        filterEvents[date] = [event]
      }
    })

    return filterEvents
  }

  eventColor (color) {
    return `background-color: ${color}`
  }

  showDayView (date) {
    this.$root.$emit('goToDate', date)
  }

  moment (date) {
    return moment(date)
  }
}
</script>

<style scoped>
.fc-list-table {
  width: 100%;
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
  /* table-layout: fixed; */
  border-collapse: collapse;
  border-spacing: 0;
  font-size: 1em;
}
.fc-list-heading {
  border-bottom-width: 1px;
  font-weight: bold;
}
.fc-list-heading td {
  background: #eee;
  padding: 10px;
}
.fc-list-item-marker,
.fc-list-item-time {
  white-space: nowrap;
}
.fc-list-table tr {
  width: 100%;
}
.fc-view-container {
  border: 1px solid;
}
.fc-view-container td {
  padding: 10px;
}
</style>
