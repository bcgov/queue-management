<template>
  <div>
    <template v-if="showPesticideModal">
      <UploadPesticideModal
        :actionedExam="actionedExam"
        :resetExam="resetActionedExam"
      />
    </template>
    <EditExamModal
      :actionedExam="actionedExam"
      :resetExam="resetActionedExam"
    />
    <ReturnExamModal
      :actionedExam="actionedExam"
      :resetExam="resetActionedExam"
    />
    <EditGroupExamBookingModal
      :actionedExam="actionedExam"
      :resetExam="resetActionedExam"
    />
    <DeleteExamModal
      v-if="showDeleteExamModal"
      :actionedExam="actionedExam"
      :resetExam="resetActionedExam"
    />
    <SelectInvigilatorModal />

    <!--  Modal that allows user to choose a new office -->
    <b-modal
      v-model="officeFilterModal"
      size="sm"
      centered
      hide-backdrop
      @hide="resetInvalidOfficeOnHide()"
      hide-header
      hide-footer
    >
      <h5>View Another Office</h5>
      <p>To search, start typing or enter an office #</p>
      <b-form autocomplete="off">
        <b-form-row>
          <OfficeDrop
            columnW="8"
            :office_number="officeNumber"
            :setOffice="setOfficeFilter"
          />
        </b-form-row>
      </b-form>
      <div style="display: flex; justify-content: space-between">
        <b-button class="mr-2 btn-secondary" @click="setHomeOffice"
          >This Office</b-button
        >
        <b-button class="ml-2 btn-primary" @click="officeFilterModal = false"
          >Ok</b-button
        >
      </div>
    </b-modal>

    <!--  Top part of the screen, including filters and pagination.-->
    <div
      style="display: flex; justify-content: space-between"
      class="q-w100-flex-fs"
    >
      <div>
        <b-form inline class="ml-3">
          <!--  The Search label and input box.  -->
          <b-input-group>
            <b-input-group-prepend>
              <label class="mx-1 pt-3 ml-2 my-auto label-text">Search</label>
            </b-input-group-prepend>
            <b-input size="sm" class="mb-1 mt-3" v-model="searchTerm"></b-input>
          </b-input-group>

          <!--  The filters label, and the Office filter.  -->
          <b-input-group class="ml-3">
            <b-input-group-prepend>
              <label class="mx-1 pt-3 mr-2 my-auto label-text">Filters:</label>
            </b-input-group-prepend>
            <b-dd
              v-if="is_pesticide_designate || is_ita2_designate"
              split
              size="sm"
              :variant="
                officeFilter === userOffice || officeFilter === 'default'
                  ? 'primary'
                  : 'warning'
              "
              class="btn-sm mr-2 mt-2"
              :text="officeFilterText"
              @click="officeFilterModal = true"
            >
              <b-dd-item
                v-if="is_pesticide_designate"
                @click="viewAllOfficePesticideExams"
                >View All Offices</b-dd-item
              >
            </b-dd>
          </b-input-group>

          <!--  The Exam Type filter.  -->
          <b-input-group>
            <!--  The Exam Type filter, initial set up if filter not yet set.  -->
            <b-btn-group v-if="selectedExamTypeFilter === ''">
              <b-dropdown
                size="sm"
                v-if="!isPesticideOffice"
                variant="primary"
                text="Exam Type Filters"
                v-model="selectedExamTypeFilter"
                class="mt-2 mr-2"
              >
                <b-dropdown-item
                  v-for="option in examTypeOptions"
                  @click="setExamTypeFilter(option)"
                  v-bind:key="option.value"
                  >{{ option.text }}</b-dropdown-item
                >
              </b-dropdown>
              <b-dropdown
                size="sm"
                v-if="isPesticideOffice"
                variant="primary"
                text="Exam Type Filters"
                v-model="selectedExamTypeFilter"
                class="mt-2 mr-2"
              >
                <b-dropdown-item
                  v-for="option in examTypeOptions"
                  @click="setExamTypeFilter(option)"
                  v-bind:key="option.value"
                  >{{ option.text }}</b-dropdown-item
                >
              </b-dropdown>
            </b-btn-group>

            <!--  The Exam Type filter, if the filter has previously been set.  -->
            <b-btn-group v-else>
              <b-dropdown
                size="sm"
                variant="primary"
                :text="this.selectedExamTypeFilter"
                v-model="selectedExamTypeFilter"
                class="mt-2 mr-2"
              >
                <b-dropdown-item
                  v-for="option in examTypeOptions"
                  @click="setExamTypeFilter(option)"
                  v-bind:key="option.value"
                  >{{ option.text }}</b-dropdown-item
                >
              </b-dropdown>
            </b-btn-group>

            <!--  The Quick Action filter, if ITA designate or GA.  -->
            <template v-if="is_office_manager || role_code === 'GA'">
              <!--  The Quick Action filter if no filter has been set.  -->
              <b-btn-group v-if="selectedQuickActionFilter === ''">
                <b-dropdown
                  size="sm"
                  variant="primary"
                  text="Quick Action Filters"
                  v-model="selectedQuickActionFilter"
                  class="mt-2 mr-2"
                >
                  <b-dropdown-item
                    v-for="option in newQuickActionOptions"
                    @click="setQuickActionFilter(option)"
                    v-bind:key="option.value"
                  >
                    <!--  The various Quick Action options. -->
                    <div style="display: flex; justify-content: space-between">
                      <div class="mr-3">{{ option.text }}</div>
                      <div v-if="option.text === 'Ready'">
                        <font-awesome-icon
                          icon="clipboard-check"
                          style="font-size: 1rem; color: green"
                        />
                      </div>
                      <div v-if="option.text === 'Requires Attention'">
                        <font-awesome-icon
                          icon="life-ring"
                          style="font-size: 1rem; color: red"
                        />
                        <font-awesome-icon
                          icon="exclamation-triangle"
                          style="font-size: 1rem; color: #ffc32b"
                        />
                      </div>
                    </div>
                  </b-dropdown-item>
                </b-dropdown>
              </b-btn-group>

              <!--  The Quick Action filter if a filter has been previously set.  -->
              <b-btn-group v-else>
                <b-dropdown
                  size="sm"
                  variant="primary"
                  :text="this.selectedQuickActionFilter"
                  v-model="selectedQuickActionFilter"
                  class="mt-2 mr-2"
                >
                  <b-dropdown-item
                    v-for="option in newQuickActionOptions"
                    @click="setQuickActionFilter(option)"
                    v-bind:key="option.value"
                  >
                    <!--  The various Quick Action options. -->
                    <div style="display: flex; justify-content: space-between">
                      <div class="mr-3">{{ option.text }}</div>
                      <div v-if="option.text === 'Ready'">
                        <font-awesome-icon
                          icon="clipboard-check"
                          style="font-size: 1rem; color: green"
                        />
                      </div>
                      <div v-if="option.text === 'Requires Attention'">
                        <font-awesome-icon
                          icon="life-ring"
                          style="font-size: 1rem; color: red"
                        />
                        <font-awesome-icon
                          icon="exclamation-triangle"
                          style="font-size: 1rem; color: #ffc32b"
                        />
                      </div>
                    </div>
                  </b-dropdown-item>
                </b-dropdown>
              </b-btn-group>
            </template>

            <!--  The Quick Action filter, if NOT ITA designate or GA.  -->
            <template v-else>
              <b-btn-group v-if="selectedQuickActionFilter === ''">
                <b-dropdown
                  size="sm"
                  variant="primary"
                  text="Quick Action Filters"
                  v-model="selectedQuickActionFilter"
                  class="mt-2 mr-2"
                >
                  <b-dropdown-item
                    v-for="option in newQuickActionOptionsNoOEM"
                    @click="setQuickActionFilter(option)"
                    v-bind:key="option.value"
                  >
                    <div style="display: flex; justify-content: space-between">
                      <div class="mr-3">{{ option.text }}</div>
                      <div v-if="option.text === 'Ready'">
                        <font-awesome-icon
                          icon="clipboard-check"
                          style="font-size: 1rem; color: green"
                        />
                      </div>
                      <div v-if="option.text === 'Requires Attention'">
                        <font-awesome-icon
                          icon="life-ring"
                          style="font-size: 1rem; color: red"
                        />
                        <font-awesome-icon
                          icon="exclamation-triangle"
                          style="font-size: 1rem; color: #ffc32b"
                        />
                      </div>
                    </div>
                  </b-dropdown-item>
                </b-dropdown>
              </b-btn-group>
              <b-btn-group v-else>
                <b-dropdown
                  size="sm"
                  variant="primary"
                  :text="this.selectedQuickActionFilter"
                  v-model="selectedQuickActionFilter"
                  class="mt-2 mr-2"
                >
                  <b-dropdown-item
                    v-for="option in newQuickActionOptionsNoOEM"
                    @click="setQuickActionFilter(option)"
                    v-bind:key="option.value"
                  >
                    <div style="display: flex; justify-content: space-between">
                      <div class="mr-3">{{ option.text }}</div>
                      <div v-if="option.text === 'Ready'">
                        <font-awesome-icon
                          icon="clipboard-check"
                          style="font-size: 1rem; color: green"
                        />
                      </div>
                      <div v-if="option.text === 'Requires Attention'">
                        <font-awesome-icon
                          icon="life-ring"
                          style="font-size: 1rem; color: red"
                        />
                        <font-awesome-icon
                          icon="exclamation-triangle"
                          style="font-size: 1rem; color: #ffc32b"
                        />
                      </div>
                    </div>
                  </b-dropdown-item>
                </b-dropdown>
              </b-btn-group>
            </template>
          </b-input-group>
          <!--  End of all the Exam Type filter.  -->
        </b-form>
      </div>
      <!--  End of all the Exam Type filter division.  -->

      <!--  Display pagination options, if too many items for the screen. -->
      <div>
        <b-pagination
          :total-rows="totalRows"
          :per-page="10"
          v-if="filteredExams().length > 10"
          v-model="page"
          class="mb-0 pt-2 mr-4 mt-1"
          style="display: flex; justify-content: flex-end"
        />
      </div>
    </div>
    <!--  End of top part of the screen, including filters and pagination.-->

    <!--  Display of exams.  -->
    <div :style="tableStyle" class="my-0 mx-3">
      <b-table
        :items="filteredExams()"
        :fields="fields"
        sort-by="scheduled"
        :sort-desc="true"
        head-variant="light"
        :style="availableH"
        empty-text="There are no exams that match this filter criteria"
        small
        :sort-compare="sortCompare"
        outlined
        @row-clicked="clickModalRow"
        hover
        show-empty
        responsive
        :current-page="page"
        :per-page="10"
        :filter="searchTerm"
        v-if="!isLoading"
        id="exam_inventory_table"
      >
        <!--  Field 1 - Event id??? Don't see it.  -->
        <!--  Field 2 - Exam Type -->
        <template #cell(exam_type_name)="row">{{
          row.item.exam_type.exam_type_name
        }}</template>

        <!--  Field 3 - Exam name??? Don't see it.  -->
        <!--  Field 4 - Scheduled Date -->
        <template #cell(start_time)="row">
          <span v-if="!row.item.booking">-</span>
          <span
            v-else-if="checkStartDate(row.item.booking.start_time,row.item.exam_returned_date)"
            class="expired"
            >{{ formatDate(row.item.booking.start_time) }}</span
          >
          <span v-else>{{ formatDate(row.item.booking.start_time) }}</span>
        </template>

        <!--  Field 5 - Exam method??? Don't see it.  -->
        <!--  Field 6 - Expiry Date. -->
        <template #cell(expiry_date)="row">
          <span
            v-if="
              row.item.exam_type.exam_type_name === 'Monthly Session Exam' &&
              !checkExpiryDate(row.item.expiry_date,row.item.exam_returned_date)
            "
            >–</span
          >
          <span
            v-else-if="
              row.item.exam_type.group_exam_ind &&
              !checkExpiryDate(row.item.expiry_date,row.item.exam_returned_date)
            "
            >–</span
          >
          <span
            v-else-if="checkExpiryDate(row.item.expiry_date,row.item.exam_returned_date)"
            class="expired"
            >{{ formatDate(row.item.expiry_date) }}</span
          >
          <span v-else>{{ formatDate(row.item.expiry_date) }}</span>
        </template>

        <!--  Field 7 - Exam Received -->
        <template #cell(exam_received)="row">{{
          row.item.exam_received_date ? 'Yes' : 'No'
        }}</template>

        <!--  Field 8 - Candidate name??? Don't see it.  -->
        <!--  Field 9 - Notes??? Don't see it.  -->
        <!--  Field 10 - The Status column/flag -->
        <template #cell(scheduled)="row">
          <font-awesome-icon
            v-if="!row.detailsShowing"
            :icon="statusIcon(row.item).icon"
            @click="row.toggleDetails"
            class="m-0 p-0 icon-cursor-hover"
            :style="statusIcon(row.item).style"
          />
          <b-button
            v-if="row.detailsShowing"
            variant="link"
            style="padding: 0px"
            @click="row.toggleDetails"
            >Hide</b-button
          >
        </template>

        <!--  Expanded row - Details and still required. -->
        <template #row-details="row">
          <!--  If no items to be done, display some (debugging?) info. -->
          <template v-if="stillRequires(row.item).length === 0">
            <div class="details-slot-div">
              <template v-for="(val, key) in readyDetailsMap(row.item)">
                <div class="ml-3 mt-1" style="flex-grow: 1" v-bind:key="key">
                  <strong>{{ key }}:</strong>
                  {{ val }}
                </div>
              </template>
              <div style="flex-grow: 6"></div>
            </div>
          </template>

          <!--  There are some items to be done.  Display them. -->
          <template v-if="stillRequires(row.item).length > 0">
            <div class="details-slot-div">
              <!--  The Still Requires info. -->
              <div class="ml-3" style="font-size: 1rem; flex-grow: 1">
                Still Requires:
              </div>
              <template v-for="(req, i) in stillRequires(row.item)">
                <div :key="i + 'it'" class="ml-3 mt-1" style="flex-grow: 1">
                  {{ req }}
                </div>
              </template>
              <div style="flex-grow: 6" />
              <!--  The Details info. -->
              <div style="flex-grow: 1; font-size: 1rem">Details</div>
              <template v-for="(val, key) in readyDetailsMap(row.item)">
                <div class="ml-3 mt-1" style="flex-grow: 1" :key="key">
                  <strong>{{ key }}:</strong>
                  {{ val }}
                </div>
              </template>
              <div style="flex-grow: 12" />
            </div>
          </template>
        </template>

        <!--  Field 11 - the actions column.-->
        <template #cell(actions)="row">
          <!--  The various dropdown actions allowed.  -->
          <b-dropdown
            variant="link"
            no-caret
            size="sm"
            class="pl-0 ml-0 mr-3"
            id="nav-dropdown"
            right
          >
            <!--  The down caret to open up the dropdown list.  -->
            <template slot="button-content">
              <font-awesome-icon
                icon="caret-down"
                style="
                  padding: -2px;
                  margin: -2px;
                  font-size: 1rem;
                  color: dimgray;
                "
              />
            </template>

            <!--  Various options, if the exam hasn't been returned.  -->
            <template v-if="!row.item.exam_returned_date">
              <!--  Options for if you're editing an exam for the office you're in.  -->
              <template
                v-if="officeFilter == userOffice || officeFilter == 'default'"
              >
                <!--  Options for Monthly Session Exam.  -->
                <template
                  v-if="
                    row.item.exam_type.exam_type_name === 'Monthly Session Exam'
                  "
                >
                  <template v-if="row.item.offsite_location">
                    <b-dropdown-item
                      size="sm"
                      v-if="row.item.offsite_location"
                      @click="editGroupBooking(row.item)"
                      >{{
                        checkInvigilator(row.item)
                          ? 'Update Booking'
                          : 'Add Invigilator'
                      }}</b-dropdown-item
                    >
                  </template>

                  <template
                    v-if="!row.item.offsite_location || row.item.is_pesticide"
                  >
                    <b-dropdown-item
                      size="sm"
                      v-if="
                        row.item.booking &&
                        Object.keys(row.item.booking).length > 0
                      "
                      @click="updateCalendarBooking(row.item)"
                      >{{
                        checkInvigilator(row.item)
                          ? 'Update Booking'
                          : 'Edit/Print/Add Invigilator'
                      }}</b-dropdown-item
                    >
                    <b-dropdown-item
                      size="sm"
                      v-if="
                        !row.item.booking ||
                        Object.keys(row.item.booking).length === 0
                      "
                      @click="addCalendarBooking(row.item)"
                      >Schedule Exam</b-dropdown-item
                    >
                  </template>
                </template>

                <!--  Options for group exam ind (???).  -->
                <template v-else-if="row.item.exam_type.group_exam_ind">
                  <b-dropdown-item
                    size="sm"
                    v-if="row.item.offsite_location || row.item.is_pesticide"
                    @click="editGroupBooking(row.item)"
                    >{{
                      checkInvigilator(row.item)
                        ? 'Update Booking'
                        : 'Edit/Print/Add Invigilator'
                    }}</b-dropdown-item
                  >
                </template>

                <!--  Options for a pesticide exam -->
                <template v-else-if="row.item.exam_type.pesticide_exam_ind">
                  <template template v-if="row.item.sbc_managed_ind === 1">
                    <b-dropdown-item
                      size="sm"
                      v-if="
                        row.item.booking &&
                        Object.keys(row.item.booking).length > 0
                      "
                      @click="updateCalendarBooking(row.item)"
                      >{{
                        checkInvigilator(row.item)
                          ? 'Update Booking'
                          : 'Edit/Print/Add Invigilator'
                      }}</b-dropdown-item
                    >
                    <b-dropdown-item
                      size="sm"
                      v-if="
                        !row.item.booking ||
                        Object.keys(row.item.booking).length === 0
                      "
                      @click="addCalendarBooking(row.item)"
                      >Schedule Exam</b-dropdown-item
                    >
                  </template>
                  <template v-else>
                    <b-dropdown-item
                      size="sm"
                      v-if="
                        row.item.booking &&
                        Object.keys(row.item.booking).length > 0
                      "
                      @click="updateCalendarBooking(row.item)"
                      >{{
                        checkInvigilator(row.item)
                          ? 'Update Booking'
                          : 'Edit/Print/Add Invigilator'
                      }}</b-dropdown-item
                    >
                    <b-dropdown-item
                      size="sm"
                      v-if="
                        !row.item.booking ||
                        Object.keys(row.item.booking).length === 0
                      "
                      @click="addCalendarBooking(row.item)"
                      >Schedule Exam</b-dropdown-item
                    >
                  </template>
                </template>

                <!--  Options for all other exams.  -->
                <template v-else>
                  <template
                    v-if="
                      row.item.offsite_location &&
                      row.item.offsite_location === '_offsite'
                    "
                  >
                    <b-dropdown-item
                      size="sm"
                      v-if="
                        !row.item.booking ||
                        Object.keys(row.item.booking).length === 0
                      "
                      @click="editGroupBooking(row.item)"
                      >Schedule Exam</b-dropdown-item
                    >
                  </template>
                  <template
                    v-if="
                      row.item.offsite_location &&
                      row.item.offsite_location !== '_offsite'
                    "
                  >
                    <b-dropdown-item
                      size="sm"
                      v-if="row.item.offsite_location"
                      @click="editGroupBooking(row.item)"
                      >{{
                        checkInvigilator(row.item)
                          ? 'Update Booking'
                          : 'Add Invigilator'
                      }}</b-dropdown-item
                    >
                  </template>
                  <template template v-if="!row.item.offsite_location">
                    <b-dropdown-item
                      size="sm"
                      v-if="
                        row.item.booking &&
                        Object.keys(row.item.booking).length > 0
                      "
                      @click="updateCalendarBooking(row.item)"
                      >{{
                        checkInvigilator(row.item)
                          ? 'Update Booking'
                          : 'Add Invigilator'
                      }}</b-dropdown-item
                    >
                    <b-dropdown-item
                      size="sm"
                      v-if="
                        !row.item.booking ||
                        Object.keys(row.item.booking).length === 0
                      "
                      @click="checkExpiryDateAndAddCalendarBooking(row.item)"
                      >Schedule Exam</b-dropdown-item
                    >
                  </template>
                </template>

                <b-dropdown-item
                  size="sm"
                  v-if="
                    !(
                      row.item.exam_type.group_exam_ind && row.item.is_pesticide
                    )
                  "
                  @click="editExamDetails(row.item)"
                  >Edit/Print Exam Details</b-dropdown-item
                >
                <b-dropdown-item size="sm" @click="returnExam(row.item)">{{
                  row.item.is_pesticide ? 'Upload Exam' : 'Return Exam'
                }}</b-dropdown-item>
              </template>

              <!--  Options for if you're editing an exam for a different office.  -->
              <template
                v-if="officeFilter != userOffice && officeFilter != 'default'"
              >
                <b-dropdown-item
                  size="sm"
                  v-if="row.item.offsite_location"
                  @click="editGroupBooking(row.item)"
                  >Edit Booking</b-dropdown-item
                >
                <b-dropdown-item size="sm" @click="editExamDetails(row.item)"
                  >Edit/Print Exam Details</b-dropdown-item
                >
                <b-dropdown-item
                  size="sm"
                  v-if="row.item.is_pesticide"
                  @click="returnExam(row.item)"
                  >Upload Exam</b-dropdown-item
                >
              </template>
            </template>

            <!--  If a returned exam, show Edit Return Details option.  -->
            <template v-if="examReturnedFilter(row.item)">
              <b-dropdown-item size="sm" @click="returnExam(row.item)"
                >Edit Return Details</b-dropdown-item
              >
            </template>
          </b-dropdown>
        </template>
        <template #cell(office)="row">{{
          row.item.office.office_name
        }}</template>
      </b-table>
      <div class="text-center" v-if="isLoading">
        <b-spinner variant="primary" label="Loading"></b-spinner>
      </div>
    </div>
    <!--  End of exam display.  -->
    <div data-app>
      <v-dialog
            v-model="expiryNotificationDialog"
            max-width="290"
          >
        <v-card>
          <v-card-title class="headline">
            Schedule Exam
          </v-card-title>
          <v-card-text>
            This exam has expired on {{ examExpiryDateScheduling }}. Scheduling is not allowed.
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="red darken-1"
              text
              @click="expiryNotificationDialog = false"
            >
              OK
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script lang="ts">

