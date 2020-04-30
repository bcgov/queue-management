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
import { mapActions, mapState } from 'vuex'
import GeocoderService from '@/services/geocoder.services'
import { LatLng } from '@/models/geo'
import { debounce } from '@/utils/common-util'

@Component({
  methods: {
    ...mapActions('geo', [
      'getCurrentLocation'
    ])
  }
})
export default class GeocoderInput extends Vue {
  private results = []
  private isLoading = false
  private model = null
  private search = null;
  private debouncedSearch: (value: string, oldValue: string) => void

  constructor () {
    super()
    // Only trigger search after user has stopped typing for 250ms
    this.debouncedSearch = debounce(this.handleSearchUpdate, 250)
  }

  @Watch('search')
  async onSearchChanged (value: string, oldValue: string) {
    this.isLoading = true
    this.debouncedSearch(value, oldValue)
  }

  async handleSearchUpdate (value: string, oldValue: string) {
    const res = await GeocoderService.lookup(value)
    this.isLoading = false
    this.results = res
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
    // TODO - Potentially enable spinner / loading icon at this point
    this.isLoading = true
    const geo = await this.getCurrentLocation()
    this.isLoading = false
    this.$emit('set-location-event', {
      latitude: geo.latitude,
      longitude: geo.longitude
    })
  }
}
</script>

<style lang="scss" scope>
// @import "@/assets/scss/theme.scss";
.v-input.v-autocomplete {
  max-width: calc(100% - 100px);
}
</style>
