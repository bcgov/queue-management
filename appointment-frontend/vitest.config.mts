import { fileURLToPath, URL } from 'node:url'
import { defineConfig, mergeConfig } from 'vitest/config'
import viteConfig from './vite.config.mjs'

export default mergeConfig(
  viteConfig,
  defineConfig({
    resolve: {
      alias: {
        vue: fileURLToPath(
          new URL(
            './node_modules/vue/dist/vue.runtime.common.js',
            import.meta.url
          )
        )
      }
    },
    test: {
      pool: 'threads',
      maxWorkers: 1,
      globals: true,
      environment: 'jsdom',
      environmentOptions: {
        jsdom: {
          url: 'http://localhost:8081/'
        }
      },
      include: ['tests/unit/**/*.spec.ts']
    }
  })
)