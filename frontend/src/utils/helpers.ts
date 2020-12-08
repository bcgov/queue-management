import moment from 'moment'

const rounded = (time, inteval = 15) => Math.round(moment(time).minute() / inteval) * inteval
const roundedDown = (time, inteval = 15) => Math.floor(moment(time).minute() / inteval) * inteval
const roundedUp = (time, inteval = 15) => Math.ceil(moment(time).minute() / inteval) * inteval

const roundedDownTime = (time, inteval = 15) => {
    const roundedMinut = roundedDown(time, inteval)
    return `${moment(time).hour()}:${roundedMinut}`
}

const formatedStartTime = (date, time) => {
    const selectedTime = moment(`${date} ${time}`)// event.start.clone()
    const roundedTime = roundedDownTime(selectedTime) // roundingdown  time to 15 min inteval

    const roundTime = moment(`${date} ${roundedTime}`)
    return roundTime
}

export {
    rounded,
    roundedDown,
    roundedUp,
    roundedDownTime,
    formatedStartTime
}
