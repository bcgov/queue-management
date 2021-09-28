<template>
  <v-footer
    absolute
    dark
    class="font-weight-medium"
  >
    <v-col
      class="text-left container py-2"
      cols="12"
    >
      <nav>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="https://www2.gov.bc.ca/gov/content/home/disclaimer" rel="noopener noreferrer" target="_blank">Disclaimer</a></li>
          <li><a href="https://www2.gov.bc.ca/gov/content/home/privacy" rel="noopener noreferrer" target="_blank">Privacy</a></li>
          <li><a href="https://www2.gov.bc.ca/gov/content/home/accessibility" rel="noopener noreferrer" target="_blank">Accessibility</a></li>
          <li><a href="https://www2.gov.bc.ca/gov/content/home/copyright" rel="noopener noreferrer" target="_blank">Copyright</a></li>
          <li><a href="https://www2.gov.bc.ca/gov/content/home/get-help-with-government-services" rel="noopener noreferrer" target="_blank">Contact Us</a></li>
        </ul>
      </nav>
    </v-col>
  </v-footer>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class AppFooter extends Vue {
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";

.v-footer {
  display: flex;
  align-items: center;
  min-height: 3.5rem;
  border-top: 2px solid $BCgovGold5 !important;
  background: $BCgovBlue5 !important;
  font-size: 0.875rem;
}
nav {
  ul {
    margin: -0.5rem;
    padding: 0;
    list-style-type: none;
  }

  li {
    display: inline-block;
    margin-right: 0.25rem;

    a {
      display: block;
      padding: 0.25rem 0.5rem;
      color: #fff;
      text-decoration: none;

      &:hover {
        text-decoration: underline;
      }
    }
  }
  li:last-child {
    margin-right: 0;
    border-right: none;
  }
}
@media (min-width: 960px) {
  nav {
    li {
      margin-right: 0.5rem;
      padding-right: 0.5rem;
      border-right: 1px solid $BCgovBlue3;

      a {
        padding: 0.25rem 0.5rem;
      }
    }
  }
}
</style>
