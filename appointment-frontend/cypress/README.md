
# How to run

There are multiple ways to run Cypress.

- `npm run cy` - run the entire test suite headless
- `npm run cy -s cypress/integration/image_snapshot/step1.spec.ts` - run a
  single set of tests headless. If you want to run a single test within the
  spec, change that test from `if` to `if.only`.
- `npm run cy:open` - start the Cypress GUI. Requires that you first have a
  browser open to
  `http://localhost:10000/index.html?encoding=rgb32&password=<YOUR_PASSWORD>`

# Gotchas

1. There is some workaround custom code added to Cypress for dealing with the
   fancy things that Vuetify does. These allow us to not have cy.wait() all over
   the place. The downside is that they rely on inner workings of Vuetify and
   may be fragile.
1. When running 'cypress open' be sure to move your mouse out of the window
   where the tests are running. The mouse position can affect the image
   snapshots by causing things such as changes in button colour.

# Snapshots

There is an experimental feature of Cypress that allows you to take a DOM
snapshot that is stored as a string. This is an ideal tool for diagnosing
intermittent image snapshot failures based on timing issues. You can do
snapshots until it finally fails, and then you have the DOM differences to sort
out the problem.
1. `npm i -D @cypress/snapshot`
1. In support/commands.ts add `require('@cypress/snapshot').register()`
1. Do something like the following:
   ```
   cy.get(SELECTOR_XYZ).snapshot('1')
   cy.wait(1000)
   cy.get(SELECTOR_XYZ).snapshot('2')
   ```
   Note that there are TypeScript warnings - try to fix and then update these
   docs!
1. Once you've sorted out the image snapshot problem, revert the above changes.
