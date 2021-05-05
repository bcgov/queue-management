import Vue from 'vue'

export enum ShowBookingFlagBusEvents {
    // eslint is complaining this is never used, but I see many examples of it elsewhere
    ShowBookingFlagEvent = 'show_booking_flag_bus',
}

export const showBookingFlagBus = new Vue()