import { Action, Getter, Mutation, State } from 'vuex-class'
import { Component, Prop, Vue } from 'vue-property-decorator'

import moment from 'moment'
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
import EditExamModal from './edit-exam-form-modal.vue'
import EditGroupExamBookingModal from './edit-group-exam-modal.vue'
import SelectInvigilatorModal from './select-invigilator-modal.vue'
import FailureExamAlert from './failure-exam-alert.vue'
import OfficeDrop from './office-drop.vue'
import ReturnExamModal from './return-exam-form-modal.vue'
import SuccessExamAlert from './success-exam-alert.vue'
import DeleteExamModal from './delete-exam-modal.vue'
import AddCitizen from '../AddCitizen/add-citizen.vue'
import zone from 'moment-timezone'
import UploadPesticideModal from './upload-pesticide-exam.vue'

@Component({
  components: {
    UploadPesticideModal,
    AddCitizen,
    DeleteExamModal,
    EditExamModal,
    EditGroupExamBookingModal,
    FailureExamAlert,
    OfficeDrop,
    ReturnExamModal,
    SuccessExamAlert,
    SelectInvigilatorModal
  },
  computed: {
    ...mapState({
      showAllPesticide: (state: any) => state.addExamModule.showAllPesticideExams,
      showPesticideModal: (state: any) => state.addExamModule.uploadPesticideModalVisible
    })

  }
})
export default class ExamInventoryTable extends Vue {
  @State('bookings') private bookings!: any
  @State('calendarSetup') private calendarSetup!: any
  @State('calendarEvents') private calendarEvents!: any
  @State('exams') private exams!: any
  @State('inventoryFilters') private inventoryFilters!: any
  @State('selectedExamType') private selectedExamType!: any
  @State('selectedExamTypeFilter') private selectedExamTypeFilter!: any
  @State('selectedQuickAction') private selectedQuickAction!: any
  @State('selectedQuickActionFilter') private selectedQuickActionFilter!: any
  @State('showDeleteExamModal') private showDeleteExamModal!: any
  @State('showEditExamModal') private showEditExamModal!: any
  @State('showExamInventoryModal') private showExamInventoryModal!: any
  @State('showReturnExamModalVisible') private showReturnExamModalVisible!: any
  @State('offices') private offices!: any
  @State('user') private user!: any
  @State('invigilators') private invigilators!: any

