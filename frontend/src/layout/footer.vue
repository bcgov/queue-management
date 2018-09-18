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
    <div class="p-0" style="display:inline-block; color: white; margin-right:15px;">
      v1.06
    </div>
  </div>
</template>

<script>
  import { mapMutations, mapState } from 'vuex'

  export default {
    name: 'Footer',
  }
</script>

<style scoped>
  #main-footer {
    display: flex;
    justify-content:space-between;
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
    font-size: .850rem;
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
    border: none;
    background-color: #4678b0;
  }
</style>
