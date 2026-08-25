import type { Config } from '@react-router/dev/config'

// SSR for runtime rendering; /locations is also prerendered at build time for SEO.
export default {
  ssr: true,
  prerender: ['/locations'],
} satisfies Config