  private readonly showAllPesticide!: any

  private readonly showPesticideModal!: any

  private expiryNotificationDialog: boolean = false
  private examExpiryDateScheduling: string = ''

  @Getter('calendar_events') private calendar_events!: any;
  @Getter('exam_inventory') private exam_inventory!: any;
  @Getter('role_code') private role_code!: any;
  @Getter('is_ita2_designate') private is_ita2_designate!: any;
  @Getter('is_pesticide_designate') private is_pesticide_designate!: any;
  @Getter('is_office_manager') private is_office_manager!: any;

  @Action('getBookings') public getBookings: any
  @Action('getExams') public getExams: any
  @Action('getExamsForOffice') public getExamsForOffice: any
  @Action('getInvigilators') public getInvigilators: any
  @Action('getOffices') public getOffices: any
  @Action('updateExamStatus') public updateExamStatus: any

  @Mutation('setEditedBooking') public setEditedBooking: any
  @Mutation('setEditedBookingOriginal') public setEditedBookingOriginal: any
  @Mutation('setEditExamInfo') public setEditExamInfo: any
  @Mutation('setInventoryFilters') public setInventoryFilters: any
  @Mutation('setSelectedExam') public setSelectedExam: any
  @Mutation('setSelectedExamType') public setSelectedExamType: any
  @Mutation('setSelectedExamTypeFilter') public setSelectedExamTypeFilter: any
  @Mutation('setSelectedQuickAction') public setSelectedQuickAction: any
  @Mutation('setSelectedQuickActionFilter') public setSelectedQuickActionFilter: any
  @Mutation('toggleDeleteExamModal') public toggleDeleteExamModal: any
  @Mutation('toggleEditBookingModal') public toggleEditBookingModal: any
  @Mutation('toggleEditExamModal') public toggleEditExamModal: any
  @Mutation('toggleEditGroupBookingModal') public toggleEditGroupBookingModal: any
  @Mutation('toggleExamInventoryModal') public toggleExamInventoryModal: any
  @Mutation('toggleSelectInvigilatorModal') public toggleSelectInvigilatorModal: any
  @Mutation('toggleReturnExamModal') public toggleReturnExamModal: any
  @Mutation('toggleScheduling') public toggleScheduling: any
  @Mutation('toggleUploadExamModal') public toggleUploadExamModal: any

