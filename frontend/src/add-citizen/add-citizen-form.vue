<template>
  <div class="add_citizen_template">
    <template v-if="addModalSetup === 'add_mode' || addModalSetup === 'edit_mode' ">
      <b-container fluid class="add_citizen_template">
        <b-form>
          <Channel />
          <Filters />
          <Tables />
        </b-form>
      </b-container>
    </template>
    <template v-else>
      <b-container fluid class="add_citizen_template" v-if="reception">
        <b-form>
          <Comments />
          <Channel />
          <Filters />
          <Tables />
        </b-form>
      </b-container>
      <b-container fluid class="add_citizen_template" v-if="!reception">
        <b-form>
          <Channel />
          <Filters />
          <Tables />
          <Comments style="margin-top:5px"/>
        </b-form>
      </b-container>
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
  .add_citizen_template div {
    padding-left: 0px;
    padding-right: 0px;
  }
  .add_citizen_form_table {
    border-bottom: 1px solid darkgrey;
  }
</style>
