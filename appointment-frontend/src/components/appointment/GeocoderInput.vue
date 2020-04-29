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
    // ...mapState('geo', {
    //   // eslint-disable-next-line
    //   coords: state => state.currentCoordinates
    // })
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
    console.log('onAddressSelection', address, { coords: address.coords.latitude })
    // const selectedAddress: LatLng = await address.coordinates
    // console.log('geo/setCurrentLocation', { address, selectedAddress, model: this.model.coordinates })
    const selectedAddress = { latitude: address.coords.latitude, longitude: address.coords.longitude }
    console.log('geo/setCurrentLocation', { address, selectedAddress })
    this.$store.commit('geo/setCurrentLocation', selectedAddress)

    // PROBLEM - This forceUpdate does not cause parent to update UI
    // If you cause a hotreload of a component it does update though
    // and data is in store according to Vuex
    this.$forceUpdate()
  }

  private async fetchLocation () {
    // TODO - Potentially enable spinner / loading icon at this point
    console.log('fetching location')
    const geo = await this.getCurrentLocation()
    console.log('fetchLocation', { geo })
    // this.$forceUpdate()
  }

  // TODO - On selection, update geostore's currentCoordinates lat/lng
}
</script>

<style lang="scss" scope>
// @import "@/assets/scss/theme.scss";
</style>
