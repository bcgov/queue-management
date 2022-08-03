<template>
  <div :class="{'service-selection-mobile': $vuetify.breakpoint.xs}">
    <v-card-text>
      <v-row justify="center">
        <v-col cols="12" sm="6" class="text-center">
          <v-combobox
            :items="serviceList"
            :item-text="'externalServiceName'"
            :filter="serviceSearchFilter"
            label="Select Service"
            outlined
            color="primary"
            class="service-selection"
            v-model="selectedService"
            name="service-select"
            @change="serviceSelection"
            @input="clickSelection"
            @keyup="setKeyPressed"
            auto-select-first="true"
            data-cy="step-2-combobox-service"
            hide-details
          >
            <template v-slot:selection="data">
              {{ data.item.externalServiceName }}
              <span v-if="checkDisabled(data.item)" class="ml-1 caption">(Unavailable)</span>
            </template>
            <template v-slot:item="data">
              <div
                v-bind:class="{'disabled-selection': checkDisabled(data.item)}"
                class="service-selection-options"
              >
                <div>{{ data.item.externalServiceName }}</div>
              </div>
            </template>
          </v-combobox>
        </v-col>
      </v-row>
      <template v-if="selectedService && !keyPressed && !checkDisabled(selectedService)">
        <div class="d-flex justify-center mb-6">
          <v-btn
            large
            @click="proceedBooking"
            color="primary"
            data-cy="step-2-button-next"
          >
            Next
            <v-icon right small class="ml-1">mdi-arrow-right</v-icon>
          </v-btn>
        </div>
        <p v-if="selectedService.onlineLink" class="text-center mb-6"><strong>{{selectedService.externalServiceName}}</strong> can be completed online.</p>
        <p v-if="selectedService.onlineLink" class="text-center mb-6"><a :href="selectedService.onlineLink" target="_blank">Would you like to try online?</a></p>
        <p class="text-center body-2">
          Information is collected under the authority of
          <a href="http://www.bclaws.ca/civix/document/id/complete/statreg/96165_03#d2e3154" rel="noopener noreferrer" target="_blank">Sections 26(c)</a>
          of the Freedom of Information and Protection of Privacy Act to help us assess and respond to your enquiry. Questions about the collection of information can be directed to the Director, Provincial Operations, PO BOX 9412 STN PROV GOVT, Victoria, BC, V8W 9V1, 1 800 663-7867.
        </p>
      </template>
      <template v-if="checkDisabled(selectedService)">
        <p class="text-center mb-6">We're sorry, <strong>{{selectedService.externalServiceName}}</strong> is not available by appointment.</p>
        <p v-if="selectedService.onlineLink" class="text-center mb-6"><a :href="selectedService.onlineLink" target="_blank">Would you like to try online?</a></p>
      </template>
    </v-card-text>
    <!-- Other Booking Option Model Popup -->
    <v-dialog
      v-model="otherBookingOptionModel"
      max-width="600"
    >
      <v-card>
        <v-toolbar flat color="grey lighten-3">
          <v-toolbar-title>Other Booking Options for BC Services Card</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn icon @click="otherBookingOptionModel = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <v-card-text>
          <p class="mt-4 mb-6">Please use one of the below methods to book your appointment</p>
          <p>
            <strong>Phone: </strong> (250)-387-6121
          </p>
          <p>
            <strong>Email: </strong> info@gov.bc.ca
          </p>
          <p>
            <strong>Fax: </strong> (250)-952-4124
          </p>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { Component, Mixins } from 'vue-property-decorator'
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
import { Office } from '@/models/office'
import { Service } from '@/models/service'
import { ServiceAvailability } from '@/utils/constants'
import StepperMixin from '@/mixins/StepperMixin.vue'
import { User } from '@/models/user'

