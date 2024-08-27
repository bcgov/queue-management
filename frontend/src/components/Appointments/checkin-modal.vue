<template>
  <b-modal
    v-model="modalVisible"
    @shown="clearTime"
    modal-class="q-modal"
    body-class="q-modal"
    no-close-on-backdrop
    no-close-on-esc
    hide-header
    size="sm"
  >

 <b-form autocomplete="off" v-if="isDraftAppointment">
      <b-form-row>
        <b-col>
          <b-form-group  class="mb-0 mt-2">
            <p class="mb-0 no-edit">You cannot edit or delete draft appointments.</p>
          </b-form-group>
        </b-col>
      </b-form-row>
  </b-form>
    <div id="navi" v-if="!isDraftAppointment">
      <template v-if="this.$store.state.showServeCitizenSpinner">
        <div class="q-loader2"></div>
      </template>
    </div>
    <template slot="modal-footer">
      <b-button class="btn-secondary" @click="hide">Close</b-button>
    </template>
    <b-form autocomplete="off" v-if="!isDraftAppointment">
      <b-form-row>
        <b-col>
          <b-form-group v-if="(isNotBlackoutFlag) && (!checkRecurringStatStatus)" class="mb-0 mt-2">
            <p class="mb-0">Citizen Has Arrived?</p><br />
            <b-button class="w-100 btn-success" @click="checkIn">
              Check-In
            </b-button>
          </b-form-group>
        </b-col>
      </b-form-row>
      <b-form-row v-if="!checkRecurringStatStatus">
        <b-col>
          <b-form-group class="mb-0 mt-2">
            <p class="mb-0">Edit or Cancel Appointment?</p><br />
            <b-button class="w-100 btn-secondary" @click="editAppt">
              Edit Appointment
            </b-button>
          </b-form-group>
        </b-col>
      </b-form-row>
      <b-form-row v-if="checkRecurringStatus">
        <b-col>
          <b-form-group class="mb-0 mt-2">
            <p class="mb-0">Edit or Cancel Recurring Series?</p><br />
            <b-button class="w-100 btn-secondary" @click="editSeries">
              Edit Recurring Series
            </b-button>
          </b-form-group>
        </b-col>
      </b-form-row>
      <b-form-row v-if="checkRecurringStatStatus">
        <b-col>
          <b-form-group class="mb-0 mt-2">
            <span v-if="is_Support" class="mb-0">Edit or Cancel Recurring STAT Series?</span>
            <span v-else class="mb-0">View STAT?</span>
            <br />
            <b-button class="w-100 btn-secondary" @click="editStatSeries">
              <span v-if="is_Support" >
                Edit Recurring STAT Series
              </span>
              <span v-else>
                View STAT
              </span>
            </b-button>
          </b-form-group>
        </b-col>
      </b-form-row>
    </b-form>
  </b-modal>
</template>

<script lang="ts">

import { Component, Prop, Vue } from 'vue-property-decorator'
import { namespace } from 'vuex-class'

const appointmentsModule = namespace('appointmentsModule')

@Component
export default class CheckInModal extends Vue {
  @Prop({ default: '' })
  private clickedAppt!: any

  @appointmentsModule.State('showCheckInModal') private showCheckInModal!: any
  @appointmentsModule.State('showServeCitizenSpinner') private showServeCitizenSpinner!: any
  @appointmentsModule.State('checkInClicked') private checkInClicked!: any

  @appointmentsModule.Getter('is_Support') private is_Support!: any;

  @appointmentsModule.Action('getAppointments') public getAppointments: any
  @appointmentsModule.Action('postCheckIn') public postCheckIn: any

  @appointmentsModule.Mutation('toggleCheckInModal') public toggleCheckInModal: any
  @appointmentsModule.Mutation('toggleApptBookingModal') public toggleApptBookingModal: any
  @appointmentsModule.Mutation('toggleEditDeleteSeries') public toggleEditDeleteSeries: any
  @appointmentsModule.Mutation('toggleCheckInClicked') public toggleCheckInClicked: any

  public showcheckInSpinner: boolean = false

  get modalVisible () { return this.showCheckInModal }
  set modalVisible (e) { this.toggleCheckInModal(e) }

  get isNotBlackoutFlag () {
    if (this.clickedAppt && this.clickedAppt.blackout_flag) {
      if (this.clickedAppt.blackout_flag === 'Y') {
        return false
      } else if (this.clickedAppt.blackout_flag === 'N') {
        return true
      }
    }
    return false
  }

  get isDraftAppointment () {
    if (this.clickedAppt && this.clickedAppt.is_draft) {
      return true
    }
    return false
  }

  get checkRecurringStatus () {
    if (this.clickedAppt && (this.clickedAppt.recurring_uuid === null || this.clickedAppt.stat_flag)) {
      return false
    }
    return true
  }

  get checkRecurringStatStatus () {
    if (this.clickedAppt && this.clickedAppt.stat_flag) {
      return true
    }
    return false
  }

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
  }

  clearTime () {
    this.$root.$emit('cleardate')
  }

  hide () {
    this.getAppointments().then(() => {
      this.toggleCheckInModal(false)
      this.$root.$emit('clear-clicked-appt')
      this.$root.$emit('clear-clicked-time')
    })
  }

  editAppt () {
    this.toggleApptBookingModal(true)
    this.toggleCheckInModal(false)
    this.toggleEditDeleteSeries(false)
    this.getAppointments()
  }

  editSeries () {
    this.toggleApptBookingModal(true)
    this.toggleCheckInModal(false)
    this.toggleEditDeleteSeries(true)
    this.getAppointments()
  }

  editStatSeries () {
    this.editSeries()
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
  opacity: 0.9;
  border-radius: 50%;
  border-top-color: DodgerBlue;
  animation: spin 1s ease-in-out infinite;
  -webkit-animation: spin 1s ease-in-out infinite;
}
.no-edit{
  font-size: 14px;
  font-weight: 800;
}
</style>
