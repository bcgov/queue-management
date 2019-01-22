<template >
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
                  <h3>Return Exam Form</h3>
              </b-col>
          </b-row>
          <b-row class="my-1">
              <b-col sm="4"><label>Exam Returned: </label></b-col>
              <b-col sm="7">
                  <select class="form-control" name="examReturned" v-model=selectedReturned>
                      <option v-for="returned in examReturnedOptions" :value="returned.value">{{ returned.value }}</option>
                  </select>
              </b-col>
          </b-row>
          <b-row>
              <b-col sm="4"><label>Tracking Number: </label></b-col>
              <b-col sm="7"><b-form-input id="trackingNumber" type="text" v-model=fields.exam_returned_tracking_number></b-form-input></b-col>
          </b-row>
      </b-container>
  </b-modal>
</template>

<script>
    import { mapMutations, mapState, mapActions } from 'vuex'
    export default {
        name: "ReturnExamModal",
        mounted() {
            this.selectedExam.exam_id = this.fields.exam_id;
            if(this.fields.exam_returned_ind === 0) {
                  this.selectedReturned = 'No';
            }else if (this.fields.exam_returned_ind === 1) {
                  this.selectedReturned = 'Yes';
            }
        },
        data () {
            return {
                selectedReturned: '',
                examReturnedOptions: [
                    { id: 0, value: 'No' },
                    { id: 1, value: 'Yes' }
                ],
            }
        },
        methods: {
            ...mapActions([
              'getExams',
              'putExamInfo'
            ]),
            ...mapMutations([
                'toggleReturnExamModalVisible',
                'setEditExamSuccess',
                'setEditExamFailure'
            ]),
            ok() {
                this.toggleReturnExamModalVisible(false);
                this.setEditExamSuccess(false);
                this.setEditExamFailure(false);
            },
            cancel() {
                this.toggleReturnExamModalVisible(false);
                this.selectedReturned = '';
            },
            submit() {
                this.setEditExamSuccess(false)
                this.setEditExamFailure(false)
                this.selectedExam.exam_id = this.fields.exam_id;
                if(this.selectedReturned === 'No'){
                    this.selectedReturned = 0;
                }else{
                    this.selectedReturned =1;
                }
                let return_exam = {
                    exam_id: this.selectedExam.exam_id,
                    exam_returned_ind: this.selectedReturned,
                    exam_returned_tracking_number: this.fields.exam_returned_tracking_number
                };
                this.putExamInfo(return_exam);
                this.getExams();
                console.log(this.editExamSuccess)
            },
        },
        computed: {
            ...mapState({
                showReturnExamModalVisible: state => state.showReturnExamModalVisible,
                fields: state => state.returnExams,
                selectedExam: state => state.selectedExam,
                editExamSuccess: state => state.editExamSuccess,
                editExamFailure: state => state.editExamFailure,
            }),
            modal: {
              get() {
                  return this.showReturnExamModalVisible
              },
              set(e) {
                  this.toggleReturnExamModalVisible(e)
              }
            }
        },

    }
</script>
