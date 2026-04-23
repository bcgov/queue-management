const fetch = require('node-fetch');
const { randomInt } = require('crypto');

const DEFAULT_KEYCLOAK_BASE_URL = 'http://localhost:8085/auth';
const DEFAULT_KEYCLOAK_REALM = 'servicebc-local';
const DEFAULT_KEYCLOAK_CLIENT_ID = 'theq-queue-management-api';
const DEFAULT_KEYCLOAK_CLIENT_SECRET = 'theq-local-dev-secret';
const DEFAULT_KEYCLOAK_USERNAME = 'admin@idir';
const DEFAULT_KEYCLOAK_PASSWORD = 'password';
const DEFAULT_TARGET = 'http://localhost:5000';
const DEFAULT_OFFICE_TIMEZONE = 'America/Vancouver';
const DEFAULT_DRAFT_OFFICE_ID = 2;
const DEFAULT_DRAFT_SERVICE_ID = 11;
const DEFAULT_DRAFT_OFFICE_TIMEZONE = 'America/Creston';
const DEFAULT_DRAFT_SLOT_WEEK_RANGE = 300000;

// This implementation assumes it never has to refresh a token and they never expire
// As most load testing is short lived (minutes, not hours) this works fine.
// Cache auth tokens to a plain old JavaScript object
const authTokenList = {};

function getKeycloakConfig() {
    return {
        baseUrl: process.env.KEYCLOAK_BASE_URL || DEFAULT_KEYCLOAK_BASE_URL,
        realm: process.env.KEYCLOAK_REALM || DEFAULT_KEYCLOAK_REALM,
        clientId: process.env.KEYCLOAK_CLIENT_ID || DEFAULT_KEYCLOAK_CLIENT_ID,
        clientSecret: process.env.KEYCLOAK_CLIENT_SECRET || DEFAULT_KEYCLOAK_CLIENT_SECRET,
    };
}

function getKeycloakCredentials() {
    return {
        username: process.env.KEYCLOAK_USERNAME || DEFAULT_KEYCLOAK_USERNAME,
        password: process.env.KEYCLOAK_PASSWORD || DEFAULT_KEYCLOAK_PASSWORD,
    };
}

function getLoadTestConfig() {
    const officeId = Number(process.env.LOADTEST_OFFICE_ID || 1);
    const createServiceId = Number(process.env.LOADTEST_CREATE_SERVICE_ID || 11);

    return {
        target: process.env.TARGET || DEFAULT_TARGET,
        officeId,
        createServiceId,
        updateServiceId: Number(process.env.LOADTEST_UPDATE_SERVICE_ID || 7),
        draftOfficeId: Number(process.env.LOADTEST_DRAFT_OFFICE_ID || DEFAULT_DRAFT_OFFICE_ID),
        draftServiceId: Number(process.env.LOADTEST_DRAFT_SERVICE_ID || DEFAULT_DRAFT_SERVICE_ID),
        officeTimezone: process.env.LOADTEST_OFFICE_TIMEZONE || DEFAULT_OFFICE_TIMEZONE,
        draftOfficeTimezone: process.env.LOADTEST_DRAFT_OFFICE_TIMEZONE || DEFAULT_DRAFT_OFFICE_TIMEZONE,
        draftSlotWeekRange: Number(
            process.env.LOADTEST_DRAFT_SLOT_WEEK_RANGE || DEFAULT_DRAFT_SLOT_WEEK_RANGE
        ),
    };
}

function buildApiUrl(target, path) {
    return new URL(path, target.replace(/\/$/, '')).toString();
}

function parseSlotDate(day, time, timezone) {
    const [month, date, year] = day.split('/').map(Number);
    const [hour, minute] = time.split(':').map(Number);
    const utcGuess = Date.UTC(year, month - 1, date, hour, minute);
    const localParts = new Intl.DateTimeFormat('en-CA', {
        timeZone: timezone,
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hourCycle: 'h23',
    }).formatToParts(new Date(utcGuess)).reduce((parts, part) => {
        parts[part.type] = part.value;
        return parts;
    }, {});
    const zonedAsUtc = Date.UTC(
        Number(localParts.year),
        Number(localParts.month) - 1,
        Number(localParts.day),
        Number(localParts.hour),
        Number(localParts.minute),
        Number(localParts.second)
    );
    const timezoneOffset = zonedAsUtc - utcGuess;

    return new Date(utcGuess - timezoneOffset).toISOString();
}

function findFirstAvailableSlot(slotsByDay) {
    for (const [day, slots] of Object.entries(slotsByDay)) {
        if (!Array.isArray(slots)) {
            continue;
        }
        const slot = slots.find(({ no_of_slots }) => no_of_slots > 0);
        if (slot) {
            return { day, slot };
        }
    }

    return null;
}

function addDaysToSlotDay(day, daysToAdd) {
    const [month, date, year] = day.split('/').map(Number);
    const slotDate = new Date(Date.UTC(year, month - 1, date));
    slotDate.setUTCDate(slotDate.getUTCDate() + daysToAdd);

    return `${String(slotDate.getUTCMonth() + 1).padStart(2, '0')}/${String(slotDate.getUTCDate()).padStart(2, '0')}/${slotDate.getUTCFullYear()}`;
}