  public actionedExam: any = {}
  public detailsRowSetup: any = null
  public searchTerm: any = null
  public officeFilterModal: any = false
  public page: any = 1
  public tableStyle: any = null
  public buttonH: any = 45
  public qLengthH: any = 28
  public totalH: any = 0
  public examTypeOptions: any = [
    { text: 'Individual', value: 'individual' },
    { text: 'Group', value: 'group' },
    { text: 'All', value: 'all' }
  ]

  public newQuickActionOptions: any = [
    { text: 'Ready', value: 'ready' },
    { text: 'Requires Attention', value: 'require_attention' },
    { text: 'Office Exam Manager Action Items', value: 'oemai' },
    { text: 'Expired', value: 'expired' },
    { text: 'Returned', value: 'returned' }
  ]

  public newQuickActionOptionsNoOEM: any = [
    { text: 'Ready', value: 'ready' },
    { text: 'Requires Attention', value: 'require_attention' },
    { text: 'Expired', value: 'expired' },
    { text: 'Returned', value: 'returned' }
  ]

  public isLoading: boolean = false

  get availableH () {
    const h = this.totalH - 240
    return { height: `${h}px`, border: '1px solid dimgrey' }
  }

  get isPesticideOffice () {
    // Karim has envisioned creating a pesticide office (an office in offices table like Victoria or
    // 100 mile house, etc) that isn't a real office but which would hold in-progress pesticide exams
    // and trigger a different setup of the exam_inventory_table
    // as this is not implemented yet, this computed value can simply return true or false depending on what
    // features of the exam_inventory_table you want to see/use/test
    return true
  }

  get fields () {
    if (!this.showExamInventoryModal) {
      const pesticideFields: any = [
        { key: 'office', sortable: true, thStyle: 'width: 5%' }

      ]
      const fields: any = [
        { key: 'event_id', label: 'Event ID', sortable: false, thStyle: 'width: 6%' },
        { key: 'exam_type_name', label: 'Exam Type', sortable: true },
        { key: 'exam_name', label: 'Exam Name', sortable: true, thStyle: 'width: 11%' },
        { key: 'start_time', label: 'Scheduled Date', sortable: true, thStyle: 'width: 9%' },
        { key: 'exam_method', label: 'Method', sortable: false, thStyle: 'width: 5%' },
        { key: 'expiry_date', label: 'Expiry Date', sortable: true, thStyle: 'width: 8%' },
        { key: 'exam_received', label: 'Received?', sortable: true, thStyle: 'width: 5%' },
        { key: 'notes', label: 'Notes', sortable: false, thStyle: 'width: 21%' },
        { key: 'scheduled', label: 'Status', sortable: true, thStyle: 'width: 5%', tdClass: 'text-center' },
        { key: 'actions', label: 'Actions', sortable: false, thStyle: 'width: 5%' },
        {
          key: 'examinee_name',
          label: 'Candidate Name',
          sortable: true,
          thStyle: this.showAllPesticide ? 'width: 7%' : 'width: 12%'
        }
      ]
      if (!this.showAllPesticide) {
        return fields
      }
      if (this.showAllPesticide) {
        return fields.concat(pesticideFields)
      }
    }
    if (this.showExamInventoryModal) {
      return [
        { key: 'event_id', label: 'Event ID', sortable: false, thStyle: 'width: 6%' },
        { key: 'exam_type.exam_type_name', label: 'Exam Type', sortable: true },
        { key: 'exam_name', label: 'Exam Name', sortable: true, thStyle: 'width: 15%' },
        { key: 'booking.start_time', label: 'Scheduled Date', sortable: true, thStyle: 'width: 9%' },
        { key: 'exam_method', label: 'Method', sortable: true, thStyle: 'width: 5%' },
        { key: 'expiry_date', label: 'Expiry Date', sortable: true, thStyle: 'width: 8%' },
        { key: 'exam_received', label: 'Received?', sortable: true, thStyle: 'width: 5%' },
        { key: 'examinee_name', label: 'Candidate Name', sortable: true, thStyle: 'width: 20%' },
        { key: 'notes', label: 'Notes', sortable: false }
      ]
    }
  }

  get officeFilter () {
    if (this.inventoryFilters && this.inventoryFilters.office_number) {
      return this.inventoryFilters.office_number
    }
    return ''
  }

  get officeFilterText () {
    if (this.showAllPesticide) {
      return 'Exams from All Offices'
    }
    return 'Office # ' + this.officeNumber + ' - ' + this.officeName
  }

  get officeName () {
    if (this.offices && this.offices.length > 0) {
      const office = this.offices.find(office => office.office_number == this.officeNumber)
      if (office) {
        return office.office_name
      }
      return 'Invalid Office'
    }
    if (this.user && this.user.office_id) {
      return this.user.office.office_name
    }
    return ''
  }

