import Axios, { AxiosResponse } from 'axios'
import { GeolocatorSuccess, LatLng } from '@/models/geo'
import { Office } from '@/models/office'
import { addAxiosInterceptors } from '@/utils/interceptors'

const axios = addAxiosInterceptors(Axios.create())

export interface GeoAddressResult {
  name: string,
  coords: LatLng
}

const BASE_URL = 'https://geocoder.api.gov.bc.ca'
const ADDRESS_URL = `${BASE_URL}/addresses.json?`

export default class GeocoderService {
  public static async lookup (address: string): Promise<AxiosResponse<GeoAddressResult[]>> {
    const params = {
      minScore: 50,
      maxResults: 10,
      echo: true,
      interpolation: 'adaptive',
      addressString: address,
      autoComplete: true,
      matchPrecisionNot: 'street'

    }

    const response = await axios.get(ADDRESS_URL, { params })
    // Strip out useless data
    // Convert response into array of
    // {name: string, coords: lat/lng}
    return response?.data?.features?.map(item => {
      return {
        name: item.properties.fullAddress,
        coords: {
          latitude: item.geometry.coordinates[1],
          longitude: item.geometry.coordinates[0]
        }
      }
    })
  }

  public static async getCurrentLocation (): Promise<GeolocatorSuccess> {
    const options = {
      enableHighAccuracy: true,
      timeout: 15000,
      maximumAge: 0
    }

    return new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition((pos: GeolocatorSuccess) => {
        resolve(pos)
      }, (error) => {
        reject(error)
      }, options)
    })
  }

  public static distance (origin: LatLng, destination: LatLng) {
    return GeocoderService.distanceSplit(origin.latitude, origin.longitude, destination.latitude, destination.longitude)
  }

  // https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
  public static distanceSplit (lat1, lon1, lat2, lon2) {
    const p = 0.017453292519943295 // Math.PI / 180
    const c = Math.cos
    const a = 0.5 - c((lat2 - lat1) * p) / 2 +
            c(lat1 * p) * c(lat2 * p) *
            (1 - c((lon2 - lon1) * p)) / 2

    return 12742 * Math.asin(Math.sqrt(a)) // 2 * R; R = 6371 km
  }
}
