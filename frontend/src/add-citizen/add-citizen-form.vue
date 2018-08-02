<template>
  <div class="add_citizen_template">
    <template v-if="addModalSetup === 'non-reception'">
      <b-container fluid class="add_citizen_template">
        <b-form>
          <Comments />
          <Channel />
          <Filters />
          <Tables />
        </b-form>
      </b-container>
    </template>
    <template v-else-if="addModalSetup === 'reception'">
      <b-container fluid class="add_citizen_template">
        <b-form>
          <Comments />
          <Channel />
          <Filters />
          <Tables />
        </b-form>
      </b-container>
    </template>
    <template v-else-if="addModalSetup === 'edit_mode' || addModalSetup === 'add_mode' ">
      <b-container fluid class="add_citizen_template">
        <b-form>
          <Channel />
          <Filters />
          <Tables />
        </b-form>
      </b-container>
    </template>
  </div>
</template>

<script>
import {mapState} from 'vuex'

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
    ...mapState(['addModalSetup'])
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