  get officeNumber () {
    if (this.inventoryFilters && this.inventoryFilters.office_number) {
      const { office_number } = this.inventoryFilters
      if (this.inventoryFilters.office_number === 'pesticide_offsite') {
        const office = (this.offices.find(office => office.office_name == 'Pesticide Offsite'))
        return office.office_number
      } else if (office_number !== 'default') {
        return office_number
      }
    }
    if (this.user && this.user.office_id) {
      return this.user.office.office_number
    }
    return ''
  }

  get totalRows () {
    const exams = this.filteredExams() || null
    if (exams && exams.length > 0) {
      return exams.length
    }
    return 10
  }

  get userOffice () {
    if (this.user && this.user.office_id) {
      return this.user.office.office_number
    }
    return ''
  }

  checkExpiryDateAndAddCalendarBooking (item) {
    if (moment(item.expiry_date).isValid() && moment(item.expiry_date).isBefore(moment(), 'day')) {
      this.examExpiryDateScheduling = moment(item.expiry_date).format('MMMM DD, YYYY')
      this.expiryNotificationDialog = true
    } else {
      this.addCalendarBooking(item)
    }
  }

  addCalendarBooking (item) {
    this.toggleScheduling(true)
    item.referrer = 'inventory'
    this.setSelectedExam(item)
    this.$router.push('/booking')
    this.toggleExamInventoryModal(false)
  }

  viewAllOfficePesticideExams () {
    this.$store.dispatch('getAllPesticideExams')
    this.$store.commit('toggleShowAllPesticideExams', false)
  }

  checkChallenger (item) {
    if (item.event_id && item.booking.invigilator_id && item.number_of_students) {
      return true
    }
    return false
  }

  checkInvigilator (item) {
    let length_of_invigilator_array: any = null
    const number_of_invigilators = Math.ceil(item.number_of_students / 24)
    if (!item.booking) {
      length_of_invigilator_array = 0
    } else {
      length_of_invigilator_array = item.booking.invigilators.length
    }
    if (item.exam_type.group_exam_ind === 1 && length_of_invigilator_array == 0) {
      return false
    } else if (item.exam_type.group_exam_ind === 1 && length_of_invigilator_array >= number_of_invigilators) {
      return true
    } else if (item.exam_type.group_exam_ind === 1 && length_of_invigilator_array < number_of_invigilators) {
      return false
    } else if (item.exam_type.group_exam_ind === 0 && item.booking && item.exam_type.exam_type_name !== 'Monthly Session Exam' &&
      (number_of_invigilators == 1 || item.booking.sbc_staff_invigilated)) {
      return true
    } else if (item.exam_type.exam_type_name === 'Monthly Session Exam' &&
      length_of_invigilator_array >= number_of_invigilators) {
      return true
    } else if (item.exam_type.exam_type_name === 'Monthly Session Exam' &&
      length_of_invigilator_array < number_of_invigilators) {
      return false
    }
    return false
  }

  clickModalRow (item) {
    if (this.showExamInventoryModal) {
      this.toggleScheduling(true)
      this.setSelectedExam(item)
      this.$router.push('/booking')
      this.toggleExamInventoryModal(false)
    }
  }

  editExamDetails (item) {
    this.actionedExam = item
    this.toggleEditExamModal(true)
  }

  editGroupBooking (item) {
    this.actionedExam = item
    this.toggleEditGroupBookingModal(true)
  }

  examReturnedFilter (item) {
    if (item.exam_returned_date && (this.officeFilter === this.userOffice || this.officeFilter === 'default')) {
      return true
    }
    return false
  }

  examReturnedAttention (item) {
    if (item.exam_returned_date) {
      return true
    }
    return false
  }

  filterByGroup (ex) {
    if (ex.exam_type.exam_type_name === 'Monthly Session Exam' || ex.exam_type.group_exam_ind) {
      return true
    }
    if (ex.number_of_students && parseInt(ex.number_of_students) > 1) {
      return true
    }
    return false
  }

  filterByExpiry (ex) {
    if (moment(ex.expiry_date).isValid()) {
      if (moment(ex.expiry_date).isBefore(moment(), 'day')) {
        return true
      }
    }
    return false
  }

  filterByScheduled (ex) {
    if (this.inventoryFilters.expiryFilter === 'current') {
      if (ex.booking) {
        if (moment(ex.booking.start_time).isBefore(moment(), 'day')) {
          return false
        }
      }
    }
    if (ex.exam_received_date) {
      if (ex.booking && ((ex.booking.invigilators.length > 0) || ex.booking.sbc_staff_invigilated)) {
        if (ex.booking.invigilator && ex.booking.invigilator.deleted) {
          return false
        }
        if (ex.exam_type.exam_type_name !== 'Monthly Session Exam') {
          return true
        }
        if (ex.exam_type.exam_type_name === 'Monthly Session Exam') {
          if (ex.number_of_students && ex.event_id) {
            return true
          }
        }
      }
    }
    return false
  }

  checkAllAttention (ex) {
    if (this.examReturnedAttention(ex)) {
      return false
    }
    if (ex.booking && !ex.exam_received_date) {
      return true
    }
    if (!ex.booking) {
      return true
    }
    if (this.filterByExpiry(ex)) {
      return true
    }
    if (this.filterByGroup(ex)) {
      if (ex.booking && (this.checkInvigilator(ex))) {
        return false
      } else if (ex.booking && (!this.checkInvigilator(ex))) {
        return true
      }
    }
    if (ex.booking) {
      if (moment(ex.booking.start_time).isValid()) {
        if (moment(ex.booking.start_time).isBefore(moment(), 'day')) {
          return true
        }
      }
    }
    if (ex.exam_type.exam_type_name === 'Monthly Session Exam') {
      if (!ex.number_of_students || !ex.event_id) {
        return true
      }
    }
    return false
  }

  checkIndividualAttention (ex) {
    if (this.filterByGroup(ex)) {
      return false
    }
    if (this.examReturnedAttention(ex)) {
      return false
    }
    if (ex.booking && !ex.exam_received_date) {
      return true
    }
    if (!ex.booking) {
      return true
    }
    if (this.filterByExpiry(ex)) {
      return true
    }
    if (ex.booking) {
      if (moment(ex.booking.start_time).isValid()) {
        if (moment(ex.booking.start_time).isBefore(moment(), 'day')) {
          return true
        }
      }
    }
    return false
  }

  checkGroupAttention (ex) {
    if (this.filterByGroup(ex) && this.examReturnedAttention(ex)) {
      return false
    }
    if (this.filterByGroup(ex) && ex.booking && !ex.exam_received_date) {
      return true
    }
    if (this.filterByGroup(ex)) {
      if (ex.booking && (this.checkInvigilator(ex))) {
        return false
      } else if (ex.booking && (!this.checkInvigilator(ex))) {
        return true
      }
    }
    if (this.filterByGroup(ex) && ex.booking) {
      if (moment(ex.booking.start_time).isValid()) {
        if (moment(ex.booking.start_time).isBefore(moment(), 'day')) {
          return true
        }
      }
    }
    if (ex.exam_type.exam_type_name === 'Monthly Session Exam') {
      if (!ex.number_of_students || !ex.event_id) {
        return true
      }
    }
    return false
  }

  checkOEMAllAttention (ex) {
    if (this.examReturnedAttention(ex)) {
      return false
    }
    if (ex.is_pesticide && !ex.exam_received_date) {
      return true
    }
    if (this.filterByExpiry(ex)) {
      return true
    }
    if (this.filterByGroup(ex)) {
      if (!this.checkInvigilator(ex)) {
        return true
      }
    }
    if (ex.booking) {
      if (moment(ex.booking.start_time).isValid()) {
        if (moment(ex.booking.start_time).isBefore(moment(), 'day')) {
          return true
        }
      }
    }
    return false
  }

