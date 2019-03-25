<template>
  <div class="add_citizen_template">
    <template v-if="addModalSetup === 'add_mode' || addModalSetup === 'edit_mode' ">
      <div class="add_citizen_template">
        <div class="add_citizen_padding" style="background: rgb(240, 240, 240); padding-top: 12px; padding-bottom: 1px">
            <Channel />
            <div style="transform: translateY(19px);">
                <Filters />
            </div>
        </div>
        <b-container fluid class="add_citizen_padding" style="background:#504e4f; padding-top: 35px;">
            <Tables />
        </b-container>
      </div>
    </template>
    <template v-else>
      <div class="add_citizen_template">
        <div class="add_citizen_padding" style="background: rgb(240, 240, 240);padding-top: 12px;">
            <Comments v-if="!simplifiedModal" />
            <Channel />
            <div style="transform: translateY(18px);">
                <Filters />
            </div>
        </div>
        <b-container fluid class="add_citizen_padding" style="background:#504e4f; padding-top: 25px;">
            <Tables />
        </b-container>
      </div>
    </template>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

import Comments from './form-components/comments'
import Channel from './form-components/channel'
import Filters from './form-components/filters'
import Tables from './form-components/tables'

export default {
  name: 'AddCitizenForm',
  components: {
    Comments,
    Channel,
    Filters,
    Tables
  },
  computed: {
    ...mapState({addModalSetup: 'addModalSetup', }),
    ...mapGetters({reception: "reception",}),
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
    },  }
}

</script>

<style>
  .add_citizen_form_table {
    border-bottom: 1px solid darkgrey;
  }
  .add_citizen_form_label {
    font-size: 15px;
    font-weight: 400;
    width: 75px;
    text-align: right;
    line-height: 38px;
  }
  .add_citizen_padding {
      padding-left: 30px;
      padding-right: 30px;
  }
</style>
