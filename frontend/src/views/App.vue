/* Copyright 2015 Province of British Columbia Licensed under the Apache
License, Version 2.0 (the "License"); you may not use this file except in
compliance with the License. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or
agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. See the License for the specific language governing permissions and
limitations under the License. */

<template>
  <div id="App">
    <Header />
    <Socket v-show="false" />
    <div v-if="user.username && isLoggedIn" v-bind:style="style">
      <Alert />
      <ExamAlert />
      <SuccessExamAlert />
      <Nav v-if="isLoggedIn" />
      <AddExamModal />
      <Feedback />
      <Response />
    </div>
    <LoginWarning />
    <Footer />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
// eslint-disable-next-line sort-imports
import { Getter, State } from 'vuex-class'
import AddExamModal from '@/components/exams/add-exam-modal.vue'
import Alert from './alert.vue'
import ExamAlert from './exam-alert.vue'
import FailureExamAlert from '@/components/exams/failure-exam-alert.vue'
import Feedback from './feedback.vue'
import Footer from '@/components/Layout/footer.vue'
import Header from '@/components/Layout/header.vue'
import Login from '@/components/Login/Login.vue'
import LoginWarning from '@/components/Login/login-warning.vue'
import Nav from '@/components/Layout/nav.vue'
import Response from './response.vue'
import Socket from './Socket.vue'
import SuccessExamAlert from '@/components/exams/success-exam-alert.vue'

@Component({
  components: {
    AddExamModal,
    Alert,
    ExamAlert,
    FailureExamAlert,
    Feedback,
    Footer,
    Header,
    Login,
    LoginWarning,
    Nav,
    Response,
    Socket,
    SuccessExamAlert
  }
  // computed: {
  //   ...mapGetters([
  //     'show_scheduling_indicator'
  //   ]),
  //   ...mapState(['isLoggedIn', 'user'])
  // }
  // methods: {
  //   ...mapActions('account', ['loadUserInfo', 'getUser']),
  //   ...mapActions('auth', ['syncWithSessionStorage'])
  // }
})
export default class App extends Vue {
  // eslint-disable-next-line camelcase
  // private readonly show_scheduling_indicator!: boolean
  // private readonly isLoggedIn!: boolean
  // private readonly user!: any

  @Getter('show_scheduling_indicator') private showSchedulingIndicator!: false;
  @State('isLoggedIn') private isLoggedIn!: string | undefined;
  @State('user') private user!: string | undefined;
  // updated () {
  //   console.log('user', this.user)
  //   console.log('isLoggedIn', this.isLoggedIn)
  //   console.log('showSchedulingIndicator', this.showSchedulingIndicator)
  // }

  // mounted () {
  //   console.log('user', this.user)
  //   console.log('isLoggedIn', this.isLoggedIn)
  //   console.log('showSchedulingIndicator', this.showSchedulingIndicator)
  // }

  get style () {
    // removing overflowX: 'hidden' from { marginTop: 72 + 'px', width: '100%', overflowX: 'hidden' } for serviceflow double scrolling fix
    const output: any = { marginTop: 72 + 'px', width: '100%' }
    if (this.showSchedulingIndicator) {
      output.marginBottom = '100px'
    }
    if (!this.showSchedulingIndicator) {
      output.marginBottom = '40px'
    }

    return output
  }
}
</script>

<style lang="scss">
.custom-select-sm {
  font-size: 0.8rem !important;
}
.btn-link {
  text-decoration: underline;
}
.dash-flex-button-container {
  display: flex;
  justify-content: space-between;
  height: 100% !important;
}
#__BVID__13__BV_toggle_ {
  background-color: #ffffff;
  color: #1a5a96;
  border: 1px solid silver;
  width: 375px;
}
.txt-85 {
  font-size: 1rem;
}
.txt-14 {
  font-size: 1.4rem;
}
#fixed-viewport-app {
  display: block;
  overflow-y: auto;
  overflow-x: auto;
  background-color: blue;
  margin: 0px;
  padding: 0px;
  position: absolute;
  left: 0px;
  top: 72px;
}
.view-screen-title {
  font-family: "Helvetica Neue", Arial, sans-serif;
  color: black;
  font-weight: 500;
  font-size: 1.9rem;
}
#counter-selection-csr,
#counter-selection-add,
#counter-selection-serve,
#priority-selection {
  display: inline-block;
  width: 135px;
  padding-right: 0;
  margin-left: 4px;
}
</style>
