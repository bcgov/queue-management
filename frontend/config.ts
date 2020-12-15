/*eslint-disable */
const config = {
    APP_API_URL: process.env.VUE_APP_API_URL || '/api/v1/',
    SOCKET_URL: process.env.VUE_APP_SOCKET_URL || '',
    REFRESH_TOKEN_SECONDS_LEFT: process.env.VUE_APP_REFRESH_TOKEN_SECONDS_LEFT || '180',
    BASE_URL: process.env.BASE_URL || ''
}

// localhost and OpenShfit can return strings/envs, so we handle both
// eg handles true and "true"
function handleBooleanString(input: string | Boolean): Boolean {
    if (!input) return false;
    if (typeof input === 'boolean') return input;
    if (typeof input === 'string') {
        return input.toLowerCase() === 'true';
    }
    return false;
}

export default { ...config }
