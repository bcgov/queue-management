

<template>
  <div id="serve-citizen-table-container">
    <b-row>
      <b-col>
        <b-table :fields="fields"
                 :items="invited_service_reqs"
                 head-variant="light"
                 class="m-0 p-0 align-middle"
                 small
                 id="serve-table"
                 fixed
                 bordered
                 style="text-align: center">
          <template slot="status" slot-scope="row">
            <div v-if="row.item.periods.some(p=>p.time_end===null)===true">
              <div style="font-weight: 900;">Active</div>
            </div>
            <div v-if="row.item.periods.some(p=>p.time_end===null)===false">
              Inactive
            </div>
          </template>
          <template slot="quantity" slot-scope="row">
            <div v-if="row.item.periods.some(p=>p.time_end===null)===true" >
              <div style="margin: auto;">
                <b-input :value="getQuantity()"
                         @input="setQuantity"
                         size="sm"
                         style="height: 1.8em; width: 40%; margin-left: 30%; text-align: center;" />
              </div>
            </div>
            <div v-if="row.item.periods.some(p=>p.time_end===null)===false">
              {{ invited_service_reqs[row.index].quantity }}
            </div>
          </template>
          <template slot="service.service_name" slot-scope="row">
            {{ row.item.service.service_name }}
            <div style="display: none">
              {{
                row.item.periods.some(p=>p.time_end===null) ?
                   row.item._rowVariant='info' : row.item._rowVariant=''
              }}
            </div>
          </template>
          <template slot="editBut" slot-scope="row">
            <div v-if="row.item.periods.some(p => p.time_end === null) === true" >
              <b-button size="sm"
                        @click="clickEdit"
                        variant="link">edit</b-button>
            </div>
            <div v-if="row.item.periods.some(p=>p.time_end===null)===false">
              <b-button size="sm" variant="link" @click="clickMakeActive(row.item.sr_id)">make active</b-button>
            </div>
          </template>
        </b-table>
      </b-col>
    </b-row>
    <div v-if="showTicketNotice"
         style="background-color: #bee5eb;"
         class="p-2 m-0 tr-container-div">
      You don't have a ticket started at this time.  Click Begin to start one.
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'

export default {
  name: 'ServeCitizenTable',

  data() {
    return {
      fields: [
        {key:'status', label: 'Status', thStyle:'text-align: center;'},
        {key:'service.parent.service_name', tdClass: 'align-middle', label:'Category', thStyle:'text-align: center;'},
        {key:'service.service_name', tdClass: 'align-middle', label:'Service', thStyle:'text-align: center;'},
        {key:'quantity', label:'Quantity', thStyle:'text-align: center;'},
        {key:'editBut', label:'Change Service', thStyle:'text-align: center;'}
      ]
    }
  },

  computed: {
    ...mapState(['serviceModalForm']),
    ...mapGetters([
      'invited_service_reqs',
      'active_service',
      'active_index'
    ]),
    showTicketNotice() {
      if (this.$route.path !== '/queue' && !this.serviceModalForm.citizen_id) {
        return true
      }
      return false
    },
  },

  methods: {
    ...mapActions([
      'clickEdit',
      'clickMakeActive'
    ]),
    ...mapMutations(['editServiceModalForm']),

    formatTime(data) {
      let time = new Date(data)
      return time.toLocaleTimeString()
    },

    setQuantity(value) {
      this.editServiceModalForm({
        type: 'activeQuantity',
        value
      })
    },

    getQuantity() {
      if (!this.serviceModalForm.activeQuantity) {
        return ''
      } else {
        return this.serviceModalForm.activeQuantity
      }
    }
  }
}
</script>
<style>
#serve-citizen-table-container {
    width: 100%;
    padding-right: 15px;
    padding-left: 15px;
    margin-right: auto;
    margin-left: auto;
    background: #504E4F;
    padding-top: 40px;
}

#serve-table {
    background-color: white;
}
#serve-table .table-info,
#serve-table .table-info>td,
#serve-table .table-info>th {
    background-color: #ecf9ff;
}
#serve-table > thead > tr > th {
    background-color: #B5B7BC;
    color: white;
    padding: 7px;
    font-size: 16px;
}
td {
    vertical-align: middle!important;
}
</style>
