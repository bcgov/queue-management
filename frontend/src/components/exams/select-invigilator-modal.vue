<template>
  <b-modal
    v-model="modal"
    :no-close-on-backdrop="true"
    hide-header
    @ok="submit"
    ok-title="Email Invigilator"
    size="md"
  >
    <b-alert
      :show="this.alertMessage != ''"
      style="justify-content: center"
      variant="danger"
      >{{ this.alertMessage }}</b-alert
    >
    <b-table
      selectable
      select-mode="single"
      :fields="fields"
      :items="pesticide_invigilators"
      responsive
      selected-variant="success"
      ref="invigilator_table"
      @row-selected="rowSelected"
      bordered
      striped
    >
      <template #cell(selected)="{ rowSelected }">
        <span v-if="rowSelected">✔</span>
      </template>
    </b-table>
    <template slot="modal-footer">
      <div style="display: flex; justify-content: flex-end; width: 100%">
        <b-btn class="btn-secondary mr-2" @click="closeModal()">Cancel</b-btn>
        <b-btn
          class="btn-primary"
          :disabled="!this.selected_invigilator || this.loading"
          @click="submit()"
        >
          <b-spinner small v-if="this.loading"></b-spinner>
          Email Invigilator
        </b-btn>
      </div>
    </template>
  </b-modal>
</template>

<script lang="ts">

import { Action, Mutation, State } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class SelectInvigilatorModal extends Vue {
  public $refs: any = {
    invigilator_table: HTMLElement
  };

  @State('showSelectInvigilatorModal') private showSelectInvigilatorModal!: any
  @State('pesticide_invigilators') private pesticide_invigilators!: any
  @State('selectedExam') private selectedExam!: any

  @Action('emailInvigilator') public emailInvigilator: any
  @Action('getPesticideOfficeInvigilators') public getPesticideOfficeInvigilators: any
  @Action('getPesticideOffsiteInvigilators') public getPesticideOffsiteInvigilators: any

  @Mutation('setSelectedExam') public setSelectedExam: any
  @Mutation('toggleSelectInvigilatorModal') public toggleSelectInvigilatorModal: any

  public alertMessage: any = ''
  public fields: any = ['selected', 'invigilator_name']
  public invigilators: any = []
  public loading: any = false
  public selected_invigilator: any = null

  mounted () {
    this.getPesticideOfficeInvigilators()
    this.getPesticideOffsiteInvigilators()
  }

  get modal () {
    return this.showSelectInvigilatorModal
  }

  set modal (e) {
    this.toggleSelectInvigilatorModal(e)

    if (!e) {
      this.setSelectedExam(null)
    }
  }

  clearModal () {
    this.alertMessage = ''
    this.loading = false
    this.$refs.invigilator_table.clearSelected()
    this.selected_invigilator = null
  }

  closeModal () {
    this.clearModal()
    this.toggleSelectInvigilatorModal(false)
  }

  rowSelected (item) {
    if (item.length >= 1) {
      this.selected_invigilator = item[0]
    }
  }

  submit () {
    this.loading = true
    this.emailInvigilator({
      invigilator: this.selected_invigilator,
      // JSTOTS confirm changed  selectedExam to this.selectedExam
      // exam: selectedExam
      exam: this.selectedExam
    })
      .then(() => {
        this.toggleSelectInvigilatorModal(false)
        this.loading = false
      })
      .catch(() => {
        this.alertMessage = 'An error occurred emailing the invigilator'
        this.loading = false
      })
  }
}
</script>
