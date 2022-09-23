/**
 * Place to put all the custom utility methods
 */
import { format, parseISO } from 'date-fns'
import { utcToZonedTime, zonedTimeToUtc } from 'date-fns-tz'
import { TimeSlots } from '../models/office'

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
  static getFormattedTimeslots (timeslots: TimeSlots[]) {
    const timeslotArray = []
    // this loop will get the minimum start time and maximum end time of a timeslot
    timeslots.forEach(timeslot => {
      timeslot.dayOfWeek.forEach(day => {
        if (timeslotArray[Days[day]]) {
          if (!this.compareTime(timeslotArray[Days[day]].startTime, timeslot.startTime)) {
            timeslotArray[Days[day]].startTime = timeslot.startTime
          }
          if (this.compareTime(timeslotArray[Days[day]].endTime, timeslot.endTime)) {
            timeslotArray[Days[day]].endTime = timeslot.endTime
          }
        } else {
          timeslotArray[Days[day]] = {
            startTime: timeslot.startTime,
            endTime: timeslot.endTime
          }
        }
      })
    })
    let index = 1
    const returnArray = []
    // this loop will map the time with the Days enum
    do {
      const timeslot = timeslotArray[index]
      returnArray.push({
        ...timeslot,
        dayStr: this.getDayOfWeek(index),
        endTimeStr: (timeslot?.endTime) ? this.get12HTimeString(timeslot.endTime) : '',
        startTimeStr: (timeslot?.startTime) ? this.get12HTimeString(timeslot.startTime) : ''
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
      } else {
        return CommonUtils.getUTCToTimeZoneTime(date, timezone, dateFormat)
      }
    }
  }

  static getUTCToTimeZoneTime (date: string | Date, timezone = 'America/Vancouver', dateFormat = 'yyyy-MM-dd') {
    return format(utcToZonedTime(date || new Date(), timezone), dateFormat)
  }

  static changeDateFormat (date) {
    const pattern = /(\d{4})-(\d{2})-(\d{2})/
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

  static getBrowser () {
    const ua = navigator.userAgent
    let tem = []
    let M = ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || []
    if (/trident/i.test(M[1])) {
      tem = /\brv[ :]+(\d+)/g.exec(ua) || []
      return { name: 'IE', version: (tem[1] || '') }
    }
    if (M[1] === 'Chrome') {
      tem = ua.match(/\bOPR|Edge\/(\d+)/)
      if (tem != null) { return { name: 'Opera', version: tem[1] } }
    }
    M = M[2] ? [M[1], M[2]] : [navigator.appName, navigator.appVersion, '-?']
    if ((tem = ua.match(/version\/(\d+)/i)) != null) { M.splice(1, 1, tem[1]) }
    return {
      name: M[0],
      version: M[1]
    }
  }

  static isAllowedBrowsers () {
    const allowedBrowerNLowestVersion = { 'Chrome': [24], 'Firefox': [29], 'Safari': [10], 'Opera': [15] }
    if (allowedBrowerNLowestVersion.hasOwnProperty(CommonUtils.getBrowser()['name'])) {
      if (Number(CommonUtils.getBrowser()['version']) >= allowedBrowerNLowestVersion[CommonUtils.getBrowser()['name']]) {
        return {
          'isAllowed': true,
          'currentBrowser': CommonUtils.getBrowser()['name'],
          'currentVersion': CommonUtils.getBrowser()['version'],
          'allowedBrowsers': 'Chrome, Firefox, Safari, Edge'
        }
      }
    }
    return {
      'isAllowed': false,
      'currentBrowser': CommonUtils.getBrowser()['name'],
      'currentVersion': CommonUtils.getBrowser()['version'],
      'allowedBrowsers': 'Chrome >= 24, Firefox >= 29, Safari >= 10, Opera >= 15'
    }
  }

  static isAllowedIEVersion () {
    const ua = window.navigator.userAgent
    let version = 0
    const msie = ua.indexOf('MSIE ')
    if (msie > 0) {
      // IE 10 or older => return version number
      version = parseInt(ua.substring(msie + 5, ua.indexOf('.', msie)), 10)
    }

    const trident = ua.indexOf('Trident/')
    if (!version && trident > 0) {
      // IE 11 => return version number
      const rv = ua.indexOf('rv:')
      version = parseInt(ua.substring(rv + 3, ua.indexOf('.', rv)), 10)
    }
    // returning true if version is IE and greater than 11
    return (version && version < 11)
  }

  static getUserAgent (): string {
    const userAgent: string = window.navigator.userAgent
    const osBeginIndex = userAgent.indexOf('(')
    const osEndIndex = userAgent.indexOf(')')
    const os = '[' + userAgent.substring(osBeginIndex + 1, osEndIndex) + ']'
    let browser = ''
    let version = ''
    let lowercaseUserAgent: string = userAgent.toLowerCase()
    if (lowercaseUserAgent.indexOf('opera') !== -1) {
      browser = 'Opera'
      const versionIndex = lowercaseUserAgent.indexOf('opera/')
      const versionString = lowercaseUserAgent.substring(versionIndex + 6)
      const versionarray = versionString.split(' ')
      version = 'v' + versionarray[0]
    } else if (lowercaseUserAgent.indexOf('edg') !== -1) {
      browser = 'Edge'
      const versionIndex = lowercaseUserAgent.indexOf('edg/')
      const versionString = lowercaseUserAgent.substring(versionIndex + 4)
      const versionarray = versionString.split(' ')
      version = 'v' + versionarray[0]
    } else if (lowercaseUserAgent.indexOf('chrome') !== -1) {
      browser = 'Chrome'
      const versionIndex = lowercaseUserAgent.indexOf('chrome/')
      const versionString = lowercaseUserAgent.substring(versionIndex + 7)
      const versionarray = versionString.split(' ')
      version = 'v' + versionarray[0]
    } else if (lowercaseUserAgent.indexOf('firefox') !== -1) {
      browser = 'Firefox'
      const versionIndex = lowercaseUserAgent.indexOf('firefox/')
      const versionString = lowercaseUserAgent.substring(versionIndex + 8)
      const versionarray = versionString.split(' ')
      version = 'v' + versionarray[0]
    } else if (lowercaseUserAgent.indexOf('safari') !== -1) {
      browser = 'Safari'
      const versionIndex = lowercaseUserAgent.indexOf('safari/')
      const versionString = lowercaseUserAgent.substring(versionIndex + 7)
      const versionarray = versionString.split(' ')
      version = 'v' + versionarray[0]
    } else {
      browser = 'Unknown'
      version = 'Not Applicable'
    }
    return 'OS: ' + os + ' Browser: ' + browser + ' ' + version
  }
}

export function debounce (func, wait, immediate) {
  let timeout
  return function () {
    const context = this; const args = arguments
    const later = function () {
      timeout = null
      if (!immediate) func.apply(context, args)
    }
    const callNow = immediate && !timeout
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
    if (callNow) func.apply(context, args)
  }
}

// https://stackoverflow.com/a/50069453
// returns e.g. "-7:00" and can be appended to end of date string
// appending timezone string is important for Safari which otherwise
// defaults to UTC
export function timezoneOffset () {
  const date = new Date()
  const timezoneOffset = date.getTimezoneOffset()
  const hours = ('00' + Math.floor(Math.abs(timezoneOffset / 60))).slice(-2)
  const minutes = ('00' + Math.abs(timezoneOffset % 60)).slice(-2)
  return (timezoneOffset >= 0 ? '-' : '+') + hours + ':' + minutes
}
