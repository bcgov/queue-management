# Keycloak Setup for TheQ and Online Appointments applications

#### Keycloak Overview
Keycloak is an open source identity and access management platform. FOI uses Keycloak as an identity broker platform to delegate authentication to other identity providers. 

#### Keycloak Base URL
|Environment|URL|
|---|---|
|DEV| https://sso-dev.pathfinder.gov.bc.ca/auth/admin/vtkayq4c/console/|
|TEST| https://sso-test.pathfinder.gov.bc.ca/auth/admin/vtkayq4c/console/|
|PROD|  https://sso.pathfinder.gov.bc.ca/auth/admin/vtkayq4c/console/|


#### Identity Providers
|IDP|Users|
|---|---|
|BC Services Card| Citizens using BC Services Card to book appointments online|
|IDIR| Internal staff users|
|BCeID|  Citizens to book appointments online and internal staff users|

#### Roles
Default role mapper is added for all identity ptovider to populate the role by default whenever someone logs in to the application for first time. 
This is done using a 'Hardcoded Role' mapper on identity provider. Below are the roles mapped for identity provider;
- IDIR : internal_user
- BCeID : online_appointment_user
- BC Services Card : online_appointment_user

Enable scope for the client which the application is using to innclude the roles in jwt token. For this;
1. Login to keycloak realm and select the client
2. Go to 'Scope' tab
3. Enable 'Full Scope Allowed'

#### Groups
For BCeID users who wants to access TheQ application would need internal_user role. Add those users to the group 'theq_internal_user' which would add the internal_user role to them.

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


##### Configure BC Services Card Identity Provider (Using Import)
To import the BC Services Card configuration,
1. Login to Keycloak as a realm administrator
2. Click on 'Import' Link
3. Select the file [keycloak config](/keycloak-config/config.json) for 'Exported json file'
4. Select 'Skip' for 'If a resource exists'
5. Import

##### Step 3) Change client id and secret for BC Services Card
1. Login to Keycloak as a realm administrator
2. Navigate to 'Identity Providers'
3. Select 'BC Services Card'
4. Scroll down to 'Client ID' and 'Client Secret' and paste the value received from IDIM team
5. Save 

##### Step 4) Add mappers for the attributes from BC Services Card
1. Login to Keycloak as a realm administrator
2. Navigate to 'Identity Providers'
3. Select 'BC Services Card'
4. Select 'Mappers' and create the mappers with the values from below table


|Name|Mapper Type|Claim|User Attribute Name|
|---|---|---|---|
|name|Attribute Importer|display_name|displayName|
|lastName|Attribute Importer|family_name|lastName|
|email|Attribute Importer|email|email|
|username|Username Template Importer|\${ALIAS}/\${CLAIM.sub}|
|online appointment role mapper|Hardcoded Role| online_appointment_user|
