import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators'
import { GeolocatorSuccess, LatLng } from '@/models/geo'
import GeocoderService from '@/services/geocoder.services'
import { store } from '@/store'

@Module({
  name: 'appointment',
  namespaced: true,
  store,
  dynamic: true
})
export default class GeoModule extends VuexModule {
  currentCoordinates: LatLng // TODO - TYPE

  /**
    Mutations in this Module
  **/

  @Mutation
  public setCurrentLocation (currentCoordinates: LatLng) {
    this.currentCoordinates = currentCoordinates
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
