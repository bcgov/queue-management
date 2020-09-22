<template>
  <b-modal v-model="modalVisible"
           @shown="clearTime"
           modal-class="q-modal"
           body-class="q-modal"
           no-close-on-backdrop
           no-close-on-esc
           hide-header
           size="sm">
     <div id="navi">
        <template v-if="this.$store.state.showServeCitizenSpinner">
          <div class="q-loader2" ></div>
        </template>
     </div>
    <template slot="modal-footer">
      <b-button class="btn-secondary"
                @click="hide">Close</b-button>
    </template>
    <b-form autocomplete="off">
      <b-form-row>
        <b-col>
          <b-form-group v-if="isNotBlackoutFlag"
                        class="mb-0 mt-2">
            <label class="mb-0">Citizen Has Arrived?</label><br>
            <b-button class="w-100 btn-success"
                      @click="checkIn">
              Check-In
            </b-button>
          </b-form-group>
        </b-col>
      </b-form-row>
      <b-form-row>
        <b-col>
          <b-form-group class="mb-0 mt-2">
            <label class="mb-0">Edit or Cancel Appointment?</label><br>
            <b-button class="w-100 btn-secondary"
                      @click="editAppt">
              Edit Appointment
            </b-button>
          </b-form-group>
        </b-col>
      </b-form-row>
      <b-form-row v-if="checkRecurringStatus">
        <b-col>
          <b-form-group class="mb-0 mt-2">
            <label class="mb-0">Edit or Cancel Recurring Series?</label><br>
            <b-button class="w-100 btn-secondary"
                      @click="editSeries">
              Edit Recurring Series
            </b-button>
          </b-form-group>
        </b-col>
      </b-form-row>
    </b-form>
  </b-modal>
</template>

<script>
import { createNamespacedHelpers } from 'vuex'
const { mapActions, mapGetters, mapMutations, mapState } = createNamespacedHelpers('appointmentsModule')

export default {
  name: 'CheckInModal',
  props: ['clickedAppt'],
  data () {
    return {
      showcheckInSpinner: false
    }
  },
  computed: {
    ...mapState(['showCheckInModal', 'showServeCitizenSpinner', 'checkInClicked']),
    modalVisible: {
      get () { return this.showCheckInModal },
      set (e) { this.toggleCheckInModal(e) }
    },
    isNotBlackoutFlag () {
      if (this.clickedAppt && this.clickedAppt.blackout_flag) {
        if (this.clickedAppt.blackout_flag === 'Y') {
          return false
        } else if (this.clickedAppt.blackout_flag === 'N') {
          return true
        }
      }
      return false
    },
    checkRecurringStatus () {
      if (this.clickedAppt && this.clickedAppt.recurring_uuid === null) {
        return false
      }
      return true
    }
  },
  methods: {
    ...mapActions([
      'getAppointments',
      'postCheckIn'
    ]),
    ...mapMutations([
      'toggleCheckInModal',
      'toggleApptBookingModal',
      'toggleEditDeleteSeries',
      'toggleCheckInClicked'
    ]),
    checkIn () {
      if (this.$store.state.serviceModalForm.citizen_id) {
        this.hide()
        this.$store.commit('setMainAlert', 'Already have appointment in progress.  Please close ticket then check-in citizen')
      } else {
        if (!this.checkInClicked) {
          this.toggleCheckInClicked(true)
          this.$store.commit('toggleServeCitizenSpinner', true)
          this.postCheckIn(this.clickedAppt).then(response => {
            this.$root.$emit('clear-clicked-appt')
            this.$root.$emit('clear-clicked-time')
            this.hide()
            if (this.$store.state.officeType == 'nocallonsmartboard') {
              this.$router.push('/queue')
            }

            this.$store.commit('toggleServeCitizenSpinner', false)
          })
        }
      }
    },
    clearTime () {
      this.$root.$emit('cleardate')
    },
    hide () {
      this.getAppointments().then(() => {
        this.toggleCheckInModal(false)
        this.$root.$emit('clear-clicked-appt')
        this.$root.$emit('clear-clicked-time')
      })
    },
    editAppt () {
      this.toggleApptBookingModal(true)
      this.toggleCheckInModal(false)
      this.toggleEditDeleteSeries(false)
      this.getAppointments()
    },
    editSeries () {
      this.toggleApptBookingModal(true)
      this.toggleCheckInModal(false)
      this.toggleEditDeleteSeries(true)
      this.getAppointments()
    }
  }
}
</script>

<style scoped>
   @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
  #navi {
    position: relative;
  }
  .q-loader2 {
    position: absolute;
    z-index: 1100;
    text-align: center;
    margin: 50px auto auto 100px;
    width: 50px;
    height: 50px;
    border: 10px solid LightGrey;
    opacity:0.9;
    border-radius: 50%;
    border-top-color: DodgerBlue;
    animation: spin 1s ease-in-out infinite;
    -webkit-animation: spin 1s ease-in-out infinite;
}
</style>
