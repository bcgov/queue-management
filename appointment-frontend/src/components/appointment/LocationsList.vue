<template>
  <v-card-text
    :class="{'location-list-mobile': $vuetify.breakpoint.xs}"
  >
    <v-row justify="center">
      <v-col cols="12" sm="6" md="4">
        <v-combobox
            :items="locationListData"
            :item-text="'office_name'"
            :filter="officeSearchFilter"
            label="Select Office"
            outlined
            color="primary"
            v-model="selectedOffice"
            name="office-select"
            @change="officeSelection"
            @input="clickSelection"
            @keyup="setKeyPressed"
            auto-select-first="true"
            hide-details
          >
          </v-combobox>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="12" class="location-sorted-msg">
      </v-col>
      <v-col
        cols="12"
        sm="10"
        v-for="(location) in selectedlocationListData"
        :key="location.office_id"
      >
        <v-card
        v-show="selectedOffice"
          :disabled="location.online_status === 'Status.DISABLE'"
          :outlined="(currentOffice && currentOffice.office_id === location.office_id)"
          :color="(currentOffice && currentOffice.office_id === location.office_id) ? 'blue-grey lighten-5' : ''"
          class="mx-auto location-card">
          <v-card-text>
            <v-row class="d-flex" justify="space-around">
              <v-col cols="12" md="6" align-self="stretch">
                <v-row>
                  <v-col cols="12" md="12">
                    <v-btn
                      block
                      color="primary"
                      class="pl-5 mt-0 mt-md-2"
                      large
                      @click="selectLocation(location)"
                    >
                      Book Appointment
                    </v-btn>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="6">
                    <h4 class="mb-3 location-name">
                  {{location.office_name}}
                </h4>
                  </v-col>
                </v-row>
                <v-alert
                  dense
                  :text=(!location.appointments_enabled_ind)
                  border="left"
                  :type="(!location.appointments_enabled_ind) ? 'error' : 'info'"
                  class="subtitle-2 font-weight-bold mb-4"
                  v-if="location.office_appointment_message"
                >
                  {{location.office_appointment_message}}
                </v-alert>
                <v-alert
                  :type="(!$vuetify.breakpoint.xs) ? 'info' : undefined"
                  text
                  color="blue-grey darken-4"
                  :icon="(!$vuetify.breakpoint.xs) ? 'mdi-clock' : false"
                >
                  <v-row no-gutters v-for="(timeslot, index) in location.timeslots" :key="index">
                    <v-col cols="6" md="5" class="px-5 nobr">{{timeslot.day_str}}</v-col>
                    <v-col cols="6" md="7">
                      <span v-if="!(timeslot.start_time_str && timeslot.end_time_str)" class="hours-closed">Closed</span>
                      <span v-else>
                        {{`${timeslot.start_time_str}` }} - {{ `${timeslot.end_time_str}`}}
                      </span>
                    </v-col>
                  </v-row>
                </v-alert>
                <v-row>
                  <v-col col="12" md="6">
                    <v-btn
                        block
                        color="primary"
                        outlined
                        class='mt-0 mt-md-2 float-right'
                        large
                        @click="showLocationServices(location)"
                      >
                        Available Services
                    </v-btn>
                  </v-col>
                </v-row>
              </v-col>
              <v-col cols="12" md="6" align-self="stretch" align="center" class="loc-map">
                <template v-if='location.external_map_link'>
                  <a class='link-w-icon mt-6' v-bind:href='location.external_map_link' target="_blank" rel="noopener noreferrer" :alt='`Open link for ${ location.civic_address}`'>
                    <v-img v-if="location.civic_address" :src="require('@/assets/img/officemaps/' + (location.office_number ? location.office_number.toString() + '.png' : '999.png'))" :alt="location.civic_address || 'No address'" class='static-map'>
                    </v-img>
                  </a>
                </template>
                <template v-else>
                  <v-img v-if="location.civic_address" :src="require('@/assets/img/officemaps/' + (location.office_number ? location.office_number.toString() + '.png' : '999.png'))" :alt="location.civic_address || 'No address'" class='static-map'>
                    </v-img>
                </template>
                <div class="text-center mt-2 body-2" v-if="location.civic_address">
                  <template v-if='location.external_map_link'>
                    <a class='link-w-icon mt-6' v-bind:href='location.external_map_link' target="_blank" rel="noopener noreferrer" :alt='`Open link for ${ location.civic_address}`'>
                      <v-icon small class="mr-2">mdi-open-in-new</v-icon>
                      {{location.civic_address}}
                    </a>
                  </template>
                  <template v-else>{{location.civic_address}}</template>

                </div>
                <div class="text-center mt-2 body-2 green--text font-weight-bold" v-if='location.latitude && location.longitude && hasCoordinates'>
                  {{ getDistance(location.latitude, location.longitude) }}
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col
        class="text-center container py-2"
        cols="12"
      >
         {{ footerMsg[0] }} <a :href="footerLinks[0]" target="_blank">{{ footerMsg[1] }}</a>
         {{ footerMsg[2] }} <a :href="footerLinks[1]" target="_blank">{{ footerMsg[3] }}</a>
         {{ footerMsg[4] }} <a :href="footerLinks[2]" target="_blank">{{ footerMsg[5] }}</a>
         {{ footerMsg[6] }} <a :href="footerLinks[3]" target="_blank">{{ footerMsg[7] }}</a>
         {{ footerMsg[8] }} <a :href="footerLinks[4]" target="_blank">{{ footerMsg[9] }}</a>
      </v-col>
    </v-row>
    <!-- Service Model Popup -->
    <ServiceListPopup
      ref="locationServiceListPopup"
      :locationServicesModal="locationServicesModal"
      :serviceList="serviceList"
      :selectedLocationName="selectedLocationName"
    ></ServiceListPopup>
  </v-card-text>
