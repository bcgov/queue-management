import Vue from 'vue'

export enum APIProgressBusEvents {
    // eslint is complaining this is never used, but I see many examples of it elsewhere
    APIProgressEvent = 'api_progress_bus',
}

export const apiProgressBus = new Vue()
