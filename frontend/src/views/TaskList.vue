<template>
  <div class="service-flow-container">
    <CamundaTasklist
      v-if="isServiceFLowEnabled"
      :bpmApiUrl="configs.BPM_URL"
      :token="token"
      :formIOApiUrl="configs.FORM_IO_API_URL"
      :formIOResourceId="configs.FORM_IO_RESOURCE_ID"
      :formIOReviewerId="configs.FORM_IO_REVIEWER_ID"
      :formIOReviewer="configs.FORM_IO_REVIEWER"
      :formsflowaiUrl="configs.FORM_FLOW_URL"
      :formsflowaiApiUrl="configs.FORM_FLOW_API_URL"
      :formIOJwtSecret="configs.FORMIO_JWT_SECRET"
      :webSocketEncryptkey="configs.WEBSOCKET_ENCRYPT_KEY"
      :getTaskId="getTaskId"
      :formIOUserRoles="userKeyclockGroups"
      :reviewer="configs.FORM_IO_REVIEWER"
      :userRoles="userKeyclockGroups"
      :formioServerUrl="configs.FORM_IO_API_URL"
      containerHeight ="280"
      taskSortBy="dueDate"
      taskSortOrder="asc"
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
  },
  computed: {
    getTaskId: {
      get: function () {
        return this.$route.params.taskId
      }
    },
    userKeyclockGroups: {
      get: function () {
        const token = sessionStorage.getItem('token') ?? ''
        const decodeToken = atob(token.split('.')[1])
        const userDetails = JSON.parse(decodeToken)
        return userDetails?.resource_access?.['forms-flow-web']?.roles ? userDetails?.resource_access?.['forms-flow-web']?.roles.join() : ''
      }
    }
  }
})
export default class TaskList extends Vue {
  @State('bearer') private bearer!: any;
  public token: any = sessionStorage.getItem('token');
  public configs = configMap.getconfig();
  public isServiceFLowEnabled = configMap.isServiceFLowEnabled();

  loadProps () {
    this.isServiceFLowEnabled = configMap.isServiceFLowEnabled()
    console.log("CONFIGS:", this.configs);
  }

  mounted () {
    this.loadProps()
    this.$root.$on('finishBeginServiceTheQ', (customEvent: any) => {
      this.$root.$emit('navBeginService')
    })
  }

  @Watch('bearer')
  onbearerChange () {
    this.token = sessionStorage.getItem('token')
  }

  beforeCreate () {
    document.body.className = 'service-flow-body'
  }

  beforeDestroy () {
    document.body.className = ''
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