</template>

<script lang="ts">
import { Component, Mixins } from 'vue-property-decorator'
import { GeoModule, OfficeModule } from '@/store/modules'
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
import ConfigHelper from '@/utils/config-helper'
import GeocoderInput from './GeocoderInput.vue'
import GeocoderService from '@/services/geocoder.services'
import { Office } from '@/models/office'
import { Service } from '@/models/service'
import ServiceListPopup from './ServiceListPopup.vue'
import StepperMixin from '@/mixins/StepperMixin.vue'
import { User } from '@/models/user'
import { getModule } from 'vuex-module-decorators'

@Component({
  components: {
    ServiceListPopup,
    GeocoderInput
  },
  computed: {
    ...mapState('office', [
      'currentOffice',
      'officeList'
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
      'setCurrentOffice',
      'setCurrentService'
    ]),
    ...mapActions('office', [
      'getOffices',
      'getServiceByOffice',
      'getAvailableAppointmentSlots',
      'getCategories',
      'callSnowplowClick'
    ]),
    ...mapState('geo', [
      'currentCoordinates'
    ])
  }
})
export default class LocationsList extends Mixins(StepperMixin) {
  private officeModule = getModule(OfficeModule, this.$store)
  private geoModule = getModule(GeoModule, this.$store)
  private mapConfigurations = ConfigHelper.getMapConfigurations()
  private readonly getOffices!: () => Promise<Office[]>
  private readonly getServiceByOffice!: (officeId: number) => Promise<Service[]>
  private readonly getAvailableAppointmentSlots!: (officeId: number) => Promise<any>
  private readonly getCategories!: () => Promise<any>
  private readonly setCurrentOffice!: (office: Office) => void
  private readonly setCurrentService!: (service: Service) => void
  private readonly callSnowplowClick!: (mySP: any) => any
  private readonly currentUserProfile!: User
  private readonly currentOffice!: Office
  private readonly isAuthenticated!: boolean
  private footerMsg = []
  private footerLinks = []
  private readonly currentCoordinates!: () => any;
  private selectedOffice: Office = null
  private keyPressed = true

  private selectedRadius = null
  private radiusList = [2, 4, 6, 10]
  private selectedLocationName: string = ''
  private locationServicesModal = false

  private locationListData: Office[] = []
  private selectedlocationListData: Office[] = []
  private serviceList: Service[] = []

  $refs: {
    locationServiceListPopup: ServiceListPopup
  }

