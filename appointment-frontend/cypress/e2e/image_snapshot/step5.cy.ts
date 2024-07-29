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
  SELECTOR_FEEDBACK,
  SELECTOR_HEADER_IMAGE_BCGOV,
  SELECTOR_STEP_1_BUTTON_BOOK_APPOINTMENT,
  SELECTOR_STEP_1_COMBOBOX_OFFICE,
  SELECTOR_STEP_2_BUTTON_NEXT,
  SELECTOR_STEP_2_COMBOBOX_SERVICE,
  SELECTOR_STEP_3_BUTTON_TIMESLOT,
  SELECTOR_STEP_5_BUTTON_CONFIRM,
  SELECTOR_STEP_5_CHECKBOX_CONSENT,
  SELECTOR_STEP_5_DIALOG_APPOINTMENT,
  SELECTOR_STEP_5_IMAGE_MAP
} from '../../support/selectors'

import { API_PREFIX } from '../../support/e2e'

describe('step 5', () => {
  beforeEach(() => {
    // Intercept API calls to provide testing data.

    cy.fixture('appointments').then((json) => {
      cy.intercept('POST', API_PREFIX + 'appointments', json)
    })

    cy.fixture('appointments/draft').then((json) => {
      cy.intercept('POST', API_PREFIX + 'appointments/draft', json)
    })

    cy.fixture('offices').then((json) => {
      cy.intercept('GET', API_PREFIX + 'offices/', json)
    })

    cy.fixture('offices/3/slots/service_id=85').then((json) => {
      cy.intercept('GET', API_PREFIX + 'offices/3/slots/?service_id=85', json)
    })

    cy.fixture('services').then((json) => {
      cy.intercept('GET', API_PREFIX + 'services', json)
    })

    cy.fixture('services/office_id=3').then((json) => {
      cy.intercept('GET', API_PREFIX + 'services/?office_id=3', json)
    })

    cy.fixture('users/appointments').then((json) => {
      cy.intercept('GET', API_PREFIX + 'users/appointments', json)
    })

    cy.fixture('users/me').then((json) => {
      cy.intercept('GET', API_PREFIX + 'users/me', json)
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

    cy.get(SELECTOR_STEP_1_COMBOBOX_OFFICE)
      .type('Victoria{downarrow}{enter}')

    cy.get(SELECTOR_STEP_1_BUTTON_BOOK_APPOINTMENT)
      .click()

    cy.get(SELECTOR_STEP_2_COMBOBOX_SERVICE)
      .type('Legal Change of Name{downarrow}{enter}')

    // The API fixtures are based on a certain date, so act like it's that day.
    cy.clock(new Date('2022-01-16').getTime())

    cy.get(SELECTOR_STEP_2_BUTTON_NEXT)
      .click()

    cy.get(SELECTOR_STEP_3_BUTTON_TIMESLOT)
      .click()

    // Get something from the next page, so that we know page load is complete.
    cy.get(SELECTOR_STEP_5_CHECKBOX_CONSENT)

    // Flake: https://github.com/cypress-io/cypress/issues/2681
    cy.workaroundPositionFixed(SELECTOR_HEADER_IMAGE_BCGOV)
    cy.workaroundPositionFixed(SELECTOR_FEEDBACK)

    // Flake: v-img has a default fade transition. Wait for it to complete.
    cy.workaroundImageFade(SELECTOR_HEADER_IMAGE_BCGOV)
    cy.workaroundImageFade(SELECTOR_STEP_5_IMAGE_MAP)

    // TODO: Flake: these tests are failing with portions of the dialog box
    // visible in the image snapshot to the left of the page itself. It is as if
    // Vuetify is not hiding the dialog box until after the page is rendered,
    // and the image snapshot is fairly frequently catching it when visible. It
    // needs some research but this workaround will have to do for now.
    cy.wait(1000)
  })

  it('page loaded', () => {
    cy.matchImageSnapshot()
  })

  it('consent checked', () => {
    cy.get(SELECTOR_STEP_5_CHECKBOX_CONSENT)
      .parent() // Workaround for v-checkbox: click the parent.
      .click()

    cy.get(SELECTOR_STEP_5_BUTTON_CONFIRM)
      .should('be.visible')

      cy.screenshot('SELECTOR_STEP_5_BUTTON_CONFIRM');

    cy.matchImageSnapshot()
  })

  it('confirm clicked', () => {
    cy.get(SELECTOR_STEP_5_CHECKBOX_CONSENT)
      .parent() // Workaround for v-checkbox: click the parent.
      .click()

    cy.get(SELECTOR_STEP_5_BUTTON_CONFIRM)
      .click()

    // Flake: https://github.com/cypress-io/cypress/issues/2681
    cy.workaroundPositionFixed(SELECTOR_STEP_5_DIALOG_APPOINTMENT)

    cy.get(SELECTOR_STEP_5_DIALOG_APPOINTMENT)
      .should('be.visible')

    cy.matchImageSnapshot()
  })
})
