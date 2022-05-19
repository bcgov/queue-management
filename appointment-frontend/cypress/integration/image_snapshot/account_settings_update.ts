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
  SELECTOR_ACCOUNT_SETTINGS_EMAIL_SWITCH,
  SELECTOR_ACCOUNT_SETTINGS_MSG,
  SELECTOR_ACCOUNT_SETTINGS_NAV,
  SELECTOR_ACCOUNT_SETTINGS_PHONE_INPUT,
  SELECTOR_ACCOUNT_SETTINGS_UPDATE_BUTTON,
  SELECTOR_APPOINTMENT_CANCEL_USER_NAV,
  SELECTOR_FEEDBACK,
  SELECTOR_HEADER_IMAGE_BCGOV
} from '../../support/selectors'

import { API_PREFIX } from '../../support'

describe('Account Settings', () => {
  beforeEach(() => {
    // Intercept API calls to provide testing data.
    cy.fixture('offices.json').then((json) => {
      cy.intercept('GET', API_PREFIX + 'offices/', json).as('getOffices')
    })

    cy.fixture('services/appointment_cancel.json').then((json) => {
      cy.intercept('GET', API_PREFIX + 'services', json).as('getServices')
    })

    cy.fixture('users/me').then((json) => {
      cy.intercept('GET', API_PREFIX + 'users/me', json)
    })
    cy.fixture('users/id=12706').then((json) => {
      cy.intercept('PUT', API_PREFIX + 'users/12706', json).as('getUserUpdate')
    })

    cy.fixture('users/appointments').then((json) => {
      cy.intercept('GET', API_PREFIX + 'users/appointments', json)
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

    cy.get(SELECTOR_ACCOUNT_SETTINGS_NAV)

    cy.get(SELECTOR_ACCOUNT_SETTINGS_NAV)
      .click()

    // Need to wait for nav bar to fade
    cy.get(SELECTOR_ACCOUNT_SETTINGS_NAV).should('not.be.visible')

    // TODO: Find alternative to the cy.wait below.
    // The above should result in the below line not being required, but the nav bar results in the test failing.
    cy.wait(2000)
  })

  it('page loaded', () => {
    cy.matchImageSnapshot()
  })
  it('Update User', () => {
    cy.get(SELECTOR_ACCOUNT_SETTINGS_PHONE_INPUT)

    cy.get(SELECTOR_ACCOUNT_SETTINGS_PHONE_INPUT).clear()

    cy.get(SELECTOR_ACCOUNT_SETTINGS_PHONE_INPUT).type('604-123-1234')

    cy.get(SELECTOR_ACCOUNT_SETTINGS_EMAIL_SWITCH).click({ force: true })

    // Flake: https://github.com/cypress-io/cypress/issues/2681
    cy.workaroundPositionFixed(SELECTOR_HEADER_IMAGE_BCGOV)
    cy.workaroundPositionFixed(SELECTOR_FEEDBACK)
    cy.workaroundPositionFixed(SELECTOR_ACCOUNT_SETTINGS_MSG)

    cy.get(SELECTOR_ACCOUNT_SETTINGS_UPDATE_BUTTON).click()

    cy.get(SELECTOR_ACCOUNT_SETTINGS_MSG)

    cy.wait(1000)

    cy.matchImageSnapshot()
  })
})
