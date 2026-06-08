import { describe, expect, it } from 'vitest'
import { mapApiOfficesToVisibleLocations, type OfficeApiModel } from './service-locations'

describe('mapApiOfficesToVisibleLocations', () => {
  it('excludes offices where online_status is HIDE or Status.HIDE', () => {
    const offices: OfficeApiModel[] = [
      {
        office_id: 1,
        office_name: 'Visible Office',
        online_status: 'SHOW',
        appointments_enabled_ind: 1,
      },
      {
        office_id: 2,
        office_name: 'Hidden Office',
        online_status: 'HIDE',
        appointments_enabled_ind: 1,
      },
      {
        office_id: 3,
        office_name: 'Hidden Enum Office',
        online_status: 'Status.HIDE',
        appointments_enabled_ind: 1,
      },
    ]

    const locations = mapApiOfficesToVisibleLocations(offices)

    expect(locations).toHaveLength(1)
    expect(locations[0].officeId).toBe(1)
    expect(locations[0].name).toBe('Service BC - Visible Office')
  })
})
