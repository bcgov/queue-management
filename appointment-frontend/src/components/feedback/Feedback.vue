<template>
  <v-col>
    <v-col class="feedback_view" :class="showFeedbackArea ? 'feedback_view_expanded':''" v-show="!$vuetify.breakpoint.xs">
          <v-row class="feedback_container" :class="getFeedbackViewStyle()">
            <v-col>
              <v-col class="feedback_strip_parent">
                <div class="feedback_strip">
                          Your Feedback
                </div>
                <div class="icon_strip" v-show="!$vuetify.breakpoint.xs">
                  <div class="row-f feedback_icon clickable" :class="feedbackType === 'suggestion' ?  'invert_colors':''" v-on:click="showFeedBack('suggestion')">
                    <span class="mdi mdi-lightbulb-outline mdi-rotate-90"/>
                  </div>
                  <div class="row-f feedback_icon clickable" :class="feedbackType === 'complaint' ?  'invert_colors':''" v-on:click="showFeedBack('complaint')">
                    <span class="mdi mdi-emoticon-sad-outline mdi-rotate-90"/>
                  </div>
                  <div class="row-f feedback_icon clickable" :class="feedbackType === 'compliment' ?  'invert_colors':''" v-on:click="showFeedBack('compliment')">
                    <span class="mdi mdi-emoticon-happy-outline mdi-rotate-90"/>
                  </div>
                </div>
              </v-col>
            </v-col>
            <div>
              <div class="feedback_area" v-show="!$vuetify.breakpoint.xs">
                <v-card-text class="align_center" v-show="viewFeebackArea()">
                  <v-form ref="form" v-model="valid">
                    <v-row class="clickable close_btn" v-on:click="toggleFeedback()"><span class="mdi mdi-close"/></v-row>
                    <v-col class="feedback_header"><h3>{{feedbackHeader}}</h3></v-col>
                    <v-textarea v-show="!showResponsePage || !responseRequired"
                        :maxlength="3000"
                        :label="'* Feedback'"
                        :rules="messageRules"
                        class="mt-3"
                        outlined
                        name="feedback-message"
                        height="100"
                        v-model="feedbackMessage"
                        counter="3000"
                        required
                    >
                      <template v-slot:label>
                        <div><span class="mandatory">*</span> Feedback</div>
                      </template>
                    </v-textarea>
                    <v-col class="feedback_caption response_required"><span class="mandatory">*</span> Would you like a response from us?</v-col>
                    <v-row justify="center">
                        <!-- <v-col><input type="radio" v-model="feedbackModel.responseRequired" v-bind:value="yes"><span class="feedback_caption">Yes</span></v-col> -->
                        <v-radio-group class="no_margin" v-model="responseRequired" row :disabled="feedbackMessage.length === 0">
                          <v-radio  label="Yes" v-bind:value="yes"></v-radio>
                          <v-radio  label="No" v-bind:value="no" @click="showResponsePage = false" ></v-radio>
                        </v-radio-group>
                    </v-row>
                    <v-col v-show="showResponsePage && responseRequired">
                      <v-text-field name="citizen-name" v-model="citizenName" outlined dense :rules="nameRules" required>
                        <template v-slot:label>
                          <div><span class="mandatory">*</span> Name</div>
                        </template>
                      </v-text-field>
                      <v-text-field v-model="email"  label="Email" outlined dense :rules="emailRules" @blur="validateRules" @input="validateRules"></v-text-field>
                      <v-text-field v-model="phone"  label="Phone" outlined dense :rules="phoneRules" @blur="validateRules" @input="validateRules"></v-text-field>
                      <v-row class="consent">{{consentMessage}}</v-row>
                      <v-row justify="center">
                        <v-radio-group class="no_margin" v-model="consent" required row>
                          <v-radio v-bind:value="yes" :rules="consentRules">
                            <template v-slot:label>
                              <div><span class="mandatory">*</span> I Consent</div>
                            </template>
                          </v-radio>
                        </v-radio-group>
                      </v-row>
                    </v-col>
                    <v-row class="justify-space-around">
                      <v-btn v-show="!responseRequired && !showResponsePage" @click="postFeedback"
                              color="primary"
                              width="15em"
                              :disabled="validateSubmit()"
                      >Submit</v-btn>
                      <v-btn v-show="responseRequired && !showResponsePage" @click="toggleResponsePage"
                              color="primary"
                              width="15em"
                      >Next</v-btn>
                      <v-btn v-show="showResponsePage" @click="toggleResponsePage"
                              color="primary"
                              width="7em"
                      >Back</v-btn>
                      <v-btn v-show="showResponsePage" @click="postFeedback"
                              color="primary"
                              width="7em"
                              :disabled="validateSubmit()"
                      >Submit</v-btn>
                    </v-row>
                  </v-form>
                </v-card-text>
                <div v-show="submitComplete || submitInProgress" class="response_content">
                  <v-col class="align-self-center" v-show="submitComplete">
                    <v-col class="text-center">{{submitMessage}}</v-col>
                    <v-col><v-btn @click="toggleFeedback"
                              color="primary"
                              width="15em"
                      >Close</v-btn>
                    </v-col>
                  </v-col>
                  <v-col class="align-self-center" v-show="submitInProgress">
                    <v-col class="text-center">Submitting feedback</v-col>
                    <v-col>
                      <v-progress-linear
                        indeterminate
                      ></v-progress-linear>
                    </v-col>
                  </v-col>
                </div>
              </div>
            </div>
        </v-row>
      </v-col>
      <v-col class="feedback_view_mobile" :class="showFeedbackArea || showMobileFeedbackPanel ? 'feedback_view_expanded_xs':''" v-show="$vuetify.breakpoint.xs">
        <div class="feedback_strip_parent feedback_strip_parent_xs   clickable" v-on:click="toggleMobileFeedbackPanel()" v-show="!showMobileFeedbackPanel && !showFeedbackArea">
          <div class="feedback_strip">
                          Your Feedback
                </div>
        </div>
        <v-form ref="form" v-model="valid">
        <v-card-text class="align_center" v-show="viewFeebackArea()">
            <v-row class="clickable close_btn" v-on:click="toggleFeedback()"><span class="mdi mdi-close"/></v-row>
            <v-col class="feedback_header"><h3>{{feedbackHeader}}</h3></v-col>
            <v-col v-show="!showResponsePage || !responseRequired">
              <v-col>
                <v-textarea
                    :maxlength="3000"
                    :label="'Feedback'"
                    :rules="messageRules"
                    class="mt-3"
                    outlined
                    name="feedback-message"
                    height="100"
                    counter="3000"
                    v-model="feedbackMessage"
                >
                  <template v-slot:label>
                    <div><span class="mandatory">*</span> Feedback</div>
                  </template>
                </v-textarea>
              </v-col>
            </v-col>
            <v-col class="feedback_caption response_required"><span class="mandatory">*</span> Would you like a response from us?</v-col>
            <v-row justify="center">
                <v-radio-group class="no_margin" v-model="responseRequired" row :disabled="feedbackMessage.length === 0">
                  <v-radio  label="Yes" v-bind:value="yes"></v-radio>
                  <v-radio  label="No" v-bind:value="no" @click="showResponsePage = false"></v-radio>
                </v-radio-group>
            </v-row>
            <v-col v-if="showResponsePage && responseRequired">
              <v-text-field v-model="citizenName" :rules="nameRules" label="Name" outlined dense required>
                <template v-slot:label>
                  <div><span class="mandatory">*</span> Name</div>
                </template>
              </v-text-field>
              <v-text-field v-model="email" :rules="emailRules" label="Email" outlined dense @blur="validateRules" @input="validateRules"></v-text-field>
              <v-text-field v-model="phone" :rules="phoneRules" label="Phone" outlined dense @blur="validateRules" @input="validateRules"></v-text-field>
              <v-row justify="center" class="consent_xs"><v-col cols="10">{{consentMessage}}</v-col></v-row>
              <v-row justify="center">
                <v-radio-group class="no_margin" v-model="consent" row>
                  <v-radio  label="I Consent" v-bind:value="yes">
                    <template v-slot:label>
                      <div><span class="mandatory">*</span> I Consent</div>
                    </template>
                  </v-radio>
                </v-radio-group>
              </v-row>
            </v-col>
            <v-row class="justify-space-around">
              <v-btn v-show="!responseRequired && !showResponsePage" @click="postFeedback"
                      color="primary"
                      width="15em"
                      :disabled="validateSubmit()"
              >Submit</v-btn>
              <v-btn v-show="responseRequired && !showResponsePage" @click="toggleResponsePage"
                      color="primary"
                      width="15em"
              >Next</v-btn>
              <v-btn v-show="showResponsePage" @click="toggleResponsePage"
                      color="primary"
                      width="7em"
              >Back</v-btn>
              <v-btn v-show="showResponsePage" @click="postFeedback"
                      color="primary"
                      width="7em"
                      :disabled="validateSubmit()"
              >Submit</v-btn>
            </v-row>
          </v-card-text>
        </v-form>
          <v-card-text class="fill-height" v-show="showMobileFeedbackPanel">
            <v-col class="fill-height" >
              <v-row>
                <v-col class="align_center margin-left-20"><h3>Your Feedback</h3></v-col>
                <v-icon v-on:click="toggleMobileFeedbackPanel()" dense>mdi-close</v-icon>
              </v-row>
              <v-row class="icon_container_xs" justify="center"><v-icon v-on:click="showFeedBack('compliment')" class="icon_fb_xs">mdi-emoticon-happy</v-icon></v-row>
              <v-row class="icon_container_xs" justify="center"><v-icon v-on:click="showFeedBack('complaint')" class="icon_fb_xs">mdi-emoticon-sad</v-icon></v-row>
              <v-row class="icon_container_xs" justify="center"><v-icon v-on:click="showFeedBack('suggestion')" class="icon_fb_xs">mdi-lightbulb</v-icon></v-row>
            </v-col>
          </v-card-text>
          <div v-show="submitComplete || submitInProgress" class="response_content max_height">
                  <v-col class="align-self-center" v-show="submitComplete">
                    <v-col class="text-center">{{submitMessage}}</v-col>
                    <v-row justify="center"><v-btn @click="toggleFeedback"
                              color="primary"
                              width="15em"
                      >Close</v-btn></v-row>
                  </v-col>
                  <v-col class="align-self-center" v-show="submitInProgress">
                    <v-col class="text-center">Submitting feedback</v-col>
                    <v-col>
                      <v-progress-linear
                        indeterminate
                      ></v-progress-linear>
                    </v-col>
                  </v-col>
                </div>
      </v-col>
  </v-col>
