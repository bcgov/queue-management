<template>
  <b-modal v-model="modalVisible"
           :no-close-on-backdrop="true"
           hide-header
           @shown="show"
           hide-footer
           size="md">
    <div v-if="showModal">
      <span class="q-modal-header">Edit {{ titleText }} Exam Booking</span>
      <b-form autocomplete="off">
        <b-form-row>
          <b-col class="mb-2">
            <div class="q-info-display-grid-container">
              <div class="q-id-grid-outer">
                <div class="q-id-grid-head">Exam Details</div>
                <div class="q-id-grid-col">
                  <div>Exam: </div>
                  <div>{{ actionedExam.exam_name }}</div>
                </div>
                <div class="q-id-grid-col">
                  <div>Event ID: </div>
                  <div>{{ actionedExam.event_id }}</div>
                </div>
                <div class="q-id-grid-col">
                  <div>Type: </div>
                  <div>{{ actionedExam.exam_type.exam_type_name }}</div>
                </div>
                <div class="q-id-grid-col">
                  <div>Writers: </div>
                  <div>{{ actionedExam.number_of_students }}</div>
                </div>
                <div class="q-id-grid-col" v-if="is_liaison_designate">
                  <div>Office: </div>
                  <div>{{ actionedExam.office.office_name }}</div>
                </div>
              </div>
            </div>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col cols="6">
            <b-form-group>
              <label>Exam Date</label><br>
              <DatePicker :value="date"
                          style="color: black"
                          :disabled="fieldDisabled"
                          name="date"
                          input-class="custom-disabled-fields form-control"
                          class="w-100 date-time-fields"
                          @input="checkDate"
                          lang="en">
              </DatePicker>
            </b-form-group>
          </b-col>

          <b-col cols="6">
            <b-form-group>
              <label>Exam Time</label><br>
              <DatePicker v-model="time"
                          class="w-100"
                          :disabled="fieldDisabled"
                          :time-picker-options="{ start: '8:00', step: '00:30', end: '17:00' }"
                          lang="en"
                          format="h:mm a"
                          input-class="custom-disabled-fields form-control"
                          name="time"
                          @input="checkTime"
                          type="time">
                <template slot="calendar-icon">
                  <font-awesome-icon icon="clock"
                                     class="m-0 p-0"
                                     style="font-size: .9rem;"/>
                </template>
              </DatePicker>
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col>
            <b-form-group>
              <label>Location</label><br>
              <b-textarea v-model="offsite_location"
                          :disabled="fieldDisabled"
                          style="color: #525252"
                          class="mb-0 custom-disabled-fields"
                          :rows="2"
                          name="offsite_location"
                          @input.native="checkInput" />
            </b-form-group>
          </b-col>
        </b-form-row>
      </b-form>
      <template v-if="actionedExam.is_pesticide">
        <b-form-row>
          <b-col>
            <b-form-group>
              <label>Event ID</label><br>
              <b-form-input v-model="eventId"
                          :disabled="fieldDisabled"
                          type="text"
                          class="less-10-mb"
                          @input.native="checkInput"
                          name="event_id" />
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col>
            <label class="my-0">Retrieve Exam and Print</label>
            <b-btn class="btn-success w-100" @click="checkAndDownloadExam()">Print</b-btn>
          </b-col>
          <b-col :col="!this.fields.exam_received_date" :cols="this.exam_received ? '' : 3 ">
            <b-form-group>
              <label class="my-0">Exam Printed?</label>
              <b-select id="exam_received"
                        v-model="exam_received"
                        @input="updateExamReceived"
                        class="less-10-mb"
                        :options="examReceivedOptions" />
            </b-form-group>
          </b-col>
          <b-col v-if="exam_received">
            <b-form-group>
              <label class="my-0">Printed Date</label><br>
              <DatePicker :value="fields.exam_received_date"
                          @input="handleDate"
                          format="YYYY-MM-DD"
                          value-type="format"
                          lang="en"
                          id="exam_received_date"
                          input-class="form-control"
                          class="w-100 my-0 less-10-mb">
              </DatePicker>
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row v-if="examNotReady">
          <b-col cols="12" style="color: red">
            This exam is not yet ready for retrieval.  Please try again in no less than 15 minutes.
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col cols="12">
            <b-form-group>
              <label class="my-0">Invigilator</label>
              <b-form-select
                v-model="invigilator_id"
                :options="invigilatorList"
                @change="invigilatorChanged"
              >
              </b-form-select>
            </b-form-group>
          </b-col>
        </b-form-row>
      </template>
      <template v-else>
        <!-- Invigilator Start -->
        <template>
          <b-button v-if="this.currentInvigilatorList.length == 0 && this.groupInvigilatorBoolean"
                    v-b-toggle.collapse-invigilators
                    variant="primary"
                    style="width: 95%; margin-left: 10px;"
                    class="mb-0"
                    @click="setShadowInvigilatorBoolean">
            Add Invigilators
          </b-button>
        </template>
        <template>
          <b-row style="display: inline-flex;" class="w-100 ml-0 mb-1">
            <b-col class="w-50">
              <b-button v-if="this.currentInvigilatorList.length > 0 && this.changeInvigilatorState "
                        v-b-toggle.collapse-invigilators
                        variant="primary"
                        style="padding-left: 40px; padding-right: 25px; margin-left: -4px; white-space: nowrap;"
                        @click="setRemoveShadowInvigilatorBoolean">
                <span>Change Invigilator(s)</span>
              </b-button>
              <b-button v-if="this.currentInvigilatorList.length > 0 && !this.groupInvigilatorBoolean && !this.changeInvigilatorState"
                        style="padding-left: 40px; padding-right: 25px; margin-left: -4px; white-space: nowrap;"
                        variant="primary"
                        disabled>
                <span>Change Invigilator(s)</span>
              </b-button>
            </b-col>
            <b-col class="w-50">
              <b-button v-if="this.currentInvigilatorList.length > 0 && this.removeInvigilatorState"
                        v-b-toggle.collapse-remove-invigilators
                        variant="danger"
                        style="padding-left: 40px; padding-right: 28px; margin-left: -11px; white-space: nowrap;"
                        @click="setChangeShadowInvigilatorBoolean">
                Remove Invigilator(s)
              </b-button>
              <b-button v-if="this.currentInvigilatorList.length > 0 && !this.groupInvigilatorBoolean && !this.removeInvigilatorState"
                        style="padding-left: 40px; padding-right: 28px; margin-left: -11px; white-space: nowrap;"
                        variant="danger"
                        disabled>
                <span>Remove Invigilator(s)</span>
              </b-button>
            </b-col>
          </b-row>
        </template>
        <b-collapse id="collapse-remove-invigilators"
                    class="mt-2 w-100">
          <b-form-group class="q-info-display-grid-container">
            <b-row class="ml-1">
              <span style="font-weight: bold;">Current Invigilator(s): </span>
            </b-row>
            <b-row v-for="current in this.currentInvigilatorList"
                      style="justify-content: center"
                      class="mb-1"
                      v-bind:key="current">
                {{ current.name }}
              </b-row>
            <b-row class="ml-1">
              <span style="font-weight: bold;">Would you like to remove invigilator(s)?</span>
            </b-row>
            <template>
              <b-row style="display: flex; justify-content: center;"
                      class="w-100 mb-0">
                <b-button class="mr-2 mt-1"
                          variant="danger"
                          @click="setSelectedInvigilator">
                  Yes
                </b-button>
                <b-button class="ml-2 mt-1"
                          variant="primary"
                          @click="closeRemoveInvigilator">
                  No
                </b-button>
              </b-row>
            </template>
          </b-form-group>
        </b-collapse>
        <b-collapse id="collapse-invigilators"
                    class="mt-2 mb-1 w-100">
          <label class="mb-1">Add Invigilators</label>
          <b-form class="q-info-display-grid-container">
            <b-row>
              <b-col cols="7">
                <b-table selectable
                        select-mode="multi"
                        :fields="invigilatorFields"
                        :items="invigilator_multi_select"
                        responsive
                        selected-variant="success"
                        style="height: 110px; width: 250px;"
                        @row-selected="rowSelected"
                        bordered
                        striped>
                  <template slot="selected" slot-scope="{ rowSelected }">
                    <span v-if="rowSelected">✔</span>
                  </template>
                </b-table>
              </b-col>
              <b-col cols="4">
                <b-row class="mb-2"
                      style="font-weight: bold;">
                  Required Invigilators: {{ Math.ceil(actionedExam.number_of_students / 24) }}
                </b-row>
                <template v-if="checkCurrentLength">
                  <b-row class="mb-2"
                        style="font-weight: bold;">
                    Current Invigilators:
                  </b-row >
                  <b-row v-for="current in this.currentInvigilatorList"
                        style="justify-content: center"
                        class="mb-1"
                        v-bind:key="current">
                    {{ current.name }}
                  </b-row>
                </template>
                <b-row style="font-weight: bold;" class="mb-2">
                  Selected Invigilators
                </b-row>
                <b-row v-for="select in selected"
                      style="justify-content: center;"
                      v-bind:key="select">
                  {{ select.name }}
                </b-row>
                <b-row style="justify-content: center;"
                      v-if="this.currentInvigilatorList.length == 0 && this.selected.length == 0"
                      class="mt-2">
                  <font-awesome-icon icon="life-ring"
                                    style="font-size: 3.0rem; color: red;"
                                    class="p-1"/>
                </b-row>
                <b-row style="justify-content: center;"
                      v-else-if="(selected.length > 0 && selected.length < Math.ceil(actionedExam.number_of_students / 24)) ||
                              (selected.length > Math.ceil(actionedExam.number_of_students / 24))"
                      class="mt-2">
                  <font-awesome-icon icon="exclamation-triangle"
                                    style="font-size: 3.0rem; color: #FFC32B;"
                                    class="p-1"/>

                </b-row>
                <b-row style="justify-content: center;"
                      v-else-if="(selected.length == 0 && this.currentInvigilatorList.length < Math.ceil(actionedExam.number_of_students / 24))"
                      class="mt-2">
                  <font-awesome-icon icon="exclamation-triangle"
                                    style="font-size: 3.0rem; color: #FFC32B;"
                                    class="p-1"/>

                </b-row>
                <b-row style="justify-content: center;"
                      v-else-if="(selected.length > 0 && selected.length == Math.ceil(actionedExam.number_of_students / 24))"
                      class="mt-2">
                  <font-awesome-icon icon="check"
                                    style="font-size: 3.0rem; color: green;"
                                    class="p-1"/>
                </b-row>
                <b-row style="justify-content: center;"
                      v-else-if="(this.currentInvigilatorList.length == Math.ceil(actionedExam.number_of_students / 24))"
                      class="mt-2">
                  <font-awesome-icon icon="check"
                                    style="font-size: 3.0rem; color: green;"
                                    class="p-1"/>
                </b-row>
              </b-col>
            </b-row>
          </b-form>
        </b-collapse>
        <!-- Invigilator End -->

        <!-- Shadow Invigilator Start -->
        <b-form-group>
          <b-form-row>
            <template v-if="this.currentShadowInvigilator != null">
            <b-row style="display: flex;" class="w-100 ml-0 mb-2">
                <b-col class="w-50 ml-0 mr-0 pr-1">
                  <b-button v-if="this.changeState && this.shadowInvigilatorBoolean"
                            v-b-toggle.collapse-1
                            variant="primary"
                            @click="setRemove"
                            class="mt-1 ml-0">
                    Change Shadow Invigilator
                  </b-button>
                  <b-button v-else-if="!this.changeState || !this.shadowInvigilatorBoolean"
                            disabled
                            variant="primary"
                            class="mt-1 ml-0">
                    Change Shadow Invigilator
                  </b-button>
                </b-col>
                <b-col class="w-50 ml-1 mr-1 pl-1">
                  <b-button v-if="this.removeState && this.shadowInvigilatorBoolean"
                            v-b-toggle.collapse-2
                            variant="danger"
                            @click="setChange"
                            class="mt-1 mr-0">
                    Remove Shadow Invigilator
                  </b-button>
                  <b-button v-else-if="!this.removeState || !this.shadowInvigilatorBoolean"
                            disabled
                            variant="danger"
                            class="mt-1 mr-0">
                    Remove Shadow Invigilator
                  </b-button>
                </b-col>
              </b-row>
            </template>
            <template v-else>
              <b-button v-b-toggle.collapse-1
                        variant="primary"
                        class="mt-2"
                        style="width: 93%; margin-left: 15px;"
                        @click="setInvigilatorBoolean">
                Add Shadow Invigilator
              </b-button>
            </template>
            <b-collapse id="collapse-1"
                        class="mt-2 mb-2 w-100">
              <b-form-group class="q-info-display-grid-container">
                <label>Shadow Invigilators</label>
                <b-form>
                  <b-row>
                    <b-col cols="7">
                      <b-table selectable
                              select-mode="single"
                              :fields="shadowFields"
                              :items="shadow_invigilator_options"
                              @row-selected="rowSelectedShadow"
                              responsive
                              selected-variant="success"
                              style="height: 150px; width: 250px;"
                              bordered
                              striped
                              class="pl-2">
                        <template slot="selected" slot-scope=" { rowSelected } ">
                          <span v-if="rowSelected">✔</span>
                        </template>
                      </b-table>
                    </b-col>
                    <b-col cols="4">
                      <b-row>
                        Shadow Invigilator Limit: 1
                      </b-row>
                      <b-row v-if="this.currentShadowInvigilator != null"
                            class="mb-1">
                        Current Invigilator
                      </b-row>
                      <b-row v-if="this.currentShadowInvigilator != null"
                            style="justify-content: center;"
                            class="mb-1">
                        {{ this.currentShadowInvigilatorName }}
                      </b-row>
                      <b-row style="font-weight: bold;"
                            class="mb-0">
                        Selected Invigilators
                      </b-row>
                      <b-row v-for="select in selectedShadow"
                            style="justify-content: center;"
                            class="mb-0"
                            v-bind:key="select">
                        {{ select.name }}
                      </b-row>
                      <b-row style="justify-content: center;"
                            v-if="this.selectedShadow"
                            class="mt-2">
                        <font-awesome-icon icon="check"
                                          style="font-size: 3.0rem; color: green;"
                                          class="p-1"/>
                      </b-row>
                    </b-col>
                  </b-row>
                </b-form>
              </b-form-group>
            </b-collapse>
            <b-collapse id="collapse-2"
                        class="mt-2 w-100">
              <b-form-group class="q-info-display-grid-container">
                <b-row class="ml-1">
                  <span style="font-weight: bold;">Current Shadow Invigilator: </span>
                </b-row>
                <b-row class="mb-2"
                      style="justify-content: center;">
                  <span>{{ this.currentShadowInvigilatorName}}</span>
                </b-row>
                <b-row class="ml-1">
                  <span style="font-weight: bold;">Would you like to remove this shadow invigilator?</span>
                </b-row>
                <template>
                  <b-row style="display: flex; justify-content: center;"
                        class="w-100 mb-0">
                    <b-button class="mr-2 mt-1"
                              variant="danger"
                              @click="setSelectedShadowNull">
                      Yes
                    </b-button>
                    <b-button class="ml-2 mt-1"
                              variant="primary"
                              v-b-toggle.collapse-2
                              @click="setChange">
                      No
                    </b-button>
                  </b-row>
                </template>
              </b-form-group>
            </b-collapse>
          </b-form-row>
        </b-form-group>
        <!-- Shadow Invigilator End -->
      </template>

      <div v-if="showMessage"
            class="mb-3"
            style="color: red;">Nothing has changed.  All fields contain their initial values.</div>
      <div style="display: flex; justify-content: flex-end; width: 100%">
        <b-btn class="w-12 mr-2 btn-warning" @click="show">Reset</b-btn>
        <b-btn class="btn-secondary mr-2" @click="cancel">Cancel</b-btn>
        <b-btn v-if="!allowSubmit"
               class="btn-primary disabled"
               @click="showMessage=true">Submit</b-btn>
        <b-btn v-else-if="allowSubmit"
               class="btn-primary"
               @click="submit">Submit</b-btn>
      </div>
    </div>
  </b-modal>
