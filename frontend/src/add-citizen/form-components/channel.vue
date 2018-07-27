<template>
  <b-container fluid class="add_citizen_form mt-2">
    <b-form-row no-gutters>
      <b-col cols="auto">
        <label>Channel</label>
      </b-col>
      <b-col>
        <b-select id="add_citizen_channels_select"
                  :options="channel_options" 
                  v-model="channel"
                  size="sm"
                  label="Channels"
                  placeholder="Select delivery channel"
                  />
      </b-col>
    </b-form-row>
  </b-container>
</template>

<script>
  import { mapGetters } from 'vuex'
  
  export default {
    name: 'Channel',
    data() {
      return {
        t: true,
        f: false,
        state: 'invalid'
      }
    },
    computed: {
      ...mapGetters(['channel_options', 'form_data']),
      channel: {
        get() { return this.form_data.channel },
        set(value) {
          this.$store.commit('updateModalForm',{type: 'channel', value})
        }
      }
    }
  }
</script>