</template>
<script lang="ts">
import { AppointmentModule, AuthModule } from '@/store/modules'
import { Component, Vue } from 'vue-property-decorator'
import { FeedbackRequestObject, FeedbackResponseObject } from '@/models/feedback'
import { mapActions, mapState } from 'vuex'
import CommonUtils from '@/utils/common-util'
import ConfigHelper from '@/utils/config-helper'
import { getModule } from 'vuex-module-decorators'

@Component({
  computed: {
    ...mapState('auth', [
      'currentUserProfile'
    ])
  },
  methods: {
    ...mapActions('appointment', [
      'submitFeedback'
    ])
  },
  data: function () {
    return {
      valid: false,
      messageRules: [
        v => !!v || 'Feedback message is required'
      ],
      nameRules: [
        v => !!v || 'name is required'
      ],
      emailRules: [
        v => !!v || 'E-mail or Phone no is required',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid'
      ],
      consentRules: [
        v => !!v || 'consent is required'
      ],
      phoneRules: [
        v => !!v || 'E-mail or Phone no is required',
        v => /^\d{10}$/.test(v) || 'Phone must be valid'
      ],
      yes: true,
      no: false
    }
  }
})
export default class Feedback extends Vue {
  private emailRules
  private phoneRules
  private valid
  private submitMessage: string = ''
  private feedbackServiceChannel: string = ConfigHelper.getFeedbackServiceChannel()
  private formEntryTime: number
  private submitComplete: boolean = false
  private submitInProgress: boolean = false
  private showResponsePage: boolean = false
  private feedbackMessage: string = ''
  private feedbackHeader: string = ''
  private feedbackType: string = ''
  private citizenName: string = ''
  private email: string = ''
  private phone: string = ''
  private appointmentModule = getModule(AppointmentModule, this.$store)
  private authModule = getModule(AuthModule, this.$store)
  private showFeedbackArea = false
  private consent: boolean = false
  private feedbackRequest: FeedbackRequestObject = { variables: { engagement: {}, citizen_comments: {}, service_channel: {}, response: {}, citizen_name: {}, citizen_contact: {}, citizen_email: {}, entity_key: {}, service_date: {}, submit_date_time: {}, entered_by: {} } }
  private feedbackResponse: FeedbackResponseObject
  private responseRequired: boolean = false
  private showMobileFeedbackPanel: boolean = false
  private readonly submitFeedback!: (feedbackRequest: FeedbackRequestObject) => any
  private consentMessage: string = 'The information on this form is collected under the authority of Sections 26(c) and 27(1)(c) of the Freedom of Information and Protection of Privacy Act to help us assess and respond to your enquiry. Questions about the collection of information can be directed to government’s Privacy Office.'
  private bookingStepInfo = ['None', 'Location Selection', 'Select Service', 'Select Date', 'Login', 'Appointment Summary']
  private toggleFeedback () {
    this.showFeedbackArea = !this.showFeedbackArea
    this.submitComplete = false
    this.submitInProgress = false
    this.feedbackType = ''
    this.responseRequired = false
    this.clearFields()
  }

