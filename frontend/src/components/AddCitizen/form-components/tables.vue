<template>
  <b-container
    fluid
    class="add_citizen_form"
    style="
      border: 1px solid dimgrey;
      margin: 0px;
      padding-left: 0px;
      padding-right: 0px;
      padding-bottom: 5px;
    "
  >
    <b-form-row no-gutters class="m-0 add_citizen_table_header">
      <b-col
        cols="1"
        style="text-align: center"
        class="m-0 p-0"
        v-if="showQuickQIcon"
        >To Q</b-col
      >
      <b-col cols="2" style="text-align: center" class="m-0 p-0">Serve</b-col>
      <b-col cols="4" style="text-align: left" class="m-0 p-0">Service</b-col>
      <b-col
        cols="*"
        style="text-align: left"
        class="m-0 p-0"
        v-if="!simplifiedModal"
        >&nbsp;&nbsp;&nbsp;&nbsp;Category</b-col
      >
    </b-form-row>

    <b-form-row no-gutters>
      <b-col>
        <div
          id="innertable"
          style="
            height: 200px;
            overflow-y: scroll;
            overflow-x: hidden;
            margin: 0px;
            background-color: #fcfcfc;
          "
        >
          <div id="navi">
            <template v-if="showServeCitizenSpinner">
              <div class="q-loader2"></div>
            </template>
            <b-table
              :items="filtered_services"
              :fields="fields"
              sort-by="parent.service_name"
              :filter="filter"
              :small="t"
              :bordered="t"
              :striped="f"
              id="table2"
              @row-clicked="rowClicked"
              class="add_citizen_categories_table"
            >
              <!--  This is for the quick send to queue column  -->
              <template #cell(queueBut)="data" v-if="showQuickQIcon">
                <div @click.once="sendToQueue(data.item)">
                  &nbsp;&nbsp;&nbsp;
                  <font-awesome-icon
                    icon="share-square"
                    style="font-size: 1rem; color: blue"
                  />
                </div>
              </template>

              <!--  This is for the quick serve column  -->
              <template #cell(serveBut)="data">
                <div @click.once="serveCustomer(data.item)">
                  &nbsp;&nbsp;&nbsp;
                  <font-awesome-icon
                    icon="hands-helping"
                    style="font-size: 1rem; color: green"
                  />
                </div>
              </template>

              <!--  Service name column. Active variant is for row selected, bind to description.  -->
              <template #cell(service_name)="data">
                <div>
                  <span v-bind:title="data.item.service_desc">{{
                    data.item.service_name
                  }}</span>
                  <div style="display: none">
                    {{
                      data.item.service_id == form_data.service
                        ? (data.item._rowVariant = 'active')
                        : (data.item._rowVariant = '')
                    }}
                  </div>
                </div>
              </template>

              <!--  This is for the category, the parent name.  -->
              <template #cell(parent)="data">
                <div>{{ data.item.parent.service_name }}</div>
              </template>
            </b-table>
          </div>
        </div>
      </b-col>
    </b-form-row>
  </b-container>
</template>

<script lang="ts">

import { Action, Getter, Mutation, State } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'

@Component({})
export default class Tables extends Vue {
  @State('addModalSetup') private addModalSetup!: any
  @State('addCitizenModal') private addCitizenModal!: any
  @State('serviceModalForm') private serviceModalForm!: any
  @State('addModalForm') private addModalForm!: any
  @State('performingAction') private performingAction!: any
  @State('showServeCitizenSpinner') private showServeCitizenSpinner!: any

  @Getter('form_data') private form_data!: any;
  @Getter('filtered_services') private filtered_services!: any;
  @Getter('reception') private reception!: any;
  @Getter('receptionist_status') private receptionist_status!: any;

  @Action('clickQuickServe') public clickQuickServe: any
  @Action('clickAddServiceApply') public clickAddServiceApply: any
  @Action('clickBeginService') public clickBeginService: any
  @Action('resetAddCitizenModal') public resetAddCitizenModal: any
  @Action('clickAddToQueue') public clickAddToQueue: any
  @Action('clickEditApply') public clickEditApply: any

  @Mutation('setAddModalSelectedItem') public setAddModalSelectedItem: any
  @Mutation('toggleExamsTrackingIP') public toggleExamsTrackingIP: any
  @Mutation('setPerformingAction') public setPerformingAction: any

  // seems like not using confirm and remove
  private f: boolean = false
  private t: boolean = true
  private actionToExecute: string = 'NOTHING'

  get showQuickQIcon () {
    return this.reception && this.receptionist_status &&
      this.addModalSetup == 'reception' && this.$route.path == '/queue'
  }

  get simplified () {
    if (this.$route.path !== '/queue') {
      return true
    }
    return false
  }

  get simplifiedModal () {
    if (this.simplified && this.addModalSetup !== 'edit_mode') {
      return true
    }
    return false
  }

