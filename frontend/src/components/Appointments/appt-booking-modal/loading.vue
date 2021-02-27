<template>
  <b-modal
  visible
  no-close-on-backdrop
  no-close-on-esc
  hide-header
  hide-footer
  centered
  >
  <div>
    <div class="ml-3 my-3 no-exam-notice">
      Please wait while the blackouts are created. Do not Refresh/Go back.
    </div>
    <div class="q-loader"></div>
    <b-progress  :max="max" :animated="flag" :striped="flag">
      <b-progress-bar variant="primary" :value="value"></b-progress-bar>
    </b-progress>
    </div>
  </b-modal>
</template>

<script lang="ts">
import { APIProgressBusEvents, apiProgressBus } from '../../../events/progressBus'
import { Component, Vue } from 'vue-property-decorator'
import { namespace } from 'vuex-class'
const appointmentsModule = namespace('appointmentsModule')
@Component
export default class ApptBookingModal extends Vue {
  @appointmentsModule.Getter('getApiTotalCount') private getApiTotalCount: any;

  private max: number = 0;
  private value: number = 50;
  private flag: boolean = true;

  created () {
    this.max = this.getApiTotalCount
    apiProgressBus.$on(APIProgressBusEvents.APIProgressEvent, (count: number) => {
      this.value = this.value + count
    })
  }
}
</script>
