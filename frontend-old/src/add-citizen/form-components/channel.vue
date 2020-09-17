<template>
  <div class="add_citizen_form mt-1" v-if="$route.path !== '/appointments'">
    <b-form-row no-gutters>
      <b-col cols="auto">
        <label class="add_citizen_form_label">Channel:</label>
      </b-col>
      <b-col>
        <b-select id="add_citizen_channels_select"
                  :options="channel_options"
                  v-model="channel"
                  style="height: 38px; font-size: .8rem;"
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
      ...mapGetters([ 'channel_options', 'form_data' ]),
      channel: {
        get() { return this.form_data.channel },
        set(value) {
          this.$store.commit('updateAddModalForm', { type: 'channel', value })
        }
      }
    }
  }
</script>

<style>
  .add_citizen_form {
    padding-bottom: 2px;
  }
</style>
