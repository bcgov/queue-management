<template>
  <fragment>
    <b-row class="my-0 p-0 margin-1st-row">
      <b-col cols="12" class="my-0 p-0 pl-2">
          Enter Exam Types and Candidates
      </b-col>
    </b-row>
    <b-row class="my-0">
      <b-col cols="12">
        <b-form-select v-model="selectedExamType"
                       :options="examTypes"
                       autocomplete="off"
                       class="my-0 pb-0"
                       size="sm"
                       @click.prevent
                       @input.prevent="clickSelectItem"
                       :select-size="6" />
      </b-col>
    </b-row>


    <!-- grey area row 2, main inputs-->
    <b-row no-gutters class="add-candidate-top-row" style="height: 58px">
        <!--Name-->
        <b-col cols="5">
          <div style="display: flex; justify-content: start">
            <div class="w-50">
              <b-form-group>
                <label class="my-0 p-0 pl-1">First Name</label>
                <b-input size="sm"
                         autocomplete="off"
                         ref="first-name-input"
                         v-model="firstName"
                         class="my-0" />
              </b-form-group>
            </div>
            <div class="w-50">
              <b-form-group>
                <label class="my-0 p-0">Last Name</label>
                <b-input size="sm"
                         autocomplete="off"
                         v-model="lastName"
                         class="my-0" />
              </b-form-group>
            </div>
          </div>


        </b-col>

        <!--Email-->
        <b-col cols="3">
          <b-form-group>
            <label class="my-0 p-0">Email</label>
            <b-input size="sm"
                     autocomplete="off"
                     v-model="email"
                     class="my-0" />
          </b-form-group>
        </b-col>

        <!--Fees-->
        <b-col :cols="fees === 'paid' ? 1 : 2">
          <b-form-group>
            <label class="my-0 p-0">Fees</label>
            <select type="select"
                   size="sm"
                   autocomplete="off"
                   style="height: 31px;"
                   v-model="fees"
                   class="my-0 form-control">
              <option value='collect'>Collect</option>
              <option value='paid'>Paid</option>
            </select>
          </b-form-group>

        </b-col>

        <!--Receipt-->
        <b-col v-if="fees === 'paid'">
          <b-form-group>
            <label class="my-0 p-0">Receipt</label>
            <b-input size="sm"
                     v-model="receipt"
                     class="my-0" />
          </b-form-group>
        </b-col>

        <!--Bill To-->
        <b-col :cols="fees === 'paid' ? '' : 2">
          <b-form-group>
            <label class="my-0 p-0">Bill To</label>
            <b-form-select size="sm"
                           style="min-height: 30px;"
                           v-model="billTo"
                           class="my-0">
              <option value='candidate'>Candidate</option>
              <option value='payee'>Payee</option>
            </b-form-select>
          </b-form-group>
        </b-col>

    </b-row>

    <b-row no-gutters class="add-candidate-last-row" v-if="billTo === 'payee'">
      <b-col cols="6" />
      <b-col cols="3">
        <b-form-group>
          <label class="my-0 p-0">Payee Name</label>
          <b-input size="sm"
                   v-model="payeeName" />
        </b-form-group>
      </b-col>
      <b-col cols="3">
        <b-form-group>
          <label class="my-0 p-0">Payee Email</label>
          <b-input size="sm"
                   v-model="payeeEmail" />
        </b-form-group>

      </b-col>
    </b-row>

    <b-row class="py-1 mt-0">
      <b-col cols="12" style="padding: 0 16px 0 16px; margin: 0;">
        <b-table :items="tableData"
                 :fields="tableFields"
                 selectable
                 bordered
                 sticky-header
                 borderless
                 no-border-collapse
                 ref="examstable"
                 v-on:row-clicked.self="clickTableRow"
                 select-mode="single"
                 small
                 tbody-class="candidate-table-style"
                 class="my-1">

          <template slot="thead-top">
            <tr>
              <td colspan="8" style="border-bottom: 1px solid lightgrey">
                <div style="display: flex; width: 100%; background-color: white;">
                  <div style="flex-grow: 1; font-size: 14px; align-self: center" class="pl-2">
                    {{ instructionMessage }}
                  </div>
                  <div style="flex-shrink: 1; font-size: 15px;" v-if="currentlyEditing">
                    <b-btn @click="resetForm()"
                           style="width: 120px"
                           class="btn-sm btn-warning m-1">Cancel Updating
                    </b-btn>
                  </div>
                  <div style="flex-shrink: 1; font-size: 15px;">
                    <b-btn class="btn-sm btn-success m-1"
                           :disabled="!selectedExamType && !currentlyEditing"
                           style="width: 120px"
                           @click="handleClick">{{ currentlyEditing ? 'Update' : 'Add' }}
                    </b-btn>
                  </div>
                </div>
              </td>
            </tr>
          </template>

          <template slot="qty" slot-scope="row" v-if="row.item.qty">
            <span style="font-size: 16px; margin-left: 5px;">
              {{ row.item.qty }}
            </span>
          </template>

          <template slot="name" slot-scope="row">
            <div v-if="row.item.qty"
                 style="display: flex; justify-content: start; font-size: 16px; font-weight: 700">
              <div>
                <font-awesome-icon icon="file-alt"
                                   class="mr-2"
                                   style="font-size: 1rem;" />
              </div>
              <div>{{ row.item.name }}</div>
              <div v-show="false">
                {{ currentlyEditing === 'exam' && row.item.examTypeId === highlightedTableRow.examTypeId ?
                row.item._rowVariant = 'primary' : row.item._rowVariant = 'secondary' }}
              </div>
            </div>
            <div v-else style="margin-left: 35px; display: flex; justify-content: start;">
              <div>
                <font-awesome-icon icon="user-alt"
                                   class="mr-2"
                                   style="font-size: .85rem;" />
              </div>
              <div>{{ row.item.name }}</div>
              <div v-show="false">
                {{ currentlyEditing === 'candidate' && row.item.id === highlightedTableRow.id ?
                row.item._rowVariant = 'primary' : row.item._rowVariant = '' }}
              </div>
            </div>

          </template>

          <template slot="billTo" slot-scope="row">
            <template v-if="row.item.billTo === 'payee'">
              <div style="color: blue; cursor: pointer;" @click.stop.capture="row.toggleDetails()">Payee</div>
            </template>
            <template v-else>
              {{ row.item.billTo }}
            </template>
          </template>

          <template slot="row-details" slot-scope="row">
            Payee Name: {{ row.item.payeeName }} | Payee Email: {{ row.item.payeeEmail }}
          </template>

          <template slot="sent" slot-scope="row" v-if="row.item.fees === 'paid'">
            <div class="text-center">
              <b-form-checkbox sm
                               class="m-0 p-0"
                               style="position: relative; top: -3px;"
                               size="sm"
                               small />
            </div>

          </template>

          <template slot="delete" slot-scope="row">
            <div v-if="row.item.id" style="width: 100%; display: flex; justify-content: center">
              <div>
                <font-awesome-icon icon="eraser"
                                   class="cursor-pointer"
                                   @click.stop.capture="deleteExam(row.item)"
                                   style="font-size: 1rem; color: #CF1C3C;" />
              </div>
            </div>
          </template>

        </b-table>
      </b-col>
    </b-row>
  </fragment>
