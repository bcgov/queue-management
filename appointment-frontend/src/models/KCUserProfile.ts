// Do not remove the eslint-disable camelcase below as the Python data model uses
// snake_case and Vue can't translate it to camelCase easily.
/* eslint-disable camelcase */
export interface KCUserProfile {
    lastName: string;
    firstName: string;
    keycloakGuid: string;
    userName: string;
    roles: string[];
    email: string;
    fullName: string;
    loginSource: string;
    display_name: string;
}
