import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue2'
import type { Plugin } from 'vite'

// Compatibility workaround for vue2-google-maps source files.
function googleMapsCompatibility (): Plugin {
  return {
    name: 'vue2-google-maps-compatibility',
    enforce: 'pre',

    transform (code, id) {
      const filename = id.split('?')[0].replace(/\\/g, '/')

      if (!filename.includes('/node_modules/vue2-google-maps/src/')) {
        return null
      }

      // Convert the four Vue component wrappers.
      if (
        /\/(autocomplete|infoWindow|map|streetViewPanorama)\.vue$/.test(filename)
      ) {
        const match = code.match(/require\(['"](\.\/[^'"]+Impl\.js)['"]\)/)

        if (!match) return null

        const updated = code
          .replace(
            '<script>',
            `<script>\nimport * as implementation from '${match[1]}'`
          )
          .replace(match[0], 'implementation')

        return { code: updated, map: null }
      }

      // Convert the cluster import in the package entry point.
      if (filename.endsWith('/src/main.js')) {
        const pattern = /require\(['"]\.\/components\/cluster['"]\)/

        if (!pattern.test(code)) return null

        return {
          code:
            "import * as clusterModule from './components/cluster.js'\n" +
            code.replace(pattern, 'clusterModule'),
          map: null
        }
      }

      return null
    }
  }
}

export default defineConfig({
  plugins: [googleMapsCompatibility(), vue()],

  define: {
    'process.env.BUILD_DEV': JSON.stringify('0')
  },

  base: '/',

  resolve: {
    dedupe: ['vue'],
    alias: {
      vue: fileURLToPath(
        new URL('./node_modules/vue/dist/vue.runtime.esm.js', import.meta.url)
      ),
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '$assets': fileURLToPath(new URL('./src/assets', import.meta.url)),
      'vue2-google-maps': fileURLToPath(
        new URL('./node_modules/vue2-google-maps/src/main.js', import.meta.url)
      )
    }
  },

  optimizeDeps: {
    exclude: ['vue2-google-maps'],
    include: ['vue2-google-maps > marker-clusterer-plus']
  },

  server: {
    host: 'localhost',
    port: 8081,
    strictPort: true,
    proxy: {
      '/api/v1': {
        target: 'https://test-theq-public.apps.silver.devops.gov.bc.ca',
        changeOrigin: true,
        secure: true
      }
    }
  },

  build: {
    outDir: 'dist',
    sourcemap: true
  }
})