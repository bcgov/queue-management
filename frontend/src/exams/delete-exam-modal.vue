<template>
    <b-modal v-model="deleteModalVisible"
             :no-close-on-backdrop="true"
             hide-header
             hide-footer
             hide-cancel
             size="md">
        <b-container>
          <h5>Are you sure you want to delete this Exam?</h5>
          <div style="font-size:0.9rem; display:flex; justify-content:center;">
            <b-col>
              <ul><b>Exam Name: {{ this.returnExam.exam_name }}</b></ul>
              <ul><b>Examinee Name:</b> {{ this.returnExam.examinee_name }}</ul>
              <ul><b>Event ID:</b>{{ this.returnExam.event_id }}</ul>
            </b-col>
          </div>
          <b-row>
            <b-col>
              <b-form-group>
                <b-btn class="w-100 btn-danger"
                       @click="clickNo">No</b-btn>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group>
                <b-btn class="w-100 btn-primary"
                       @click="clickYes">Yes</b-btn>
              </b-form-group>
            </b-col>
          </b-row>
        </b-container>
    </b-modal>
</template>

<script>
    import { mapActions, mapMutations, mapState } from 'vuex'
    export default {
        name: "DeleteExamModal",
        methods: {
          ...mapActions([
            'deleteBooking',
            'deleteExam',
            'getExams',
          ]),
          ...mapMutations([
            'toggleDeleteExamModalVisible'
          ]),
          clickYes() {
            let exam_id = this.returnExam.exam_id
            this.deleteExam(exam_id)
                .then(() => { this.getExams() })
            this.toggleDeleteExamModalVisible(false)
            if (this.returnExam.booking_id){
              this.deleteBooking(this.returnExam.booking_id)
            }
          },
          clickNo() {
            this.toggleDeleteExamModalVisible(false)
          }
        },
        computed: {
            ...mapState({
              showDeleteExamModal: state => state.showDeleteExamModal,
              returnExam: state => state.returnExam,
            }),
            deleteModalVisible: {
                get() {
                    return this.showDeleteExamModal
                },
                set(e) {
                    this.toggleDeleteExamModalVisible(e)
                }
            },
            exam() {
              if(Object.keys(this.actionedExam).length > 0){
                return this.actionedExam
              }
              return false
            }
        }
    }
</script>

<style scoped>

</style>