  private toggleResponsePage () {
    this.showResponsePage = !this.showResponsePage
  }

  private showFeedBack (feedbackType: string) {
    this.formEntryTime = new Date().getTime()
    this.submitInProgress = false
    this.submitInProgress = false
    this.feedbackType = feedbackType
    this.responseRequired = false
    this.showResponsePage = false
    if (feedbackType === 'compliment') {
      this.feedbackHeader = 'Send us a compliment'
    }
    if (feedbackType === 'complaint') {
      this.feedbackHeader = 'Make a complaint'
    }
    if (feedbackType === 'suggestion') {
      this.feedbackHeader = 'Share a Suggestion'
    }
    this.showFeedbackArea = true
    this.showMobileFeedbackPanel = false
  }

  private getFeedbackViewStyle () {
    if (this.showFeedbackArea && this.responseRequired) {
      return 'feedback_response_expanded'
    }
    if (this.showFeedbackArea) {
      return 'feedback_container_expanded'
    }
  }

  private toggleMobileFeedbackPanel () {
    this.showMobileFeedbackPanel = !this.showMobileFeedbackPanel
  }

  private async postFeedback () {
    const formSubmitTime = new Date().getTime() - this.formEntryTime
    if (formSubmitTime < 500) {
      return
    }
    this.submitInProgress = true
    this.initModel()
    this.feedbackRequest.variables.engagement.value = this.feedbackType
    let appointmentLocation = this.$store.state.appointmentLocation
    let appointmentStep = this.$store.state.stepperCurrentStep
    let nonStepperLocation = this.$store.state.nonStepperLocation
    this.feedbackMessage = 'Feedback Message: ' + this.feedbackMessage + '\n'
    this.feedbackMessage = nonStepperLocation ? this.feedbackMessage + 'Step: ' + nonStepperLocation : this.feedbackMessage + 'Step: ' + this.bookingStepInfo[appointmentStep]
    this.feedbackMessage = appointmentLocation ? this.feedbackMessage + '\n' + 'Location: ' + appointmentLocation : this.feedbackMessage
    this.feedbackRequest.variables.citizen_comments.value = this.feedbackMessage + '\n' + CommonUtils.getUserAgent()
    this.feedbackRequest.variables.response.value = this.responseRequired ? 'true' : 'false'
    this.feedbackRequest.variables.citizen_name.value = this.citizenName === '' ? 'None' : this.citizenName
    this.feedbackRequest.variables.citizen_contact.value = this.phone === '' ? 'None' : this.phone
    this.feedbackRequest.variables.citizen_email.value = this.email === '' ? 'None' : this.email
    this.feedbackRequest.variables.service_date.value = this.getCurrentDateinFormat()
    this.feedbackRequest.variables.submit_date_time.value = this.getCurrentDateinFormat()
    const resp = await this.submitFeedback(this.feedbackRequest)
    if (resp.status) {
      if (resp.status === 200 && resp.data.response_code === 200) {
        this.submitMessage = 'Thank you!'
        this.submitInProgress = false
        this.submitComplete = true
        this.clearFields()
      } else {
        this.submitMessage = 'Feedback submission failed.'
        this.submitInProgress = false
        this.submitComplete = true
        this.clearFields()
      }
    }
  }