  checkOEMIndividualAttention (ex) {
    if (this.filterByGroup(ex)) {
      return false
    }
    if (this.examReturnedAttention(ex)) {
      return false
    }
    if (ex.is_pesticide && !ex.exam_received_date) {
      return true
    }
    if (this.filterByExpiry(ex)) {
      return true
    }
    if (ex.booking) {
      if (moment(ex.booking.start_time).isValid()) {
        if (moment(ex.booking.start_time).isBefore(moment(), 'day')) {
          return true
        }
      }
    }
    return false
  }

  checkOEMGroupAttention (ex) {
    if (this.filterByGroup(ex) && this.examReturnedAttention(ex)) {
      return false
    }
    if (this.filterByGroup(ex) && this.filterByExpiry(ex)) {
      return true
    }
    if (this.filterByGroup(ex) && ex.is_pesticide && !ex.exam_received_date) {
      return true
    }
    if (this.filterByGroup(ex)) {
      if (ex.booking) {
        if (moment(ex.booking.start_time).isValid()) {
          if (moment(ex.booking.start_time).isBefore(moment(), 'day')) {
            return true
          }
        }
        if (!this.checkInvigilator(ex)) {
          return true
        }
      }
    }
    return false
  }

  checkExpiryDate (date, exam_returned_date) {
    if (exam_returned_date != null) {      
      return false
    }
    if (moment(date).isValid() && moment(date).isBefore(moment(), 'day')) {
      return true
    }
    return false
  }

  checkStartDate (date, exam_returned_date) {    
    if (exam_returned_date != null) {      
      return false
    }
    if (moment(date).isValid() && moment(date).isBefore(moment(), 'day')) {
      return true
    }
    return false
  }

  filteredExams () {
    const examInventory: any = this.exam_inventory
    let office_number = this.inventoryFilters.office_number === 'default'
      ? this.user.office.office_number : this.inventoryFilters.office_number
    if (this.inventoryFilters.office_number === 'pesticide_offsite') {
      office_number = (this.offices.find(office => office.office_name == 'Pesticide Offsite')).office_number
      this.inventoryFilters.office_number = office_number
    }
    let filtered = []
    if (examInventory.length > 0) {
      if (this.showExamInventoryModal) {
        filtered = examInventory.filter(ex => moment(ex.expiry_date).isSameOrAfter(moment(), 'day'))
        const moreFiltered: any = filtered.filter((ex: any) => !ex.booking)
        const evenMoreFiltered = moreFiltered.filter(ex => !ex.offsite_location)
        const { office_id } = this.user
        return evenMoreFiltered.filter(ex => ex.office_id == office_id)
      }

      const exams = this.showAllPesticide ? examInventory
        : examInventory.filter((ex: any) => ex.office.office_number == office_number)

      if (this.inventoryFilters.requireAttentionFilter === 'both') {
        return exams.filter(ex => this.checkAllAttention(ex))
      } else if (this.inventoryFilters.requireAttentionFilter === 'individual') {
        return exams.filter(ex => this.checkIndividualAttention(ex))
      } else if (this.inventoryFilters.requireAttentionFilter === 'group') {
        return exams.filter(ex => this.checkGroupAttention(ex))
      }

      if (this.inventoryFilters.requireOEMAttentionFilter === 'both') {
        return exams.filter(ex => this.checkOEMAllAttention(ex))
      } else if (this.inventoryFilters.requireOEMAttentionFilter === 'individual') {
        return exams.filter(ex => this.checkOEMIndividualAttention(ex))
      } else if (this.inventoryFilters.requireOEMAttentionFilter === 'group') {
        return exams.filter(ex => this.checkOEMGroupAttention(ex))
      }

      switch (this.inventoryFilters.expiryFilter) {
        case 'all':
          filtered = exams
          break
        case 'expired':
          filtered = exams.filter(ex => moment(ex.expiry_date).isBefore(moment(), 'day'))
          break
        case 'current':
          const step1 = exams.filter(ex => moment(ex.expiry_date).isSameOrAfter(moment(), 'day'))
          const step2 = exams.filter(ex => !ex.expiry_date)
          filtered = step1.concat(step2)
          break
        default:
          filtered = exams
          break
      }
      let moreFiltered = []
      switch (this.inventoryFilters.scheduledFilter) {
        case 'both':
          moreFiltered = filtered
          break
        case 'unscheduled':
          moreFiltered = filtered.filter(x => !this.filterByScheduled(x))
          break
        case 'scheduled':
          moreFiltered = filtered.filter(x => this.filterByScheduled(x))
          break
        default:
          moreFiltered = filtered
          break
      }
      let evenMoreFiltered: any = []
      switch (this.inventoryFilters.groupFilter) {
        case 'both':
          evenMoreFiltered = moreFiltered
          break
        case 'individual':
          evenMoreFiltered = moreFiltered.filter(ex => !this.filterByGroup(ex))

          break
        case 'group':
          evenMoreFiltered = moreFiltered.filter(ex => this.filterByGroup(ex))
          break
        default:
          evenMoreFiltered = moreFiltered
          break
      }
      let uploadFiltered = []
      switch (this.inventoryFilters.uploadFilter) {
        case 'notuploaded':
          uploadFiltered = evenMoreFiltered.filter((exam: any) => !exam.upload_received_ind)
          break
        default:
          uploadFiltered = evenMoreFiltered
      }
      let receptSentFiltered: any = []
      switch (this.inventoryFilters.receptSentFilter) {
        case 'notsent':
          receptSentFiltered = uploadFiltered.filter((exam: any) => !exam.receipt_sent_ind)
          break
        default:
          receptSentFiltered = uploadFiltered
      }
      let finalFiltered = []
      switch (this.inventoryFilters.returnedFilter) {
        case 'both':
          finalFiltered = receptSentFiltered
          break
        case 'returned':
          finalFiltered = receptSentFiltered.filter((ex: any) => ex.exam_returned_date)
          break
        case 'unreturned':
          finalFiltered = receptSentFiltered.filter(ex => !ex.exam_returned_date)
          break
        default:
          finalFiltered = receptSentFiltered
          break
      }
      return finalFiltered
    }
    return []
  }

  formatDate (d) {
    // JSTOTS TOCHECK removed new from moment. no need to use new with moment
    return moment(d).format('ddd MMM DD, YYYY')
  }

  formatTime (d) {
    const tz = d.office.timezone.timezone_name
    const time = zone.tz(d.start_time, tz).format('2017-MM-DD[T]HH:mm:ss').toString()

    // JSTOTS TOCHECK removed new from moment. no need to use new with moment
    return moment(time).format('h:mm a')
  }

  getSize () {
    this.totalH = window.innerHeight - 70 - 36
    if (!this.showExamInventoryModal) {
      this.tableStyle = { height: `${this.availableH}px`, width: `${window.innerWidth - 40}px` }
    }
    if (this.showExamInventoryModal) {
      this.tableStyle = { width: 98 + '%' }
    }
  }

  readyDetailsMap (item) {
    const output: any = {}
    if (item.exam_returned_date) {
      return {
        Returned: moment(item.exam_returned_date).format('YYYY-MMM-DD'),
        Disposition: item.exam_returned_tracking_number,
        Written: item.exam_written_ind ? 'Yes' : 'No'
      }
    }
    if (item.offsite_location && item.offsite_location !== '_offsite') {
      output.Location = item.offsite_location
    }
    if (item.booking) {
      if (item.booking.sbc_staff_invigilated) {
        output.Invigilator = 'SBC Employee'
      }
      if (item.booking.invigilators) {
        const invigilator_name_list: any = []
        item.booking.invigilators.forEach(exam_invigilator => {
          this.invigilators.forEach(office_invigilator => {
            if (exam_invigilator == office_invigilator.invigilator_id) {
              invigilator_name_list.push(office_invigilator.invigilator_name)
            }
          })
        })
        let invigilator_string = ''
        if (invigilator_name_list.length > 0) {
          invigilator_name_list.forEach(invigilator => {
            invigilator_string += invigilator
            invigilator_string += ', '
          })
          invigilator_string = invigilator_string.replace(/,\s*$/, '')
        }
        if (invigilator_string.length > 0) {
          output.Invigilators = invigilator_string
        }
      }
      if (item.booking.room_id) {
        output.Room = item.booking.room.room_name
      }
    }
    return output
  }