</template>

<script>
  import { mapGetters, mapMutations, mapState } from 'vuex'


  export default {
    name: 'GroupPesticideModal',
    props: ['error', 'q', 'validationObj', 'handleInput', 'exam'],
    data() {
      return {
        billTo: 'candidate',
        email: '',
        fees: 'collect',
        firstName: '',
        selectedExamType: null,
        highlightedTableRow: null,
        lastName: '',
        payeeEmail: '',
        payeeName: '',
        receipt: '',
        formFields:['firstName', 'lastName', 'email', 'payeeName', 'payeeEmail','fees', 'billTo', 'receipt'],
        tableFields: [
          { key: 'qty', label: 'Qty', thStyle: { width: '4%' } },
          { key: 'name', thStyle: { width: '32%' } },
          { key: 'email', thStyle: { width: '23%' } },
          { key: 'fees', thStyle: { width: '7%' } },
          { key: 'billTo', label: 'Bill To', thStyle: { width: '10%' } },
          { key: 'receipt', thStyle: { width: '10%' } },
          { key: 'sent', thStyle: { width: '6%' } },
          { key: 'delete', label: 'Delete', thStyle: { width: '8%' } },
        ]
      }
    },
    mounted() {
      this.removeListener()
      document.addEventListener('keydown', this.handleKeyboard)
    },
    destroyed() {
      this.removeListener()
    },
    computed: {
      ...mapState({
        Candidates: state => state.addExamModule.candidates,
        pesticideExamTypes: state => state.addExamModule.pesticideExamTypes,
      }),
      instructionMessage() {
        if (this.currentlyEditing) {
          if (this.currentlyEditing === 'exam') {
            return 'You are currently editing the below highlighted exam'
          }
          return 'You are currently editing the below highlighted candidate'
        }
        return 'To add a candidate, select an exam above and press enter or Add Button'
      },
      candidates: {
        get() {
          return this.Candidates
        },
        set(value) {
          if ( typeof value === 'object' ) {
            if ( Array.isArray(value) ) {
              this.$store.commit('setSelectedExams', value)
              return
            }
            let candidatesCopy = [...this.candidates]
            candidatesCopy.push(value)
            this.$store.commit('setSelectedExams', candidatesCopy)
          }
        }
      },
      currentlyEditing() {
        if (this.highlightedTableRow) {
          if (!('id' in this.highlightedTableRow)) return 'exam'
          return 'candidate'
        }
        return false
      },
      examTypes() {
        return this.pesticideExamTypes.map(type =>
          ({
            text: type.examName,
            value: type,
          })
        )
      },
      tableData() {
        let examsObj = {}
        this.candidates.forEach(candidate => {
          if ( candidate.examTypeId in examsObj ) {
            examsObj[candidate.examTypeId].push(candidate)
          } else {
            examsObj[candidate.examTypeId] = [candidate]
          }
        })
        let output = []
        for ( let examTypeId in examsObj ) {
          let exam = this.pesticideExamTypes.find(pesticideExam => pesticideExam.examTypeId == examTypeId)
          output.push({
            name: exam.examName,
            ...exam,
            qty: examsObj[examTypeId].length,
          })
          for ( let candidate of examsObj[examTypeId] ) {
            let { firstName, lastName } = candidate
            candidate.name = `${ firstName || '' }${ lastName ? ' ' : '' }${ lastName || '' }`
            output.push(candidate)
          }
        }
        return output
      },
    },
    methods: {
      addCandidate()  {
        if (!this.selectedExamType) return
        let id = Array.isArray(this.candidates) ? this.candidates.length + 1 : 1
        let newCandidate = {
          id,
          examTypeId: this.selectedExamType.examTypeId,
          examName: this.selectedExamType.examName,
        }
        this.formFields.forEach(field => {
          if (this[field]) {
            newCandidate[field] = this[field]
          } else {
            newCandidate[field] = ''
          }
        })
        this.candidates = newCandidate
        this.resetForm()
      },
      clickSelectItem(item) {
        this.selectedExamType = item
      },
      clickTableRow(examRow) {
        this.highlightedTableRow = examRow
        this.formFields.forEach(field => {
          if ( examRow[field] ) {
            this[field] = examRow[field]
          }
        })
        this.selectedExamType = this.pesticideExamTypes.find(type => type.examTypeId === examRow.examTypeId)

      },
      deleteExam({ id }) {
        let candidatesCopy = [ ...this.candidates ]
        let index = candidatesCopy.findIndex(candidate => candidate.id == id)
        candidatesCopy.splice(index, 1)
        this.candidates = candidatesCopy
        this.resetForm()
      },
      handleClick() {
        if ( this.currentlyEditing === 'exam' ) {
          this.updateExam()
          return
        }
        if ( this.currentlyEditing === 'candidate' ) {
          this.updateCandidate()
          return
        }
        this.addCandidate()
      },
      handleKeyboard(event) {
        if (event.key !== 'Enter') {
          return event
        } else {
          event.preventDefault()
          this.handleClick()
          this.$refs['first-name-input'].focus()
        }
      },
      removeListener() {
        document.removeEventListener('keydown', this.handleKeyboard)
      },
      resetForm() {
        for ( let field of this.formFields ) {
          this[field] = null
        }
        this.fees = 'collect'
        this.billTo = 'candidate'
        this.highlightedTableRow = null
        this.$nextTick(function() {
          if ( this.$refs.examstable ) {
            this.$refs.examstable.clearSelected()
          }
        })
      },
      updateCandidate() {
        let candidatesCopy = [ ...this.candidates ]
        let index = candidatesCopy.findIndex(candidate => candidate.id === this.highlightedTableRow.id)
        let updatedCandidate = { ...this.highlightedTableRow }
        if (this.selectedExamType) {
          updatedCandidate.examTypeId = this.selectedExamType.examTypeId
          updatedCandidate.examName = this.selectedExamType.examName
        }
        this.formFields.forEach(field => {
          if ( this[field] ) {
            updatedCandidate[field] = this[field]
          } else {
            updatedCandidate[field] = ''
          }
        })
        candidatesCopy[index] = updatedCandidate
        this.candidates = candidatesCopy
        this.resetForm()
      },
      updateExam() {
        let candidatesCopy = [...this.candidates]
        let oldExam = this.highlightedTableRow
        let newExam = this.selectedExamType
        candidatesCopy.forEach(candidate => {
          if (candidate.examTypeId === oldExam.examTypeId) {
            candidate.examTypeId = newExam.examTypeId
            candidate.examName = newExam.examName
          }
        })
        this.candidates = candidatesCopy
        this.resetForm()
      },
    }
  }

</script>

<style scoped>
  label {
    font-weight: 700 !important;
  }
  .mt-otto {
    margin-top: auto;
  }

  .candidate-table-style {
    font-size: 13px !important;
  }

  .add-candidate-top-row {
    margin: 8px 0 0 0 !important;
    padding: 0 8px 0 8px ! important;
    height: 20px;
    background-color: #D9E0E2;
  }

  .add-candidate-middle-row {
    margin: 0 !important;
    padding: 4px 8px 0 8px !important;
    background-color: #D9E0E2;
  }

  .label-reposition {
    position: relative;
    top: 3px !important;
  }

  .cursor-pointer {
    cursor: pointer !important;
  }

  .add-candidate-last-row {
    margin: 0 !important;
    padding: 0 8px 8px 8px !important;
    background-color: #D9E0E2;
  }
</style>