  private clearFields () {
    this.feedbackMessage = ''
    this.citizenName = ''
    this.email = ''
    this.phone = ''
  }

  private viewFeebackArea () {
    if (this.showFeedbackArea && !this.submitComplete && !this.submitInProgress) {
      return true
    } else {
      return false
    }
  }

  private initModel () {
    this.feedbackRequest.variables.engagement.type = 'String'
    this.feedbackRequest.variables.citizen_comments.type = 'String'
    this.feedbackRequest.variables.service_channel.type = 'String'
    this.feedbackRequest.variables.service_channel.value = this.feedbackServiceChannel
    this.feedbackRequest.variables.entered_by.type = 'String'
    this.feedbackRequest.variables.entered_by.value = this.feedbackServiceChannel
    this.feedbackRequest.variables.response.type = 'Boolean'
    this.feedbackRequest.variables.citizen_name.type = 'String'
    this.feedbackRequest.variables.citizen_contact.type = 'String'
    this.feedbackRequest.variables.citizen_email.type = 'String'
    this.feedbackRequest.variables.entity_key.type = 'String'
    this.feedbackRequest.variables.entity_key.value = 'CCII'
    this.feedbackRequest.variables.service_date.type = 'String'
  }

  private getCurrentDateinFormat () {
    const currentDate = new Date()
    const day = currentDate.getDate().toString().length === 1 ? '0' + currentDate.getDate().toString() : currentDate.getDate().toString()
    const month = (currentDate.getMonth() +1).toString().length === 1 ? '0' + (currentDate.getMonth() + 1).toString() : (currentDate.getMonth() + 1).toString()
    return currentDate.getFullYear() + '-' + month + '-' + day
  }