  resetActionedExam () {
    this.actionedExam = {}
  }

  resetInvalidOfficeOnHide () {
    if (this.officeName === 'Invalid Office') {
      this.setFilter({ type: 'office_number', value: 'default' })
    }
  }

  returnExam (item) {
    this.actionedExam = item
    if (item.is_pesticide) {
      this.toggleUploadExamModal(true)
    } else {
      this.toggleReturnExamModal(true)
    }
  }

  setExamTypeFilter (option) {
    this.setSelectedExamType(option.value)
    this.setSelectedExamTypeFilter(option.text)
    this.page = 1

    this.setSelectedQuickAction('')
    this.setSelectedQuickActionFilter('')

    if (option.value === 'individual') {
      this.setInventoryFilters({ type: 'groupFilter', value: 'individual' })
    } else if (option.value === 'group') {
      this.setInventoryFilters({ type: 'groupFilter', value: 'group' })
    } else if (option.value === 'all') {
      this.setInventoryFilters({ type: 'groupFilter', value: 'both' })
    }

    this.setInventoryFilters({ type: 'expiryFilter', value: 'all' })
    this.setInventoryFilters({ type: 'scheduledFilter', value: 'both' })
    this.setInventoryFilters({ type: 'returnedFilter', value: 'both' })
    this.setInventoryFilters({ type: 'requireAttentionFilter', value: 'default' })
    this.setInventoryFilters({ type: 'receptSentFilter', value: 'default' })
    this.setInventoryFilters({ type: 'uploadFilter', value: 'default' })
  }

  setQuickActionFilter (option) {
    this.setSelectedQuickAction(option.value)
    this.setSelectedQuickActionFilter(option.text)
    this.page = 1

    // Setting Default Values
    this.setInventoryFilters({ type: 'expiryFilter', value: 'all' })
    this.setInventoryFilters({ type: 'scheduledFilter', value: 'both' })
    this.setInventoryFilters({ type: 'returnedFilter', value: 'both' })
    this.setInventoryFilters({ type: 'requireAttentionFilter', value: 'default' })
    this.setInventoryFilters({ type: 'requireOEMAttentionFilter', value: 'default' })
    this.setInventoryFilters({ type: 'receptSentFilter', value: 'default' })
    this.setInventoryFilters({ type: 'uploadFilter', value: 'default' })
    this.$store.commit('toggleShowAllPesticideExams', false)

    if (option.value === 'returned') {
      this.setInventoryFilters({ type: 'returnedFilter', value: 'returned' })
    } else if (option.value === 'require_attention') {
      if (this.selectedExamType === 'individual') {
        this.setInventoryFilters({ type: 'requireAttentionFilter', value: 'individual' })
      } else if (this.selectedExamType === 'group') {
        this.setInventoryFilters({ type: 'returnedFilter', value: 'unreturned' })
        this.setInventoryFilters({ type: 'scheduledFilter', value: 'unscheduled' })
        this.setInventoryFilters({ type: 'requireAttentionFilter', value: 'group' })
      } else {
        this.setInventoryFilters({ type: 'requireAttentionFilter', value: 'both' })
      }
    } else if (option.value === 'ready') {
      this.setInventoryFilters({ type: 'expiryFilter', value: 'current' })
      this.setInventoryFilters({ type: 'returnedFilter', value: 'unreturned' })
      this.setInventoryFilters({ type: 'scheduledFilter', value: 'scheduled' })
    } else if (option.value === 'expired') {
      this.setInventoryFilters({ type: 'expiryFilter', value: 'expired' })
      this.setInventoryFilters({ type: 'returnedFilter', value: 'unreturned' })
    } else if (option.value === 'oemai') {
      if (this.selectedExamType === 'individual') {
        this.setInventoryFilters({ type: 'requireOEMAttentionFilter', value: 'individual' })
      } else if (this.selectedExamType === 'group') {
        this.setInventoryFilters({ type: 'requireOEMAttentionFilter', value: 'group' })
      } else {
        this.setInventoryFilters({ type: 'requireOEMAttentionFilter', value: 'both' })
      }
    } else if (option.value === 'awaiting_upload') {
      this.isLoading = true
      this.setInventoryFilters({ type: 'office_number', value: 'pesticide_offsite' })
      this.updateExamStatus().then(success => {
        console.log('==> In this.updateExamStatus().then()', success)
        this.$store.commit('toggleShowAllPesticideExams', false)
        this.setInventoryFilters({ type: 'expiryFilter', value: 'current' })
        this.setInventoryFilters({ type: 'groupFilter', value: 'both' })
        this.setInventoryFilters({ type: 'returnedFilter', value: 'unreturned' })
        this.setInventoryFilters({ type: 'uploadFilter', value: 'notuploaded' })
        this.isLoading = false
      }, err => {
        console.error(err)
        this.isLoading = false
      }).catch(err => {
        this.isLoading = false
      })
    } else if (option.value === 'awaiting_receipt') {
      this.viewAllOfficePesticideExams()
      this.setInventoryFilters({ type: 'expiryFilter', value: 'current' })
      this.setInventoryFilters({ type: 'returnedFilter', value: 'unreturned' })
      this.setInventoryFilters({ type: 'receptSentFilter', value: 'notsent' })
    } else if (option.value === 'all') {
      this.setInventoryFilters({ type: 'groupFilter', value: 'both' })
    }
  }

  setFilter (e) {
    this.setInventoryFilters(e)

    if (e.type === 'office_number') {
      this.getExamsForOffice(e.value)
    }
  }

  setOfficeFilter (office_number) {
    this.setFilter({ type: 'office_number', value: office_number })
    this.$store.commit('toggleShowAllPesticideExams', false)
  }

  setHomeOffice () {
    this.setFilter({ type: 'office_number', value: 'default' })
    this.officeFilterModal = false
    this.$store.commit('toggleShowAllPesticideExams', false)
  }

  sortCompare (a, b, key) {
    if (key === 'scheduled') {
      let val1, val2
      if (this.statusIcon(a).rank !== this.statusIcon(b).rank) {
        val1 = parseInt(this.statusIcon(a).rank)
        val2 = parseInt(this.statusIcon(b).rank)
      }
      if (this.statusIcon(a).rank === this.statusIcon(b).rank) {
        val1 = parseInt(a.exam_id)
        val2 = parseInt(b.exam_id)
      }
      return val1 < val2 ? -1 : val1 > val2 ? 1 : 0
    }
    else if (key === 'start_time') {
      if (a.booking == null && b.booking == null) {
        return 0
      }
      else if (a.booking == null) {
        return 1
      }
      else if (b.booking == null) {
        return -1
      } else {
        let val1, val2
        if(a.booking.start_time != null) {
          val1 = parseInt((new Date(a.booking.start_time).getTime() / 1000).toFixed(0))
        }
        if(b.booking.start_time != null) {
          val2 = parseInt((new Date(b.booking.start_time).getTime() / 1000).toFixed(0))
        }
        return val1 - val2
      }

    }

    if (typeof a[key] === 'number' && typeof b[key] === 'number') {      
      return a[key] < b[key] ? -1 : a[key] > b[key] ? 1 : 0
    } else {      
      return toString(a[key]).localeCompare(toString(b[key]), undefined, {
        numeric: true
      })
    }
    function toString (value) {
      if (!value) {
        return ''
      } else if (value instanceof Object) {
        return Object.keys(value)
          .sort()
          .map(key => toString(value[key]))
          .join(' ')
      }
      return String(value)
    }
  }

