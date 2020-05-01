<template>
  <v-card-text>
    <p class="step-desc">To book an appointment, please find your nearest BC Service Location</p>
    <v-row justify="center">
      <v-col cols="6" sm="4">
        <v-text-field
          append-icon="mdi-map-marker-radius"
          type="text"
          name="postal-code"
          label="Postal Code"
          outlined
          hide-details
          dense
          @click:append="fetchLocation"
        ></v-text-field>
      </v-col>
      <v-col cols="6" sm="4">
        <v-select
          :items="radiusList"
          label="Radius"
          outlined
          color="primary"
          class="text-left"
          v-model="selectedRadius"
          name="radius-select"
          dense
          hide-details
        >
          <template v-slot:selection="data">
            {{ data.item }} Km
          </template>
        </v-select>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="12">
        <p class="text-center mb-0">Locations sorted by nearest to you</p>
      </v-col>
      <v-col
        cols="12"
        sm="10"
        v-for="(location) in locationListData"
        :key="location.office_id"
      >
        <v-card
          :disabled="!location.appointments_enabled_ind"
          class="mx-auto">
          <v-card-text>
            <v-row class="d-flex" justify="space-around">
              <v-col cols="6" align-self="stretch">
                <GmapMap
                  :center="getCoordinates(location)"
                  :zoom="14"
                  class="map-view"
                  :options="mapConfigurations"
                >
                  <GmapMarker
                    :position="getCoordinates(location)"
                    :clickable="true"
                    :draggable="false"
                    :label='{text: location.office_name, fontWeight: "600"}'
                  />
                </GmapMap>
                <div class="text-center mt-2 body-2" v-if="location.civic_address">
                  {{location.civic_address}}
                </div>
              </v-col>
              <v-col cols="6" align-self="stretch">
                <h4 class="mb-3 location-name">
                  {{location.office_name}}
                  <span class="body-1 ml-2" v-if="location.distance">
                    {{location.distance}}Km
                  </span>
                </h4>
                <v-alert
                  dense
                  :text=(!location.appointments_enabled_ind)
                  border="left"
                  :type="(!location.appointments_enabled_ind) ? 'error' : 'info'"
                  class="subtitle-2 font-weight-bold"
                  v-if="location.office_appointment_message"
                >
                  {{location.office_appointment_message}}
                </v-alert>
                <v-alert
                  type="info"
                  text
                  color="blue-grey darken-4"
                  icon="mdi-clock"
                  class="mb-0"
                >
                  <v-row no-gutters v-for="(timeslot, index) in location.timeslots" :key="index">
                    <v-col cols="5" class="px-5">{{timeslot.day_str}}</v-col>
                    <v-col cols="7">
                      <span v-if="!(timeslot.start_time_str && timeslot.end_time_str)" class="hours-closed">Closed</span>
                      <span v-else>
                        {{`${timeslot.start_time_str} - ${timeslot.end_time_str}`}}
                      </span>
                    </v-col>
                  </v-row>
                </v-alert>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="primary"
              outlined
              large
              @click="showLocationServices(location)"
            >
              View Location Services
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              class="pl-5"
              large
              @click="selectLocation(location)"
            >
              Select Location
              <v-icon right small class="ml-1">mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <!-- Service Model Popup -->
    <ServiceListPopup
      :locationServicesModal="locationServicesModal"
      :serviceList="serviceList"
      :selectedLocationName="selectedLocationName"
    ></ServiceListPopup>
  </v-card-text>
</template>

<script lang="ts">
import { Component, Mixins, Prop, Vue } from 'vue-property-decorator'
import { mapActions, mapMutations } from 'vuex'
import ConfigHelper from '@/utils/config-helper'
import { Office } from '@/models/office'
import { OfficeModule } from '@/store/modules'
import { Service } from '@/models/service'
import ServiceListPopup from './ServiceListPopup.vue'
import StepperMixin from '@/mixins/StepperMixin.vue'
import { getModule } from 'vuex-module-decorators'

@Component({
  components: {
    ServiceListPopup
  },
  methods: {
    ...mapMutations('office', [
      'setCurrentOffice'
    ]),
    ...mapActions('office', [
      'getOffices',
      'getServiceByOffice',
      'getAvailableAppointmentSlots',
      'getCategories'
    ])
  }
})
export default class LocationsList extends Mixins(StepperMixin) {
  private officeModule = getModule(OfficeModule, this.$store)
  private mapConfigurations = ConfigHelper.getMapConfigurations()
  private readonly getOffices!: () => Promise<Office[]>
  private readonly getServiceByOffice!: (officeId: number) => Promise<Service[]>
  private readonly getAvailableAppointmentSlots!: (officeId: number) => Promise<any>
  private readonly getCategories!: () => Promise<any>
  private readonly setCurrentOffice!: (office: Office) => void
  private selectedRadius = null
  private radiusList = [2, 4, 6, 10]
  private selectedLocationName: string = ''
  private locationServicesModal = false

  private locationListData: Office[] = []
  private serviceList: Service[] = []

  private async mounted () {
    this.locationListData = await this.getOffices()
    await this.getCategories()
  }

  private fetchLocation () {
    // eslint-disable-next-line no-console
    console.log('fetchLocation')
  }

  private async showLocationServices (location) {
    this.serviceList = await this.getServiceByOffice(location.office_id)
    this.selectedLocationName = location.office_name
    this.locationServicesModal = true
  }

  private getCoordinates (location) {
    return {
      lat: location.latitude || 0,
      lng: location.longitude || 0
    }
  }

  private async selectLocation (location) {
    this.setCurrentOffice(location)
    this.stepNext()
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
.hours-day {
  width: 90px;
  margin-right: 24px;
}
.hours-closed {
    color: $BCgovInputError;
    font-weight: 600;
}
.location-name {
  font-size: 1.25rem;
}
.map-view {
  width: 100%;
  height: 100%;
  min-height: 240px;
}
.service-unavailable {
  color: $BCgovInputError;
  font-weight: 600;
}
</style>
