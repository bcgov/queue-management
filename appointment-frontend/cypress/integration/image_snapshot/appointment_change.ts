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
  SELECTOR_APPOINTMENT_CANCEL_NAV_APPOINTMENTS,
  SELECTOR_APPOINTMENT_CANCEL_USER_NAV,
  SELECTOR_APPOINTMENT_CHANGE_APPOINTMENT,
  SELECTOR_FEEDBACK,
  SELECTOR_HEADER_IMAGE_BCGOV,
  SELECTOR_STEP_3_BUTTON_TIMESLOT,
  SELECTOR_STEP_5_BUTTON_CONFIRM,
  SELECTOR_STEP_5_CHECKBOX_CONSENT,
  SELECTOR_STEP_5_DIALOG_APPOINTMENT
} from '../../support/selectors'

import { API_PREFIX } from '../../support'

describe('Change Appointment', () => {
  beforeEach(() => {
    // Intercept API calls to provide testing data.
    cy.fixture('offices.json').then((json) => {
      cy.intercept('GET', API_PREFIX + 'offices/', json).as('getOffices')
    })

    cy.fixture('services/appointment_cancel.json').then((json) => {
      cy.intercept('GET', API_PREFIX + 'services', json)
    })

    cy.fixture('users/appointments/appointment_cancel.json').then((json) => {
      cy.intercept('GET', API_PREFIX + 'users/appointments', json)
    })

    cy.fixture('users/me').then((json) => {
      cy.intercept('GET', API_PREFIX + 'users/me', json)
    })

    cy.intercept('DELETE', API_PREFIX + 'appointments/66/', (req) => {
      req.reply({
        statusCode: 204
      })
    })
    cy.fixture('offices/3/slots/service_id=7.json').then((json) => {
      cy.intercept('GET', API_PREFIX + 'offices/3/slots/?service_id=7', json)
    })

    cy.intercept('POST', API_PREFIX + 'appointments/draft', (req) => {
      req.reply({
        statusCode: 201
      })
    })
    cy.fixture('appointments/id=66').then((json) => {
      cy.intercept('PUT', API_PREFIX + 'appointments/66', json)
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
      .click()

    // Need to wait for nav bar to fade
    cy.get(SELECTOR_APPOINTMENT_CANCEL_NAV_APPOINTMENTS).should('not.be.visible')

    // TODO: Find alternative to the cy.wait below.
    // The above should result in the below line not being required, but the nav bar results in the test failing.
    cy.wait(2000)
  })

  it('page loaded', () => {
    cy.matchImageSnapshot()
  })

  it('Change Appointment', () => {
    cy.clock(new Date('2022-05-3').getTime())
    cy.get(SELECTOR_APPOINTMENT_CHANGE_APPOINTMENT)
      .click()

    cy.get(SELECTOR_STEP_3_BUTTON_TIMESLOT)
      .first()
      .click()

    cy.get(SELECTOR_STEP_5_CHECKBOX_CONSENT)

    // Flake: https://github.com/cypress-io/cypress/issues/2681
    cy.workaroundPositionFixed(SELECTOR_HEADER_IMAGE_BCGOV)
    cy.workaroundPositionFixed(SELECTOR_FEEDBACK)

    // TODO: these tests fail without the wait below. Looks to be an issue with the transition of the page.
    cy.wait(1000)

    cy.get(SELECTOR_STEP_5_CHECKBOX_CONSENT)
      .parent() // Workaround for v-checkbox: click the parent.
      .click()

    cy.get(SELECTOR_STEP_5_BUTTON_CONFIRM)
      .click()

    cy.workaroundPositionFixed(SELECTOR_STEP_5_DIALOG_APPOINTMENT)

    cy.matchImageSnapshot()
  })
})
