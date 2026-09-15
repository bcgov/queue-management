import Vue from 'vue'
import moment from 'moment'

// Keep computed Today/status displays fresh in tabs left open overnight.
const clock = Vue.observable({ tick: 0 })
if (typeof window !== 'undefined') {
  window.setInterval(() => { clock.tick += 1 }, 60000)
}

// UTC-mode Moments here are comparable wall-clock values, not UTC instants.
// The API supplies the offset periods from its pinned database, including
// transitions. Never consult the browser's time zone to obtain office "now".
export function officeNow (office: any, instant = Date.now()) {
  // Establish a reactive dependency while still reading exact time on each call.
  // eslint-disable-next-line no-void
  void clock.tick
  const periods = office?.timezone?.clock_offsets || []
  const period = periods.find(p => Date.parse(p.start) <= instant && instant < Date.parse(p.end))
  return period
    ? moment.utc(instant).add(period.offset_seconds, 'seconds')
    : moment.invalid()
}

export function officeWallTime (value: any) {
  // Calendar widgets already carry office wall time in browser-local objects.
  // Preserve their displayed fields instead of interpreting them as instants.
  if (value == null || value === '') return moment.invalid()
  return moment.utc(moment.isMoment(value) || value instanceof Date
    ? moment(value).format('YYYY-MM-DD[T]HH:mm:ss.SSS')
    : value)
}

export function isPastOfficeTime (value: any, office: any, unit?: 'day', instant = Date.now()) {
  const now = officeNow(office, instant)
  const wallTime = officeWallTime(value)
  return !now.isValid() || !wallTime.isValid() || wallTime.isBefore(now, unit)
}
