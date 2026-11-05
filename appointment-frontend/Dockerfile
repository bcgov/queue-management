FROM artifacts.developer.gov.bc.ca/docker-remote/node:24.21.0 AS build-stage

WORKDIR /app

ENV CYPRESS_INSTALL_BINARY=0 \
    PUPPETEER_SKIP_DOWNLOAD=true

COPY package*.json ./
RUN npm ci --ignore-scripts

COPY . .
RUN npm run build

FROM artifacts.developer.gov.bc.ca/docker-remote/nginx:1.31.7 AS production-stage

COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /app
COPY --from=build-stage /app/dist /app

EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]