  statusIcon (item: any) {
    const number_of_students: any = item.number_of_students
    const number_of_invigilators: any = Math.ceil(number_of_students / 24)
    let length_of_invigilator_array: any = null
    if (!item.booking) {
      length_of_invigilator_array = 0
    } else {
      length_of_invigilator_array = item.booking.invigilators.length
    }
    const lifeRing: any = {
      icon: 'life-ring',
      rank: 4,
      style: { font: '1rem', color: 'red' }
    }
    const exclamationTriangle: any = {
      icon: 'exclamation-triangle',
      rank: 3,
      style: { font: '.9rem', color: '#FFC32B' }
    }
    const clipboardCheck: any = {
      icon: 'clipboard-check',
      rank: 2,
      style: { font: '1rem', color: 'green' }
    }
    const envelopeOpenText: any = {
      icon: 'shipping-fast',
      rank: 1,
      style: { font: '1rem', color: '#4e9de0' }
    }
    const feePending: any = {
      icon: 'dollar-sign',
      rank: 2,
      style: { font: '1rem', color: 'green' }
    }

    if (item.is_pesticide && !item.exam_received_date && !item.exam_returned_date) {
      return lifeRing
    }

    if (item.exam_returned_date) {
      return envelopeOpenText
    }

    if (item.booking) {
      // I assume this empty block is intentional
    }
    if (item.booking && item.booking.invigilator) {
      // I assume this empty block is intentional
    }
    if (item.booking && item.booking.invigilator && item.booking.invigilator.deleted) {
      return lifeRing
    }

    if (item.exam_type.exam_type_name === 'Monthly Session Exam') {
      console.log('    --> Monthly Session Exam, name: ' + item.exam_name)
      console.log('    --> item.booking: ', item.booking)
      if (!item.booking) {
        return lifeRing
      }
      console.log('    --> this.checkInvigilator(item): ', this.checkInvigilator(item))
      if (!this.checkInvigilator(item)) {
        return lifeRing
      }
      if (this.filterByExpiry(item)) {
        return lifeRing
      }
      if (item.booking) {
        if (moment(item.booking.start_time).isValid()) {
          if (moment(item.booking.start_time).isBefore(moment(), 'day')) {
            return lifeRing
          }
        }
      }
      if (item.number_of_students === null && length_of_invigilator_array > 0) {
        return exclamationTriangle
      }
      if (!item.event_id || !item.number_of_students || !item.exam_received_date) {
        return exclamationTriangle
      }
      return clipboardCheck
    }
    if (item.exam_type.group_exam_ind) {
      if (!item.booking) {
        return lifeRing
      }
      if (item.booking && (!this.checkInvigilator(item))) {
        return lifeRing
      }
      if (this.filterByExpiry(item)) {
        return lifeRing
      }
      if (item.booking) {
        if (moment(item.booking.start_time).isValid()) {
          if (moment(item.booking.start_time).isBefore(moment(), 'day')) {
            return lifeRing
          }
        }
      }
      if (!item.exam_received_date) {
        return exclamationTriangle
      }
      return clipboardCheck
    }
    if (this.filterByExpiry(item)) {
      return lifeRing
    }
    if (item.booking) {
      if (moment(item.booking.start_time).isValid()) {
        if (moment(item.booking.start_time).isBefore(moment(), 'day')) {
          return lifeRing
        }
      }
    }
    if (!item.booking) {
      return exclamationTriangle
    }
    if (!item.exam_received_date) {
      return exclamationTriangle
    }
    if (item.is_pesticide && item.exam_received_date && !item.receipt) {
      return feePending
    }
    return clipboardCheck
  }

  stillRequires (item) {
    const output: any = []
    let length_of_invigilator_array: any = null
    if (!item.booking) {
      length_of_invigilator_array = 0
    } else {
      length_of_invigilator_array = item.booking.invigilators.length
    }
    const number_of_invigilators = Math.ceil(item.number_of_students / 24)
    if (item.exam_returned_date) {
      return output
    }
    if (!item.booking) {
      output.push('Scheduling and Assignment of Invigilator')
    }

    if (!item.exam_received_date) {
      if (item.is_pesticide) {
        output.push('Print Materials')
      } else {
        output.push('Receipt of Materials')
      }
    }
    if (item.exam_type.exam_type_name === 'Monthly Session Exam') {
      if (!item.number_of_students) {
        output.push('Number of Students')
      }
      if (!item.event_id) {
        output.push('Event ID')
      }
    }
    console.log('==> In stillRequires(item), item: ', item)
    if (item.booking) {
      if (item.exam_type.group_exam_ind == 1) {
        if (length_of_invigilator_array == 0 && number_of_invigilators == 1) {
          output.push('Assignment of Invigilator')
        } else if (length_of_invigilator_array == 0 && number_of_invigilators > 1) {
          output.push('Assignment of Invigilators')
        } else if (length_of_invigilator_array > 0 && length_of_invigilator_array < number_of_invigilators) {
          output.push('Assignment of More Invigilators')
        }
      } else if (item.exam_type.group_exam_ind == 0) {
        if (length_of_invigilator_array == 0 && !item.booking.sbc_staff_invigilated) {
          output.push('Assignment of Invigilator')
        }
      }
    }
    return output
  }

  updateCalendarBooking (item) {
    // JSTOTS TOCHECK removed new from moment. no need to use new with moment
    item.gotoDate = moment(item.booking.start_time)
    item.referrer = 'rescheduling'
    this.setSelectedExam(item)
    const booking = this.calendarEvents.find(event => event.id == item.booking_id)

    // not needed to change to moment
    // JSTOTS TOCHECK removed new from moment. no need to use new with moment
    // JSTOTS TOCHECK removed new from moment. no need to use new with moment
    this.setEditedBooking(booking)
    this.setEditedBookingOriginal(booking)
    this.toggleEditBookingModal(true)
    this.$router.push('/booking')
  }

  openInvigilatorModal (item) {
    this.setSelectedExam(item)
    this.toggleSelectInvigilatorModal(true)
  }

  mounted () {
    if (this.is_pesticide_designate) {
      const pestFilterOptions = [
        { text: 'Awaiting Upload', value: 'awaiting_upload' },
        { text: 'Awaiting Receipt', value: 'awaiting_receipt' },
        { text: 'All', value: 'all' }
      ]
      this.newQuickActionOptions = this.newQuickActionOptions.concat(pestFilterOptions)
      this.newQuickActionOptionsNoOEM = this.newQuickActionOptionsNoOEM.concat(pestFilterOptions)
    } else {
      const nonpestFilterOptions = [
        { text: 'All', value: 'all' }
      ]
      this.newQuickActionOptions = this.newQuickActionOptions.concat(nonpestFilterOptions)
      this.newQuickActionOptionsNoOEM = this.newQuickActionOptionsNoOEM.concat(nonpestFilterOptions)
    }
    this.getExams().then(() => { this.getBookings() })
    this.getOffices()
    this.getInvigilators()
    this.getSize()
    this.$nextTick(function () {
      window.addEventListener('resize', () => { this.getSize() })
    })
    this.setFilter({ type: 'office_number', value: 'default' })
  }
}
</script>

<style scoped>
.open-cal-link {
  text-decoration: #007bff underline !important;
  text-underline-position: under !important;
  font-size: 0.85rem !important;
  color: #007bff !important;
  font-weight: 300 !important;
}
.expired {
  color: red;
}
.view-details-link {
  text-decoration: #007bff underline !important;
  text-underline-position: under;
  font-size: 0.85rem;
  color: #007bff !important;
  font-weight: 300;
}
.view-details-link:hover {
  font-weight: 600;
}
.open-cal-link:hover {
  font-weight: 600;
}
.schedule-link {
  text-decoration: #28a745 underline !important;
  text-underline-position: under;
  font-size: 0.85rem;
  color: #28a745 !important;
  font-weight: 300;
}
.schedule-link:hover {
  font-weight: 600;
}
.label-text {
  font-size: 0.9rem;
}
.exam-table-holder {
  border: 1px solid dimgrey;
}
.tr-container-div {
  min-height: 50% !important;
}
.details-slot-div {
  display: flex;
  justify-content: flex-start;
  justify-items: flex-start;
  width: 100%;
  padding-top: 6px;
  padding-bottom: 6px;
}
.pagination-class {
  position: fixed;
  bottom: 35px;
  left: 30px;
}
.icon-cursor-hover {
  cursor: pointer !important;
}
.btn:active,
.btn.active {
  background-color: #184368 !important;
  color: white !important;
}
</style>