  private async mounted () {
    let fm = ConfigHelper.getFooterText()
    let fl = ConfigHelper.getFooterLinks()
    this.footerMsg = fm.split('{link}')
    this.footerLinks = fl.split('{link}')
    if (this.isOnCurrentStep) {
      this.locationListData = await this.getOffices()
      this.locationListData = this.locationListData.filter(location => location.appointments_enabled_ind).filter(location => location.online_status === 'Status.SHOW')
      this.$store.commit('setAppointmentLocation', undefined)
    }
  }

  private sortOfficesByDistance (locationList) {
    // If we have no distance, we can't sort
    if (!this.hasCoordinates()) {
      return locationList
    } else {
      // Add a "calculated_distance" to every location that has lat/lng
      // Then sort array based on that value
      return this.locationListData.map(location => {
        const locationCoords = { latitude: location.latitude, longitude: location.longitude }
        let result

        if (!location.latitude || !location.longitude) {
          result = null
        } else {
          result = GeocoderService.distance(this.currentCoordinates(), locationCoords)
        }
        location['calculated_distance'] = result
        return location
      })
        .sort((a, b) => {
          // Put all null values at bottom of list
          let aDist = a['calculated_distance']
          let bDist = b['calculated_distance']

          if (aDist === null) {
            aDist = 999
          }
          if (bDist === null) {
            bDist = 999
          }

          return aDist - bDist
        })
    }
  }

  private setKeyPressed (e) {
    if (e.key !== 'Enter') {
      this.keyPressed = true
    }
  }

  private scrollTop () {
    this.selectedOffice = null
  }

  private checkDisabled (value) {
    return (value?.appointments_enabled_ind)
  }

  private clickSelection (value) {
    if (!value?.service_name) {
      this.selectedOffice = null
      this.setCurrentOffice(undefined)
    } else {
      if (this.checkDisabled(value)) {
        this.selectedOffice = null
        this.setCurrentOffice(undefined)
      } else {
        this.setCurrentOffice(value)
      }
    }
  }

  private officeSelection (value) {
    this.keyPressed = false
    this.selectedOffice = value
    this.selectedlocationListData = this.locationListData.filter(location => location.office_id === this.selectedOffice.office_id)
  }

  private officeSearchFilter (item, queryText, itemText) {
    return `${item?.office_name || ''}`.toLowerCase().indexOf((queryText || '').toLowerCase()) > -1
  }

  private getDistance (latitude, longitude) {
    if (!this.hasCoordinates()) {
      return null
    }
    const destination = { latitude, longitude }
    const dist = GeocoderService.distance(this.currentCoordinates(), destination)

    if (dist < 1) {
      return '<1km'
    } else {
      return dist.toFixed(0) + 'km'
    }
  }

  private hasCoordinates (): boolean {
    return !!this.currentCoordinates()
  }

  private async showLocationServices (location) {
    this.serviceList = await this.getServiceByOffice(location.office_id)
    await this.getCategories()
    this.selectedLocationName = location.office_name
    this.$refs.locationServiceListPopup.open()
    const mySP = { label: 'View Location Services', step: 'Location Selection', loggedIn: this.isAuthenticated, apptID: null, clientID: this.currentUserProfile?.user_id, loc: location.office_name, serv: null, url: null }
    this.callSnowplowClick(mySP)
  }

  private getCoordinates (location) {
    return {
      lat: location.latitude || 0,
      lng: location.longitude || 0
    }
  }

  private async selectLocation (location) {
    if (this.currentOffice?.office_id !== location?.office_id) {
      this.$store.commit('setAppointmentLocation', location.office_name)
      this.setCurrentOffice(location)
      this.setCurrentService(undefined)
    }
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
    // We can't use the $BCgovInputError on the background here, as it will break accessibility.
    // The only colour which works on the background is black, or this muddy dark red
    color: black;
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
.static-map {
  max-width: 100%;
}
.location-list-mobile {
  .location-sorted-msg {
    padding: 0;
    font-size: .85rem;
  }
  .location-card {
    .v-card__text {
      padding-top: 2px;
      .loc-map {
        padding: 0;
        .body-2 {
          display: inline-block;
          &:last-child {
            margin-left: 12px;
          }
        }
      }
      .location-name {
        text-align: center;
      }
    }
    .v-card__actions {
      padding-top: 0px;
    }
  }
}
</style>
