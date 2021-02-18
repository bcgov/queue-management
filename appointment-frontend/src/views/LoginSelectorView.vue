<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="9">
        <v-card>
          <v-card-title class="justify-center">
            <h3>Login</h3>
          </v-card-title>
          <v-divider class="mx-4"></v-divider>
          <p class="text-center mt-2 login-msg">Please login using one of the following</p>
          <LoginToConfirm></LoginToConfirm>
        </v-card>
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
.login-msg{
  margin: 0;
}
</style>
