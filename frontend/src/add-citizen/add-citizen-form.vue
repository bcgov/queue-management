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
        <div class="add_citizen_template" v-if="reception">

      <b-container fluid style="background:#F0F0F0;">
          <Comments />
          <Channel />
          <Filters />
      </b-container>
      <b-container fluid style="background:black;">
          <Tables />
      </b-container>
        </div>
      <!-- <b-container fluid class="add_citizen_template" v-if="!reception">
          <Channel />
          <Filters />
          <Tables />
          <Comments style="margin-top:5px"/>
      </b-container> -->
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
</style>
