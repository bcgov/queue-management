/*eslint-disable */
const config = {
    APP_API_URL: process.env.VUE_APP_API_URL || '/api/v1/',
    SOCKET_URL: process.env.VUE_APP_SOCKET_URL  || ''
}

export default { ...config }
