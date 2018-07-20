<template>
  <div>
  <b-form-row>
    <b-col class="px-0 pb-0 pt-2 m-0" cols="2">
      <label>Channel</label>
    </b-col>
    <b-col class="px-0 pb-0 pt-2 m-0">
      <b-select id="add_citizen_channels_select"
                :options="channel_options" 
                v-model="channel"
                size="sm"
                label="Channels"
                placeholder="Select delivery channel"
                />
    </b-col>
  </b-form-row>
</div>
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