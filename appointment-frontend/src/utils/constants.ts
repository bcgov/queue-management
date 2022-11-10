
export enum SessionStorageKeys {
    KeyCloakToken = 'KEYCLOAK_TOKEN',
    KeyCloakRefreshToken = 'KEYCLOAK_REFRESH_TOKEN',
    KeyCloakIdToken = 'KEYCLOAK_ID_TOKEN',
    ApiConfigKey = 'AUTH_API_CONFIG',
    UserFullName = 'USER_FULL_NAME',
    UserKcId = 'USER_KC_ID',
    PreventStorageSync = 'PREVENT_STORAGE_SYNC',
    AccountName = 'ACCOUNT_NAME',
    UserAccountType = 'USER_ACCOUNT_TYPE',
    CurrentUserProfile = 'CURRENT_USER_PROFILE',
}

export enum Role {
    OnlineAppointmentUser = 'online_appointment_user',
    Public = 'public_user',
    Edit = 'edit',
    Basic = 'basic',
}

export enum Pages {
    SIGNIN = 'signin',
    SIGNOUT = 'signout',
    HOME = 'home'
}

export enum IdpHint {
    BCEID = 'bceidboth',
    IDIR = 'idir',
    BCSC = 'bcsc'
}

export enum LoginSource {
    BCEID = 'BCEID',
    IDIR = 'IDIR',
    BCSC = 'BCSC'
}

export enum ServiceAvailability {
    SHOW = 'Availability.SHOW',
    HIDE = 'Availability.HIDE',
    DISABLE = 'Availability.DISABLE'
}
