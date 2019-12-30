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
      <b-col cols="1" class="m-0 p-0" v-if="showQuickQIcon">To Q</b-col>
      <b-col cols="1" class="m-0 p-0">Serve</b-col>
      <b-col cols="5" class="m-0 p-0">Service</b-col>
      <b-col cols="*" class="m-0 p-0" v-if="!simplifiedModal">Category</b-col>
    </b-form-row>
    <b-form-row no-gutters>
      <b-col>
        <div id="innertable"
             style="height: 200px;
                    overflow-y: scroll;
                    margin: 0px;
                    background-color: #fcfcfc">
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
            <template slot="queueBut" slot-scope="data"
                      v-if="showQuickQIcon">
              <div @click.once="sendToQueue(data.item)">
                &nbsp;&nbsp;&nbsp;
                <font-awesome-icon icon="share-square"
                                   style="fontSize: 1rem; color: blue;"/>
              </div>
            </template>
            <template slot="serveBut" slot-scope="data">
              <div @click.once="serveCustomer(data.item)">
                &nbsp;&nbsp;&nbsp;
                <font-awesome-icon icon="hands-helping"
                                   style="fontSize: 1rem; color: green;"/>
              </div>
            </template>
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
            <template slot="parent.service_name" slot-scope="data">
              <div>
                {{data.item.parent.service_name}}
              </div>
            </template>
          </b-table>
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
      }
    },
    computed: {
      ...mapState({
        addModalSetup: 'addModalSetup',
        addCitizenModal: 'addCitizenModal',
        serviceModalForm: 'serviceModalForm',
        addModalForm: 'addModalForm',
        performingAction: 'performingAction'
      }),
      ...mapGetters({
        form_data: 'form_data',
        filtered_services: 'filtered_services',
        reception: 'reception',
        receptionist_status: 'receptionist_status'
      }),
      showQuickQIcon() {
        return this.reception && this.receptionist_status && this.addModalSetup == 'reception'
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
              { key: 'queueBut', label: 'To Q', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-icon' },
              { key: 'serveBut', label: 'Begin Service', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-icon' },
              { key: 'service_name', label: 'Service', thClass: 'd-none', sortable: false, style: "width: 5%", tdClass: 'addcit-td width-service' },
              { key: 'parent.service_name', label: 'Category', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-category', },
              {key: 'service_desc', label: '', thClass: 'd-none', sortable: false, tdClass: 'd-none',}
            ]
          }
          else {
            displayFields = [
              { key: 'serveBut', label: 'Begin Service', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-icon' },
              { key: 'service_name', label: 'Service', thClass: 'd-none', sortable: false, style: "width: 5%", tdClass: 'addcit-td width-service' },
              { key: 'parent.service_name', label: 'Category', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-category', },
              {key: 'service_desc', label: '', thClass: 'd-none', sortable: false, tdClass: 'd-none',}
              ]
          }
        }
        else {
          displayFields = [
            { key: 'serveBut', label: 'Begin Service', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-icon'},
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
        let id = item.service_id
        this.setAddModalSelectedItem(item.service_name)
        this.$store.commit('updateAddModalForm', {type:'service',value:id})
      },

      sendToQueue(service) {
        this.setAddModalSelectedItem(service.service_name)
        this.$store.commit('updateAddModalForm', {type: 'service', value: service.service_id})
        this.clickAddToQueue()
      },
      serveCustomer(service) {
        if (this.performingAction == false) {
          this.setAddModalSelectedItem(service.service_name)
          this.$store.commit('updateAddModalForm', {type: 'service', value: service.service_id})
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
        }
        else {
          console.log("==> Cannot quick serve customer, they are being added to the queue.")
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
.width-icon {
  width: 8%;
}
.width-service {
  width: 42%;
}
.width-category {
  width: 50%;
}
</style>
