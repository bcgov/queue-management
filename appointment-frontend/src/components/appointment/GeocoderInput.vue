<template>
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
          :items="results"
          item-text="name"
          item-value="coords"
          v-on:change='onAddressSelection'
          return-object
  ></v-autocomplete>
  <!-- TODO - NOt sure fetchLocation above is working, may need to separate to separate icon -->
          <!-- @click:append="fetchLocation" -->
</template>

<script lang="ts">
/* eslint-disable no-console */
import { Component, Mixins, Prop, Vue, Watch } from 'vue-property-decorator'
import { mapActions, mapState } from 'vuex'
import GeocoderService from '@/services/geocoder.services'
import { LatLng } from '@/models/geo'

@Component({
  methods: {
    ...mapActions('geo', [
      'getCurrentLocation'
    ])
  }
})
export default class GeocoderInput extends Vue {
  // private descriptionLimit = 60
  private results = []
  private isLoading = false
  private model = null
  private search = null;

  @Watch('search')
  async onSearchChanged (value: string, oldValue: string) {
    // console.log('search', value)
    const res = await GeocoderService.lookup(value)
    // console.log('lookup res', { res })
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
    const geo = await this.getCurrentLocation()
    this.$emit('set-location-event', {
      latitude: geo.latitude,
      longitude: geo.longitude
    })
  }
}
</script>

<style lang="scss" scope>
// @import "@/assets/scss/theme.scss";
</style>
