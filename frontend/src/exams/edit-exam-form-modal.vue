<template>
  <b-modal v-model="modal"
           :no-close-on-backdrop="true"
           hide-ok
           hide-header
           hide-cancel
           @hidden="ok"
           @ok="submit"
           size="md">
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
  </b-modal>
</template>

<script>
  import { mapActions, mapMutations, mapState } from 'vuex'
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
        methods: {
            ...mapActions([
                'putExamInfo',
                'putBookingInfo',
                'getExams',
                'getBookings'
            ]),
            ...mapMutations([
                'toggleEditExamModalVisible',
                'setEditExamSuccess',
                'setEditExamFailure'
            ]),
            ok() {
                this.toggleEditExamModalVisible(false);
                this.setEditExamSuccess(false);
                this.setEditExamFailure(false);
            },
            cancel() {
                this.toggleEditExamModalVisible(false);
                this.selectedMethod = '';
                this.expiryDate = '';
                this.selectedReceived = '';
            },
            submit() {
                this.setEditExamSuccess(false)
                this.setEditExamFailure(false)
                this.selectedExam.exam_id = this.fields.exam_id;
                if (this.selectedReceived === 'No') {
                    this.selectedReceived = 0;
                }else {
                    this.selectedReceived = 1;
                }
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
                console.log(this.editExamSuccess)

            },
        },
        computed: {
            ...mapState({
              showEditExamModal: state => state.showEditExamModal,
                fields: state => state.editExams,
                selectedExam: state => state.selectedExam,
                selectedBooking: state => state.selectedBooking,
                editExamSuccess: state => state.editExamSuccess,
                editExamFailure: state => state.editExamFailure
            }),
            modal: {
              get() {
                return this.showEditExamModal
              },
              set(e) {
                  this.toggleEditExamModalVisible(e)
              }
            }
        },

    }
</script>

<style scoped>

</style>
