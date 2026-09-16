/* eslint-env jest */
import { isPastOfficeTime, officeNow } from '../../src/utils/office-time'
import moment from 'moment'

const office = (offset: number) => ({
  timezone: {
    clock_offsets: [{
      start: '2026-03-08T10:00:00Z', end: '2028-01-01T00:00:00Z', offset_seconds: offset
    }]
  }
})

// Execute this suite under different TZ values; calendar objects must retain
// their displayed wall time regardless of the runtime's UTC offset.
test('remote browser accepts a future office slot and rejects a past one', () => {
  const now = Date.parse('2026-09-09T16:00:00Z') // Vancouver 09:00
  expect(isPastOfficeTime(moment('2026-09-09T10:00:00'), office(-25200), undefined, now)).toBe(false)
  expect(isPastOfficeTime(new Date('2026-09-09T08:59:00'), office(-25200), undefined, now)).toBe(true)
})

test('office date differs at the same instant in Cranbrook and Creston', () => {
  const now = Date.parse('2026-11-03T06:30:00Z')
  expect(officeNow(office(-25200), now).format('YYYY-MM-DD HH:mm')).toBe('2026-11-02 23:30')
  expect(officeNow(office(-21600), now).format('YYYY-MM-DD HH:mm')).toBe('2026-11-03 00:30')
  expect(isPastOfficeTime('2026-11-02T09:00:00', office(-25200), 'day', now)).toBe(false)
  expect(isPastOfficeTime('2026-11-02T09:00:00', office(-21600), 'day', now)).toBe(true)
})

test('cached periods select the new offset at the exact transition', () => {
  const vancouver = office(-25200)
  vancouver.timezone.clock_offsets.unshift({
    start: '2026-01-01T00:00:00Z',
    end: '2026-03-08T10:00:00Z',
    offset_seconds: -28800
  })
  expect(officeNow(vancouver, Date.parse('2026-03-08T09:59:59Z')).format('HH:mm:ss')).toBe('01:59:59')
  expect(officeNow(vancouver, Date.parse('2026-03-08T10:00:00Z')).format('HH:mm:ss')).toBe('03:00:00')
})

test('missing clock data never falls back to browser time for scheduling', () => {
  expect(isPastOfficeTime('2026-11-02T09:00:00', {}, undefined, Date.parse('2026-11-02T15:00:00Z'))).toBe(true)
})
