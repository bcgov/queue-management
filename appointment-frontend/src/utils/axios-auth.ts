import axios from 'axios'

const instance = axios.create()

instance.interceptors.request.use(
  config => {
    config.headers.common['Authorization'] = `Bearer ${sessionStorage.getItem('KEYCLOAK_TOKEN')}`
    return config
  },
  error => Promise.reject(error)
)

instance.interceptors.response.use(
  response => response,
  error => Promise.reject(error)
)

export default instance
