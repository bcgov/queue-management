<template>
    <b-modal v-model="modal"
             hide-header
             size="md"
             modal-class="q-modal"
             body-class="q-modal"
             no-close-on-backdrop
             @shown="show"
             >
      <template slot="modal-footer">
      <div class="d-flex flex-row-reverse">
        <b-button class="btn-primary ml-2"
                  @click="submit"
                  >
          Submit</b-button>
        <b-button @click="cancel">
          Cancel
        </b-button>
      </div>
    </template>
    <span style="font-size:1.75rem;">Schedule Booking Blackout</span><br>
    <b-form>
      <b-form-row class="mb-2">
        <b-col cols="6">
          <label>Booking Name</label><br>
          <b-form-input v-model="this.blackout_name"
                        disabled>
          </b-form-input>
        </b-col>
        <b-col cols="6">
          <label>Contact Information (optional)</label>
          <b-form-input v-model="this.user_contact_info">
          </b-form-input>
        </b-col>
      </b-form-row>
      <b-form-row>
        <b-col cols="6">
          <b-form-group>
            <label>Blackout Date</label><br>
            <DatePicker v-model="blackout_date"
                        id="appointment_blackout_date"
                        type="date"
                        lang="en"
                        class="w-100">
            </DatePicker>
          </b-form-group>
        </b-col>
      </b-form-row>
      <b-form-row>
        <b-col cols="6">
          <b-form-group>
            <label>Blackout Start Time</label><br>
            <DatePicker v-model="start_time"
                        id="appointment_blackout_start_time"
                        :time-picker-options="{ start: '8:00', step: '00:30', end: '17:30' }"
                        lang="en"
                        format="h:mm a"
                        autocomplete="off"
                        placeholder="Select Start Time"
                        class="w-100"
                        type="time">
            </DatePicker>
          </b-form-group>
        </b-col>
        <b-col cols="6">
          <b-form-group>
            <label>Blackout End Time</label><br>
            <DatePicker v-model="end_time"
                        id="appointment_blackout_end_time"
                        :time-picker-options="{ start: '8:30', step: '00:30', end: '18:00' }"
                        lang="en"
                        format="h:mm a"
                        autocomplete="off"
                        placeholder="Select End Time"
                        class="w-100"
                        type="time">
            </DatePicker>
          </b-form-group>
        </b-col>
      </b-form-row>
      <template>
        <b-form-row class="mb-1">
          <b-col class="mr-2">
            <label>Select Room(s)</label>
            <b-table selectable
                     select-mode="multi"
                     selected-variant="success"
                     responsive
                     :fields="room_fields"
                     :items="this.roomResources"
                     style="height: 100px;"
                     bordered
                     striped
                     @row-selected="onRowSelected">
              <template slot="selected" slot-scope="{ rowSelected }">
                <template v-if="rowSelected">
                  <span aria-hidden="true">&check;</span>
                  <span class="sr-only"Selected></span>
                </template>
                <template v-else>
                  <span aria-hidden="true">&nbsp;</span>
                  <span class="sr-only">Not selected</span>
                </template>
              </template>
            </b-table>
          </b-col>
          <b-col>
            <b-row>
              <label>Selected Room(s)</label>
            </b-row>
            <b-row v-for="room in selected"
                   style="justify-content: center;">
                {{ room.name }}
            </b-row>
          </b-col>
        </b-form-row>
      </template>
      <b-form-row>
        <b-form-group class="ml-1" style="width: 465px;">
            <label>Blackout Notes (optional)</label><br>
            <b-textarea v-model="notes"
                        id="appointment_blackout_notes"
                        placeholder="Enter notes about blackout period"
                        rows="3"
                        max-rows="6"
                        size="md">
            </b-textarea>
        </b-form-group>
      </b-form-row>
    </b-form>
    </b-modal>
</template>

