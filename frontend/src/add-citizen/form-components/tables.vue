<template>
  <b-container fluid
               class="add_citizen_form"
               style="border: 1px solid dimgrey;
                      margin: 0px;
                      padding-left: 0px;
                      padding-right: 0px;
                      padding-bottom: 5px;"
                      >
    <b-form-row no-gutters class="m-0 add_citizen_table_header">
      <b-col cols="2" class="m-0 p-0" v-if="showQuickQIcon">To Q</b-col>
      <b-col cols="2" class="m-0 p-0">Serve</b-col>
      <b-col cols="4" class="m-0 p-0">Service</b-col>
      <b-col cols="*" class="m-0 p-0" v-if="!simplifiedModal">Category</b-col>
    </b-form-row>

    <b-form-row no-gutters>
      <b-col>
        <div id="innertable"
             style="height: 200px;
                    overflow-y: scroll;
                    margin: 0px;
                    background-color: #fcfcfc">
        <div>
                <template v-if="showServeCitizenSpinner">
                   <div class="q-loader2" ></div>
                </template>
          <b-table :items="filtered_services"
                   :fields="fields"
                   sort-by="parent.service_name"
                   :filter="filter"
                   :small="t"
                   :bordered="f"
                   :striped="f"
                   id="table2"
                   @row-clicked="rowClicked"
                   class="add_citizen_categories_table">

            <!--  This is for the quick send to queue column  -->
            <template slot="queueBut" slot-scope="data"
                      v-if="showQuickQIcon">
              <div @click.once="sendToQueue(data.item)">
                &nbsp;&nbsp;&nbsp;
                <font-awesome-icon icon="share-square"
                                   style="fontSize: 1rem; color: blue;"/>
              </div>
            </template>

            <!--  This is for the quick serve column  -->
            <template slot="serveBut" slot-scope="data">
              <div @click.once="serveCustomer(data.item)">
                &nbsp;&nbsp;&nbsp;
                <font-awesome-icon icon="hands-helping"
                                   style="fontSize: 1rem; color: green;"/>
              </div>
            </template>

            <!--  Service name column. Active variant is for row selected, bind to description.  -->
            <template slot="service_name" slot-scope="data">
              <div>
                <span v-bind:title="data.item.service_desc">
                  {{data.item.service_name}}
                </span>
                <div style="display: none">
                  {{ data.item.service_id==form_data.service ?
                      data.item._rowVariant='active' : data.item._rowVariant='' }}
                </div>
              </div>
            </template>

            <!--  This is for the category, the parent name.  -->
            <template slot="parent.service_name" slot-scope="data">
              <div>
                {{data.item.parent.service_name}}
              </div>
            </template>
          </b-table>
          </div>
        </div>
      </b-col>
    </b-form-row>
  </b-container>
</template>

