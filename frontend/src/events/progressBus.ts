import Vue from 'vue'

export enum APIProgressBusEvents {
    APIProgressEvent = 'api_progress_bus',
}

export const apiProgressBus = new Vue()
