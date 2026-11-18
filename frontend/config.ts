/*eslint-disable */
const config = {
    APP_API_URL: import.meta.env.VITE_API_URL || '/api/v1/',
    SOCKET_URL: import.meta.env.VITE_SOCKET_URL || '',
    REFRESH_TOKEN_SECONDS_LEFT: import.meta.env.VITE_REFRESH_TOKEN_SECONDS_LEFT || '180',
    BASE_URL: import.meta.env.BASE_URL,
    IS_INTERNET_EXPLORER: isInternetExplorer()
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


// We check this here, so it's only ever done once in the entire application
function isInternetExplorer(): boolean {
    // MSIE = IE10 and lower
    // Trident = IE11
    return window.navigator.userAgent.match(/(MSIE|Trident)/) !== null;
}

export default { ...config }
