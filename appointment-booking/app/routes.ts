import { type RouteConfig, index, route } from '@react-router/dev/routes'

export default [
  index('routes/home.tsx'),
  route('services', 'routes/services.tsx'),
  route('service-locations', 'routes/service-locations.tsx'),
  route('signin/:idpHint', 'routes/signin.$idpHint.tsx'),
  route('login', 'routes/login.tsx'),
  route('locations', 'routes/locations.tsx'),
] satisfies RouteConfig
