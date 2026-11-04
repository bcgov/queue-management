import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue2'
import { nodePolyfills } from 'vite-plugin-node-polyfills'
import type { Plugin } from 'vite'
import ts from 'typescript'

function camundaLegacyDecorators(): Plugin {
  return {
    name: 'camunda-legacy-decorators',
    enforce: 'pre',

    transform(code, id) {
      const filename = id.replace(/\\/g, '/')

      if (
        !filename.includes('/node_modules/camunda-formio-tasklist-vue/') ||
        !filename.endsWith('.vue')
      ) {
        return null
      }

      const scriptPattern =
        /(<script\b[^>]*\blang=["']ts["'][^>]*>)([\s\S]*?)(<\/script>)/

      if (!scriptPattern.test(code)) {
        return null
      }

      const transformed = code.replace(
        scriptPattern,
        (_match, opening, source, closing) => {
          const result = ts.transpileModule(source, {
            fileName: filename + '.ts',
            compilerOptions: {
              target: ts.ScriptTarget.ES2020,
              module: ts.ModuleKind.ESNext,
              experimentalDecorators: true,
              useDefineForClassFields: false,
              importHelpers: false
            }
          })

          return `${opening}\n${result.outputText}\n${closing}`
        }
      )

      return {
        code: transformed,
        map: null
      }
    }
  }
}

export default defineConfig({
  plugins: [
    camundaLegacyDecorators(),
    vue(),
    nodePolyfills({
      include: [
        'buffer',
        'crypto',
        'events',
        'process',
        'stream',
        'string_decoder',
        'util',
        'vm'
      ],
      globals: {
        Buffer: true,
        global: true,
        process: true
      },
      protocolImports: true
    })
  ],

  base: '/',

  optimizeDeps: {
    include: ['jsonwebtoken']
  },

    esbuild: {
    tsconfigRaw: {
      compilerOptions: {
        experimentalDecorators: true,
        useDefineForClassFields: false
      }
    }
  },

  resolve: {
    dedupe: ['vue'],
    alias: [
      {
        find: /^vue$/,
        replacement: fileURLToPath(
          new URL('./node_modules/vue/dist/vue.esm.js', import.meta.url)
        )
      },
      {
        find: '@',
        replacement: fileURLToPath(new URL('./src', import.meta.url))
      }
    ]
  },

		  server: {
			host: 'localhost',
			port: 8082,
			strictPort: true,
			proxy: {
        '/api': {
          target: 'https://test-theq.apps.silver.devops.gov.bc.ca',
          changeOrigin: true,
          secure: true,
          ws: true,
          configure: (proxy) => {
            proxy.on('proxyReqWs', (proxyReq) => {
              proxyReq.setHeader(
                'Origin',
                'https://test-theq.apps.silver.devops.gov.bc.ca'
              )
            })
          }
        },
			  '/socket.io': {
				target: 'https://test-theq.apps.silver.devops.gov.bc.ca',
				changeOrigin: true,
				secure: true,
				ws: true
			  }
			}
		  },

		  build: {
			outDir: 'dist',
			sourcemap: true
		  }
		})