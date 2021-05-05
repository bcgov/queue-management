/* eslint-disable indent */

import moment from 'moment'
import tZone from 'moment-timezone'

export const makeBookingReqObj = (context, responses) => {
    const timezoneName: any = context.state.user.office.timezone

    //  NOTE!!!!  The following lines of code are to allow booking an ITA individual exam
    //            when both the ITA liaison flag and Pesticide liaison flags are false.
    //            If both flags are false, then there are no offices, so the .find statement
    //            doesn't work.  In this case, set the booking office to be the CSR office
    //            This is NOT really how this should be done, but time is tight, as always.
    let bookingOffice: any = null
    if (context.state.offices.length === 0) {
        bookingOffice = context.state.user.office
    } else {
        bookingOffice = context.state.offices.find(
            office => office.office_id === responses.office_id
        )
    }
    const bookingTimezoneName: any = bookingOffice.timezone.timezone_name
    // JSTOTS TOCHECK removed new from moment. no need to use new with moment
    const date = moment(responses.expiry_date).format('YYYY-MM-DD')
    // JSTOTS TOCHECK removed new from moment. no need to use new with moment
    const time = moment(responses.exam_time).format('HH:mm:ss')
    const datetime = date + 'T' + time
    let start
    if (bookingTimezoneName !== timezoneName) {
        start = tZone.tz(datetime, bookingTimezoneName)
    } else {
        // JSTOTS TOCHECK removed new from moment. no need to use new with moment
        start = moment(datetime).local()
    }
    const length = context.state.examTypes.find(
        (ex: any) => ex.exam_type_id === responses.exam_type_id
    ).number_of_hours
    const end = start.clone().add(length, 'hours')
    const booking: any = {
        start_time: start
            .clone()
            .utc()
            .format('YYYY-MM-DD[T]HH:mm:ssZ'),
        end_time: end
            .clone()
            .utc()
            .format('YYYY-MM-DD[T]HH:mm:ssZ'),
        fees: 'false',
        booking_name: responses.exam_name,
        office_id: responses.office_id
    }
    if (
        responses.is_pesticide &&
        !responses.sbc_managed_ind &&
        responses.invigilator_id
    ) {
        booking.invigilator_id = [responses.invigilator_id]
    }
    return booking
}
