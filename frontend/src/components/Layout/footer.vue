<template>
  <div style="outer-header-style">
    <SchedulingIndicator />
    <div id="main-footer">
      <div id="footer-links">
        <div class="footer-anchor-item">
          <a
            href="http://www2.gov.bc.ca/gov/content/home/disclaimer"
            target="_blank"
            >Disclaimer</a
          >
        </div>
        <div class="footer-anchor-item">
          <a
            href="http://www2.gov.bc.ca/gov/content/home/privacy"
            target="_blank"
            >Privacy</a
          >
        </div>
        <div class="footer-anchor-item">
          <a
            href="http://www2.gov.bc.ca/gov/content/home/accessibility"
            target="_blank"
            rel="noopener noreferrer"
            >Accessibility</a
          >
        </div>
        <div class="footer-anchor-item-last">
          <a
            href="http://www2.gov.bc.ca/gov/content/home/copyright"
            target="_blank"
            >Copyright</a
          >
        </div>
      </div>

      <div class="p-0" style="display: inline-block; color: white">
        <div
          v-if="!this.$store.state.isLoggedIn"
          class="footer-anchor-item"
          style="display: inline-block; color: white"
        >
          <a href="#" @click="keycloakLogin()" id="keycloak-login"
            >Keycloak Login</a
          >
        </div>
        <div
          class="footer-anchor-item-last"
          style="display: inline-block; color: white; margin-right: 15px"
        >
          v2.1.10
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import SchedulingIndicator from '../Booking/scheduling-indicator.vue'
// import * as version from '../../version.GENERATED'

@Component({
  components: {
    SchedulingIndicator
  }
})
export default class Footer extends Vue {
  $keycloak: any
  keycloakLogin () {
    this.$keycloak.login()
  }
}
</script>

<style scoped>
.outer-header-style {
  position: fixed;
  width: 100%;
  left: 0px;
  bottom: 0px;
  display: block;
  z-index: 3000;
}
#main-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: fixed;
  bottom: 0px;
  left: 0px;
  height: 36px;
  padding-top: 7px;
  padding-bottom: 7px;
  width: 100%;
  background-color: #123263;
  border-top: 2px solid #fcba19;
  font-size: 0.85rem;
  font-family: Myriad-Pro, Calibri, Arial, sans serif;
  z-index: 1000;
}
#footer-links {
  padding-left: 10px;
}
.footer-anchor-item {
  border-right: 1px solid grey;
  display: inline-block;
  padding-right: 7px;
  padding-left: 7px;
}
.footer-anchor-item-last {
  display: inline-block;
  padding-right: 7px;
  padding-left: 7px;
}
a,
a:visited,
a:hover {
  color: white;
}
button,
button:hover {
  font-size: 0.8rem;
  font-family: Myriad-Pro, Calibri, Arial, sans serif;
  color: white;
  border: none;
  background-color: #4678b0;
}
</style>
