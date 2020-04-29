import Axios, { AxiosResponse } from 'axios'
import { GeolocatorSuccess, LatLng } from '@/models/geo'
import { addAxiosInterceptors } from '@/utils/interceptors'

const axios = addAxiosInterceptors(Axios.create())

export interface GeoAddressResult {
  /** String from the API that includes street, city, province, and country. */
  fullAddress: string;
  city: string;
  street: string;
  // Set to defaults in response
  country: string;
  province: string;
}

const BASE_URL = 'https://geocoder.api.gov.bc.ca'
const ADDRESS_URL = `${BASE_URL}/addresses.json?`

export default class GeocoderService {
  // protecteds _headers: HttpHeaders = new HttpHeaders();
  // protected BASE_URL = 'https://geocoder.api.gov.bc.ca';
  // protected ADDRESS_URL = `${this.BASE_URL}/addresses.json?`;

  // https://github.com/bcgov/api-specs/blob/master/geocoder/geocoder-developer-guide.md
  // lookupOLD(address: string): Observable<GeoAddressResult[]> {
  //     const params = new HttpParams()
  //         .set('minScore', '50')
  //         .set('maxResults', '10')
  //         .set('echo', 'true')
  //         .set('interpolation', 'adaptive')
  //         .set('addressString', address);

  //     return this.get(this.ADDRESS_URL, params).pipe(map(this.processResponse));
  // }

  public static async lookup (address: string): Promise<AxiosResponse<GeoAddressResult[]>> {
    // return axios.post(`${ConfigHelper.getAppAPIUrl()}/users/`, {})
    const params = {
      minScore: 50,
      maxResults: 10,
      echo: true,
      interpolation: 'adaptive',
      addressString: address
    }

    return axios.get(ADDRESS_URL, { params })
  }

  public static async getCurrentLocation (): Promise<GeolocatorSuccess> {
    // eslint-disable-next-line no-console
    console.log('geocoder service, getCurrentLocation called')
    const options = {
      enableHighAccuracy: true,
      timeout: 5000,
      maximumAge: 0
    }

    // const authModule = getModule(AuthModule, this.store)

    return new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition((pos: GeolocatorSuccess) => {
        // eslint-disable-next-line no-console
        console.log('success', pos)
        // TODO - NEED TO STORE IT TOO
        resolve(pos)
      }, (error) => {
        // eslint-disable-next-line no-console
        console.log('error', error)
        reject(error)
      }, options)
    })
  }

  public static distance (origin: LatLng, destination: LatLng) {
    return GeocoderService.distanceSplit(origin.latitude, origin.longitude, destination.latitude, destination.longitude)
  }

  // https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
  // public static distance (lat1, lon1, lat2, lon2) {
  public static distanceSplit (lat1, lon1, lat2, lon2) {
    var p = 0.017453292519943295 // Math.PI / 180
    var c = Math.cos
    var a = 0.5 - c((lat2 - lat1) * p) / 2 +
            c(lat1 * p) * c(lat2 * p) *
            (1 - c((lon2 - lon1) * p)) / 2

    return 12742 * Math.asin(Math.sqrt(a)) // 2 * R; R = 6371 km
  }
}
