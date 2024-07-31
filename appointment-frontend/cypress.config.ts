import { defineConfig } from 'cypress'

export default defineConfig({
  chromeWebSecurity: true,
  env: {
    'cypress-plugin-snapshots': {
      imageConfig: {
        threshold: 10,
        thresholdType: 'percent',
      },
      screenshotConfig: {
        blackout: [],
        capture: 'fullPage',
        clip: null,
        disableTimersAndAnimations: true,
        log: false,
        scale: false,
        timeout: 50000,
      }
    },
  },
  video: false,
  e2e: {
    // We've imported your old cypress plugins here.
    // You may want to clean this up later by importing these.
    setupNodeEvents(on, config) {
      return require('./cypress/plugins/index.ts').default(on, config)
    },
    baseUrl: 'http://localhost:8081',
    excludeSpecPattern: ['**/__snapshots__/*', '**/__image_snapshots__/*'],
    retries: {
      runMode: 4,
      openMode: 4
    }
  }
})
