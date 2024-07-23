import { defineConfig } from "cypress";
import { addMatchImageSnapshotPlugin } from '@simonsmith/cypress-image-snapshot/plugin'


export default defineConfig({
  chromeWebSecurity: true,
  env: {
    'cypress-plugin-snapshots': {
      imageConfig: {
        threshold: 0,
        thresholdType: 'percent'
      },
      screenshotConfig: {
        blackout: [],
        capture: 'fullPage',
        clip: null,
        disableTimersAndAnimations: true,
        log: false,
        scale: false,
        timeout: 30000
      }
    }
  },
  video: false,
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
      addMatchImageSnapshotPlugin(on)
    },
    baseUrl: 'http://localhost:8080',
    excludeSpecPattern: ['**/__snapshots__/*', '**/__image_snapshots__/*']
  }
})
