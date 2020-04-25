
export enum SessionStorageKeys {
    KeyCloakToken = 'KEYCLOAK_TOKEN',
    KeyCloakRefreshToken = 'KEYCLOAK_REFRESH_TOKEN',
    KeyCloakIdToken = 'KEYCLOAK_ID_TOKEN',
    ApiConfigKey = 'AUTH_API_CONFIG',
    BusinessIdentifierKey = 'BUSINESS_IDENTIFIER',
    UserFullName = 'USER_FULL_NAME',
    UserKcId = 'USER_KC_ID',
    PreventStorageSync = 'PREVENT_STORAGE_SYNC',
    AccountName = 'ACCOUNT_NAME',
    UserAccountType = 'USER_ACCOUNT_TYPE',
    PendingApprovalCount = 'PENDING_APPROVAL_COUNT',
    CurrentAccount = 'CURRENT_ACCOUNT',
    NamesRequestNumberKey = 'NR_NUMBER',
}

export enum Role {
    Staff = 'staff',
    Public = 'public_user',
    Edit = 'edit',
    Basic = 'basic',
    StaffAdmin = 'staff_admin',
    AnonymousUser = 'anonymous_user'
}

export enum Pages {
    USER_PROFILE = 'userprofile',
    CREATE_ACCOUNT = 'createaccount',
    DUPLICATE_TEAM_MESAGE = 'duplicateteam',
    PENDING_APPROVAL = 'pendingapproval',
    MAIN = 'account',
    SIGNIN = 'signin',
    SIGNOUT = 'signout',
    CREATE_USER_PROFILE = 'createuserprofile',
    SEARCH_BUSINESS = 'searchbusiness',
    DIRSEARCH_CONFIRM_TOKEN = 'dirsearch-confirmtoken',
    USER_PROFILE_TERMS = 'userprofileterms',
    USER_PROFILE_TERMS_DECLINE = 'unauthorizedtermsdecline',
    HOME = 'home'
}

export enum Account {
    ANONYMOUS = 'ANONYMOUS'
}

export enum IdpHint {
    BCROS = 'bcros',
    IDIR = 'idir',
    BCSC = 'bcsc'
}

export enum LoginSource {
    BCROS = 'BCROS',
    IDIR = 'IDIR',
    BCSC = 'BCSC'
}
