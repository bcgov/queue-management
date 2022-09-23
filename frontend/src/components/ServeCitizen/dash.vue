/*Copyright 2015 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.*/

<template>
  <div
    v-bind:style="{height: totalH}"
    class="dashmaincontainer"
    key="dashmaincontainer"
    v-if="user.username"
  >
    <div
      style="display: flex; flex-direction: row; justify-content: space-between;"
      v-if="!showAdmin"
    >
      <div style="width: 100%">
        <template v-if="reception && isLoggedIn">
          <div
            v-bind:style="{width:'100%', height: `${qLengthH}px`}"
            class="font-900-rem"
          >Citizens Waiting: {{ queueLength }}</div>
          <div class="dash-table-holder" v-bind:style="{width:'100%', height:`${dashH}px`}">
            <DashTable></DashTable>
          </div>
          <div v-bind:style="{width:'100%', height:`${qLengthH}px`}">
            <div style="display: flex; width: 100%; justify-content: space-between;">
              <div class="font-900-rem">Citizens on Hold: {{on_hold_queue.length}}</div>
              <b-button variant="link" v-dragged="onDrag" class="m-0 p-0">
                <font-awesome-icon icon="sort" class="m-0 p-0" style="font-size: 1.5rem;"></font-awesome-icon>
              </b-button>
            </div>
          </div>
          <div class="dash-table-holder" v-bind:style="{width:'100%',height:`${holdH}px`}">
            <DashHoldTable></DashHoldTable>
          </div>
        </template>
        <template v-else-if="!reception && isLoggedIn">
          <div class="font-900-rem">Citizens on Hold: {{on_hold_queue.length}}</div>
          <div class="dash-table-holder" v-bind:style="{width:'100%',height:`${fullHoldH}px`}">
            <DashHoldTable></DashHoldTable>
          </div>
        </template>
      </div>
      <div v-if="showGAScreenModal || showAgendaScreenModal" style="margin-left: 1em; padding-top: 1em; width: 75%">
        <AgendaScreen v-if="showAgendaScreenModal"  style='margin-bottom: 2rem' />
        <GAScreen v-if="showGAScreenModal" />
      </div>
    </div>
  </div>
  <div v-else-if="isLoggedIn && !userLoadingFail">
    <div class="loader" style="margin-top: 250px"></div>
  </div>
</template>

<script lang="ts">
// /* eslint-disable */
import { Action, Getter, Mutation, State } from 'vuex-class'
import { Component, Vue, Watch } from 'vue-property-decorator'

import DashHoldTable from './dash-hold-table.vue'
import DashTable from './dash-table.vue'
import GAScreen from './../ga-screen/ga-screen.vue'
import AgendaScreen from './../agenda-screen/agenda-screen.vue'

@Component({
  components: {
    DashTable,
    DashHoldTable,
    GAScreen,
    AgendaScreen
  }
})
export default class Dash extends Vue {
  @State('citizenInvited') private citizenInvited!: any
  @State('dismissCountDown') private dismissCountDown!: any
  @State('examsTrackingIP') private examsTrackingIP!: any
  @State('isLoggedIn') private isLoggedIn!: any
  @State('performingAction') private performingAction!: any
  @State('serveNowStyle') private serveNowStyle!: any
  @State('serviceBegun') private serviceBegun!: any
  @State('serviceModalForm') private serviceModalForm!: any
  @State('showAddModal') private showAddModal!: any
  @State('showAdmin') private showAdmin!: any
  @State('showGAScreenModal') private showGAScreenModal!: any
  @State('showAgendaScreenModal') private showAgendaScreenModal!: any
  @State('showServiceModal') private showServiceModal!: any
  @State('showTimeTrackingIcon') private showTimeTrackingIcon!: any
  @State('toggleShowAdmin') private toggleShowAdmin!: any
  @State('user') private user!: any
  @State('userLoadingFail') private userLoadingFail!: any

  @Getter('citizens_queue') private citizens_queue!: any;
  @Getter('on_hold_queue') private on_hold_queue!: any;
  @Getter('reception') private reception!: any;

  @Action('clickAddCitizen') public clickAddCitizen: any
  @Action('clickInvite') public clickInvite: any
  @Action('clickAdmin') public clickAdmin: any
  @Action('clickServiceModalClose') public clickServiceModalClose: any
  @Action('clickCitizenLeft') public clickCitizenLeft: any
  @Action('clickGAScreen') public clickGAScreen: any
  @Action('clickServeNow') public clickServeNow: any
  @Action('clickBackOffice') public clickBackOffice: any
  @Action('screenAllCitizens') public screenAllCitizens: any

  @Mutation('setMainAlert') public setMainAlert: any
  @Mutation('toggleServiceModal') public toggleServiceModal: any
  @Mutation('toggleFeedbackModal') public toggleFeedbackModal: any
  @Mutation('toggleBegunStatus') public toggleBegunStatus: any

