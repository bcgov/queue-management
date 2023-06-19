// Copyright 2022 Province of British Columbia
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may not
// use this file except in compliance with the License. You may obtain a copy of
// the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations under
// the License.

/// <reference types='cypress' />
/// <reference types='cypress-image-snapshot' />

import {
  SELECTOR_APPOINTMENT_CANCEL_CANCEL_APPOINTMENT,
  SELECTOR_APPOINTMENT_CANCEL_CANCEL_CONFIRM,
  SELECTOR_APPOINTMENT_CANCEL_NAV_APPOINTMENTS,
  SELECTOR_APPOINTMENT_CANCEL_USER_NAV,
  SELECTOR_APPOINTMENT_NO_APPOINTMENTS,
  SELECTOR_FEEDBACK,
  SELECTOR_HEADER_IMAGE_BCGOV
} from '../../support/selectors'

import { API_PREFIX } from '../../support/e2e'

describe('Cancel Appointment', () => {
  beforeEach(() => {
    // Intercept API calls to provide testing data.
    cy.fixture('offices.json').then((json) => {
      cy.intercept('GET', API_PREFIX + 'offices/', json).as('getOffices')
    })

    cy.fixture('services/appointment_cancel.json').then((json) => {
      cy.intercept('GET', API_PREFIX + 'services', json).as('getServices')
    })

    cy.fixture('users/appointments/appointment_cancel.json').then((json) => {
      cy.intercept('GET', API_PREFIX + 'users/appointments', json).as('getAppointments')
    })

    cy.fixture('users/me').then((json) => {
      cy.intercept('GET', API_PREFIX + 'users/me', json)
    })

    cy.intercept('DELETE', API_PREFIX + 'appointments/66/', (req) => {
      req.reply({
        statusCode: 204
      })
    })

    // Clear the session storage, otherwise Vuex remembers which page we're on.
    cy.window().then((window) => {
      window.sessionStorage.clear()
    })

    cy.bceidLogin(
      Cypress.env('BCEID_ENDPOINT'),
      Cypress.env('BCEID_USERNAME'),
      Cypress.env('BCEID_PASSWORD')
    )

    cy.visit('/')

    cy.get(SELECTOR_APPOINTMENT_CANCEL_USER_NAV)
      .click()

    cy.get(SELECTOR_APPOINTMENT_CANCEL_NAV_APPOINTMENTS)

    cy.get(SELECTOR_APPOINTMENT_CANCEL_NAV_APPOINTMENTS)
      .click()

    cy.get(SELECTOR_APPOINTMENT_CANCEL_CANCEL_APPOINTMENT)

    // Need to wait for nav bar to fade
    cy.get(SELECTOR_APPOINTMENT_CANCEL_NAV_APPOINTMENTS).should('not.be.visible')

    // TODO: Find alternative to the cy.wait below.
    // The above should result in the below line not being required, but the nav bar results in the test failing.
    cy.wait(2000)
  })

  it('page loaded', () => {
    cy.matchImageSnapshot()
  })

  it('Cancel Appointment', () => {
    cy.fixture('users/appointments.json').then((json) => {
      cy.intercept('GET', API_PREFIX + 'users/appointments', json).as('getAppointmentsAfterDeletion')
    })
    // Flake: https://github.com/cypress-io/cypress/issues/2681
    cy.workaroundPositionFixed(SELECTOR_HEADER_IMAGE_BCGOV)
    cy.workaroundPositionFixed(SELECTOR_FEEDBACK)

    cy.get(SELECTOR_APPOINTMENT_CANCEL_CANCEL_APPOINTMENT)
      .click()

    cy.get(SELECTOR_APPOINTMENT_CANCEL_CANCEL_CONFIRM)
      .click()

    cy.get(SELECTOR_APPOINTMENT_CANCEL_CANCEL_CONFIRM).should('not.be.visible')
    cy.wait('@getAppointmentsAfterDeletion')
    cy.get(SELECTOR_APPOINTMENT_NO_APPOINTMENTS)

    cy.matchImageSnapshot()
  })
})
