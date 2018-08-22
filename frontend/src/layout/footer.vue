<template>
  <div id="main-footer">
    <div id="footer-links">
      <div id="footer-anchor-item-1st">
        <a href="http://www2.gov.bc.ca/gov/content/home/disclaimer" target="_blank">Disclaimer</a>
      </div>
      <div class="footer-anchor-item">
        <a href="http://www2.gov.bc.ca/gov/content/home/privacy" target="_blank">Privacy</a>
      </div>
      <div class="footer-anchor-item">
        <a href="http://www2.gov.bc.ca/gov/content/home/accessibility" target="_blank">Accessibility</a>
      </div>
      <div class="footer-anchor-item">
        <a href="http://www2.gov.bc.ca/gov/content/home/copyright" target="_blank">Copyright</a>
      </div>
    </div>
    <div class="p-0 m-0">
      <div class="p-0" style="width: 80px; height: 20px; display:inline-block; margin-right: 25px;">
        <b-btn v-if="!showServiceModal" variant="link" @click="toggleModal">
          Feedback
        </b-btn>
      </div>
      <div class="p-0" style="display:inline-block; color: white; margin-right:15px;">
        v1.0
      </div>
    </div>

  </div>
</template>

<script>
  import { mapMutations, mapState } from 'vuex'

  export default {
    name: 'Footer',

    computed: {
      ...mapState(['showServiceModal'])
    },

    methods: {
      ...mapMutations(['toggleFeedbackModal']),

      toggleModal() {
        this.toggleFeedbackModal(true)
      }
    }
  }
</script>

<style scoped>
  #main-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: fixed;
    bottom: 0px;
    left: 0px;
    padding-top: 7px;
    padding-bottom: 7px;
    width: 100%;
    background-color: #123263;
    border-top: 2px solid #fcba19;
    font-size: .750rem;
    font-family: Myriad-Pro, Calibri, Arial, sans serif;
  }
  #footer-links {
    padding-left: 10px;
  }
  .footer-anchor-item {
     border-left: 1px solid grey;
     display: inline-block;
     padding-right: 7px;
     padding-left: 7px;
   }
  #footer-anchor-item-1st {
    display: inline-block;
    padding-right: 7px;
    padding-left: 7px;
  }
  a, a:visited, a:hover {
    color: white;
  }
  button, button:hover {
    font-size: .800rem;
    font-family: Myriad-Pro, Calibri, Arial, sans serif;
    color: white;
  }
</style>
