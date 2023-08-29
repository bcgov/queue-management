
const fetch = require('node-fetch');

//KEYCLOAK_URI = 'https://dev.oidc.gov.bc.ca/auth'
KEYCLOAK_URI = 'https://dev.loginproxy.gov.bc.ca/auth'
KEYCLOAK_CLIENT = 'cfms-dev-staff'

// This implementation assumes it never has to refresh a token and they never expire
// As most load testing is short lived (minutes, not hours) this works fine.
// Cache auth tokens to a plain old JavaScript object
const authTokenList = {}
async function getAuthToken(username, password){
    if (authTokenList[username]) return authTokenList[username];
    const newToken = await loginToKeycloak(username, password);
    authTokenList[username] = newToken;
    return newToken;
}

// Working
async function loginToKeycloak(username, password) {
    const res = await fetch(`${KEYCLOAK_URI}/realms/vtkayq4c/protocol/openid-connect/token`, {
        "headers": {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site"
        },
        "body": `grant_type=password&username=${username}&password=${password}&client_id=${KEYCLOAK_CLIENT}`,
        "method": "POST",
        "mode": "cors",
        "credentials": "include"
    })
    const body = await res.json();
    return body;
}

async function setAuthHeader(requestParams, context, ee, next) {
    const {access_token} = await getAuthToken(process.env.KEYCLOAK_USERNAME, process.env.KEYCLOAK_PASSWORD)
    requestParams = {};
    requestParams.headers = {};
    requestParams.Authorization = {};
    requestParams.cookie = {};
    // HTTP requests use Authorization
    requestParams.headers.Authorization = `Bearer ${access_token}`
    // Websocket requests use oidc-jwt cookie
    requestParams.headers.cookie = `oidc-jwt=${access_token}`
    next();
}

// Main / script start
(async () => {
    // Only execute if script is called directly, not if imported.
    if (require.main === module){
        if (process.argv.includes('--get-keycloak-token')){
            const {access_token} = await loginToKeycloak(process.env.KEYCLOAK_USERNAME, process.env.KEYCLOAK_PASSWORD);
            // Log access token to STDOUT, so it can be used as environment variable.

            console.log( access_token )
            return access_token;
        }
    }
})();

module.exports = {
    setAuthHeader
}
