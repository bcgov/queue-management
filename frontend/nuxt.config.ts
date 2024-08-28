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

  css: ['@/assets/css/main.scss'], // Global CSS

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
    '@nuxtjs/tailwindcss', // Tailwind CSS
  ],

  modules: [
    '@nuxt/content',
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt', // Ensure this is correctly listed
  ],

  build: {
    transpile: ['@pinia', 'pinia'], // Ensure Pinia is transpiled correctly
  },

  nitro: {
    output: {
      publicDir: path.join(__dirname, 'dist'),
    },
  },
  runtimeConfig: {
    // Private keys are only available on the server
    // apiSecret: '123',

    // Public keys that are exposed to the client
    public: {
      VUE_APP_API_URL: process.env.VUE_APP_API_URL,

    },
  },

  compatibilityDate: '2024-08-16', // Compatibility date for Nuxt presets
});
