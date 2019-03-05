<template>
    <b-modal v-model="deleteModalVisible"
             :no-close-on-backdrop="true"
             hide-header
             hide-footer
             hide-cancel
             size="md">
        <b-container style="font-size:1.1rem;">
          <label>Are you sure you want to delete this Exam?</label>
          <div style="font-size:0.9rem; display:flex; justify-content:center;">
            <b-col>
              <ul><b>Exam Name:</b> {{ fields.exam_name }}</ul>
              <ul><b>Examinee Name:</b> {{ fields.examinee_name }}</ul>
              <ul><b>Event ID:</b> {{ fields.event_id }}</ul>
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
            'deleteExam',
            'getExams'
          ]),
          ...mapMutations([
            'toggleDeleteExamModalVisible'
          ]),
          clickYes() {
            let id = this.fields.exam_id
            this.deleteExam(id)
              .then(() => { this.getExams() })
            this.toggleDeleteExamModalVisible(false)
          },
          clickNo() {
            this.toggleDeleteExamModalVisible(false)
          }
        },
        computed: {
            ...mapState({
              showDeleteExamModal: state => state.showDeleteExamModal,
              fields: state => state.returnExam,
            }),
            deleteModalVisible: {
                get() {
                    return this.showDeleteExamModal
                },
                set(e) {
                    this.toggleDeleteExamModalVisible(e)
                }
            }
        }
    }
</script>

<style scoped>

</style>