  private phoneEmail (value) {
    if (this.phone !== '' && this.email !== '') {
      return true
    } else {
      return 'Email or Phone no is required'
    }
  }

  private validateRules () {
    const phoneCondition = this.phone !== undefined && this.phone !== ''
    const emailCondition = this.email !== undefined && this.email !== ''
    if (emailCondition || phoneCondition) {
      if (emailCondition) {
        const formatResponse = /.+@.+\..+/.test(this.email) ? true : 'Email must be valid'
        this.emailRules = [formatResponse]
        this.phoneRules = [true]
      }
      if (phoneCondition) {
        this.phoneRules = [true]
        this.emailRules = [true]
      }
    } else {
      this.emailRules = ['Email or Phone is required']
      this.phoneRules = ['Email or Phone is required']
    }
  }

  private validateSubmit () {
    if (this.responseRequired) {
      return !(this.valid && this.consent)
    } else if (!this.responseRequired) {
      return !this.valid
    } else {
      return true
    }
  }
}

</script>

<style lang="scss" scoped>
$background_unselected:#F2F2F2;
$icons_unselected:#313132;
$icons_selected:$background_unselected;
$background_selected:#003366;
$fb_border_color:#d0cece;
$background_selected:#003366;
$feedback_strip_color:$background_selected;
$caption_medium:0.9rem;
$caption_small:0.7rem;
$mandatory_star:#ff0000;
.feedback_area{
    position: relative;
    background: #ffffff;
}
.feedback_container{
    float: right;
    display: flex;
    align-items: center;
}
.feedback_icon{
    text-align: center;
    padding: 10px;
    padding-left: 5px;
    font-size: 29px;
}
.feedback_strip_parent{
    transform: rotate(
        -90deg
         );
    bottom: 0!important;
    float: right;
    transform-origin: 60%;
    position: relative;
    width: auto;
}
.feedback_strip_parent.feedback_strip_parent_xs{
    top: 45%;
    transform-origin: 75%;
}
.feedback_strip{
    background: $feedback_strip_color;
    color: aliceblue;
    padding: 10px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    text-align: center;
}
.icon_strip{
    background: $background_unselected;
    color: $icons_unselected;
}
.row-f{
    display: inline-block;
}
.feedback_view{
  width: auto;
  position: fixed;
  z-index: 5;
  height: auto;
  right: 0px;
  display: flex;
  align-items: center;
  top: 40%;
}
.feedback_view .col{
  padding: 0;
}
.clickable {
  text-decoration: underline;
  cursor: pointer;
}
.align_center{
  text-align: center;
}
.feedback_view .feedback_header.col{
  padding: 10px;
}
.feedback_header h3{
  font-weight: 400;
}
.feedback_message{
  width: 100%;
  height: 5em;
  border: 2px solid $fb_border_color;
}
.feedback_caption{
  font-size: $caption_medium;
}
.submit_row{
  display: block;
}
.feedback_view .submit_row.col{
  padding-left: 20px;
  padding-right: 20px;
}
.invert_colors{
  background: $background_selected;
  color: $icons_selected;
}

