<template>
  <fragment>
    <b-row no-gutters>
      <b-col :cols="exam[q.key] === 'collect' ? 11 : 6">
        <b-form-group>
          <label>{{q.text}}
            <span v-if="error" style="color: red">{{ validationObj[q.key].message }}</span>
          </label><br>
          <b-form-select :options="q.options"
                         v-model="feesSelect"
                         autocomplete="off"
                         :name="q.key" />
        </b-form-group>
      </b-col>
      <b-col v-if="showReceiptField" cols="5">
        <b-form-group>
          <label>Receipt </label>
          <b-form-input v-model="receiptNumber"
                        key="receipt_number"
                        id="receipt_number"
                        autocomplete="off" />
        </b-form-group>
      </b-col>
      <checkmark :validated="isValidated" />
    </b-row>
    <b-row>
      <b-col cols="11">
        <b-form-group>
          <label>Payee is not candidate</label>
          <b-form-checkbox v-model="capturePayeeDetails"/>
        </b-form-group>
      </b-col>
    </b-row>
  </fragment>

</template>

<script>
  import { mapState } from 'vuex'
  import { checkmark } from '../add-exam-form-components'

  export default {
    name: 'PesticideFees',
    props: ['error', 'q', 'validationObj', 'exam',],
    components: { checkmark },
    mounted() {
      if (!('fees' in this.exam)) {
        this.$store.commit('captureExamDetail', { key: 'fees', value: 'collect'})
      }
    },
    computed: {
      ...mapState({
        addExamModal: state => state.addExamModal,
        capturePayee: state => state.captureITAExamTabSetup.capturePayee,
      }),
      feesSelect: {
        get() {
          return this.exam.fees
        },
        set(value) {
          this.$store.commit('captureExamDetail', {key: 'fees', value})
          if (value === 'collect') {
            this.$store.commit('deleteCapturedExamKey', 'receipt_number')
            return
          }
          if (value === 'paid') {
            this.$store.commit('captureExamDetail', {key: 'receipt_number', value: ''})
          }
        }
      },
      showReceiptField() {
        if (this.exam.fees === 'paid') {
          return true
        }
        return false
      },
      receiptNumber: {
        get() {
          return this.exam.receipt_number
        },
        set(value) {
          this.$store.commit('captureExamDetail', {key: 'receipt_number', value})
        }
      },
      capturePayeeDetails: {
        get() {
          return this.capturePayee
        },
        set(value) {
          this.$store.commit('updateCaptureTab', { capturePayee: value })
        }
      },
      isValidated() {
        if (!this.showReceiptField) {
          return true
        }
        if (this.exam.receipt_number) {
          return true
        }
        return false
      }
    },
    watch: {
      showReceiptField(newVal, oldVal) {
        if (!newVal) {
          this.$store.commit('deleteCapturedExamKey', 'receipt_number')
        }
      }
    },
  }
</script>
