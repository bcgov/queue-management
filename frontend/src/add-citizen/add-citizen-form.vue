<template>
  <div class="add_citizen_template">
    <template v-if="add_modal_setup === 'non-reception'">
      <b-container fluid class="add_citizen_template">
        <b-form>
          <Comments />
          <Channel />
          <Filters />
          <Tables />
        </b-form>
      </b-container>
    </template>
    <template v-else-if="add_modal_setup === 'reception'">
      <b-container fluid class="add_citizen_template">
        <b-form>
          <Comments />
          <Channel />
          <Filters />
          <Tables />
        </b-form>
      </b-container>
    </template>
    <template v-else-if="add_modal_setup === 'edit_mode'">
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
import {mapGetters} from 'vuex'

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
    ...mapGetters(['add_modal_setup'])
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