.feedback_view_expanded{
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,.48)!important;
  top:0;
  display: flex;
  align-items: center;
}
.feedback_container_expanded{
  position: relative;
}
.feedback_response_expanded{
  position: relative;
}
.close_btn{
  float: right;
  font-size: 20px;
  margin-top: -10px;
}
.feedback_text{
  border: 2px solid $fb_border_color;
}
.label_caption{
  text-align: left;
  margin-left: 12%;
  font-size: $caption_small;
}
.mandatory{
  color: $mandatory_star;
}
.consent{
    max-width: 350px;
    font-size: $caption_small;
    padding-left: 20px;
    padding-right: 20px;
    margin-top: -10px;
}
.consent_xs{
  font-size: $caption_small;
  margin-top: -10px;
}
.feedback_view .consent.col{
  padding: 10px;
}
.no_margin{
  margin: 0;
}
.consent_radio_btn {
  padding: 10px;
}

.feedback_text_field{
  border: 2px solid $fb_border_color;
}
.full_area{
  background: grey;
}
.feedback_view_mobile{
  position: fixed;
  z-index: 5;
  width: 10%;
  left: 90%;
  bottom: 8.5%;
}
.feedback_view_mobile.feedback_view_expanded_xs{
  width: 100%;
  height: 100%;
  background: #ffffff;
  top: 0;
  left: 0;
}
.icon_container_xs{
  min-height: 30%;
}
.icon_container_xs .v-icon.v-icon {
  font-size: 80px;
  color: $background_selected;
}
.response_content{
  display: flex;
  min-height: 300px;
  padding: 20px;
}

.response_content .col{
  padding: 10px;
}

.feedback_view_expanded_xs .col{
  padding: 5px;
}
.max_height{
  min-height: 100%;
}
.padding-10{
  padding: 10px;
}
.margin-left-20{
  margin-left: 20px;
}

.feedback_area .row{
  margin: 0;
}

.feedback_area h3{
  font-size: 1.3rem;
}
</style>