@Component({
  computed: {
    ...mapState('office', [
      'currentOffice',
      'currentService',
      'additionalNotes',
      'serviceList'
    ]),
    ...mapState('auth', [
      'currentUserProfile'
    ]),
    ...mapGetters('auth', [
      'isAuthenticated'
    ])
  },
  methods: {
    ...mapMutations('office', [
      'setCurrentService',
      'setAdditionalNotes'
    ]),
    ...mapActions('office', [
      'getServiceByOffice',
      'callSnowplowClick'
    ])
  }
})
export default class ServiceSelection extends Mixins(StepperMixin) {
  private readonly serviceList!: Service[]
  private readonly currentUserProfile!: User
  private readonly currentOffice!: Office
  private readonly currentService!: Service
  private readonly isAuthenticated!: boolean
  private readonly additionalNotes!: string
  private readonly setCurrentService!: (service: Service) => void
  private readonly setAdditionalNotes!: (notes: string) => void
  private readonly getServiceByOffice!: (officeId: number) => Promise<Service[]>
  private readonly callSnowplowClick!: (mySP: any) => any
  private selectedService: Service = null
  private selectedServiceType = typeof this.selectedService
  private additionalOptions = ''
  private maxChars = 220
  private charsLeft = this.maxChars
  private textCharsPrefix = 'Additional information? (Optional - '
  private textCharsSuffix = ' characters left)'
  private textCharsLeft = this.textCharsPrefix + this.charsLeft + this.textCharsSuffix
  private keyPressed = true
  private myMessage = ''

  private otherBookingOptionModel = false

  private async mounted () {
    if (this.isOnCurrentStep) {
      if (this.currentOffice?.officeId) {
        await this.getServiceByOffice(this.currentOffice.officeId)
      }
      this.selectedService = (!this.checkDisabled(this.currentService)) ? this.currentService : null
      this.additionalOptions = this.additionalNotes || ''
    }
  }

  private serviceSelection (value) {
    this.keyPressed = false
    this.setCurrentService(value)
  }

  private mylog (myText) {
    this.myMessage = this.myMessage + '\r\n' + myText
  }

  private setKeyPressed (e) {
    if (e.key !== 'Enter') {
      this.keyPressed = true
    }
  }

  private clickSelection (value: Service) {
    if (!value?.serviceName) {
      this.selectedService = null
      this.setCurrentService(undefined)
    } else {
      if (this.checkDisabled(value)) {
        this.setCurrentService(undefined)
      } else {
        this.setCurrentService(value)
      }
    }
  }

  private changeAdditionalOptions () {
    this.setCharsLeft()
    this.setAdditionalNotes(this.additionalOptions)
  }

  private proceedBooking () {
    this.stepNext()
  }

  private setCharsLeft () {
    if (this.additionalOptions.length <= this.maxChars) {
      this.charsLeft = this.maxChars - this.additionalOptions.length
    } else {
      this.charsLeft = 0
      this.additionalOptions = this.additionalOptions.substring(0, this.maxChars)
    }
    this.textCharsLeft = this.textCharsPrefix + this.charsLeft + this.textCharsSuffix
  }

  private checkDisabled (value: Service) {
    return (value?.onlineAvailability === ServiceAvailability.DISABLE)
  }

  private goToServiceLink (sn, url) {
    const mySP = { label: 'Online Option', step: 'Select Service', loggedIn: this.isAuthenticated, apptID: null, clientID: this.currentUserProfile?.userId, loc: this.currentOffice?.officeName, serv: sn, url: url }
    this.callSnowplowClick(mySP)
    window.open(url, '_blank')
  }

  private serviceSearchFilter (item: Service, queryText, itemText) {
    return `${item?.externalServiceName || ''} ${item?.serviceDesc || ''}`.toLowerCase().indexOf((queryText || '').toLowerCase()) > -1
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
.v-list-item {
  border-bottom: 1px solid $gray6;
}
.service-message {
  font-size: 10px;
  font-style: italic;
  margin-bottom: 8px;
  max-width: 450px;
}
.disabled-selection {
  color: rgba(0, 0, 0, 0.38);
}
.service-selection-options {
  width: 100%;
  border-bottom: 1px solid $gray2;
  padding-bottom: 6px;
  padding-top: 4px;
  .service-link {
    font-weight: 600;
    font-size: .85rem;
    display: block;
    float: right;
    padding: 8px;
    padding-right: 4px;
    padding-left: 14px;
    margin-top: -10px;
    color: $BCgovBlue8;
    word-break: normal;
  }
}

.service-link-mobile {
  margin-top: 0 !important;
  margin-bottom: -4px;
}
</style>
