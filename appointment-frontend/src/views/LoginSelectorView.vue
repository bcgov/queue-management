<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="9">
        <LoginToConfirm></LoginToConfirm>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
// Libraries
import { Component, Vue } from 'vue-property-decorator'
import { LoginToConfirm } from '../components/appointment'

@Component({
  components: {
    LoginToConfirm
  }
})
export default class LoginSelectorView extends Vue {

}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
</style>
