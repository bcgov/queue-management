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
        v-for="location in locationListData"
        :key="location.id"
      >
        <v-card
          :disabled="location.isTemporarlyClosed"
          class="mx-auto">
          <v-card-text>
            <v-row class="d-flex" justify="space-around">
              <v-col cols="6" align-self="stretch">
                <GmapMap
                  :center="location.coordinates"
                  :zoom="14"
                  class="map-view"
                  :options="mapConfigurations"
                >
                  <GmapMarker
                    :position="location.coordinates"
                    :clickable="true"
                    :draggable="false"
                    :label='{text: location.name, fontWeight: "600"}'
                  />
                </GmapMap>
                <div class="text-center mt-2 body-2">
                  {{location.address}}
                </div>
              </v-col>
              <v-col cols="6" align-self="stretch">
                <h4 class="mb-3 location-name">
                  {{location.name}}
                  <span class="body-1 ml-2">
                  {{location.distance}}Km
                </span>
                </h4>
                <v-alert
                  dense
                  :text=(!location.isTemporarlyClosed)
                  border="left"
                  :type="(location.isTemporarlyClosed) ? 'error' : 'info'"
                  class="subtitle-2 font-weight-bold"
                  v-if="location.message"
                >
                  {{location.message}}
                </v-alert>
                <v-alert
                  type="info"
                  text
                  color="blue-grey darken-4"
                  icon="mdi-clock"
                  class="mb-0"
                >
                  <v-row no-gutters v-for="hourDay in location.hours" :key="hourDay.day">
                    <v-col cols="5" class="px-5">{{hourDay.day}}</v-col>
                    <v-col cols="7">
                      <span v-if="hourDay.isClosed" class="hours-closed">Closed</span>
                      <span v-else>
                        {{`${hourDay.startTime} - ${hourDay.endTime}`}}
                      </span>
                    </v-col>
                    <v-col class="hours-time closed" v-if="hourDay.isClosed"></v-col>
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
            >
              Select Location
              <v-icon right small class="ml-1">mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <!-- Service Model Popup -->
    <v-dialog
      v-model="locationServicesModel"
      max-width="600"
    >
      <v-card>
        <v-toolbar dark flat color="primary">
          <v-toolbar-title>Location Services for Service BC</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn icon dark @click="locationServicesModel = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <v-card-text>
          <v-row>
            <v-col>
              <v-select
                :items="categoriesList"
                label="Radius"
                outlined
                color="primary"
                class="text-left"
                v-model="selectedCategory"
                name="categories-select"
                hide-details
                dense
              >
              </v-select>
            </v-col>
            <v-col>
              <v-text-field
                prepend-inner-icon="mdi-magnify"
                type="text"
                name="search-service"
                label="Search Service"
                outlined
                hide-details
                dense
              ></v-text-field>
            </v-col>
          </v-row>
          <v-simple-table
            fixed-header
            height="300"
          >
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">Service</th>
                  <th class="text-left">Service Information</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in serviceList" :key="item.id">
                  <td>{{ item.name }}</td>
                  <td>
                    <span v-if="item.isAvailable">{{item.info}}</span>
                    <span v-else class="service-unavailable">Unavailable</span>
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-card-text>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import ConfigHelper from '@/utils/config-helper'

@Component
export default class ServiceSelection extends Vue {
  private mapConfigurations = ConfigHelper.getMapConfigurations()
  private selectedRadius = null
  private selectedCategory = null
  private radiusList = [2, 4, 6, 10]
  private categoriesList = ['Category 1', 'Category 2']
  private locationServicesModel = false

  private locationListData = [
    {
      id: 1,
      name: 'Service BC Centre Victoria(Gateway Village)',
      message: 'Hours may vary based on staff availability',
      address: '4000 Seymour Pl, Victoria, BC V8X 4S7',
      distance: '2',
      coordinates: {
        lat: 48.452540,
        lng: -123.369040
      },
      isTemporarlyClosed: false,
      hours: [
        {
          day: 'Monday',
          startTime: '9:30am',
          endTime: '4:30pm',
          isClosed: false
        },
        {
          day: 'Tuesday',
          startTime: '9:30am',
          endTime: '4:30pm',
          isClosed: false
        },
        {
          day: 'Wednesday',
          startTime: '9:30am',
          endTime: '4:30pm',
          isClosed: false
        },
        {
          day: 'Thursday',
          startTime: '9:30am',
          endTime: '4:30pm',
          isClosed: false
        },
        {
          day: 'Friday',
          startTime: '9:30am',
          endTime: '4:30pm',
          isClosed: false
        },
        {
          day: 'Saturday',
          startTime: '9:30am',
          endTime: '4:30pm',
          isClosed: true
        },
        {
          day: 'Sunday',
          startTime: '9:30am',
          endTime: '4:30pm',
          isClosed: true
        }
      ]
    }
  ]

  private serviceList = [
    {
      id: 1,
      name: 'Affordable Child Care Benefit',
      info: 'Online options available',
      isAvailable: true
    },
    {
      id: 2,
      name: 'Community Crisis Fund',
      info: 'Online options available',
      isAvailable: true
    },
    {
      id: 3,
      name: 'Identity Verification',
      info: '',
      isAvailable: false
    },
    {
      id: 4,
      name: 'Passcode Issuance',
      info: '',
      isAvailable: false
    }
  ]

  private mounted () {
  }

  private fetchLocation () {
    // eslint-disable-next-line no-console
    console.log('fetchLocation')
  }

  private showLocationServices (location) {
    this.locationServicesModel = true
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
}
.service-unavailable {
  color: $BCgovInputError;
  font-weight: 600;
}
</style>