</template>

<script>
  import { mapActions, mapMutations, mapState, mapGetters } from 'vuex'
  import moment from 'moment'
  import zone from 'moment-timezone'
  import DatePicker from 'vue2-datepicker'
  import Vue from 'vue'
  const FileDownload = require('js-file-download')

  export default {
    name: "EditGroupExamBookingModal",
    components: { DatePicker },
    props: ['actionedExam', 'resetExam'],
    data () {
      return {
        invigilator_id: '',
        date: '',
        time: '',
        offsite_location: '',
        eventId: '',
        editedFields: [],
        showMessage: false,
        itemCopy: {},
        currentShadowInvigilator: null,
        currentShadowInvigilatorName: '',
        shadowInvigilator: null,
        selectedShadow: [],
        shadowFields: ['selected', 'name'],
        changeState: true,
        changeInvigilatorState: true,
        removeState: true,
        removeInvigilatorState: true,
        removeFlag: false,
        removeCurrentInvigilatorFlag: false,
        invigilatorFields: ['selected', 'name',],
        fields: {
          exam_received_date: null,
          notes: null,
          event_id: null,
          exam_name: null,
        },
        numberOfInvigilators: 0,
        selected: [],
        currentInvigilatorList: [],
        invigilatorBoolean: true,
        shadowInvigilatorBoolean: true,
        groupInvigilatorBoolean: true,
        exam_received: false,
        examNotReady: false,
      }
    },
    computed: {
      ...mapGetters([
        'role_code',
        'invigilator_dropdown',
        'is_liaison_designate',
        'invigilator_multi_select',
        'is_liaison_designate',
        'shadow_invigilator_options',
        'shadow_invigilators',
      ]),
      ...mapState({
        showModal: state => state.showEditGroupBookingModal,
        invigilators: 'invigilators',
        pesticide_invigilators: 'pesticide_invigilators',
        pesticide_offsite_invigilators: 'pesticide_offsite_invigilators',
        user: 'user',
        shadowInvigilators: state => state.shadowInvigilators,
      }),
      allowSubmit() {
        if (!this.editedFields || this.editedFields.length === 0) {
          return false
        }
        if (this.actionedExam.offsite_location === '_offsite') {
          if (this.editedFields.length >= 3 && this.editedFields.includes('offsite_location')) {
            return true
          }
          return false
        }
        if (this.editedFields.length > 0) {
          return true
        }
        return false
      },
      titleText() {
        switch (this.examType) {
          case 'group':
            return 'Group'
          case 'challenger':
            return 'Monthly Session'
          default:
            return 'Other'
        }
      },
      editedTimezone() {
        if (this.actionedExam && this.actionedExam.booking) {
          return this.actionedExam.booking.office.timezone.timezone_name
        }
        return ''
      },
      examType() {
        if (this.actionedExam && this.actionedExam.exam_type) {
          let { exam_type } = this.actionedExam

          if (exam_type.exam_type_name === 'Monthly Session Exam') {
            return 'challenger'
          }
          if (exam_type.group_exam_ind) {
            return 'group'
          }
          if (exam_type.ita_ind) {
            return 'individual'
          }
          return 'other'
        }
        return ''
      },
      exam() {
        console.log(this.actionedExam)
        if (Object.keys(this.actionedExam).length > 0) {
          return this.actionedExam
        }
        return false
      },
      invigilatorList() {
        console.log(this.invigilator_id)
        let invigilators = (this.actionedExam.office && this.actionedExam.office.office_name == 'Pesticide Offsite') ? this.pesticide_offsite_invigilators : this.pesticide_invigilators;
        return invigilators.map(invigilator => ({ text: invigilator.invigilator_name, value: parseInt(invigilator.invigilator_id) }))
      },
      examReceivedOptions() {
        this.exam_received = this.actionedExam.exam_received_date !== null ? true : false;
        this.fields.exam_received_date = this.actionedExam.exam_received_date
        return [
          { value: false, text: 'No' },
          { value: true, text: 'Yes' },
        ];
      },
      fieldDisabled() {
        if ((this.role_code !== 'GA' && !this.is_liaison_designate) && this.examType != 'other') {
          return true
        }
        return false
      },
      modalVisible: {
        get() {
          return this.showModal
        },
        set(e) {
          this.examNotReady = false
          this.toggleEditGroupBookingModal(e)
        }
      },
    },
    methods: {
      ...mapActions([
        'getBookings',
        'getExams',
        'postBooking',
        'putRequest',
        'downloadExam',
      ]),
      ...mapMutations([
        'toggleEditGroupBookingModal'
      ]),
      cancel() {
        this.toggleEditGroupBookingModal(false)
        this.reset()
        this.resetExam()
        this.currentInvigilatorList = []
        this.selected = []
        this.invigilatorBoolean = true
        this.shadowInvigilatorBoolean = true
        this.changeInvigilatorState = true
        this.removeInvigilatorState = true
        this.groupInvigilatorBoolean = true
      },
      formatDate(d) {
        return new moment(d).format('ddd, MMM DD, YYYY')
      },
      formatTime(d) {
        return new moment(d).format('h:mm a')
      },
      checkDate(e) {
        let date = new moment(this.itemCopy.booking.start_time)
        let event = new moment(e)
        if (event.isBefore(moment(), 'day')) {
          return
        }
        this.date = event
        this.showMessage = false
        if (!this.itemCopy.booking) {
          if (!this.editedFields.includes('date')) {
            this.editedFields.push('date')
          }
          return
        }
        let oldDate = date.format('DDMMYYYY').toString()
        let newDate = new moment(e).format('DDMMYYYY').toString()
        if (newDate === oldDate) {
          if (this.editedFields.includes('date')) {
            let i = this.editedFields.indexOf('date')
            this.editedFields.splice(i,1)
          }
        }
        if (newDate !== date) {
          if (!this.editedFields.includes('date')) {
            this.editedFields.push('date')
          }
        }
      },
      checkTime(e) {
        this.time = e
        this.showMessage = false
        if (!this.itemCopy.booking) {
          if (!this.editedFields.includes('time')) {
            this.editedFields.push('time')
          }
          return
        }
        let time = zone.tz(this.itemCopy.booking.start_time, this.editedTimezone).format('HH:mm').toString()
        let newTime = new moment(e).format('HH:mm').toString()
        if (newTime === time) {
          if (this.editedFields.includes('time')) {
            let i = this.editedFields.indexOf('time')
            this.editedFields.splice(i,1)
          }
        }
        if (newTime !== time) {
          if (!this.editedFields.includes('time')) {
            this.editedFields.push('time')
          }
        }
      },
      hideCollapse(div_id){
        if(document.getElementById(div_id)){
          if(document.getElementById(div_id).classList.contains('show')){
            this.$root.$emit('bv::toggle::collapse', div_id)
          }
        }
      },
      showCollapse(div_id){
        if(document.getElementById(div_id)){
          if(document.getElementById(div_id).style.display === 'none'){
            this.$root.$emit('bv::toggle::collapse', div_id)
          }
        }
      },
      checkInput(e) {
        let { name } = e.target
        let { value } = e.target

        this.showMessage = false
        if (name === 'offsite_location') {
          if (value !== this.itemCopy[name]) {
            if (!this.editedFields.includes(e.target.name)) {
              this.editedFields.push(e.target.name)
            }
            return
          }
          if (value === this.itemCopy[name]) {
            if (this.editedFields.includes(e.target.name)) {
              let i = this.editedFields.indexOf(e.target.name)
              this.editedFields.splice(i, 1)
            }
            return
          }
        }
        if (name === 'event_id') {
          if (value !== this.itemCopy[name]) {
            if (!this.editedFields.includes(e.target.name)) {
              this.editedFields.push(e.target.name)
            }
            return
          }
          if (value === this.itemCopy[name]) {
            if (this.editedFields.includes(e.target.name)) {
              let i = this.editedFields.indexOf(e.target.name)
              this.editedFields.splice(i, 1)
            }
            return
          }
        }
        if (name === 'invigilator_id') {
          if (!this.itemCopy.booking) {
            if (!this.editedFields.includes(name)) {
              this.editedFields.push(name)
            }
            return
          }
          if (value == '') {
            if (this.itemCopy.booking.sbc_staff_invigilated) {
              if (!this.editedFields.includes(name)) {
                this.editedFields.push(name)
              }
              return
            }
            if (this.itemCopy.booking.invigilator_id) {
              if (!this.editedFields.includes(name)) {
                this.editedFields.push(name)
              }
              return
            }
            if (!this.itemCopy.booking.invigiator_id) {
              if (this.editedFields.includes(e.target.name)) {
                let i = this.editedFields.indexOf(e.target.name)
                this.editedFields.splice(i, 1)
              }
            }
            this.invigiator_id = ''
            return
          }
        }
        value = parseInt(value)
        if (value !== this.itemCopy.booking[name]) {
          if (!this.editedFields.includes(e.target.name)) {
            this.editedFields.push(e.target.name)
          }
          this[e.target.name] = e.target.value
          return
        }
        if (value == this.itemCopy.booking[name]) {
          if (this.editedFields.includes(e.target.name)) {
            let i = this.editedFields.indexOf(e.target.name)
            this.editedFields.splice(i, 1)
          }
          this[e.target.name] = e.target.value
          return
        }
      },
      submit() {
        if (!this.actionedExam.booking || !this.actionedExam.booking.start_time) {
          let { exam_id } = this.actionedExam
          let date = new moment(this.date).format('YYYY-MM-DD').toString()
          let time = new moment(this.time).format('HH:mm:ssZ').toString()
          let start = new moment(`${date}T${time}`)
          let end = start.clone().add(parseInt(this.actionedExam.exam_type.number_of_hours), 'h')
          let bookingPost = {
            exam_id,
            invigilator_id: null,
            sbc_staff_invigilated: false,
            start_time: start.clone().utc().format('YYYY-MM-DD[T]HH:mm:ssZ'),
            end_time: end.clone().utc().format('YYYY-MM-DD[T]HH:mm:ssZ'),
            booking_name: this.actionedExam.exam_name,
          }
          if (this.invigilator_id) {
            bookingPost.invigilator_id = this.invigilator_id
            if (this.invigilator_id === 'sbc') {
              bookingPost.sbc_staff_invigilated = true
              bookingPost.invigilator_id = null
            }
          }

          let examPut = {
            offsite_location: this.offsite_location,
            event_id: this.eventId
          }
          this.postBooking(bookingPost).then( booking_id => {
            examPut.booking_id = booking_id
            this.putRequest({url: `/exams/${exam_id}/`, data: examPut}).then( () => {
              this.getBookings().then( () => {
                this.getExams().then( () => {
                  this.cancel()
                })
              })
            })
          })
          return
        }
        let edits = this.editedFields
        let putRequests = []
        let local_timezone_name = this.user.office.timezone.timezone_name
        let edit_timezone_name = this.actionedExam.booking.office.timezone.timezone_name
        let bookingChanges = {}
        let invigilator_id_list = []
        let current_invigilator_id_list = []
        let start
        this.selected.forEach(function(invigilator){
          invigilator_id_list.push(invigilator.value)
        })

        if(this.currentInvigilatorList){
          this.currentInvigilatorList.forEach(function(invigilator) {
          current_invigilator_id_list.push(invigilator.value)
          })
        }

        if (edits.includes('time') || edits.includes('date') || edits.includes('invigilator_id') ||
          edits.includes('shadow_invigilator')) {
          let baseDate = moment(this.date).clone().format('YYYY-MM-DD')
          let baseTime = moment(this.time).clone().format('HH:mm:ss')
          if (local_timezone_name !== edit_timezone_name) {
            start =  zone.tz(`${baseDate}T${baseTime}`, edit_timezone_name)
          }

          if (local_timezone_name === edit_timezone_name) {
            start = moment(`${baseDate}T${baseTime}`)
          }

          let end = start.clone().add(parseInt(this.itemCopy.exam_type.number_of_hours), 'h')

          bookingChanges['start_time'] = start.utc().format('YYYY-MM-DD[T]HH:mm:ssZ')
          bookingChanges['end_time'] = end.utc().format('YYYY-MM-DD[T]HH:mm:ssZ')
          bookingChanges['sbc_staff_invigilated'] = false

          if(this.shadowInvigilator){
            bookingChanges['shadow_invigilator_id'] = this.shadowInvigilator
          } else if (!this.shadowInvigilator && this.currentShadowInvigilator && this.removeFlag){
            bookingChanges['shadow_invigilator_id'] = null
          } else {
            bookingChanges['shadow_invigilator_id'] = this.currentShadowInvigilator
          }

          if(this.actionedExam.is_pesticide) {
            bookingChanges['invigilator_id'] = [this.invigilator_id]
          } else {
            if(current_invigilator_id_list.length === 0){
              bookingChanges['invigilator_id'] = invigilator_id_list
            }
            else if(invigilator_id_list.length >= current_invigilator_id_list.length){
              bookingChanges['invigilator_id'] = invigilator_id_list
            }
            else if(invigilator_id_list.length < current_invigilator_id_list.length){
              bookingChanges['invigilator_id'] = invigilator_id_list
            }
            else {
              bookingChanges['invigilator_id'] = current_invigilator_id_list
            }
          }


          if (this.removeCurrentInvigilatorFlag) {
            bookingChanges.invigilator_id = null
          }

          putRequests.push({url:`/bookings/${this.itemCopy.booking.booking_id}/`, data: bookingChanges})

          // Ensure that removing a shadow invigilator doesn't remove invigilators from booking
          if(this.removeFlag && !this.removeCurrentInvigilatorFlag){
            delete bookingChanges.invigilator_id
          }

          if(this.removeFlag == true){
            putRequests.push({url:`/invigilator/${this.currentShadowInvigilator}/?add=False&subtract=True`})
            this.removeFlag = false
          } else if (this.shadowInvigilator && this.currentShadowInvigilator) {
            putRequests.push({url:`/invigilator/${this.shadowInvigilator}/?add=True&subtract=False`})
            putRequests.push({url:`/invigilator/${this.currentShadowInvigilator}/?add=False&subtract=True`})
          } else if (this.shadowInvigilator && !this.currentShadowInvigilator) {
            putRequests.push({url:`/invigilator/${this.shadowInvigilator}/?add=True&subtract=False`})
          }
        }
        let examChanges = {}
        console.log(edits)
        console.log(this.itemCopy)
        if (edits.includes('offsite_location') || edits.includes('invigilator_id') || edits.includes('exam_received') || edits.includes('event_id')) {
          examChanges['offsite_location'] = this.offsite_location
          examChanges['event_id'] = this.eventId
          examChanges['invigilator_id'] = this.invigilator_id
          examChanges['exam_received_date'] = this.fields.exam_received_date
          putRequests.push({url:`/exams/${this.itemCopy.exam_id}/`, data: examChanges})
        }

        // Ensure that if a user isn't removing either invigilator or shadow invigilator, and submitting a shadow
        // Invigilator, that the submission doesn't remove invigilators from the booking
        if(!this.removeFlag && !this.removeCurrentInvigilatorFlag && bookingChanges.shadow_invigilator_id && bookingChanges.invigilator_id){
          if(bookingChanges.invigilator_id.length == 0){
            delete bookingChanges.invigilator_id
          }
        }

        let promises = []
        putRequests.forEach( put => {
          promises.push(this.putRequest(put))
        })
        Promise.all(promises).then( () => {
          this.getBookings().then( () => {
            this.getExams().then( () => {
              this.cancel()
            })
          })
        })
        this.currentInvigilatorList = []
        this.selected = []
        this.shadowInvigilator = null
        this.invigilatorBoolean = true
        this.shadowInvigilatorBoolean = true
        this.removeFlag = false
        this.removeCurrentInvigilatorFlag = false
        this.changeInvigilatorState = true
        this.removeInvigilatorState = true
        this.groupInvigilatorBoolean = true
      },
      show() {
        let self = this
        this.removeState = true
        this.changeState = true
        this.selectedShadow = null
        this.removeFlag = false
        if(this.actionedExam.booking && this.actionedExam.booking.invigilators && !this.actionedExam.is_pesticide && !this.actionedExam.sbc_managed_ind) {
          this.actionedExam.booking.invigilators.forEach(function(invigilator) {
            let indexOfInvigilator = self.invigilators.findIndex(x => x.invigilator_id == invigilator)
            let index_invigilator_id = self.invigilators[indexOfInvigilator].invigilator_id
            let index_invigilator_name = self.invigilators[indexOfInvigilator].invigilator_name
            let invigilator_json = {name: index_invigilator_name, value: index_invigilator_id}
            self.currentInvigilatorList.push(invigilator_json)
          })
        }
        let tempItem = Object.assign({}, this.actionedExam)
        if (tempItem.booking && tempItem.booking.start_time) {
          let { start_time } = tempItem.booking
          let { timezone_name } = this.actionedExam.booking.office.timezone
          let time = zone.tz(start_time, timezone_name).clone().format('YYYY-MM-DD[T]HH:mm:ss').toString()
          this.time = moment(time).format('YYYY-MM-DD[T]HH:mm:ssZ').toString()
          this.date = zone.tz(start_time, timezone_name).clone().format('YYYY-MM-DD[T]HH:mm:ssZ').toString()
          if (tempItem.booking.sbc_staff_invigilated) {
            this.invigilator_id = 'sbc'
          } else {
            this.invigilator_id = tempItem.booking.invigilator_id
          }
          let currentID = this.currentShadowInvigilator = this.actionedExam.booking.shadow_invigilator_id || null
          let currentName = ''
          this.shadow_invigilators.forEach(function(invigilator) {
            if(invigilator['id'] == currentID){
              currentName = invigilator['name']
            }
          })
          this.currentShadowInvigilatorName = currentName
        }
        this.offsite_location = tempItem.offsite_location === '_offsite' ? null : tempItem.offsite_location
        this.eventId = tempItem.event_id
        if(tempItem.is_pesticide && tempItem.invigilator_id) {
          this.invigilator_id = parseInt(tempItem.invigilator_id)
        }
        console.log('invigilator_id: ', this.invigilator_id)
        this.editedFields = []
        this.itemCopy = tempItem
      },
      reset() {
        this.time = null
        this.date = null
        this.offsite_location = null
        this.eventId = null
        this.invigilator_id = null
        this.itemCopy = {}
        this.editedFields = []
        this.exam_received = false
      },
      rowSelected(invigilator_multi_select){
        this.selected = invigilator_multi_select
        this.editedFields.push('invigilator_id')
      },
      checkCurrentLength(){
        if(this.currentInvigilatorList.length > 0){
          return true
        }
        return false
      },
      rowSelectedShadow(shadows, e){
        this.message = ''
        this.selectedShadow = shadows
         if (this.actionedExam && this.actionedExam.booking) {
          if (this.actionedExam.booking.shadow_invigilator_id !== e) {
            if (!this.editedFields.includes('shadow_invigilator')) {
              this.editedFields.push('shadow_invigilator')
            }
          } else if (this.actionedExam.booking.shadow_invigilator_id == e) {
            if (this.editedFields.includes('shadow_invigilator')) {
              this.editedFields.splice(this.editedFields.indexOf('shadow_invigilator'), 1)
            }
          }
        }
        if(shadows[0] == null){
          this.shadowInvigilator = null
        }else{
          this.shadowInvigilator = shadows[0].id
        }
      },
      setInvigilatorBoolean(){
        this.invigilatorBoolean = !this.invigilatorBoolean
        if(document.getElementById('collapse-invigilators').classList.contains('show')){
          this.hideCollapse('collapse-invigilators')
        }
      },
      setShadowInvigilatorBoolean(){
        this.shadowInvigilatorBoolean = !this.shadowInvigilatorBoolean
        if(document.getElementById('collapse-1').classList.contains('show')){
          this.hideCollapse('collapse-1')
        }
      },
      setChangeShadowInvigilatorBoolean(){
        this.shadowInvigilatorBoolean = !this.shadowInvigilatorBoolean
        this.changeInvigilatorState = !this.changeInvigilatorState
        this.groupInvigilatorBoolean = !this.groupInvigilatorBoolean
      },
      setRemoveShadowInvigilatorBoolean(){
        this.shadowInvigilatorBoolean = !this.shadowInvigilatorBoolean
        this.removeInvigilatorState = !this.removeInvigilatorState
        this.groupInvigilatorBoolean = !this.groupInvigilatorBoolean
      },
      setChange(){
        this.changeState = !this.changeState
        this.changeInvigilatorState = !this.changeInvigilatorState
        this.removeInvigilatorState = !this.removeInvigilatorState
        this.groupInvigilatorBoolean = !this.groupInvigilatorBoolean
        return
      },
      setRemove(){
        this.removeState = !this.removeState
        this.changeInvigilatorState = !this.changeInvigilatorState
        this.removeInvigilatorState = !this.removeInvigilatorState
        this.groupInvigilatorBoolean = !this.groupInvigilatorBoolean
        return
      },
      setSelectedShadowNull(e){
        this.removeFlag = true
         if (this.actionedExam && this.actionedExam.booking) {
          if (this.actionedExam.booking.shadow_invigilator_id !== e) {
            if (!this.editedFields.includes('shadow_invigilator')) {

              this.editedFields.push('shadow_invigilator')
            }
          }
        }
        this.shadowInvigilator = null
        this.submit()
      },
      setSelectedInvigilator(){
        this.removeCurrentInvigilatorFlag = true
        let current_invigilator_array_length = this.currentInvigilatorList.length
        if (this.actionedExam && this.actionedExam.booking) {
          if (current_invigilator_array_length > 0) {
            if (!this.editedFields.includes('invigilator_id')) {
              this.editedFields.push('invigilator_id')
            }
          }
        }
        this.currentInvigilatorList = []
        this.submit()
      },
      closeRemoveInvigilator(){
        if(document.getElementById('collapse-remove-invigilators')
          && document.getElementById('collapse-remove-invigilators').classList.contains('show')){
          this.$root.$emit('bv::toggle::collapse', 'collapse-remove-invigilators')
        }
        this.shadowInvigilatorBoolean = !this.shadowInvigilatorBoolean
        this.changeInvigilatorState = !this.changeInvigilatorState
        this.groupInvigilatorBoolean = !this.groupInvigilatorBoolean
      },
      updateExamReceived(e) {
        let { exam_received_date } = this.fields
        this.editedFields.push('exam_received')
        if(e.type == 'exam-downloaded') {
          this.exam_received = true
        }
        if (e && !exam_received_date) {
          this.fields.exam_received_date = new moment().format('YYYY-MM-DD')
          return
        }
        if (!e) {
          this.fields.exam_received_date = null
        }
      },
       updatePrintExamReceived(strExam) {
        let { exam_received_date } = this.fields
        if(strExam == 'exam-downloaded') {
          this.exam_received = true
        }
        if (strExam && !exam_received_date) {
          this.fields.exam_received_date = new moment().format('YYYY-MM-DD')
          return
        }
      },
      checkAndDownloadExam() {
        this.downloadExam(this.exam)
          .then((resp) => {
            let filename = `${this.exam.exam_id}.pdf`
            FileDownload(resp.data, filename, "application/pdf")
            this.updatePrintExamReceived('exam-downloaded')
          })
          .catch((error) => {
            console.error(error)
            this.examNotReady = true
            setTimeout(() => { this.examNotReady = false }, 15000)
          })
      },
      handleDate(date) {
        console.log(date)
        Vue.set(
          this.fields,
          'exam_received_date',
          date
        )
      },
      invigilatorChanged(value) {
        console.log(value)
        this.invigilator_id = value
        if (!this.editedFields.includes('invigilator_id')) {
          this.editedFields.push('invigilator_id')
        }
      }
    },
  }
</script>

<style scoped>
  .id-grid-1st-col {
    margin-left: auto;
    margin-right: 20px;
  }
  .id-grid-1st-col {
    grid-column: 1 / span 2;
    margin-right: 20px;
  }
  .custom-disabled-fields {
    color: #525252 !important;
  }
  .table-responsive {
    line-height: 5px;
  }
</style>
