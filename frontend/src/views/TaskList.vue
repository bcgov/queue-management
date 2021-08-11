<template>
  <div>
    <CamundaTasklist
      v-if="isServiceFLowEnabled"
      :bpmApiUrl="configs.BPM_URL"
      :token="token"
      :formIOUserRoles="configs.FORM_IO_USER_ROLES"
      :formIOApiUrl="configs.FORM_IO_API_URL"
      :formIOResourceId="configs.FORM_IO_RESOURCE_ID"
      :formIOReviewerId="configs.FORM_IO_REVIEWER_ID"
      :formIOReviewer="configs.FORM_IO_REVIEWER"
      :formsflowaiUrl="configs.FORM_FLOW_URL"
      :formsflowaiApiUrl="configs.FORM_FLOW_API_URL"
      :webSocketEncryptkey="configs.WEBSOCKET_ENCRYPT_KEY"
      :getTaskId="getTaskId"
    />
    <div class="no-content" v-else>You shouldnot be here !!!</div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator'
import CamundaTasklist from 'camunda-formio-tasklist-vue/src/components/TaskList.vue'
import { State } from 'vuex-class'
import configMap from '../utils/config-helper'
// css specific to service flow
import '../assets/css/service-flow.css'

@Component({
  components: {
    CamundaTasklist
  }
})
export default class TaskList extends Vue {
  @State('bearer') private bearer!: any;
  public token: any = sessionStorage.getItem('token');
  public configs = configMap.getconfig();
  public isServiceFLowEnabled = configMap.isServiceFLowEnabled();
  public getTaskId: string = this.$route.params.taskId;

  mounted () {
    this.getTaskId = this.$route.params.taskId
    this.token = sessionStorage.getItem('token')
    this.isServiceFLowEnabled = configMap.isServiceFLowEnabled()
  }

  @Watch('bearer')
  onbearerChange () {
    this.token = sessionStorage.getItem('token')
  }
}
</script>

<style scoped>
.no-content {
  display: flex;
  justify-content: center;
  font-size: 18px;
}
</style>
