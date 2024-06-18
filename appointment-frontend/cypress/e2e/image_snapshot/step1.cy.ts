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
  SELECTOR_STEP_1_BUTTON_AVAILABLE_SERVICES,
  SELECTOR_STEP_1_COMBOBOX_OFFICE,
  SELECTOR_STEP_1_DIALOG_SERVICE_LIST,
  SELECTOR_STEP_1_IMAGE_MAP
} from '../../support/selectors'

import { API_PREFIX } from '../../support/e2e'

describe('step 1', () => {
  beforeEach(() => {
    // Intercept API calls to provide testing data.

    cy.fixture('categories').then((json) => {
      cy.intercept('GET', API_PREFIX + 'categories/', json)
    })

    cy.fixture('offices').then((json) => {
      cy.intercept('GET', API_PREFIX + 'offices/', json)
    })

    cy.fixture('services/office_id=3').then((json) => {
      cy.intercept('GET', API_PREFIX + 'services/?office_id=3', json)
    })

    // Clear the session storage, otherwise Vuex remembers which page we're on.
    cy.window().then((window) => {
      window.sessionStorage.clear()
    })

    cy.visit('/')

    // Flake: https://github.com/cypress-io/cypress/issues/2681
    cy.workaroundPositionFixed(SELECTOR_FEEDBACK)

    // Flake: v-img has a default fade transition. Wait for it to complete.
    cy.workaroundImageFade(SELECTOR_HEADER_IMAGE_BCGOV)

    // Flake: This isn't visible until the API call completes. Wait for it.
    cy.get(SELECTOR_STEP_1_COMBOBOX_OFFICE)
      .should('be.visible')
  })

  it('page loaded', () => {
    cy.matchImageSnapshot()
  })

  // TODO: Fix rare "AssertionError: Timed out retrying after 4000ms: Expected
  // <div.v-image__image.v-image__image--preload.v-image__image--cover> not to
  // exist in the DOM, but it was continuously found. Queried from element:
  // <div.v-image.v-responsive.static-map.theme--light>"
  it('office selected', () => {
    // Blur to remove focus, otherwise the blinking cursor causes image changes.
    cy.get(SELECTOR_STEP_1_COMBOBOX_OFFICE)
      .type('Victoria{downarrow}{enter}')
      .blur()

    // Flake: v-img has a default fade transition. Wait for it to complete.
    cy.workaroundImageFade(SELECTOR_STEP_1_IMAGE_MAP)

    cy.matchImageSnapshot()
  })

  it('services popup', () => {
    cy.get(SELECTOR_STEP_1_COMBOBOX_OFFICE)
      .type('Victoria{downarrow}{enter}')

    cy.get(SELECTOR_STEP_1_BUTTON_AVAILABLE_SERVICES)
      .click()

    // Flake: wait until the button ripple finishes.
    cy.workaroundButtonRipple(SELECTOR_STEP_1_BUTTON_AVAILABLE_SERVICES)

    cy.get(SELECTOR_STEP_1_DIALOG_SERVICE_LIST)
      .should('be.visible')

    // Flake: https://github.com/cypress-io/cypress/issues/2681
    cy.workaroundPositionFixed(SELECTOR_STEP_1_DIALOG_SERVICE_LIST)

    cy.matchImageSnapshot()
  })
})
