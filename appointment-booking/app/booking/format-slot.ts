// Shared appointment date/time labels (callout summary and datetime picker).
import { CalendarDateTime, toZoned } from '@internationalized/date'

export function formatDate(date: string) {
  const [year, month, day] = date.split('-').map(Number)
  return new Intl.DateTimeFormat('en-CA', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
    year: 'numeric',
  }).format(new Date(year, month - 1, day))
}

function formatTime(time: string) {
  const [hour, minute] = time.split(':').map(Number)
  return new Intl.DateTimeFormat('en-CA', {
    hour: 'numeric',
    minute: '2-digit',
  }).format(new Date(2000, 0, 1, hour, minute))
}

export function formatTimeRange(startTime: string, endTime: string) {
  return `${formatTime(startTime)} – ${formatTime(endTime)}`
}

// Slot HH:MM values from the API are office-local, not the browser timezone.
export function officeWallTimeToIso(date: string, time: string, timezoneName: string): string {
  const [year, month, day] = date.split('-').map(Number)
  const [hour, minute] = time.split(':').map(Number)
  // toString includes "[America/Vancouver]"; the API wants plain ISO-8601.
  return toZoned(new CalendarDateTime(year, month, day, hour, minute), timezoneName)
    .toString()
    .replace(/\[.*\]$/, '')
}
