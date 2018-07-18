<template>
<b-form id="add_citizen_form">
  <template v-if="office == 1">
      <div id='location-config1'>
        <Comments />
        <Channel />
        <Filters />
        <Tables />
      </div>
    </template>
  <template v-else-if="office == 2">
      <div id='location-config2'>
        <Comments />
        <Channel />
        <Filters />
        <Tables />
      </div>
    </template>
  <template v-else-if="office == 3">
      <div id='location-config3'>
        <Filters />
        <Tables />
        <Channel />
        <Comments />
      </div>
    </template>
  <template v-else>
      <div id='location-config0'>
        <Comments />
        <Channel />
        <Filters />
        <Tables />
      </div>
    </template>
</b-form>
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
    office() {
      return Number(this.$store.state.userOfficeType)
    }
  }
}
</script>