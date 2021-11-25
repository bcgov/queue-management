<template>
  <div class="add_citizen_form mt-0" v-if="isNotificationEnabled === 1">
    <b-form-row no-gutters></b-form-row>
    <b-form-row no-gutters>
      <b-col cols="auto">
        <label class="add_citizen_form_label">Notification:</label>
      </b-col>
      <b-col>
        <b-form-input 
          v-model="notificationPhone" 
          type="tel" 
          placeholder="Phone Number : (xxx) xxx-xxxx"
          :state="notificationPhoneValidation"
          @keypress="isNumber($event)"
          @input="formatPhone"
          maxlength=14        
        ></b-form-input>
      </b-col>
      <b-col>
        <b-form-input 
          v-model="notificationEmail" 
          type="email" 
          placeholder="Email Address"
          :state="notificationEmailValidation"
          @change="checkEmail"
          @input="checkEmail"
        ></b-form-input>
      </b-col>
    </b-form-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Getter } from 'vuex-class'

@Component
export default class NotificationFields extends Vue {
  @Getter('form_data') private formData!: any;

  private notificationPhoneValidation: any = null
  private notificationEmailValidation: any = null

  get notificationPhone () { return this.formData.notification_phone }
  set notificationPhone (value) {
    this.$store.commit('updateAddModalForm', { type: 'notification_phone', value })
    this.setwalkinUniqueId()
  }

  get notificationEmail () { return this.formData.notification_email }
  set notificationEmail (value) {
    this.$store.commit('updateAddModalForm', { type: 'notification_email', value })
    this.setwalkinUniqueId()
  }

  setwalkinUniqueId () {
    if ((this.formData.notification_phone) || (this.formData.notification_email)) { 
      const uuidv4 = require('uuid').v4
      this.$store.commit('updateAddModalForm', { type: 'walkin_unique_id', value: uuidv4() })
    }
  }

  public isNotificationEnabled: number = 0

  mounted () {
    if (this.$store.state.user.office) {
      this.isNotificationEnabled = this.$store.state.user.office.check_in_notification
    }
  }

  checkEmail () {
    if (this.formData.notification_email) {
        let  serchfind: boolean = false;
        // IT'S NOT USELESS! :D We need it to escape the . in the regex!!
        // eslint-disable-next-line no-useless-escape
        const regexp = new RegExp(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/);
        serchfind = regexp.test(this.formData.notification_email);
        if (serchfind) {
          this.notificationEmailValidation = true
        } else {
          this.notificationEmailValidation = false
        }
    } else {
      this.notificationEmailValidation = null
    }
  }

  formatPhone () {
    if (this.formData.notification_phone) {
      const cleaned = ('' + this.formData.notification_phone).replace(/\D/g, '')
      const x = cleaned.match(/^(\d{0,3})(\d{0,3})(\d{0,4})$/)
      if (x) {
        this.formData.notification_phone = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '')
        if (this.formData.notification_phone.length === 14) {
          this.notificationPhoneValidation = true
        } else {
          this.notificationPhoneValidation = false
        }
      } else {
        this.notificationPhoneValidation = false
      }
    } else {
      this.notificationPhoneValidation = null
    }
  }

  isNumber (evt: any) {
      var charCode = (evt.which) ? evt.which : evt.keyCode;
      if ((charCode > 31 && (charCode < 48 || charCode > 57))) {
        evt.preventDefault();
      } else {
        return true;
      }
    }
}

</script>
