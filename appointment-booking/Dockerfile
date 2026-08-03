# Stage 1: Builder
FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 2: Runtime
FROM nginx:1.25.3

COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir /app
COPY --from=builder /app/dist /app

EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
