<template>
  <div class="add_citizen_template">
    <template v-if="addModalSetup === 'add_mode' || addModalSetup === 'edit_mode' ">
      <div class="add_citizen_template">
        <div
          class="add_citizen_padding"
          style="background: rgb(240, 240, 240); padding-top: 12px; padding-bottom: 1px"
        >
          <Channel />
          <div style="transform: translateY(19px);">
            <Filters />
          </div>
        </div>
        <b-container
          fluid
          class="add_citizen_padding"
          style="background:#504e4f; padding-top: 35px;"
        >
          <Tables />
        </b-container>
      </div>
    </template>
    <template v-else>
      <div class="add_citizen_template">
        <div class="add_citizen_padding" style="background: rgb(240, 240, 240);padding-top: 12px;">
          <Comments v-if="!simplifiedModal" />
          <NotificationFields />
          <Channel />
          <div style="transform: translateY(18px);">
            <Filters />
          </div>
        </div>
        <b-container
          fluid
          class="add_citizen_padding"
          style="background:#504e4f; padding-top: 25px;"
        >
          <Tables />
        </b-container>
      </div>
    </template>
  </div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import { Getter, State } from 'vuex-class'

import Channel from './form-components/channel.vue'
import Comments from './form-components/comments.vue'
import Filters from './form-components/filters.vue'
import NotificationFields from './form-components/notification_fields.vue'
import Tables from './form-components/tables.vue'

@Component({
  components: {
    Comments,
    Channel,
    Filters,
    Tables,
    NotificationFields
  }
})
export default class AddCitizenForm extends Vue {
  @State('addModalSetup') private addModalSetup!: string | undefined
  @Getter('reception') private reception!: any;

  get simplified () {
    if (this.$route.path !== '/queue') {
      return true
    }
    return false
  }

  get simplifiedModal () {
    if (this.simplified && this.addModalSetup !== 'edit_mode') {
      return true
    }
    return false
  }
}

</script>

<style>
.add_citizen_form_table {
  border-bottom: 1px solid darkgrey;
}
.add_citizen_form_label {
  font-size: 15px;
  font-weight: 400;
  width: 75px;
  text-align: right;
  line-height: 38px;
}
.add_citizen_padding {
  padding-left: 30px;
  padding-right: 30px;
}
</style>
