<template>
  <b-form-group label="Channels"
                class="mt-1 mb-0 pt-0"
                
                >
    <b-select id="add_citizen_channels_select"
              :options="channel_options" 
              v-model="channel"
              size="sm"
              class="w-50 pt-0 pb-1 *-border-red"
              placeholder="Select delivery channel"
              />
  </b-form-group>
</template>

<script>
  import { mapGetters } from 'vuex'
  
  export default {
    name: 'Channel',
    data() {
      return {
        t: 'true',
        f: 'false',
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