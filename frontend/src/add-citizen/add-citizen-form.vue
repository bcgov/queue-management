<template>
  <b-container fluid>
    <b-form id="add_citizen_form">
      <template v-if="reception == 0">
        <div id='location-config1'>
          <Comments />
          <Channel />
          <Filters />
          <Tables />
        </div>
      </template>
      <template v-else-if="reception == 1">
        <div id='location-config3'>
          <Filters />
          <Tables />
          <Channel />
          <Comments />
        </div>
      </template>
    </b-form>
  </b-container>
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