  private totalH: any = '';
  private buttonH: number = 45;
  private qLengthH: number = 28;
  private isDragged: boolean = false;
  private offset: number = 0;
  private last: number = 0;
  private dismissSecs: number = 5;
  private iframeHeight: string = '500px';
  private checkedSessionStorage: boolean = false

  get fullHoldH () {
    return this.totalH - this.qLengthH - this.buttonH - 50
  }

  get availH () {
    return this.totalH - (2 * this.qLengthH) - this.buttonH - 16
  }

  get queueLength () {
    return this.citizens_queue.length
  }

  get dashH () {
    if (!this.isDragged) return this.availH / 2
    return this.availH + this.offset
  }

  get holdH () {
    return (this.availH - this.dashH - 40)
  }

  get csrId () {
    return this.user.csr_id
  }

  @Watch('csrId')
  onCsrIdChange (val: any, oldVal: any) {
    if (val) {
      this.checkSessionStorage(val)
    }
  }

  private checkServiceReqs () {
    if (this.examsTrackingIP) {
      if (this.serviceModalForm && this.serviceModalForm.citizen_id) {
        this.toggleServiceModal(true)
        this.$store.commit('toggleBegunStatus', true)
        this.$store.commit('setPerformingAction', false)
      }
    }
  }

  private getNewHeight () {
    // window.innerHeight - height of header (70) - height of footer (36)
    this.totalH = window.innerHeight - 70 - 36
  }

  private onDrag (event: any) {
    const { deltaY, first, last } = event
    this.isDragged = true
    if (first) {
      this.offset = -this.availH / 2 + this.last
      return
    }
    if (!first && !last) {
      this.offset += deltaY
      this.last = (this.availH / 2) + this.offset
    }
    if (last) {
      const offsetRatio: any = this.offset / this.availH
      const lastRatio: any = this.last / this.availH
      sessionStorage.setItem(`${this.csrId}offset`, offsetRatio)
      sessionStorage.setItem(`${this.csrId}last`, lastRatio)
    }
  }

  private receiveSize (e: any) {
    let newHeight = e.data

    if (!Number.isInteger(newHeight)) {
      return
    }

    if (newHeight < 450) {
      newHeight = 500
    } else {
      newHeight = newHeight + 50
    }

    this.iframeHeight = newHeight + 'px'
  }

  private invite () {
    if (this.queueLength === 0) {
      this.setMainAlert('The are currently no citizens to invite.')
    } else {
      this.clickInvite()
    }
  }

  private clickFeedback () {
    this.toggleFeedbackModal(true)
  }

  private checkSessionStorage (csrId: any) {
    this.checkedSessionStorage = true
    const offsetRatio: any = sessionStorage.getItem(`${csrId}offset`)
    if (offsetRatio) {
      this.isDragged = true
      const lastRatio: any = sessionStorage.getItem(`${csrId}last`)
      this.offset = offsetRatio * this.availH
      this.last = lastRatio * this.availH
    } else {
      this.isDragged = false
    }
  }

  beforeRouteLeave (to: any, from: any, next: any) {
    if (this.showTimeTrackingIcon) {
      next()
      return
    }
    if (to.path === '/exams' || to.path === '/booking' || to.path === '/service-flow') {
      this.clickAddCitizen()
      next()
    }
    next()
  }

  mounted () {
    this.$root.$on('showMessage', () => {
      // this.Alert()
    })
    this.totalH = window.innerHeight - 70 - 36
    this.$nextTick(function () {
      window.addEventListener('resize', this.getNewHeight)
    })
    window.addEventListener('message', this.receiveSize)
    setTimeout(() => { this.checkServiceReqs() }, 400)
  }
}

</script>

<style scoped>
.dashmaincontainer {
  width: 100%;
  display: block;
  padding-left: 1%;
  padding-right: 1%;
  padding-top: 8px;
  overflow-x: auto;
}
#dash-flex-button-container {
  display: flex;
  justify-content: space-between;
  height: 100% !important;
}
.dash-table-holder {
  overflow-y: scroll;
  overflow-x: auto;
  border: 1px solid dimgrey;
}
.font-900-rem {
  font-size: 0.9rem;
}
.modal-main div {
  background-color: blue;
}
.loader {
  position: relative;
  text-align: center;
  margin: 15px auto 35px auto;
  z-index: 9999;
  display: block;
  width: 80px;
  height: 80px;
  border: 10px solid rgba(0, 0, 0, 0.3);
  border-radius: 50%;
  border-top-color: #000;
  animation: spin 1s ease-in-out infinite;
  -webkit-animation: spin 1s ease-in-out infinite;
}
@keyframes spin {
  to {
    -webkit-transform: rotate(360deg);
  }
}

@-webkit-keyframes spin {
  to {
    -webkit-transform: rotate(360deg);
  }
}
</style>
