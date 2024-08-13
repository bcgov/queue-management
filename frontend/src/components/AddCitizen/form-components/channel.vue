<template>
  <div class="add_citizen_form mt-1" v-if="$route.path !== '/appointments'">
    <b-form-row no-gutters>
      <b-col cols="auto">
        <label class="add_citizen_form_label" for="add_citizen_channels_select">Channel:</label>
      </b-col>
      <b-col>
        <b-select
          id="add_citizen_channels_select"
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

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Getter } from 'vuex-class'

@Component({})
export default class Channel extends Vue {
  @Getter('form_data') private formData!: any;
  @Getter('channel_options') private channel_options!: any;

  // seems like not using confirm and remove
  // private t: boolean = true
  // private f: boolean = false
  // private state: string = 'invalid'

  get channel () { return this.formData.channel }
  set channel (value: number) {
    this.$store.commit('updateAddModalForm', { type: 'channel', value })
  }
}

</script>

<style>
.add_citizen_form {
  padding-bottom: 2px;
}
</style>
