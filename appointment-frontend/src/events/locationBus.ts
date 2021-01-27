import Vue from 'vue'

export enum locationBusEvents {
  ClosestLocationEvent = 'closest_location_event',
}

export const locationBus = new Vue()
