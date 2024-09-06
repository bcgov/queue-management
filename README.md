[![img](https://img.shields.io/badge/Lifecycle-Stable-97ca00)]
## Queue Managment System

The Queue Managment System will be used to manage the citizen flow and provide analtyics for our Service BC locations. This system is designed to be used for government offices with a large number of services.

## Technology Stack Used

Single Signon using KeyCloak. This is used so that we don't need to manage the security concerns of passwords within the application. This also integrates to internal authentication model.

Designed for use in an application platform buld for containers specifically OpenShift:

- VueJS & BootStrap for Front End
- Flask & Python for API Backend
- EDB (Postgres)
- Redis
- Ngnix

## Features

Designed to accomodate multiple locations.  
Designed for both reception based offices and direct counter offices.

Additional features for Reception offices:

- Waiting queue displayed
- Citizens are called by name
- Digital Signage includes Current number of people waiting
- Handles a Quick Transaction Counter
- Ability to invite next citizen or pick from the waiting queue

Basic Digital Signage URLs per office

- Date and Time based on TimeZone
- MP4 to display messageing

Hold Queue

- Allows staff to place citizen tickets on hold

Track Channels of an interaction from In Person, Phone, etc.

Service Listings

- Sorted by category
- Searching service listings includes descriptions
- Hovering over a service listing displays descriptions
- Ability to customize service listing per Office
- Ability to hide Services from Digital Signage display
- Ability to add multiple services in one interaction

Office Status Panel

- Provides a manager the ability to see counter interaction details

Service Appointments (Optional)

- Calendar for booking appointments
- Ability to Checkin clients and place them at the top of the queue

Room Booking and Exam Invigilation (Optional)

- Manage Industry Trade Authority Group and Individual Exams
- Manage Other (Basic Exams)
- Manage General Room Booking
- Report on Exams

Basic Administration Panels to add, update and delete:

- Offices
- Customer Service Reps
- Service Listing
- Channels
- Roles
- Invigilators
- Exam Types
- Rooms
- Counter Types

Feedback

- Sends to Teams and / or Service Now and / or Rocket Chat

Analytics

- Key timing events are sent to snowplow for analysis and reporting
- Data is also stored in the Patroni Postgres database as an alternative method to extract analytics

## Requirements

Requires KeyCloak and additional Openshift / Kubernetes Config Maps

- keycloak.json is required in Front End Container in the following location: /var/www/html/static/keycloak

  {
  "realm": "",
  "auth-server-url": "" ,
  "ssl-required": "",
  "resource": "",
  "credentials": {
  "secret": ""
  }
  }

- secrets.json is required in API Container in the following location: /opt/app-root/src/client_secrets

  {
  "web": {
  "realm_public_key": "",
  "issuer": "" ,
  "auth_uri": "" ,
  "client_id": "",
  "client_secret": "",
  "redirect_urls": [
  ""
  ],
  "userinfo_uri": "" ,
  "token_uri": "" ,
  "token_introspection_uri": ""  
   }
  }

- Digital Signage video (with the name of sbc.mp4) needs to be manually placed in /var/www/html/static/videos

The openshift templates are used for build configs and deployment configs

Additional Enviornment Variables for API pods are used:

TEAMS_URL - to integrate feedback to Teams
THEQ_SNOWPLOW_ENDPOINT - where snowplow events are sent
THEQ_SNOWPLOW_APPID - Application ID for snowplow
THEQ_SNOWPLOW_NAMESPACE - Snowplow events namespace
THEQ_SNOWPLOW_CALLFLAG - disable/enable snowplow (Value: True or False)

## [Installation](documentation/Readme.md)

Additional information can be found in the [documention](documentation/Readme.md) folder.

## Getting Help or Reporting an Issue

To report bugs/issues/feature requests, please file an [issue](../../issues).

## How to Contribute

_If you are including a Code of Conduct, make sure that you have a [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) file, and include the following text in here in the README:_
"Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms."

## License

Detailed guidance around licenses is available
[here](/BC-Open-Source-Development-Employee-Guide/Licenses.md)

Attach the appropriate LICENSE file directly into your repository before you do anything else!

The default license For code repositories is: Apache 2.0

Here is the boiler-plate you should put into the comments header of every source code file as well as the bottom of your README.md:

    Copyright 2015 Province of British Columbia

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

For repos that are made up of docs, wikis and non-code stuff it's Creative Commons Attribution 4.0 International, and should look like this at the bottom of your README.md:

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/80x15.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">YOUR REPO NAME HERE</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">the Province of Britich Columbia</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

and the code for the cc 4.0 footer looks like this:

    <a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons Licence"
    style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/80x15.png" /></a><br /><span
    xmlns:dct="http://purl.org/dc/terms/" property="dct:title">YOUR REPO NAME HERE</span> by <span
    xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">the Province of Britich Columbia
    </span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">
    Creative Commons Attribution 4.0 International License</a>.