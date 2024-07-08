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

import { addMatchImageSnapshotCommand } from 'cypress-image-snapshot/command'

addMatchImageSnapshotCommand()

declare global {
  namespace Cypress {
    interface Chainable {
      /**
       * Call the BCeID Login task. Not chainable.
       *
       * @example
       *     cy.bceidLogin(url, username, password)
       */
       bceidLogin(url: string, username: string, password: string): void

      /**
       * Wait for Vuetify button ripple effect to complete. Not chainable.
       *
       * @example
       *     cy.workaroundButtonRipple('[data-cy=your-selector]')
       */
       workaroundButtonRipple(selector: string): void

      /**
       * Wait for Vuetify date picker transition to complete. Not chainable.
       *
       * @example
       *     cy.workaroundDatePickerTransition('[data-cy=your-selector]')
       */
       workaroundDatePickerTransition(selector: string): void

      /**
       * Wait for Vuetify image fade transition to complete. Not chainable.
       *
       * @example
       *     cy.workaroundImageFade('[data-cy=your-selector]')
       */
       workaroundImageFade(selector: string): void

       /**
       * Remove fixed position CSS that causes a Cypress bug. Not chainable.
       *
       * @example
       *     cy.workaroundPositionFixed('[data-cy=your-selector]')
       */
      workaroundPositionFixed(selector: string): void

      /**
       * Use intersection observer that says elements are visible. Not chainable.
       *
       * @example
       *     cy.workaroundVisit('/')
       */
      workaroundVisit(url: string): void
    }
  }
}

// Cypress won't allow us to switch to a different domain, so we cannot use the
// BCeID login directly. Use puppeteer to log in and then put the keycloak items
// into the session storage. Inspired by the bcscLogin.js code in
// https://github.com/bcgov/bcrs-testing
//
Cypress.Commands.add('bceidLogin', (url, username, password) => {
  cy.task<Record<string, string>>('bceidLogin', { url, username, password }, { timeout: 60000 }).then(sessionItems => {
    Object.keys(sessionItems).forEach(key => {
      sessionStorage.setItem(key, sessionItems[key])
    })
  })
})

// We have flaky tests because the default behaviour of the Vuetify v-btn is to
// produce a "ripple" effect when the button is clicked. Repeated image
// snapshots of the page will catch the v-btn elements in various states of
// rippling, and will produce false failures. By waiting on the clicked button
// we know it will have completed the ripple by the time the image snapshot is
// taken.
//
// Note that this is quite fragile. Perhaps there is a better way, but what this
// does is wait for a Vuetify v-btn "ripple" span to disappear from the DOM.
// This behaviour may change in newer versions of Vuetify, in which case a new
// workaround will need to be found (or ideally Cypress will start doing the
// right thing and wait for the ripple to complete).
//
Cypress.Commands.add('workaroundButtonRipple', (selector: string) => {
  cy.get(selector)
    .find('.v-ripple__container')
    .should('not.exist')
})

// We have flaky tests because the date displayed in the Vuetify v-date-picker
// has an animation when the component is displayed. Repeated image snapshots of
// the page will very, very rarely catch the date not displayed yet.
//
// Note that this is quite fragile. Perhaps there is a better way, but what this
// does is wait for a Vuetify transition div to disappear from the DOM. This
// behaviour may change in newer versions of Vuetify, in which case a new
// workaround will need to be found (or ideally Cypress will start doing the
// right thing and wait for the transition to complete).
//
Cypress.Commands.add('workaroundDatePickerTransition', (selector: string) => {
  cy.get(selector)
    .find('.picker-transition-enter.picker-transition-enter-active')
    .should('not.exist')
})

// We have flaky tests because the default behaviour of the Vuetify v-img is to
// fade in the image. Repeated image snapshots of the page will catch the v-img
// elements in various states of fading in, and will produce false failures. By
// waiting on each image on the page we know it will have completed the fade-in
// by the time the image snapshot is taken.
//
// Note that this is quite fragile. Perhaps there is a better way, but what this
// does is wait for a Vuetify v-img "preload" div to disappear from the DOM.
// This behaviour may change in newer versions of Vuetify, in which case a new
// workaround will need to be found (or ideally Cypress will start doing the
// right thing and wait for the fade to complete).
//
Cypress.Commands.add('workaroundImageFade', (selector: string) => {
  cy.get(selector)
    .find('.v-image__image.v-image__image--preload')
    .should('not.exist')
})

// There is a bug in Cypress where screenshot() takes pieces of the browser
// viewport and stitches them into a larger image. The problem is that if you
// have elements that stay in a fixed position as the viewport moves, the fixed
// element will appear multiple times in the stitched-together image.
//
// Given a selector, this will set the element to be absolute position. In the
// case that it is a parent element that is fixed, it will walk up the tree
// until it finds it.
//
// https://github.com/cypress-io/cypress/issues/2681
//
Cypress.Commands.add('workaroundPositionFixed', (selector: string) => {
  cy.get(selector).then(($element) => {
    while ($element && $element.css('position') !== 'fixed') {
      $element = $element.parent()
    }

    if ($element) {
      $element.css('position', 'absolute')
    }
  })
})

// There is a Cypress problem where Vuetify images are not being displayed
// because they think they are not observable yet, and since they are not
// observable, they never make themselves visible.
//
// Workaround inspired by: https://github.com/cypress-io/cypress/issues/3848
//
Cypress.Commands.add('workaroundVisit', (url: string) => {
  cy.visit(url, {
    onBeforeLoad: (window) => {
      window.IntersectionObserver =
        function (callback: IntersectionObserverCallback,
          options?: IntersectionObserverInit) {
          let instance = new IntersectionObserver(callback, options)

          // Replace the observe method with isIntersecting always true.
          instance.observe = (target: Element) => {
            const entry = [
              {
                boundingClientRect: target.getBoundingClientRect(),
                intersectionRatio: 1,
                intersectionRect: target.getBoundingClientRect(),
                isIntersecting: true,
                rootBounds:
                  instance.root && instance.root instanceof Element
                    ? instance.root.getBoundingClientRect()
                    : null,
                target: target,
                time: Date.now()
              }
            ]

            callback(entry, this)
          }

          return instance
        }
    }
  })
})
