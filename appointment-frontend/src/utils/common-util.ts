/**
 * Place to put all the custom utility methods
 */
import { format, parseISO } from 'date-fns'
import { utcToZonedTime } from 'date-fns-tz'

export enum Days {
  Monday = 1, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
}
export default class CommonUtils {
  /***
   * get Day of the week by its index
   ***/
  static getDayOfWeek (dayIndex: number) {
    return Days[dayIndex]
  }

  /***
   * convert time string to AM/PM format
   ***/
  static get12HTimeString (timeString) {
    const H = +timeString.substr(0, 2)
    return ((H % 12) || 12) + timeString.substr(2, 3) + (H < 12 ? 'AM' : 'PM')
  }

  /***
   * checks for time1 greater than time2
   ***/
  static compareTime (time1, time2) {
    return parseInt(time1.split(':').join('')) < parseInt(time2.split(':').join(''))
  }

  /***
   * Time slots formatted in a way it should need to display in the UI
   ***/
  static getFormattedTimeslots (timeslots) {
    let timeslotArray = []
    // this loop will get the minimum start time and maximum end time of a timeslot
    timeslots.forEach(timeslot => {
      timeslot.day_of_week.forEach(day => {
        if (timeslotArray[Days[day]]) {
          if (!this.compareTime(timeslotArray[Days[day]].startTime, timeslot.start_time)) {
            timeslotArray[Days[day]].startTime = timeslot.start_time
          }
          if (this.compareTime(timeslotArray[Days[day]].endTime, timeslot.end_time)) {
            timeslotArray[Days[day]].endTime = timeslot.end_time
          }
        } else {
          timeslotArray[Days[day]] = {
            startTime: timeslot.start_time,
            endTime: timeslot.end_time
          }
        }
      })
    })
    let index = 1
    let returnArray = []
    // this loop will map the time with the Days enum
    do {
      const timeslot = timeslotArray[index]
      returnArray.push({
        ...timeslot,
        day_str: this.getDayOfWeek(index),
        end_time_str: (timeslot?.endTime) ? this.get12HTimeString(timeslot.endTime) : '',
        start_time_str: (timeslot?.startTime) ? this.get12HTimeString(timeslot.startTime) : ''
      })
      index++
    } while (index <= (Object.keys(Days).length / 2))
    return returnArray
  }

  static getTzFormattedDate (date, timezone = 'America/Vancouver', dateFormat = 'yyyy-MM-dd') {
    return format(utcToZonedTime(date || new Date(), timezone), dateFormat)
  }

  static getTzDate (date, timezone = 'America/Vancouver') {
    return utcToZonedTime(date || new Date(), timezone)
  }

  static getFormattedDate (date, dateFormat = 'yyyy-MM-dd') {
    return format(parseISO(date || new Date().toISOString()), dateFormat)
  }
}

export function debounce (func, wait, immediate) {
  var timeout
  return function () {
    var context = this; var args = arguments
    var later = function () {
      timeout = null
      if (!immediate) func.apply(context, args)
    }
    var callNow = immediate && !timeout
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
    if (callNow) func.apply(context, args)
  }
};
