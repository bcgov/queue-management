import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators'
import GeocoderService from '@/services/geocoder.services'
import { LatLng } from '@/models/geo'

@Module({
  name: 'geo',
  namespaced: true
})
export default class GeoModule extends VuexModule {
  currentCoordinates: LatLng

  /**
    Mutations in this Module
  **/

  @Mutation
  public setCurrentLocation (currentCoordinates: LatLng) {
    // Need to break out into line for vuex persistence
    this.currentCoordinates = {
      latitude: currentCoordinates.latitude,
      longitude: currentCoordinates.longitude
    }
  }

  /**
    Actions in this Module
  **/

  @Action({ commit: 'setCurrentLocation', rawError: true })
  public async getCurrentLocation () {
    const response = await GeocoderService.getCurrentLocation()
    return response.coords
  }
}
