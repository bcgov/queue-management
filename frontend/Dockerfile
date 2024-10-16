FROM artifacts.developer.gov.bc.ca/docker-remote/node:20 as build-stage
ENV VUE_APP_PATH=/
WORKDIR /app
COPY ./package*.json ./
RUN npm install
COPY . .
RUN npm dedupe
RUN npm run build

FROM artifacts.developer.gov.bc.ca/docker-remote/nginx:1.25.3 as production-stage
COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir /app
COPY --from=build-stage /app/.nuxt /app/.nuxt
COPY --from=build-stage /app/static /app/static
COPY --from=build-stage /app/public /app/public

EXPOSE 8080:8080
CMD ["nginx", "-g", "daemon off;"]
