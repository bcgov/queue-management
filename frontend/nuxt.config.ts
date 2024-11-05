import { defineNuxtConfig } from 'nuxt/config'

import path from 'path';

export default defineNuxtConfig({
  ssr: false,
  devServer: {
    port: 8080,
  },
  devtools: { enabled: true },
  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: 'Service BC Queue Management System',
    },
    baseURL: '/',
  },
  routeRules: {
    '/': { redirect: '/queue' },
  },

  css: ['~/assets/css/main.scss'],

  vite: {
    optimizeDeps: {
      include: ['pinia'],
    },
    resolve: {
      dedupe: ['vue'],
    },
  },

  plugins: ['~/plugins/font-awesome.ts'],
  components: true,

  buildModules: [
    '@nuxt/typescript-build',
  ],

  modules: [
    '@nuxt/ui',
    '@nuxt/content',
    '@pinia/nuxt',
    '@nuxtjs/tailwindcss',
    '@nuxt/test-utils/module'
  ],

  build: {
    transpile: ['@pinia', 'pinia'],
    postcss: {
      plugins: {
        tailwindcss: {},
        autoprefixer: {},
      },
    },
  },

  nitro: {
    output: {
      publicDir: path.join(__dirname, 'dist'),
    },
  },
  runtimeConfig: {
    public: {
      VUE_APP_API_URL: process.env.VUE_APP_API_URL,
    },
  },

  compatibilityDate: '2024-08-16',
});
