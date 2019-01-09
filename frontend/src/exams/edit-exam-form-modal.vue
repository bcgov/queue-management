<template v-if="showExamEditModalVisible">
  <div id ="examBackground" class="edit-exam-modal-background">
    <div id="examModal" v-bind:class="{ 'edit-exam-modal': !editExamSuccess || !editExamFailure,
                                        'edit-exam-modal-content-message': editExamSuccess,
                                        'edit- exam-modal-content-message': editExamFailure }">
      <div class="edit-exam-modal-content">
        <div class="modal_header" v-if="!editExamSuccess && !editExamFailure">
          <div>
            <b-container style="font-size:1.1rem; border:1px solid lightgrey; border-radius: 10px" class="mb-2 pb-3" fluid>
              <b-row>
                <b-col>
                  <h3>Edit Exam Information Form</h3>
                </b-col>
              </b-row>
              <b-row class="my-1">
                <b-col sm="4"><label>Event ID:</label></b-col>
                <b-col sm="6"><b-form-input id="eventIDInput" type="text" v-model=fields.event_id></b-form-input></b-col>
              </b-row>
              <b-row class="my-1">
                <b-col sm="4"><label>Exam Name:</label></b-col>
                <b-col sm="6"><b-form-input id="examNameInput" type="text" v-model=fields.exam_name></b-form-input></b-col>
              </b-row>
              <b-row class="my-1">
                <b-col sm="4"><label>Exam Methods:</label></b-col>
                <b-col sm="6">
                  <select class="form-control" name="examMethod" v-model=selectedMethod>
                    <option v-for="examMethod in examMethodOptions" :value="examMethod.value">{{ examMethod.value }}</option>
                  </select>
                </b-col>
              </b-row>
              <b-row class="my-1">
                <b-col sm="4"><label>Expiry Date:</label></b-col>
                <b-col sm="6"><b-form-input id="expiryDate" type="date" v-model=expiryDate></b-form-input></b-col>
              </b-row>
              <b-row class="my-1">
                <b-col sm="4"><label>Exam Received:</label></b-col>
                <b-col sm="6">
                  <select class="form-control" name="examReceived" v-model=selectedReceived>
                    <option v-for="received in examReceivedOptions" :value="received.value">{{ received.value }}</option>
                  </select>
                </b-col>
              </b-row>
              <b-row class="my-1">
                <b-col sm="4"><label>Student Name:</label></b-col>
                <b-col sm="6"><b-form-input id="studentName" type="text" v-model=fields.examinee_name></b-form-input></b-col>
              </b-row>
              <b-row class="my-1">
                <b-col sm="4"><label>Notes:</label></b-col>
                <b-col sm="6"><b-form-input id="examNotes" type="text" v-model="fields.notes"></b-form-input></b-col>
              </b-row>
            </b-container>
          </div>
        </div>
        <div>
          <div class="" v-if="editExamSuccess">
            <b-row>
              <b-col>
                <h1 style="color:green">Success!</h1>
                <p style="color:green"><b>Changes have been submitted!</b></p>
                <b-button @click="ok" class="btn btn-success btn-secondary">Ok</b-button>
              </b-col>
            </b-row>
          </div>
        </div>
        <div>
          <div v-if="editExamFailure">
            <b-row>
              <b-col>
                <h2 style="color:red">Error!</h2>
                <p style="color:red"><b>Your changes were not submitted.</b></p>
                <b-button @click="ok" class="btn btn-warning btn-secondary">Ok</b-button>
              </b-col>
            </b-row>
          </div>
        </div>
        <div class="button-flex-end">
          <div v-if="!editExamSuccess && !editExamFailure">
            <b-button @click="cancel" class="mt-3 ml-3 mr-3">Cancel</b-button>
            <b-button @click="submit" class="btn-primary mt-3 ml-3 mr-3">Submit</b-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
    import { mapMutations, mapState, mapActions } from 'vuex'
    import moment from 'moment'
    export default {
        name: "EditExamModal",
        mounted() {
            this.selectedMethod = this.fields.exam_method;
            this.expiryDate = moment(this.fields.expiry_date).format('YYYY-MM-DD');
            if(this.fields.exam_received === 0) {
                this.selectedReceived = 'No';
            }else if (this.fields.exam_received === 1){
                this.selectedReceived = 'Yes';
            }
        },
        data () {
            return {
                selectedMethod: '',
                examMethodOptions: [
                  { id: 'paper', value: 'paper'},
                  { id: 'online', value: 'online'}
                ],
                expiryDate:'',
                selectedReceived: '',
                examReceivedOptions: [
                  { id: 0, value: 'No' },
                  { id: 1, value: 'Yes' }
                ],
                noBooking: true
            }
        },
        computed: {
            ...mapState({
                showExamEditModalVisible: state => state.showEditExamModalVisible,
                fields: state => state.editExams,
                selectedExam: state => state.selectedExam,
                selectedBooking: state => state.selectedBooking,
                editExamSuccess: state => state.editExamSuccess,
                editExamFailure: state => state.editExamFailure
            }),
        },
        methods: {
            ...mapActions([
                'putExamInfo',
                'putBookingInfo',
                'getExams',
                'getBookings' ]),
            ...mapMutations([
                'toggleEditExamModalVisible',
                'setEditExamSuccess',
                'setEditExamFailure' ]),
            cancel() {
                this.toggleEditExamModalVisible(false);
                this.selectedMethod = '';
                this.expiryDate = '';
                this.selectedReceived = '';
            },
            submit() {
                this.selectedExam.exam_id = this.fields.exam_id;
                if (this.selectedReceived === 'No') {
                    this.selectedReceived = 0;
                }else {
                    this.selectedReceived = 1;
                }
                console.log("method: ", this.selectedMethod);
                let submit_exam = {
                    exam_id: this.selectedExam.exam_id,
                    event_id: this.fields.event_id,
                    exam_name: this.fields.exam_name,
                    exam_method: this.selectedMethod,
                    expiry_date: this.expiryDate,
                    exam_received: this.selectedReceived,
                    examinee_name: this.fields.examinee_name,
                    notes: this.fields.notes
                };
                this.putExamInfo(submit_exam);
                if(this.editExamFailure === false){
                    this.setEditExamFailure(false)
                }
                this.getExams()
            },
            ok() {
                this.toggleEditExamModalVisible(false);
                this.setEditExamSuccess(false);
                this.setEditExamFailure(false);
            }
        },
    }
</script>

<style scoped>

</style>
