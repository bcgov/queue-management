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

- Get Google Map API Key from Google developer console. and use it as VUE_APP_GOOGLE_STATIC_MAP_API_KEY in .env.local file 



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
See [Configuration Reference](https://cli.vuejs.org/config/).