<script>
    import { mapActions, mapMutations, mapState } from 'vuex'
    import DatePicker from 'vue2-datepicker'
    import moment from 'moment'

    export default {
      name: "BookingBlackoutModal",
      components: { DatePicker},
      created(){
        this.blackout_name = "BLACKOUT PERIOD"
        this.user_contact_info = this.$store.state.user.username
      },
      data(){
        return {
          blackout_date: '',
          start_time: '',
          end_time: '',
          notes: '',
          blackout_name: '',
          user_contact_info: '',
          selected: [],
          selectedLength: 0,
          room_id_list: [],
          room_fields: ['selected', 'title'],
        }
      },
      methods: {
        ...mapActions([
          'getBookings',
          'postBooking',
          'finishBooking',
        ]),
        ...mapMutations([
          'toggleBookingBlackoutModal'
        ]),
        show(){
          this.start_time = ''
          this.end_time = ''
          this.blackout_date = ''
          this.notes = ''
        },
        cancel(){
          this.toggleBookingBlackoutModal(false)
        },
        onRowSelected(roomResources){

          let roomResourceLength = roomResources.length
          let roomResourceIndex = roomResources.length - 1

          if (roomResourceIndex == -1) {
            roomResourceIndex = 0
          }

          if(this.selectedLength <= roomResourceLength){
            if(roomResourceLength == 1){
              this.selected.push({id: roomResources[0].id, name: roomResources[0].title})
              this.selectedLength = this.selected.length
              this.room_id_list.push(roomResources[0].id)
            }else if(roomResourceLength > 1){
              this.selected.push({id: roomResources[roomResourceIndex].id, name: roomResources[roomResourceIndex].title})
              this.selectedLength = this.selected.length
              this.room_id_list.push(roomResources[roomResourceIndex].id)
            }
          }else if(this.selectedLength > roomResourceLength){
            let remainingIDs = []
            roomResources.forEach(function(room) {
              remainingIDs.push(room.id)
            })
            let selectedIDs = []
            this.selected.forEach(function(room) {
              selectedIDs.push(room.id)
            })
            let difference  = selectedIDs.filter(x =>  !remainingIDs.includes(x))
            let indexOfDifference = this.selected.findIndex(x => x.id == difference)
            if(indexOfDifference !== undefined){
              this.selected.splice(indexOfDifference, 1)
            }
            let indexOfDifferenceRoomList = this.room_id_list.findIndex(x => x.id == difference)
            if(indexOfDifferenceRoomList !== undefined){
              this.room_id_list.splice(indexOfDifferenceRoomList, 1)
            }
          }
        },
        submit(e){
          e.preventDefault()

          let date = moment(this.blackout_date).clone().format('YYYY-MM-DD')
          let start = moment(this.start_time).clone().format('HH:mm:ss')
          let start_date = moment(date + " " + start).format()
          let end = moment(this.end_time).clone().format('HH:mm:ss')
          let end_date = moment(date + " " + end).format()

          if(this.room_id_list.length === 1){
            let blackout_booking = {}
            if(this.selected[0].id === '_offsite'){
              blackout_booking.start_time = start_date
              blackout_booking.end_time = end_date
              blackout_booking.booking_name = this.blackout_name
              blackout_booking.booking_contact_information = this.user_contact_info
              blackout_booking.blackout_flag = 'Y'
              blackout_booking.blackout_notes = this.notes
            }else {
              blackout_booking.start_time = start_date
              blackout_booking.end_time = end_date
              blackout_booking.booking_name = this.blackout_name
              blackout_booking.booking_contact_information = this.user_contact_info
              blackout_booking.room_id  = this.selected[0].id
              blackout_booking.blackout_flag = 'Y'
              blackout_booking.blackout_notes = this.notes
            }
            this.postBooking(blackout_booking).then( () => {
              this.finishBooking()
              this.toggleBookingBlackoutModal(false)
            })
          }else if(this.room_id_list.length > 1){
            let self = this
            this.room_id_list.forEach(function (room) {
              let blackout_booking = {}
              if(room == '_offsite'){
                blackout_booking.start_time = start_date
                blackout_booking.end_time = end_date
                blackout_booking.booking_name = self.blackout_name
                blackout_booking.booking_contact_information = self.user_contact_info
                blackout_booking.blackout_flag = 'Y'
                blackout_booking.blackout_notes = self.notes
              }else {
                blackout_booking.start_time = start_date
                blackout_booking.end_time = end_date
                blackout_booking.booking_name = self.blackout_name
                blackout_booking.booking_contact_information = self.user_contact_info
                blackout_booking.room_id  = room
                blackout_booking.blackout_flag = 'Y'
                blackout_booking.blackout_notes = self.notes
              }
              self.postBooking(blackout_booking).then( () => {
                self.getBookings()
                self.toggleBookingBlackoutModal(false)
              })
            })
          }
        },
      },
      computed: {
        ...mapState({
          showBookingBlackoutModal: state => state.showBookingBlackoutModal,
          rooms: state => state.rooms,
          roomResources: state => state.roomResources,
        }),
        modal: {
          get() {
            return this.showBookingBlackoutModal
          },
          set(e) {
            this.toggleBookingBlackoutModal(e)
            let all_rooms_local = []
            this.roomResources.forEach(function(room){
              all_rooms_local.push(room.title)
            })
            this.room_names = all_rooms_local
          }
        },
      }
    }
</script>


<style scoped>

</style>
