<template>
  <div class="add_citizen_template">
    <template v-if="reception == 0">
      <b-container fluid class="add_citizen_template">
        <b-form>
          <Comments />
          <Channel />
          <Filters />
          <Tables />
        </b-form>
      </b-container>
    </template>
    <template v-else-if="reception == 1">
      <b-container fluid class="add_citizen_template">
        <b-form>
          <Comments />
          <Channel />
          <Filters />
          <Tables />
        </b-form>
      </b-container>
    </template>
  </div>
</template>

<script>
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
    reception() {
      let ind = this.$store.state.user.receptionist_ind
      return ind
    }
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