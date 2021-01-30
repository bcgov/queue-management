/**
 * Place to put all the custom utility methods
 */
import { format, parseISO } from 'date-fns'
import { utcToZonedTime, zonedTimeToUtc } from 'date-fns-tz'

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
  static convertDateToAnotherTimeZone (date, timezone) {
    const dateString = date.toLocaleString('en-US', {
      timeZone: timezone
    })
    return new Date(dateString)
  }
  static getOffsetBetweenTimezonesForDate (date, timezone1, timezone2) {
    const timezone1Date = CommonUtils.convertDateToAnotherTimeZone(date, timezone1)
    const timezone2Date = CommonUtils.convertDateToAnotherTimeZone(date, timezone2)
    return timezone1Date.getTime() - timezone2Date.getTime()
  }
  static getTzFormattedDate (date: string | Date, timezone = 'America/Vancouver', dateFormat = 'yyyy-MM-dd') {
    if (Intl.DateTimeFormat().resolvedOptions().timeZone === timezone) {
      return format(utcToZonedTime(date || new Date(), timezone), dateFormat)
    } else {
      if ((CommonUtils.getOffsetBetweenTimezonesForDate(date, Intl.DateTimeFormat().resolvedOptions().timeZone, timezone) / 60 / 1000 / 60) < 0) {
        return format(utcToZonedTime(date || new Date(), timezone), dateFormat)
      } else if ((CommonUtils.getOffsetBetweenTimezonesForDate(date, Intl.DateTimeFormat().resolvedOptions().timeZone, timezone) / 60 / 1000 / 60) > 0) {
        return format(zonedTimeToUtc(date || new Date(), timezone), dateFormat)
      }
    }
  }
  static getUTCToTimeZoneTime (date: string | Date, timezone = 'America/Vancouver', dateFormat = 'yyyy-MM-dd') {
    return format(utcToZonedTime(date || new Date(), timezone), dateFormat)
  }
  static changeDateFormat (date) {
    var pattern = /(\d{4})-(\d{2})-(\d{2})/
    if (!date || !date.match(pattern)) {
      return null
    }
    return date.replace(pattern, '$2/$3/$1')
  }
  static getTzDate (date, timezone = 'America/Vancouver') {
    return utcToZonedTime(date || new Date(), timezone)
  }

  static getFormattedDate (date, dateFormat = 'yyyy-MM-dd') {
    return format(parseISO(date || new Date().toISOString()), dateFormat)
  }

  static isAllowedIEVersion () {
    let ua = window.navigator.userAgent
    // IE 9
    // ua = 'Mozilla/5.0 (compatible; MSIE 9.0; InfoChannel RNSafeBrowser/v.1.1.0G)'

    // IE 10
    // ua = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'

    // IE 11
    // ua = 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'

    let version = 0
    let msie = ua.indexOf('MSIE ')
    if (msie > 0) {
      // IE 10 or older => return version number
      version = parseInt(ua.substring(msie + 5, ua.indexOf('.', msie)), 10)
    }

    let trident = ua.indexOf('Trident/')
    if (!version && trident > 0) {
      // IE 11 => return version number
      var rv = ua.indexOf('rv:')
      version = parseInt(ua.substring(rv + 3, ua.indexOf('.', rv)), 10)
    }
    // returning true if version is IE and greater than 11
    return (version && version < 11)
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

// https://stackoverflow.com/a/50069453
// returns e.g. "-7:00" and can be appended to end of date string
// appending timezone string is important for Safari which otherwise
// defaults to UTC
export function timezoneOffset () {
  let date = new Date()
  let timezoneOffset = date.getTimezoneOffset()
  let hours = ('00' + Math.floor(Math.abs(timezoneOffset / 60))).slice(-2)
  let minutes = ('00' + Math.abs(timezoneOffset % 60)).slice(-2)
  let string = (timezoneOffset >= 0 ? '-' : '+') + hours + ':' + minutes
  return string
}
