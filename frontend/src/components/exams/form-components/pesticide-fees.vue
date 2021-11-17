<template>
  <div>
    <b-row no-gutters>
      <b-col :cols="exam[q.key] === 'collect' ? 11 : 6">
        <b-form-group>
          <label
            >{{ q.text }}
            <span v-if="error" style="color: red">{{
              validationObj[q.key].message
            }}</span> </label
          ><br />
          <b-form-select
            :options="q.options"
            v-model="feesSelect"
            autocomplete="off"
            :name="q.key"
          />
        </b-form-group>
      </b-col>
      <b-col v-if="showReceiptField" cols="5">
        <b-form-group>
          <label>Receipt </label>
          <b-form-input
            v-model="receiptNumber"
            key="receipt_number"
            id="receipt_number"
            autocomplete="off"
          />
        </b-form-group>
      </b-col>
      <checkmark :validated="isValidated" />
    </b-row>
    <b-row v-if="showReceiptField">
      <b-col cols="5">
        <b-form-group>
          <label>Payee is not candidate</label>
          <b-form-checkbox v-model="capturePayeeDetails" />
        </b-form-group>
      </b-col>
      <b-col cols="5">
        <b-form-group>
          <label>Payee has been sent confirmation/receipt</label>
          <b-form-checkbox v-model="capturePayeeSentReceipt" />
        </b-form-group>
      </b-col>
    </b-row>
  </div>
</template>

<script lang="ts">

import { Component, Prop, Vue, Watch } from 'vue-property-decorator'

import { mapState } from 'vuex'
import { checkmark } from '../add-exam-form-components'

@Component({
  components: {
    checkmark
  },
  computed: {

    ...mapState({
      addExamModal: (state: any) => state.addExamModal,
      capturePayee: (state: any) => state.captureITAExamTabSetup.capturePayee,
      payeeSentReceipt: (state: any) => state.captureITAExamTabSetup.payeeSentReceipt
    })
  }
})
export default class PesticideFees extends Vue {
  private readonly addExamModal!: any
  private readonly capturePayee!: any
  private readonly payeeSentReceipt!: any

  @Prop()
  private error!: any

  @Prop()
  private q!: any

  @Prop()
  private validationObj!: any

  @Prop()
  private exam!: any

  @Watch('showReceiptField')
  onshowReceiptFieldChange (newVal, oldVal) {
    if (!newVal) {
      this.$store.commit('deleteCapturedExamKey', 'receipt_number')
    }
  }

  get feesSelect () {
    return this.exam.fees
  }

  set feesSelect (value) {
    this.$store.commit('captureExamDetail', { key: 'fees', value })
    if (value === 'collect') {
      this.$store.commit('deleteCapturedExamKey', 'receipt_number')
      return
    }
    if (value === 'paid') {
      this.$store.commit('captureExamDetail', { key: 'receipt_number', value: '' })
    }
  }

  get showReceiptField () {
    return true
  }

  get receiptNumber () {
    return this.exam.receipt_number
  }

  set receiptNumber (value) {
    this.$store.commit('captureExamDetail', { key: 'receipt_number', value })
  }

  get capturePayeeDetails () {
    return this.capturePayee
  }

  set capturePayeeDetails (value) {
    this.$store.commit('updateCaptureTab', { capturePayee: value })
  }

  get capturePayeeSentReceipt () {
    return this.payeeSentReceipt
  }

  set capturePayeeSentReceipt (value) {
    this.$store.commit('updateCaptureTab', { payeeSentReceipt: value })
  }

  get isValidated () {
    if (!this.showReceiptField) {
      return true
    }
    if (this.exam.receipt_number) {
      return true
    }
    return false
  }

  mounted () {
    if (!('fees' in this.exam)) {
      this.$store.commit('captureExamDetail', { key: 'fees', value: 'collect' })
    }
  }
}
</script>
