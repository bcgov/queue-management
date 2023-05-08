# Single Sign-On Setup

## Background

Users have to prove their identity to the applications, but there are security risks if the applications store the users' identities (usernames, passwords, and more). The design used is that an *identity provider* (IdP), such as Active Directory (IDIR), stores the user identities and worries about things like security, protecting the passwords, multi-factor authentication, etc. To make it easier for the applications to use multiple identity providers, everything passes through an *identity broker*. The Red Hat Single Sign-On (SSO) identity broker is provided as a service by Platform Services, and it provides easy integration with multiple identity providers.

### Identity Providers

The Identity Providers used by the applications are:

|Identity Provider|Users|
|---|---|
|BCeID|Citizens: to book appointments<br>Staff: The Q and Service Flow|
|BC Services Card|Citizens: to book appointments|
|IDIR|Staff: The Q and Service Flow|

## Red Hat SSO Configuration

### Custom Realm

Platform Services prefers that all applications use the "default" Red Hat SSO *realm*. Ideally we would use the default realm but a "custom" realm is needed because it lacks (at minimum):

1. The default realm supports *roles* but the applications use *groups* for role based access control (RBAC)
1. The default realm does not support the BC Services Card

After requesting and receiving a custom realm, initial configuration is done by an application called [CSS](https://bcgov.github.io/sso-requests). The documentation from Platform Services should be used to set up an *integration* for dev, test, and prod using the *IDIR* and *Basic or Business BCeID* IdPs.

### Administration Consoles

Further configuration is done through the administration consoles, which are found at:

|Environment|Administration Console|
|---|---|
|dev|https://dev.loginproxy.gov.bc.ca/auth/admin/master/console/#/realms/servicebc|
|test|https://test.loginproxy.gov.bc.ca/auth/admin/master/console/#/realms/servicebc|
|prod|https://loginproxy.gov.bc.ca/auth/admin/master/console/#/realms/servicebc|

### Realm Settings

Set the following in the *Realm Settings*:

- In the *Themes* tab set the *Login Theme* to `bcgov-idp-login-no-brand`

### Roles

Set up the roles by importing [roles.json](./roles.json).

* `internal_user`: automatically used for anyone logging into The Q with IDIR.
* `online_appointment_user`: automatically used for anyone logging into the Appointment application with BCeID or BC Services Card.
* `reminder_job`: used for the appointment reminder cron job.

Note: some users want to run two copies of The Q so they can view different offices (rather than constantly switching offices). Since they cannot log in twice with the same identity, they log in a second time using a BCeID account via the "Keycloak" link at the bottom of the page. To set up these BCeID accounts an administrator logs into the Admininstration Console and adds the `/theq_internal_user` Group and removes the `online_appointment_user` Role Mapping.

### Identity Providers

The Platform Services [documentation](https://stackoverflow.developer.gov.bc.ca/questions/864) is used to configure the identity providers and mappers. The identity providers can be loaded from configuration files, so import the appropriate file for the environment:

|Environment|Identity Providers Configuration File|
|---|---|
|dev|[identity-providers-dev.json](./identity-providers-dev.json)|
|test|[identity-providers-test.json](./identity-providers-test.json)|
|prod|[identity-providers-prod.json](./identity-providers-prod.json)|

After importing the identity providers, each one needs to have its *Client ID* and *Client Secret* set. Credentials for BCeID and IDIR are found in the CSS application, and BCSC credentials come from IDIM.

#### Identity Provider Mappers

The identity provider mappers have to be created through the GUI. Note that each identity provider has a `Hardcoded Role` mapper to populate the default role when someone logs in to the application for first time.

Create these *Mappers* for the *bceid* identity provider:

|Name|Sync Mode Override|Mapper Type|Additional Fields|
|---|---|---|---|
|display_name|force|Attribute Importer|Claim: `display_name`<br>User Attribute Name: `display_name`|
|identity_provider|force|Hardcoded Attribute|User Attribute: `identity_provider`<br>User Attribute Value: `bceid`|
|online_appointment_user role|import|Hardcoded Role|Role: `online_appointment_user`|
|userid|force|Attribute Importer|Claim: `bceid_username`<br>User Attribute Name: `userid`|

Create these *Mappers* for the *bcsc* identity provider:

|Name|Sync Mode Override|Mapper Type|Additional Fields|
|---|---|---|---|
|display_name|force|Attribute Importer|Claim: `display_name`<br>User Attribute Name: `display_name`|
|identity_provider|force|Hardcoded Attribute|User Attribute: `identity_provider`<br>User Attribute Value: `bcsc`|
|online_appointment_user role|import|Hardcoded Role|Role: `online_appointment_user`|
|userid|force|Attribute Importer|Claim: `sub`<br>User Attribute Name: `userid`|
|username|force|Username Template Importer|Template: `${CLAIM.sub}@${ALIAS}`<br>Target: `LOCAL`|

Create these *Mappers* for the *idir* identity provider:

|Name|Sync Mode Override|Mapper Type|Additional Fields|
|---|---|---|---|
|display_name|force|Attribute Importer|Claim: `display_name`<br>User Attribute Name: `display_name`|
|identity_provider|force|Attribute Importer|Claim: `identity_provider`<br>User Attribute Name: `identity_provider`|
|internal_user role|import|Hardcoded Role|Role: `internal_user`|
|userid|force|Attribute Importer|Claim: `idir_username`<br>User Attribute Name: `userid`|

### Client Scopes

Create a client scope for Service Flow:

Click the *Create* button and enter:
- Name: `camunda-rest-api`
- Description: `Camunda API ReST Access`

Click the *Save* button. In the *Mappers* tab click the *Create* button and enter:
- Name: `camunda-rest-api`
- Mapper Type: `Audience`
- Included Custom Audience: `camunda-rest-api`

Click the *Save* button.

### Clients

The clients and their mappers can be loaded from configuration files, so import the appropriate file for the environment:

|Environment|Clients Configuration File|
|---|---|
|dev|[clients-dev.json](./clients-dev.json)|
|test|[clients-test.json](./clients-test.json)|
|prod|[clients-prod.json](./clients-prod.json)|

After importing the clients, some need to have secrets generated. In the *Credentials* tab click the *Regenerate Secret* button for each of these clients:

* forms-flow-bpm
* theq-appointment-reminder
* theq-postman

TODO: service account roles for forms-flow-bpm needs realm-management: manage-users, query-groups, query-users, view-users
TODO: camunda-rest-api mapper in forms-flow-bpm?

#### Groups

The groups are created by importing the [groups.json](./groups.json) file, *but this is a destructive create* - any group members will be lost. (Perhaps a non-destructive way is possible? It would be nice. This file is still important, though, because it can be eventually be used when Keycloak is set up in the devcontainers).

### Users

Some internal users need to be manually added.

#### Postman / Newman Testing

Three users are needed to run the automated API tests.

##### cfms-postman-non-operator
1. Click the `Add user` button, enter the username `cfms-postman-non-operator`, and click `Save`
1. In the `Credentials` enter the password, set `Temporary` to `Off`, and click `Set Password`
1. In the `Role Mappings` tab add `internal_user`

##### cfms-postman-operator
1. Click the `Add user` button, enter the username `cfms-postman-operator`, and click `Save`
1. In the `Credentials` enter the password, set `Temporary` to `Off`, and click `Set Password`
1. In the `Role Mappings` tab add `internal_user`

##### cfms-postman-public-user
1. Click the `Add user` button, enter the username `cfms-postman-public-user`, and click `Save`
1. In the `Credentials` enter the password, set `Temporary` to `Off`, and click `Set Password`
1. In the `Role Mappings` tab add `online_appointment_user`

---
---
---

# TODO - finish everything below here.

##### Create a custom authentication flow
Keycloak by default needs email as part of the user profile and asks the user to fill it in if the profile doesn't have it. For our application there will be users who doesn't have verified email address linked with their BC Services Card.

To prevent Keycloak asking the user to fill out email if the profile doesn't have email address, create a custom authentication flow to bypass this page.

1. Login to Keycloak as a realm administrator
2. Navigate to 'Authentication' tab
3. Select First Broker Login
4. Click on 'Copy' button on the right and name it as 'BCSC first broker login'
5. Select 'Actions' link against 'Review Profile' and click on 'Config'
6. Select 'off' for the value 'Update Profile on First Login'
7. Save. 

#### Disable keycloak account linking
To not allow users to link a verified account with a unverified account. There could be scenario where a Basic BCeID user uses the same email address (unverified) as the BC Services Card user’s email address (verified). IN this case if we allow BCeID user to link the BCSC user account, that may open some security issues. If we have a requirement for user linking, we will need to make sure we have the ability to confirm both users are same. 

1. Disable 'Confirm Link Existing Account’ from the custom first broker login
2. Disable 'Verify Existing Account By Email’ from the custom first broker login
3. Add this custom first broker login for both BCeID and BCSC

## Tips
- Want to know the version of Red Hat SSO? Click your name at top right and then *Server Info*.
- Want to know the version of Keycloak used by Red Hat SSO? https://access.redhat.com/articles/2342881. Match your application JavaScript libraries to this.
- If you get an `invalidFederatedIdentityActionMessage` it's because your logged in with one of BCeID and IDIR, and then trying to log in with the other one. Incognito is your friendo.

# TODO: CONFIGURATION

*what's this?* Manually set Service Account Roles to: offline_access, reminder_job, uma_authorization - is it for manually created Users?

formsflow - the forms-flow-ai secrets (). the forms-flow-web-config configmap (REACT_APP_KEYCLOAK_URL, REACT_APP_KEYCLOAK_URL_REALM)

newman tests

Update second appointment
 - passes but API throws exception
ERROR    (root) <appointment_put.py>.put: Error on token generation - 'NoneType' object has no attribute 'email_paragraph'
Traceback (most recent call last):
  File "/workspace/api/app/resources/bookings/appointment/appointment_put.py", line 107, in put
    send_email(request.headers['Authorization'].replace('Bearer ', ''), *get_confirmation_email_contents(appointment, office, office.timezone, user))
  File "/workspace/api/app/utilities/email.py", line 96, in get_confirmation_email_contents
    service_email_paragraph = appointment.service.email_paragraph
AttributeError: 'NoneType' object has no attribute 'email_paragraph'

Public User Appointments
↳ Authenticate and create user
 - public_user fields need to be set:
    bools - fail
    bools + phone - success
    phone - fail

Public User Appointments
Book an appointment
