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
  API_FEEDBACK_PREFIX,
  API_PREFIX
} from '../../support'

import {
  SELECTOR_FEEDBACK,
  SELECTOR_FEEDBACK_COMPLAINT_BUTTON,
  SELECTOR_FEEDBACK_COMPLAINT_TEXTAREA,
  SELECTOR_FEEDBACK_CONSENT_CHECK,
  SELECTOR_FEEDBACK_EMAIL_TEXTFIELD,
  SELECTOR_FEEDBACK_NAME_TEXTFIELD,
  SELECTOR_FEEDBACK_PHONE_TEXTFIELD,
  SELECTOR_FEEDBACK_RESPONSE_NEXT,
  SELECTOR_FEEDBACK_RESPONSE_YES,
  SELECTOR_FEEDBACK_SUBMIT_BUTTON,
  SELECTOR_HEADER_IMAGE_BCGOV
} from '../../support/selectors'

describe('Feedback Submission', () => {
  beforeEach(() => {
    // Intercept API calls to provide testing data.
    cy.fixture('offices.json').then((json) => {
      cy.intercept('GET', API_PREFIX + 'offices/', json).as('getOffices')
    })

    cy.intercept('POST', API_FEEDBACK_PREFIX + 'feedback', (req) => {
      req.reply({
        statusCode: 200,
        body: { response_code: 200 }
      })
    })
    // Clear the session storage, otherwise Vuex remembers which page we're on.
    cy.window().then((window) => {
      window.sessionStorage.clear()
    })

    cy.visit('/')
  })

  it('page loaded', () => {
    cy.workaroundPositionFixed(SELECTOR_FEEDBACK)
    cy.workaroundPositionFixed(SELECTOR_HEADER_IMAGE_BCGOV)
    cy.matchImageSnapshot()
  })
  it('Submit Feedback', () => {
    cy.workaroundPositionFixed(SELECTOR_FEEDBACK)
    cy.get(SELECTOR_FEEDBACK_COMPLAINT_BUTTON).click({ force: true })
    cy.get(SELECTOR_FEEDBACK_COMPLAINT_TEXTAREA).focus()
    cy.get(SELECTOR_FEEDBACK_COMPLAINT_TEXTAREA).type('complaint message...')
    cy.get(SELECTOR_FEEDBACK_RESPONSE_YES).click({ force: true })

    cy.get(SELECTOR_FEEDBACK_RESPONSE_NEXT).click({ force: true })

    cy.get(SELECTOR_FEEDBACK_NAME_TEXTFIELD).focus()
    cy.get(SELECTOR_FEEDBACK_NAME_TEXTFIELD).type('Test Name', { force: true })

    cy.get(SELECTOR_FEEDBACK_EMAIL_TEXTFIELD).focus()
    cy.get(SELECTOR_FEEDBACK_EMAIL_TEXTFIELD).type('test@test.ca', { force: true })

    cy.get(SELECTOR_FEEDBACK_PHONE_TEXTFIELD).focus()
    cy.get(SELECTOR_FEEDBACK_PHONE_TEXTFIELD).type('123-123-1234', { force: true })

    cy.get(SELECTOR_FEEDBACK_CONSENT_CHECK).click({ force: true })
    cy.get(SELECTOR_FEEDBACK_SUBMIT_BUTTON).click({ force: true })

    cy.wait(1000)
    cy.matchImageSnapshot()
  })
})
