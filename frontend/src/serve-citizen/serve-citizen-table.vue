

<template>
  <b-table :fields="fields"
           :items="items"
           head-variant="light"
           small
           outlined
           hover
           fixed
           bordered
           style="text-align: center"
           class="p-0 m-0">
    <template slot="start_time" slot-scope="data">
      {{ formatTime(data.item.start_time) }}
    </template>
    <template slot="quantity" slot-scope="data">
      <div style="display: none">
        {{text1=data.item.service_reqs[0].quantity}}
      </div>
      <div class="w-100">
        <b-form-input v-model="text1"
                      type="text"
                      size="sm"
                      class="w-25 mx-auto"></b-form-input>
      </div>
    </template>
    <template slot="editBut" slot-scope="row">
      <b-button @click="clickEdit" >
        edit
      </b-button>
    </template>
  </b-table>
</template>

<script>
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'

export default {
    name: 'ServeCitizenTable',
    data() {
      return {
        text1: '',
        fields: [
          {key:'service_reqs[0].service.parent.service_name', label:'Category'},
          {key:'service_reqs[0].service.service_name', label:'Service'},
          {key:'start_time', label:'Stand Time'},
          {key:'quantity', label:'Quantity'},
          {key:'editBut', label:'Change Service'},
        ]
      }
    },
    computed: {
      ...mapState({
        citizen: 'invitedCitizen',
      }),
      items() {
        return [this.citizen]
      }
    },
    methods: {
      ...mapActions(['clickEdit']),

      formatTime(data) {
        let time = new Date(data)
        return time.toLocaleTimeString()
      }
    }
  }
</script>
