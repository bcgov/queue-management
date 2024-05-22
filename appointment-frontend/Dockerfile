FROM artifacts.developer.gov.bc.ca/docker-remote/node:14 as build-stage
ENV VUE_APP_PATH=/
WORKDIR /app
COPY ./package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM artifacts.developer.gov.bc.ca/docker-remote/nginx:latest as production-stage

# Update package list and upgrade nghttp2
RUN apt-get update && \
    apt-get install -y nghttp2 && \
    apt-get upgrade -y nghttp2 && \
    apt-get clean

    COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir /app
COPY --from=build-stage /app/dist /app
EXPOSE 8080:8080
CMD ["nginx", "-g", "daemon off;"]