<script>
  import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'

  export default {
    name: 'Tables',
    data() {
      return {
        f:false,
        t:true,
        actionToExecute: 'NOTHING'
      }
    },
    computed: {
      ...mapState({
        addModalSetup: 'addModalSetup',
        addCitizenModal: 'addCitizenModal',
        serviceModalForm: 'serviceModalForm',
        addModalForm: 'addModalForm',
        performingAction: 'performingAction',
        showServeCitizenSpinner: 'showServeCitizenSpinner',
      }),
      ...mapGetters({
        form_data: 'form_data',
        filtered_services: 'filtered_services',
        reception: 'reception',
        receptionist_status: 'receptionist_status'
      }),
      showQuickQIcon() {
        return this.reception && this.receptionist_status
               && this.addModalSetup == 'reception' && this.$route.path == '/queue'
      },
      simplified() {
        if (this.$route.path !== '/queue') {
          return true
        }
        return false
      },
      simplifiedModal() {
        if (this.simplified && this.addModalSetup !== 'edit_mode') {
          return true
        }
        return false
      },
      simplifiedTicketStarted() {
        if (this.$route.path == '/queue') {
          if (this.serviceModalForm.citizen_id) {
            return true
          }
        }
        return false
      },
      fields() {
        let displayFields = null
        if (!this.simplifiedModal) {
          if (this.showQuickQIcon) {
            displayFields = [
              { key: 'queueBut', label: 'To Q', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-queue' },
              { key: 'serveBut', label: 'Begin Service', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-servenow-recp' },
              { key: 'service_name', label: 'Service', thClass: 'd-none', sortable: false, style: "width: 5%", tdClass: 'addcit-td width-service' },
              { key: 'parent.service_name', label: 'Category', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-category', },
              {key: 'service_desc', label: '', thClass: 'd-none', sortable: false, tdClass: 'd-none',}
            ]
          }
          else {
            displayFields = [
              { key: 'serveBut', label: 'Begin Service', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-servenow-other' },
              { key: 'service_name', label: 'Service', thClass: 'd-none', sortable: false, style: "width: 5%", tdClass: 'addcit-td width-service' },
              { key: 'parent.service_name', label: 'Category', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-category', },
              {key: 'service_desc', label: '', thClass: 'd-none', sortable: false, tdClass: 'd-none',}
              ]
          }
        }
        else {
          displayFields = [
            { key: 'serveBut', label: 'Begin Service', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-servenow-other'},
            { key: 'service_name', label: 'Service', sortable: false, thClass: 'd-none', tdClass: 'addcit-td',}
          ]
        }

        return displayFields
      },
      filter(value) {
        return this.form_data.search
      },
    },

    methods: {
      ...mapMutations(['setAddModalSelectedItem', 'toggleExamsTrackingIP', 'setPerformingAction']),
      ...mapActions(['clickQuickServe', 'clickAddServiceApply',
        'clickBeginService', 'resetAddCitizenModal', 'clickAddToQueue',
        'clickEditApply']),

    rowClicked(item, index) {
        if (this.performingAction == false) {
          let id = item.service_id
          this.setAddModalSelectedItem(item.service_name)
          this.$store.commit('updateAddModalForm', {type:'service',value:id})
          if (this.actionToExecute == 'sendToQueue') {
            this.clickAddToQueue()
          } else if (this.actionToExecute == 'serveCustomer') {
            this.serveCustomerAction(item)
          } else {
            console.log("unknown action: ",this.actionToExecute)
          }
        }
    },
    sendToQueue() {
        this.$store.commit('toggleServeCitizenSpinner', true)
        this.actionToExecute = 'sendToQueue'
    },
    serveCustomer() {
        this.$store.commit('toggleServeCitizenSpinner', true)
        this.actionToExecute = 'serveCustomer'
    },
    serveCustomerAction() {
        //  NOTE!!     When actionToTake is serveCustomer then we execute this code
        if (this.$route.path == "/exams") {
          this.toggleExamsTrackingIP(true)
          this.clickBeginService({simple: true})
        } else if (this.$route.path == "/appointments") {
          this.$store.commit('appointmentsModule/setSelectedService', this.addModalForm.service)
          this.closeAddServiceModal()
        } else if (this.$route.path == "/booking") {
          this.toggleExamsTrackingIP(true)
          this.clickBeginService({simple: true})
        } else if ((!this.simplifiedTicketStarted) && (this.addModalSetup == "reception" || this.addModalSetup == "non_reception")) {
          this.clickBeginService({simple: false})
        } else if (this.simplifiedTicketStarted) {
          if (this.addModalSetup == "add_mode") {
             this.clickAddServiceApply()
          } else if (this.addModalSetup == "edit_mode") {
            this.clickEditApply()
          } else {
            console.log("==> No service selected.")
          }
        } else {
          console.log("==> Still no service selected")
        }
      },
      closeAddServiceModal() {
        this.resetAddCitizenModal()
        this.$store.commit('appointmentsModule/toggleApptBookingModal', true)
      },
    }
  }
</script>

<style>
.add_citizen_categories_table {
  padding: 0px;
}
.add_citizen_table_header {
    background-color: rgb(179, 183, 186);
    color: white;
    height: 35px;
    padding-top: 6px;
    padding-left: 0px;
    text-align: left;
    font-size: 17px;
    text-shadow: 0px 0px 2px #a5a5a5;
}
.addcit-td {
  cursor: pointer;
}
.q-loader2 {
  position: relative;
  text-align: center;
  margin: 15px auto 35px auto;
  z-index: 9999;
  display: block;
  width: 50px;
  height: 50px;
  border: 10px solid LightGrey;
  opacity:0.9;
  border-radius: 50%;
  border-top-color: DodgerBlue;
  animation: spin 1s ease-in-out infinite;
  -webkit-animation: spin 1s ease-in-out infinite;
}
.width-queue {
  width: 16%;
}
.width-servenow-recp {
  width: 16%;
}

.width-servenow-other {
  width: 16%;
}
.width-service {
  width: 35%;
}
.width-category {
  width: 50%;
}
</style>
