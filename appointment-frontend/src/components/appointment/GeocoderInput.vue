<template>
  <v-autocomplete
    type="text"
    name="address"
    label="Start Typing Your City Here...."
    outlined
    hide-details
    dense
    v-model="model"
    :search-input.sync="search"
    no-filter
    :items="results"
    item-text="name"
    item-value="coords"
    v-on:change='onAddressSelection'
    return-object
    :loading='isLoading'
    color="blue darken-2"
  >
    <template v-slot:append>
      <v-btn
        text
        icon
        @click="fetchLocation"
      >
        <v-icon
          color="blue darken-2"
          >
          mdi-map-marker-radius
        </v-icon>
      </v-btn>
    </template>
  </v-autocomplete>
</template>

<script lang="ts">
/* eslint-disable no-console */
/* eslint-disable sort-imports */
import { Component, Vue, Watch } from 'vue-property-decorator'
import { GeolocatorSuccess } from '@/models/geo'
import { locationBus, locationBusEvents } from '@/events/locationBus'
import { mapActions } from 'vuex'
import { GeoModule } from '@/store/modules'
import GeocoderService from '@/services/geocoder.services'
import { debounce } from '@/utils/common-util'
import { getModule } from 'vuex-module-decorators'

@Component({
  methods: {
    ...mapActions('geo', [
      'getCurrentLocation'
    ])
  }
})
export default class GeocoderInput extends Vue {
  private geoModule = getModule(GeoModule, this.$store)
  private results = []
  private isLoading = false
  private model = null
  private search = null;
  private debouncedSearch: (value: string, oldValue: string) => void
  private readonly getCurrentLocation!: () => Promise<GeolocatorSuccess>
  private async created () {
    locationBus.$on(locationBusEvents.ClosestLocationEvent, () =>
      this.fetchLocation()
    )
  }

  constructor () {
    super()
    // Only trigger search after user has stopped typing for 250ms
    this.debouncedSearch = debounce(this.handleSearchUpdate, 250, undefined)
  }

  @Watch('search')
  async onSearchChanged (value: string, oldValue: string) {
    this.isLoading = true
    this.debouncedSearch(value, oldValue)
  }

  async handleSearchUpdate (value: string, oldValue: string) {
    const res = await GeocoderService.lookup(value)
    this.isLoading = false
    this.results = (res as any)
  }

  async onAddressSelection (address) {
    const selectedAddress = {
      latitude: address.coords.latitude,
      longitude: address.coords.longitude
    }
    this.$store.commit('geo/setCurrentLocation', selectedAddress)

    // Due to Vue rendering, we must call this event to trigger a UI update.
    this.$emit('set-location-event', selectedAddress)
  }

  private async fetchLocation () {
    this.isLoading = true
    const geo = await this.getCurrentLocation()
    this.isLoading = false
    this.$emit('set-location-event', {
      latitude: (geo as any).latitude,
      longitude: (geo as any).longitude
    })
  }
}
</script>

<style lang="scss" scope>
// empty block
</style>
