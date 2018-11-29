<template>
  <div class="add_citizen_template">
    <template v-if="addModalSetup === 'add_mode' || addModalSetup === 'edit_mode' ">
      <b-container fluid class="add_citizen_template">
          <Channel />
          <Filters />
      </b-container>
      <b-container>
          <Tables />
      </b-container>
    </template>
    <template v-else>
      <div class="add_citizen_template">
        <div class="add_citizen_padding" style="background: rgb(240, 240, 240);padding-top: 12px;padding-bottom: 40px;">
            <Comments />
            <Channel />
        </div>
        <b-container class="add_citizen_padding" style="position: absolute;top: 238px;">
            <Filters />
        </b-container>
        <b-container fluid class="add_citizen_padding" style="background:#504e4f; padding-top: 35px;">
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
    ...mapState(['addModalSetup']),
    ...mapGetters(['reception'])
  }
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
