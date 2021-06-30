# SBC Appointment Booking

#### Copy these required files to the correct place in your directory structure
```
cd queue-management
mkdir -p appointment-frontend/public/config/kc

cp documentation/demo-files/keycloak.json appointment-frontend/public/config/kc/keycloak-public.json

cp documentation/demo-files/.env.appointments appointment-frontend/.env.local

--------

cd api
mkdir client_secrets
cd ..

cp documentation/demo-files/secrets.json api/client_secrets/secrets.json
```

Note: 
- inorder to book an appointment, add a user to the local keycloak with the role ***'online_appointment_user'***.

- if you need to use BCSC or BCeID services, please point to the dev keycloak


## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```


### Customize configuration
/public/config/configration.json
```
{
  "KEYCLOAK_CONFIG_URL": "./public/config/kc/keycloak-public.json",
  "VUE_APP_ROOT_API": "http://localhost:5000/api/v1",
  "hideBCServicesCard": false,
  "BCEIDRegistrationUrl": "https://www.test.bceid.ca/os/?7521&SkipTo=Basic",
  "disableSms": false,
  "VUE_APP_FEEDBACK_API": "http://localhost:5001/api/v1",
  "FEEDBACK_SERVICE_CHANNEL": "online",
  "FEEDBACK_ENABLED": true,
  "VUE_APP_HEADER_MSG": "Before you start – do you have the {link} BC Services Card Mobile app {link} or {link} Basic BCeID {link}? Login needed to confirm appointment.",
  "VUE_APP_HEADER_LINKS": "https://www.gov.bc.ca/bcservicescardapp {link} https://www.bceid.ca/",
  "VUE_APP_FOOTER_MSG": "Looking for ICBC Services? Ensure you are at the right place by visiting {link} icbc.com/locators",
  "VUE_APP_FOOTER_LINKS": "https://www.icbc.com/locators"
}
```
See [Configuration Reference](https://cli.vuejs.org/config/).
