import { type RouteConfig, index, route } from '@react-router/dev/routes'

export default [
  index('routes/home.tsx'),
  route('services', 'routes/services.tsx'),
  route('locations', 'routes/locations.tsx'),
] satisfies RouteConfig
