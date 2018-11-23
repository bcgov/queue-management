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
  <div v-bind:style="{height: totalH}" class="dashmaincontainer" key="dashmaincontainer" v-if="user.username">
    <AddCitizen v-if="showAddModal"/>
    <ServeCitizen v-if="showServiceModal"/>
    <div style="display: flex; flex-direction: row; justify-content: space-between;" v-if="!showAdmin">
      <div style="width: 100%">
        <template v-if="reception && isLoggedIn">
          <div v-bind:style="{width:'100%', height: `${qLengthH}px`}" class="font-900-rem">
            Citizens Waiting: {{ queueLength }}
          </div>
          <div class="dash-table-holder" v-bind:style="{width:'100%', height:`${dashH}px`}">
            <DashTable></DashTable>
          </div>
          <div v-bind:style="{width:'100%', height:`${qLengthH}px`}">
            <div style="display: flex; width: 100%; justify-content: space-between;">
              <div class="font-900-rem">Citizens on Hold: {{on_hold_queue.length}}</div>
              <b-button variant="link" v-dragged="onDrag" class="m-0 p-0">
                <font-awesome-icon icon="sort"
                                   class="m-0 p-0"
                                   style="font-size: 1.5rem;"></font-awesome-icon>
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
      <div v-if="showGAScreenModal"
           style="margin-left: 1em; padding-top: 1em; width: 75%">
        <GAScreen />
      </div>
    </div>
    <div v-if="showAdmin">
      <iframe :src="iframeUrl"
              :height="iframeHeight"
              width="100%"
              frameborder="0" />
    </div>
  </div>
  <div v-else-if="isLoggedIn && !userLoadingFail">
    <div class="loader" style="margin-top: 250px"></div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions, mapMutations } from 'vuex'
import AddCitizen from './../add-citizen/add-citizen'
import DashTable from './dash-table'
import DashHoldTable from './dash-hold-table'
import GAScreen from './../ga-screen/ga-screen'
import ServeCitizen from './serve-citizen'

  export default {
    name: 'Dash',

    components: {
      AddCitizen,
      DashTable,
      DashHoldTable,
      GAScreen,
      ServeCitizen
    },

    mounted() {
      this.$root.$on('showMessage', () => {
        this.showAlert()
      })
      this.totalH = window.innerHeight - 70 - 36
      this.$nextTick(function() {
        window.addEventListener('resize', this.getNewHeight)
      })
      window.addEventListener("message", this.receiveSize);
      this.iframeUrl = process.env.SOCKET_URL + "/admin/"
    },

    data() {
      return {
        totalH:'',
        buttonH: 45,
        qLengthH: 28,
        isDragged: '',
        offset: 0,
        t: true,
        f: false,
        last: 0,
        dismissSecs: 5,
        checkedLocalStorage: false,
        iframeHeight: "500px"
      }
    },

    computed: {
      ...mapGetters(['citizens_queue', 'on_hold_queue', 'reception']),
      ...mapState([
        'isLoggedIn',
        'showAddModal',
        'citizenInvited',
        'dismissCountDown',
        'performingAction',
        'showAdmin',
        'showGAScreenModal',
        'showServiceModal',
        'serveNowStyle',
        'toggleShowAdmin',
        'user',
        'userLoadingFail'
      ]),
      fullHoldH() {
        return this.totalH - this.qLengthH - this.buttonH - 16
      },
      availH() {
        return this.totalH - (2 * this.qLengthH) - this.buttonH - 16
      },
      queueLength() {
        return this.citizens_queue.length
      },
      dashH() {
        if (!this.isDragged) return this.availH / 2
        if (this.isDragged) return this.availH + this.offset
      },
      holdH() {
        return (this.availH - this.dashH - 15)
      },
      csrId() {
        return this.user.csr_id
      }
    },
    watch: {
      csrId: function(val, oldVal) {
        if (val) {
          this.checkLocalStorage(val)
        }
      }
    },
    methods: {
      ...mapMutations(['setMainAlert', 'toggleFeedbackModal']),
      ...mapActions([
        'clickInvite',
        'clickAddCitizen',
        'clickAdmin',
        'clickServiceModalClose',
        'clickCitizenLeft',
        'clickGAScreen',
        'clickServeNow',
        'clickBackOffice'
      ]),
      addCitizen() {
        this.clickAddCitizen()
      },
      getNewHeight() {
        //window.innerHeight - height of header (70) - height of footer (36)
        this.totalH = window.innerHeight - 70 - 36
      },
      onDrag({ deltaY, first, last }) {
        this.isDragged = true
        if (first) {
          this.offset = -this.availH / 2 + this.last
          return
        }
        if(!first && !last) {
          this.offset += deltaY
          this.last = (this.availH / 2) + this.offset
        }
        if (last) {
          let offsetRatio = this.offset / this.availH
          let lastRatio = this.last / this.availH
          localStorage.setItem(`${this.csrId}offset`, offsetRatio)
          localStorage.setItem(`${this.csrId}last`, lastRatio)
        }
      },
      receiveSize(e) {
        var newHeight = e.data;

        if (!Number.isInteger(newHeight)) {
          return
        }

        if (newHeight < 450) {
          newHeight = 500
        } else {
          newHeight = newHeight + 50
        }

        this.iframeHeight = newHeight + "px"
      },
      invite() {
        if (this.queueLength === 0) {
          this.setMainAlert('The are currently no citizens to invite.')
        } else {
          this.clickInvite()
        }
      },
      clickFeedback() {
        this.toggleFeedbackModal(true)
      },
      checkLocalStorage(csrId) {
        this.checkedLocalStorage = true
        let offsetRatio = localStorage.getItem(`${csrId}offset`)
        if(offsetRatio) {
          this.isDragged = true
          let lastRatio = localStorage.getItem(`${csrId}last`)
          this.offset = offsetRatio * this.availH
          this.last = lastRatio * this.availH
        } else {
          this.isDragged = false
        }
      }
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
  }
  #dash-flex-button-container {
    display: flex; justify-content: space-between; height: 100% !important;
  }
  .dash-table-holder {
    overflow-y: scroll; overflow-x: auto; border: 1px solid dimgrey;
  }
  .font-900-rem {
    font-size: .9rem;
  }
  .modal-main div {
    background-color: blue;
  }
  .btn-highlighted {
    color: black;
    border: 1px solid darkgoldenrod;
    background-color: gold;
  }
  .loader {
    position: relative;
    text-align: center;
    margin: 15px auto 35px auto;
    z-index: 9999;
    display: block;
    width: 80px;
    height: 80px;
    border: 10px solid rgba(0, 0, 0, .3);
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
