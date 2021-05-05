import Vue from 'vue'

export enum ShowFlagBusEvents {
    // eslint is complaining this is never used, but I see many examples of it elsewhere
    ShowFlagEvent = 'show_flag_bus',
}

export const showFlagBus = new Vue()
