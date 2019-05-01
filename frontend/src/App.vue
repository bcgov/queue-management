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
  <div id="App">
    <Header />
    <Socket v-show="1===2" />
    <div v-if="user.username && isLoggedIn" :style="style">
      <Alert />
      <ExamAlert />
      <SuccessExamAlert />
      <Nav v-if="isLoggedIn" />
      <Feedback />
      <Response />
    </div>
    <LoginWarning/>
    <Footer />
  </div>
</template>

<script>
  import { mapState, mapGetters } from 'vuex'
  import Alert from './alert'
  import ExamAlert from './exam-alert'
  import FailureExamAlert from './exams/failure-exam-alert'
  import Feedback from './feedback'
  import Footer from './layout/footer'
  import Header from './layout/header'
  import Login from "./Login";
  import LoginWarning from './login-warning'
  import Nav from './layout/nav'
  import Response from './response'
  import Socket from './Socket'
  import SuccessExamAlert from './exams/success-exam-alert'

  export default {
    name: 'App',
    components: {
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
      SuccessExamAlert,
    },
    computed: {
      ...mapGetters(['show_scheduling_indicator']),
      ...mapState(['isLoggedIn', 'user' ]),
      style() {
        let output = {marginTop: 72+'px', width: '100%', overflowX: 'hidden'}
        if (this.show_scheduling_indicator) {
          output['marginBottom'] = 100+'px'
        }
        if (!this.show_scheduling_indicator) {
          output['marginBottom'] = 40+'px'
        }
        return output
      }
    },
  }
</script>

<style>
  .custom-select-sm {
    font-size: .8rem !important;
  }
  .btn-link {
    text-decoration: underline;
  }
  .dash-flex-button-container {
    display: flex; justify-content: space-between; height: 100% !important;
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
    font-family: "Helvetica Neue",Arial,sans-serif;
    color: black;
    font-weight: 500;
    font-size:1.90rem;
  }
</style>
