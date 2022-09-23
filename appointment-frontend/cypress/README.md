# Running Cypress

Copy the `appointment-frontend/cypress.env.json` file from the Teams channel to
define the Cypress environment variables needed for BCeID login.

Then there are multiple ways to run Cypress:

- `npm run cy` - run the entire test suite headless
- `npm run cy -s cypress/integration/image_snapshot/step1.spec.ts` - run a
  single set of tests headless. If you want to run a single test within the
  spec, change that test from `if` to `if.only`
- `npm run cy:open` - start the Cypress GUI. Requires that you first have a
  browser open to
  `http://localhost:10000/index.html?encoding=rgb32&password=<YOUR_X_PASSWORD>`

# Cypress Filesystem Layout

The Cypress files include:

```
appointment-frontend/
│   cypress.env.json (not in repo, must be created to run BCeID tests)
│   cypress.json (Cypress configuration)
│
└───cypress/
│   │   .eslintrc.json (eslint configuration for Cypress files)
│   │   README.md (this file)
│   │
│   └───fixtures/ (json files defining stubbed API calls)
│   └───integration/ (location of the test spec files)
│   └───plugins/ (tools used by the test spec files)
│   └───screenshots/ (not committed, failed tests create images here)
│   └───snapshots/ (images defining the expected snapshots for test specs)
│   └───support/ (Cypress entry point and additional tools for tests)
```

# Making Changes to Image Snapshots

We will have updates to the application that cause expected snapshot image
changes. When this happens it is important that we do not replace the existing
images with ones that have errors. The following workflow is one way of doing
so.

1. Make your application changes
1. Run the Cypress tests
1. For the tests that fail due to image snapshot differences look in the
   `__diff_output__` directory for the differences images and confirm expected
   differences
1. Rename the changed images from `xxxxx.png` to `xxxxx.old.png`
1. Delete the `__diff_output__` directory
1. Run the tests to create the new images
1. Do a visual comparison of the `xxxxx.old.png` and the new `xxxxx.png` images
1. Run the tests (repeatedly?) to ensure that the new images are correct
1. Delete the `xxxxx.old.png` images
1. Commit your application changes plus the new `xxxxx.png` images

# Gotchas

1. There is some workaround custom code added to Cypress for dealing with the
   fancy things that Vuetify does. These allow us to not have `cy.wait()` all
   over the place. The downside is that they rely on inner workings of Vuetify
   and may be fragile.
1. When running `npm cy:open` be sure to move your mouse out of the window where
   the tests are running. The mouse position can affect the image snapshots by
   causing things like the highlighting of buttons.

# TODOs

1. There are some TODO items in the code, mostly around quirks with Vuetify. In
   order to get this completed some `cy.wait()` items were added but they are
   not ideal.
1. The beforeEach calls, particularly as you get into the higher steps, are long
   and repetative. It would be good to abstract these out somehow. It's workable
   for a small app but a better approach is needed for something bigger.
1. The BCeID code isn't ideal, it would be better to stub out the calls and not
   depend on that web site at all. It would be time consuming though.
1. There is a TypeScript error in `support/commands.ts` but it wasn't possible
   to find a solution in time.
1. We should create bugs with Cypress for the Vuetify workarounds, but they want
   working code so it would be time intensive. It would be good to get Cypress
   working better with Vuetify, though, and reduce our workarounds.

# Snapshots

There is an experimental feature of Cypress that allows you to take a DOM
snapshot that is stored as a string. This is an ideal tool for diagnosing
intermittent image snapshot failures based on timing issues. You can do
snapshots until it finally fails, and then you have the DOM differences to sort
out the problem.
1. `npm i -D @cypress/snapshot`
1. In `support/commands.ts` add `require('@cypress/snapshot').register()`
1. Do something like the following:
   ```
   cy.get(SELECTOR_XYZ).snapshot()
   cy.wait(5000)
   cy.get(SELECTOR_XYZ).snapshot()
   ```
   Note that there are TypeScript warnings - find a fix and then update these
   docs please.
1. Once you've sorted out the image snapshot problem, revert the above changes.
