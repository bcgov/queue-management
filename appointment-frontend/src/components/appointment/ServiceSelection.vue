<template>
  <v-card>
    <v-card-title class="justify-center">
      <h3>Service Selection</h3>
    </v-card-title>
    <v-divider class="mx-4"></v-divider>
    <v-card-text>
      <p class="step-desc">Please select the service you'd like to receive</p>
      <v-row justify="center">
        <v-col cols="12" sm="6">
          <v-combobox
            :items="serviceList"
            :item-disabled="checkDisabled"
            :item-text="'external_service_name'"
            label="Select Service"
            outlined
            color="primary"
            class="service-selection text-left"
            v-model="selectedService"
            name="service-select"
            @change="serviceSelection"
          >
            <template v-slot:selection="data">
              {{ data.item.external_service_name }}
            </template>
            <template v-slot:item="data">
              <div class="">
                <div>{{ data.item.external_service_name }}</div>
                <!-- <div class="service-message">{{ data.item.service_desc }}</div> -->
              </div>
            </template>
          </v-combobox>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-col cols="12" sm="6">
          <v-textarea
            outlined
            name="additional-options"
            label="Is there any additional info you'd like to add? (Optional)"
            v-model="additionalOptions"
            @change="changeAdditionalOptions"
        ></v-textarea>
        </v-col>
      </v-row>
      <template v-if="selectedService">
        <p class="text-center mb-6">Do you want to book an appointment with <strong>{{currentOffice.office_name}}</strong> for <strong>{{selectedService.external_service_name}}</strong> service?</p>
        <div class="d-flex justify-center mb-6">
          <!-- <v-btn
            large
            outlined
            color="primary"
            class="mr-3"
            @click="otherBookingOptionModel = true"
          >No, Book With Another Option</v-btn> -->
          <v-btn
            large
            @click="proceedBooking"
            color="primary"
          >Yes, Book With The Service BC Centre</v-btn>
        </div>
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
  </v-card>
</template>

<script lang="ts">
import { Component, Mixins, Prop, Vue } from 'vue-property-decorator'
import { mapActions, mapMutations, mapState } from 'vuex'
import { Office } from '@/models/office'
import { Service } from '@/models/service'
import { ServiceAvailability } from '@/utils/constants'
import StepperMixin from '@/mixins/StepperMixin.vue'

@Component({
  computed: {
    ...mapState('office', [
      'currentOffice',
      'currentService',
      'additionalNotes',
      'serviceList'
    ])
  },
  methods: {
    ...mapMutations('office', [
      'setCurrentService',
      'setAdditionalNotes'
    ]),
    ...mapActions('office', [
      'getServiceByOffice'
    ])
  }
})
export default class ServiceSelection extends Mixins(StepperMixin) {
  private readonly serviceList!: Service[]
  private readonly currentOffice!: Office
  private readonly currentService!: Service
  private readonly additionalNotes!: string
  private readonly setCurrentService!: (service: Service) => void
  private readonly setAdditionalNotes!: (notes: string) => void
  private readonly getServiceByOffice!: (officeId: number) => Promise<Service[]>
  private selectedService: Service = null
  private additionalOptions = ''
  private otherBookingOptionModel = false

  private async mounted () {
    if (this.currentOffice?.office_id) {
      await this.getServiceByOffice(this.currentOffice.office_id)
    }
    this.selectedService = this.currentService || null
    this.additionalOptions = this.additionalNotes || ''
  }

  private serviceSelection (value) {
    this.setCurrentService(value)
  }

  private changeAdditionalOptions () {
    this.setAdditionalNotes(this.additionalOptions)
  }

  private proceedBooking () {
    this.stepNext()
  }

  private checkDisabled (value) {
    return (value.online_availability === ServiceAvailability.DISABLE)
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
</style>
