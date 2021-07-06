<template>
  <div>
    <CamundaTasklist
      :bpmApiUrl="configs.BPM_URL"
      :token="token"
      :userName="user && user.username"
      :formIOUserRoles="configs.FORM_IO_USER_ROLES"
      :formIOApiUrl= "configs.FORM_IO_API_URL"
      :formIOResourceId = "configs.FORM_IO_RESOURCE_ID"
      :formIOReviewerId = "configs.FORM_IO_REVIEWER_ID"
      :formIOReviewer = "configs.FORM_IO_REVIEWER"
      :formsflowaiUrl="configs.FORM_FLOW_URL"
      :formsflowaiApiUrl="configs.FORM_FLOW_API_URL"
      v-if="isServiceFLowEnabled"
    />
    <div class="no-content" v-else>You shouldnot be here !!!</div>
  </div>
</template>

<script lang="ts">
import { Component, Vue ,Watch } from 'vue-property-decorator'
import CamundaTasklist from 'camunda-formio-tasklist-vue/src/components/TaskList.vue'
import { State } from 'vuex-class'
import configMap from '../utils/config-helper'
@Component({
  components: {
    CamundaTasklist
  }
})
export default class TaskList extends Vue {
  @State('user') private user!: any
  @State('bearer') private bearer!: any
  public token:any = sessionStorage.getItem('token')
  public  configs = configMap.getconfig()
  public isServiceFLowEnabled = configMap.isServiceFLowEnabled()
  mounted () {
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
