<template>
  <b-modal v-model="modal"
           :no-close-on-backdrop="true"
           hide-header
           @ok="submit"
           ok-title='Email Invigilator'
           size="md">
    <b-alert :show="this.alertMessage != ''"
             style="h-align: center"
             variant="danger">{{this.alertMessage}}</b-alert>
    <b-table selectable
             select-mode='single'
             :fields="fields"
             :items="pesticide_invigilators"
             responsive
             selected-variant="success"
             ref="invigilator_table"
             @row-selected="rowSelected"
             bordered
             striped>
      <template slot="selected" slot-scope="{ rowSelected }">
        <span v-if="rowSelected">✔</span>
      </template>
    </b-table>
    <template slot="modal-footer">
      <div style="display: flex; justify-content: flex-end; width: 100%">
        <b-btn class="btn-secondary mr-2"
               @click="closeModal()">Cancel</b-btn>
        <b-btn class="btn-primary"
               :disabled="!this.selected_invigilator || this.loading"
               @click="submit()">
          <b-spinner small v-if="this.loading"></b-spinner>
          Email Invigilator
        </b-btn>
      </div>
    </template>
  </b-modal>
</template>

<script>
  import { mapActions, mapMutations, mapState, mapGetters } from 'vuex'

  export default {
    name: "SelectInvigilatorModal",
    components: { },
    mounted() {
      this.getPesticideOfficeInvigilators()
      this.getPesticideOffsiteInvigilators()
    },
    props: [],
    data () {
      return {
        alertMessage: "",
        fields: ['selected', 'invigilator_name',],
        invigilators: [],
        loading: false,
        selected_invigilator: null
      }
    },
    computed: {
      ...mapGetters([]),
      ...mapState({
        showSelectInvigilatorModal: state => state.showSelectInvigilatorModal,
        pesticide_invigilators: state => state.pesticide_invigilators,
      }),
      modal: {
        get() {
          return this.showSelectInvigilatorModal
        },
        set(e) {
          this.toggleSelectInvigilatorModal(e)

          if (!e) {
            this.setSelectedExam(null)
          }
        }
      },
    },
    methods: {
      ...mapActions(['emailInvigilator', 'getPesticideOfficeInvigilators', 'getPesticideOffsiteInvigilators']),
      ...mapMutations([
        'setSelectedExam',
        'toggleSelectInvigilatorModal',
      ]),
      clearModal() {
        this.alertMessage = ''
        this.loading = false
        this.$refs.invigilator_table.clearSelected()
        this.selected_invigilator = null
      },
      closeModal() {
        this.clearModal()
        this.toggleSelectInvigilatorModal(false)
      },
      rowSelected(item) {
        if (item.length >= 1) {
          this.selected_invigilator = item[0]
        }
      },
      submit() {
        this.loading = true
        this.emailInvigilator(this.selected_invigilator)
          .then(() => {
            this.toggleSelectInvigilatorModal(false);
            this.loading = false
          })
          .catch(() => {
            this.alertMessage = "An error occurred emailing the invigilator"
            this.loading = false
          })
      },
    },
  }
</script>

<style scoped>

</style>
