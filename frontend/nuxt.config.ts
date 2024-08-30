import path from 'path';

export default defineNuxtConfig({
  ssr: false, 
  devServer: {
    port: 8080,
  },
  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: 'BC Services: Queue Management',
    },
    baseURL: '/',
  },

  css: ['~/assets/css/main.scss'], // Global CSS

  vite: {
    optimizeDeps: {
      include: ['pinia'],
    },
    resolve: {
      dedupe: ['vue'], 
    },
  },

  plugins: [], 
  components: true, 

  buildModules: [
    '@nuxt/typescript-build', // TypeScript support
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