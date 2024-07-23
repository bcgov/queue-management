
describe('Login page', () => {
  it('should match screenshot of element', () => {
    cy.visit('/')
    cy.matchImageSnapshot()
  })
})