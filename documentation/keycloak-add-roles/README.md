[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

## Usage
Job to add internal_user to staff users in keycloak. 
### Arguments 

|Argument|Mandatory|Default| Description|
|--------|:-------|:------|:------|
|kc_client| No| add-roles-client|Keycloak Service account client ID|
|kc_secret| Yes | |Keycloak Service account client secret|
|kc_realm| No| vtkayq4c|IDP realm name

### Help command
`python add_roles_to_users.py -h`

### Run
Run with default values

`python add_roles_to_users.py -kc_secret=<secret value>`



## License

    Copyright 2019 Province of British Columbia

    Licensed under the Apache License, Version 2.0 (the "License"); you may not
    use this file except in compliance with the License. You may obtain a copy
    of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
    License for the specific language governing permissions and limitations
    under the License.

