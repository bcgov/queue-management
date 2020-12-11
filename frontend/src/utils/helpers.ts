import moment from 'moment'

const rounded = (time, inteval = 15) => Math.round(moment(time).minute() / inteval) * inteval
const roundedDown = (time, inteval = 15) => Math.floor(moment(time).minute() / inteval) * inteval
const roundedUp = (time, inteval = 15) => Math.ceil(moment(time).minute() / inteval) * inteval

const roundedDownTime = (time, inteval = 15) => {
    const roundedMinut = roundedDown(time, inteval)
    return { hour: moment(time).hour(), minute: roundedMinut }
}

const formatedStartTime = (date, time) => {
    const selectedTime = moment(`${date} ${time}`)// event.start.clone()
    const { hour, minute } = roundedDownTime(selectedTime) // roundingdown  time to 15 min inteval
    const roundTime = moment(date).set({ hour, minute })

    return roundTime
}

export {
    rounded,
    roundedDown,
    roundedUp,
    roundedDownTime,
    formatedStartTime
}
