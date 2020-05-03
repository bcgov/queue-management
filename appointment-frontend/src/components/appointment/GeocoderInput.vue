<template>
  <v-row justify="end">
     <v-progress-circular
      v-if='isLoading'
      indeterminate
      :width="5"
      color="primary"
    ></v-progress-circular>
    <v-autocomplete
            append-icon="mdi-map-marker-radius"
            type="text"
            name="address"
            label="Address"
            outlined
            hide-details
            class="map-address-input"
            dense

            @click:append="fetchLocation"

            v-model="model"
            :search-input.sync="search"
            cache-items
            :items="results"
            item-text="name"
            item-value="coords"
            v-on:change='onAddressSelection'
            return-object
    ></v-autocomplete>
  </v-row>
  <!-- TODO - NOt sure fetchLocation above is working, may need to separate to separate icon -->
          <!-- @click:append="fetchLocation" -->
</template>

<script lang="ts">
/* eslint-disable no-console */
import { Component, Mixins, Prop, Vue, Watch } from 'vue-property-decorator'
import { GeolocatorSuccess, LatLng } from '@/models/geo'
import { mapActions, mapState } from 'vuex'
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
// @import "@/assets/scss/theme.scss";
.map-address-input {
  max-width: calc(100% - 100px);
}
</style>
