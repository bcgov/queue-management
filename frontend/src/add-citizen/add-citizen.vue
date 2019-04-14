<template>
  <b-modal :visible="showAddModal"
           :size="simplified ? 'md' : 'lg' "
           hide-header
           hide-footer
           no-close-on-backdrop
           no-close-on-esc
           body-class="q-modal-body"
           class="m-0 p-0"
           @shown="setupForm()">
    <div style="display: flex; flex-direction: row; justify-content: space-between"
         class="modal_header"
         v-dragged="onDrag">
      <div>
        <h4>{{modalTitle}}</h4>
      </div>
      <div>
        <button class="btn btn-link"
                style="margin-left: 20px"
                @click="toggleMinimize">{{ minimizeWindow ? "Maximize" : "Minimize" }}</button>
      </div>
    </div>
    <b-alert :show="dismissCountDown"
             style="h-align: center"
             variant="danger"
             @dismissed="dismissCountDown=0"
             @dismiss-count-down="countDownChanged">{{this.$store.state.alertMessage}}</b-alert>
    <div v-if="!minimizeWindow">
      <div v-if="!this.addModalForm.citizen">
        <div class="q-loader" />
      </div>
      <div v-else>
        <AddCitizenForm />
        <b-container class="add-buttons add_citizen_padding">
          <div class="button-row"
               style="padding-bottom:6px;">
            <div id="select-wrapper">
              <select id="priority-selection"
                      v-if="!simplified"
                      class="custom-select"
                      v-model="priority_selection">
                <option value="1">High Priority</option>
                <option value="2">Default Priority</option>
                <option value="3">Low Priority</option>
              </select>
            </div>
            <select v-show="reception && !simplified" id="counter-selection" class="custom-select" v-model="counter_selection">
              <option v-for="counter in sortedCounters"
                    :value="counter.counter_id"
                    :key="counter.counter_id">
                {{counter.counter_name}}
              </option>
            </select>
          </div>
          <div class="button-row">
            <Buttons />
          </div>
        </b-container>
      </div>
    </div>
  </b-modal>
</template>

<script>
import { mapState, mapGetters, mapMutations, mapActions } from "vuex"
import Buttons from "./form-components/buttons"
import AddCitizenForm from "./add-citizen-form"

export default {
  name: "AddCitizen",
  components: {
    AddCitizenForm,
    Buttons
  },
  mounted() {
    this.$root.$on("showAddMessage", () => {
      this.Alert()
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
    ...mapState({
      addCitizenModal: 'addCitizenModal',
      addModalForm: 'addModalForm',
      showAddModal: 'showAddModal',
      addModalSetup: 'addModalSetup',
      serviceModalForm: 'serviceModalForm',
      user: 'user'
    }),
    ...mapGetters({form_data: "form_data", reception: "reception",}),
    simplified() {
      if (this.$route.path !== '/queue') {
        return true
      }
      return false
    },
    modalTitle() {
      if (this.addModalSetup === "edit_mode") {
        return "Edit Service"
      }
      if (this.simplified) {
        return 'Begin Tracking'
      }
      return "Add Citizen"
    },

    counter_selection: {
      get() {
        return this.form_data.counter;
      },
      set(value) {
        this.updateAddModalForm({ type: "counter", value });
      }
    },
    priority_selection: {
      get() {
        return this.form_data.priority
      },
      set(value) {
        this.updateAddModalForm({ type: "priority", value })
      }
    },
    sortedCounters(){
      var sorted = this.user.office.counters.sort((a,b) => {
        return a.counter_name > b.counter_name
      })
      console.log(sorted)
      return sorted
    }
  },
  methods: {
    ...mapActions(["cancelAddCitizensModal"]),
    ...mapMutations(["updateAddModalForm", "setDefaultChannel"]),
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown
    },
    setupForm() {
      let setup = this.addModalSetup;
      if (this.simplified) {
        this.$root.$emit("focusfilter")
        return
      }
      if (setup === "add_mode" || setup === "edit_mode") {
        this.$root.$emit("focusfilter")
      } else {
        if (!this.reception) {
          this.$root.$emit("focusfilter")
        } else if (this.reception) {
          this.$root.$emit("focuscomments")
        }
      }
    },
    Alert() {
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
      var add_modal = document.getElementsByClassName('modal-content')[0]
      add_modal.style.transform = "translate("+this.left+"px,"+this.top+"px)"
    }
  }
}
</script>

<style>
.modal_header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 10px 20px 1px;
  cursor: grab;
}

.add-buttons {
  background: #504e4f;
  padding: 5px 15px 20px;
}

.button-row {
  background: #504e4f;
  display: flex;
  flex-direction: row-reverse;
}
</style>
