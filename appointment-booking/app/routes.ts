import { type RouteConfig, index, route } from '@react-router/dev/routes'

export default [
  index('routes/home.tsx'),
  route('locations', 'routes/locations.tsx'),
  route('csr-demo', 'routes/csr-demo.tsx'),
] satisfies RouteConfig