  get simplifiedTicketStarted () {
    if (this.$route.path == '/queue') {
      if (this.serviceModalForm.citizen_id) {
        return true
      }
    }
    return false
  }

  get fields () {
    let displayFields: any = null
    if (!this.simplifiedModal) {
      if (this.showQuickQIcon) {
        displayFields = [
          { key: 'queueBut', label: 'To Q', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-queue' },
          { key: 'serveBut', label: 'Begin Service', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-servenow-recp' },
          { key: 'service_name', label: 'Service', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-service' },
          { key: 'parent.service_name', label: 'Category', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-category' },
          { key: 'service_desc', label: '', thClass: 'd-none', sortable: false, tdClass: 'd-none' }
        ]
      } else {
        displayFields = [
          { key: 'serveBut', label: 'Begin Service', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-servenow-other' },
          { key: 'service_name', label: 'Service', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-service' },
          { key: 'parent.service_name', label: 'Category', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-category' },
          { key: 'service_desc', label: '', thClass: 'd-none', sortable: false, tdClass: 'd-none' }
        ]
      }
    } else {
      displayFields = [
        { key: 'serveBut', label: 'Begin Service', thClass: 'd-none', sortable: false, tdClass: 'addcit-td width-servenow-other' },
        { key: 'service_name', label: 'Service', sortable: false, thClass: 'd-none', tdClass: 'addcit-td' }
      ]
    }

    return displayFields
  }

  get filter () {
    return this.form_data.search
  }

  rowClicked (item: any, index: any) {
    if (!this.performingAction) {
      const id = item.service_id
      this.setAddModalSelectedItem(item.service_name)
      this.$store.commit('updateAddModalForm', { type: 'service', value: id })
      if (this.actionToExecute == 'sendToQueue') {
        this.clickAddToQueue()
      } else if (this.actionToExecute == 'serveCustomer') {
        this.serveCustomerAction() // item
      } else {
        console.log('unknown action: ', this.actionToExecute)
      }
    }
  }

  sendToQueue () {
    this.$store.commit('toggleServeCitizenSpinner', true)
    this.actionToExecute = 'sendToQueue'
  }

  serveCustomer () {
    this.$store.commit('toggleServeCitizenSpinner', true)
    this.actionToExecute = 'serveCustomer'
  }

  serveCustomerAction () {
    //  NOTE!!     When actionToTake is serveCustomer then we execute this code
    if (this.addModalSetup === 'add_mode') {
      this.clickAddServiceApply()
    } else if (this.addModalSetup === 'edit_mode') {
      this.clickEditApply()
    } else if (this.$route.path === '/exams') {
      this.toggleExamsTrackingIP(true)
      this.clickBeginService({ simple: true })
    } else if (this.$route.path === '/appointments') {
      this.$store.commit('appointmentsModule/setSelectedService', this.addModalForm.service)
      this.closeAddServiceModal()
    } else if (this.$route.path === '/booking') {
      this.toggleExamsTrackingIP(true)
      this.clickBeginService({ simple: true })
    } else if (this.$route.path === '/service-flow') {
      // remove continue button in service flow
      this.toggleExamsTrackingIP(true)
      this.clickBeginService({ simple: true })
    } else if ((!this.simplifiedTicketStarted) && (this.addModalSetup == 'reception' || this.addModalSetup == 'non_reception')) {
      this.clickBeginService({ simple: false })
    } else {
      console.log('==> No service selected.')
    }
  }

  closeAddServiceModal () {
    this.resetAddCitizenModal()
    this.$store.commit('appointmentsModule/toggleApptBookingModal', true)
  }
}

</script>

<style>
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
#navi {
  position: relative;
}
.q-loader2 {
  position: absolute;
  text-align: center;
  margin: 50px auto auto 300px;
  width: 50px;
  height: 50px;
  border: 10px solid LightGrey;
  opacity: 0.9;
  border-radius: 50%;
  border-top-color: DodgerBlue;
  animation: spin 1s ease-in-out infinite;
  -webkit-animation: spin 1s ease-in-out infinite;
}
.add_citizen_categories_table {
  padding: 0px;
  z-index: 1;
}
.add_citizen_table_header {
  background-color: rgb(179, 183, 186);
  color: white;
  height: 35px;
  padding-top: 6px;
  padding-left: 0px;
  text-align: center;
  font-size: 17px;
  text-shadow: 0px 0px 2px #a5a5a5;
  z-index: 1;
}
.addcit-td {
  cursor: pointer;
}
.width-queue {
  width: 8%;
  text-align: center;
}
.width-servenow-recp {
  width: 10%;
  text-align: center;
}

.width-servenow-other {
  width: 16%;
  text-align: center;
}
.width-service {
  width: 32%;
  text-align: left;
}
.width-category {
  width: 32%;
  text-align: left;
}
</style>
