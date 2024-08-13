import { API_PREFIX } from '../../support/e2e'

describe('Login page', () => {
  
  beforeEach( () => {
    cy.fixture('offices').then((json) => {
      cy.intercept('GET', API_PREFIX + 'offices/', json)
    })
  })
  it('should match screenshot of element', () => {
    cy.visit('/')
    cy.matchImageSnapshot()
  })
})