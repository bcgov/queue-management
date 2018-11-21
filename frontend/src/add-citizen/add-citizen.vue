

<template>
  <b-modal :visible="showAddModal"
           size="lg"
           hide-header
           hide-footer
           no-close-on-backdrop
           no-close-on-esc
           class="m-0 p-0"
           @shown="setupForm()" v-dragged="onDrag">
    <div style="display: flex; flex-direction: row; justify-content: space-between" class="modal_header">
      <div><h4>{{modalTitle}}</h4></div>
      <div>
        <b-button size="sm"
                  class="btn-primary"
                  style="margin-left: 20px"
                  @click="toggleMinimize">{{ minimizeWindow ? "Maximize" : "Minimize" }}</b-button>
      </div>
    </div>
    <b-alert :show="dismissCountDown"
              style="h-align: center"
              variant="danger"
              @dismissed="dismissCountDown=0"
              @dismiss-count-down="countDownChanged">{{this.$store.state.alertMessage}}</b-alert>
    <b-container class="pb-3" id="serve-citizen-modal-top" fluid v-if="!minimizeWindow">

      <div v-if="!this.addModalForm.citizen">
        <div class="loader"></div>
      </div>
      <div v-else>
        <AddCitizenForm />
        <b-container class="mt-3 pr-3">
          <b-row align-v="center" align-h="end">
            <div id="select-wrapper" style="padding-right: 10px; padding-left: 5px;">
              <select id="priority-selection" class="custom-select" v-model="priority_selection">
                <option value=1>High Priority</option>
                <option value=2>Default Priority</option>
                <option value=3>Low Priority</option>
              </select>
            </div>
            <div v-if="reception" class="mr-1 btn-success" style="border-radius: 5px">
              <b-form-checkbox v-model="quickTrans" value="1" unchecked-value="0"
                               class="mt-3 ml-1 mr-1 pb-1 quick" style="position: relative; top: -5px;">
                <span style="font: 400 16px Myriad-Pro;">Quick Txn</span>
              </b-form-checkbox>
            </div>
            <Buttons />
          </b-row>
        </b-container>
      </div>
    </b-container>
  </b-modal>
</template>

<script>

import {
  mapState, mapGetters, mapMutations, mapActions
}
from 'vuex'
import Buttons from './form-components/buttons'
import AddCitizenForm from './add-citizen-form'

export default {
    name: 'AddCitizen',

    components: {
        AddCitizenForm, Buttons
    },

    mounted() {
      this.$root.$on('showAddMessage', () => {
        this.showAlert()
      })
    },

    data() {
      return {
        dismissSecs: 5,
        dismissCountDown: 0,
        minimizeWindow: false
      }
    },

    computed: {
      ...mapState(['addCitizenModal', 'addModalForm', 'showAddModal', 'addModalSetup', 'serviceModalForm']),
      ...mapGetters(['form_data', 'reception']),

      modalTitle() {
        if (this.addModalSetup === 'edit_mode') {
          return 'Edit Service'
        } else {
          return 'Add Citizen'
        }
      },

      quickTrans: {
        get() { return this.form_data.quick },
        set(value) { this.updateAddModalForm({type:'quick',value}) }
      },

      priority_selection: {
        get() { return this.form_data.priority },
        set(value) {
          this.updateAddModalForm({type:'priority',value})
        }
      }
    },

    methods: {
      ...mapActions(['cancelAddCitizensModal']),
      ...mapMutations(['updateAddModalForm', 'setDefaultChannel']),

      countDownChanged (dismissCountDown) {
        this.dismissCountDown = dismissCountDown
      },
      setupForm() {
        let setup = this.addModalSetup
        if (setup === 'add_mode' || setup === 'edit_mode') {
          this.$root.$emit( 'focusfilter' )
        } else {
          if (!this.reception) {
            this.$root.$emit( 'focusfilter' )
          } else if (this.reception) {
            this.$root.$emit( 'focuscomments' )
          }
        }
      },
      showAlert () {
        this.dismissCountDown = this.dismissSecs
      },
      toggleMinimize() {
        this.minimizeWindow = !this.minimizeWindow
      },
      onDrag({ el, deltaX, deltaY, offsetX, offsetY, clientX, clientY, first, last }) {
        if (first) {
          this.dragged = true
          return
        }
        if (last) {
          this.dragged = false
          return
        }
        this.left = (this.left || 0) + deltaX
        this.top = (this.top || 0) + deltaY
        let transform = "translate("+this.left+"px,"+this.top+"px)"
        console.log(transform)
        console.log(el)
        el.querySelector('.modal-content').style.transform = transform
      }
    }
  }
</script>

<style>
  .disabled {
    background-color: #8e9399 !important;
    color: Gainsboro !important;
  }
  .disabled:hover {
    background-color: #8e9399 !important;
  }
  .loader {
    position: relative;
    text-align: center;
    margin: 15px auto 35px auto;
    z-index: 9999;
    display: block;
    width: 80px;
    height: 80px;
    border: 10px solid rgba(0, 0, 0, .3);
    border-radius: 50%;
    border-top-color: #000;
    animation: spin 1s ease-in-out infinite;
    -webkit-animation: spin 1s ease-in-out infinite;
  }
  @keyframes spin {
    to {
      -webkit-transform: rotate(360deg);
    }
  }

  @-webkit-keyframes spin {
    to {
      -webkit-transform: rotate(360deg);
    }
  }
</style>
