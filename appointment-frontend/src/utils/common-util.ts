/**
 * Place to put all the custom utility methods
 */
export default class CommonUtils {
  // get Day of the week by its index
  static getDayOfWeek (dayIndex: number) {
    enum Days {
      Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday
    }
    return Days[dayIndex]
  }
  // convert time string to AM/PM format
  static get12HTimeString (timeString) {
    const H = +timeString.substr(0, 2)
    return ((H % 12) || 12) + timeString.substr(2, 3) + (H < 12 ? 'AM' : 'PM')
  }
}