function buildDraftPayloadFromSlot(day, slot) {
    const { draftOfficeId, draftServiceId, draftOfficeTimezone, draftSlotWeekRange } = getLoadTestConfig();
    const sequencedDay = addDaysToSlotDay(day, randomInt(1, draftSlotWeekRange + 1) * 7);
    return {
        office_id: draftOfficeId,
        service_id: draftServiceId,
        start_time: parseSlotDate(sequencedDay, slot.start_time, draftOfficeTimezone),
        end_time: parseSlotDate(sequencedDay, slot.end_time, draftOfficeTimezone),
    };
}

async function getDraftAppointmentPayload() {
    const { target, draftOfficeId, draftServiceId } = getLoadTestConfig();
    const slotsUrl = buildApiUrl(
        target,
        `/api/v1/offices/${draftOfficeId}/slots/?service_id=${draftServiceId}`
    );
    const res = await fetch(slotsUrl);
    const responseBody = await res.text();
    let slotsByDay;

    try {
        slotsByDay = JSON.parse(responseBody);
    } catch (error) {
        throw new Error(`Unable to parse load-test appointment slots: ${responseBody}`);
    }

    if (!res.ok) {
        throw new Error(`Unable to fetch load-test appointment slots: ${res.status} ${JSON.stringify(slotsByDay)}`);
    }

    const available = findFirstAvailableSlot(slotsByDay);
    if (!available) {
        throw new Error(
            `No load-test appointment slots available for office ${draftOfficeId} and service ${draftServiceId}`
        );
    }

    return buildDraftPayloadFromSlot(available.day, available.slot);
}

function getAuthCacheKey(username) {
    const { baseUrl, realm, clientId } = getKeycloakConfig();
    return `${baseUrl}|${realm}|${clientId}|${username}`;
}

async function getAuthToken(username, password) {
    const cacheKey = getAuthCacheKey(username);
    if (authTokenList[cacheKey]) {
        return authTokenList[cacheKey];
    }
    const newToken = await loginToKeycloak(username, password);
    authTokenList[cacheKey] = newToken;
    return newToken;
}

async function loginToKeycloak(username, password) {
    const { baseUrl, realm, clientId, clientSecret } = getKeycloakConfig();
    const formData = new URLSearchParams({
        grant_type: 'password',
        username,
        password,
        client_id: clientId,
    });

    if (clientSecret) {
        formData.set('client_secret', clientSecret);
    }

    const res = await fetch(`${baseUrl}/realms/${realm}/protocol/openid-connect/token`, {
        headers: {
            accept: '*/*',
            'content-type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString(),
        method: 'POST',
    });

    const tokenResponse = await res.json();

    if (!res.ok || !tokenResponse.access_token) {
        throw new Error(`Unable to fetch Keycloak token: ${JSON.stringify(tokenResponse)}`);
    }

    return tokenResponse;
}

async function applyAuthHeader(requestParams) {
    const { username, password } = getKeycloakCredentials();
    const { access_token } = await getAuthToken(username, password);

    requestParams.headers = requestParams.headers || {};
    requestParams.headers.Authorization = `Bearer ${access_token}`;
    requestParams.headers.cookie = `oidc-jwt=${access_token}`;
}

async function setAuthHeader(requestParams, context, ee, next) {
    try {
        await applyAuthHeader(requestParams);
        if (typeof next === 'function') {
            next();
        }
    } catch (error) {
        if (typeof next === 'function') {
            next(error);
            return;
        }
        throw error;
    }
}

async function setDraftPayload(requestParams, context, ee, next) {
    try {
        await applyAuthHeader(requestParams);
        const draftPayload = await getDraftAppointmentPayload();
        requestParams.json = requestParams.json || {};
        Object.assign(requestParams.json, draftPayload);
        if (typeof next === 'function') {
            next();
        }
    } catch (error) {
        if (typeof next === 'function') {
            next(error);
            return;
        }
        throw error;
    }
}

async function setCreateAppointmentPayload(requestParams, context, ee, next) {
    try {
        await applyAuthHeader(requestParams);
        const { officeId, createServiceId } = getLoadTestConfig();
        requestParams.json = requestParams.json || {};
        requestParams.json.office_id = officeId;
        requestParams.json.service_id = createServiceId;
        if (typeof next === 'function') {
            next();
        }
    } catch (error) {
        if (typeof next === 'function') {
            next(error);
            return;
        }
        throw error;
    }
}

async function setUpdateAppointmentPayload(requestParams, context, ee, next) {
    try {
        await applyAuthHeader(requestParams);
        const { officeId, updateServiceId } = getLoadTestConfig();
        requestParams.json = requestParams.json || {};
        requestParams.json.office_id = officeId;
        requestParams.json.service_id = updateServiceId;
        if (typeof next === 'function') {
            next();
        }
    } catch (error) {
        if (typeof next === 'function') {
            next(error);
            return;
        }
        throw error;
    }
}

// Main / script start
(async () => {
    // Only execute if script is called directly, not if imported.
    if (require.main === module) {
        if (process.argv.includes('--get-keycloak-token')) {
            const { username, password } = getKeycloakCredentials();
            const { access_token } = await loginToKeycloak(username, password);
            // Log access token to STDOUT, so it can be used as environment variable.

            console.log(access_token);
            return access_token;
        }
    }
})();

module.exports = {
    setAuthHeader,
    setDraftPayload,
    setCreateAppointmentPayload,
    setUpdateAppointmentPayload,
    getDraftAppointmentPayload,
    buildDraftPayloadFromSlot,
    findFirstAvailableSlot,
    parseSlotDate,
};
