FROM node:24-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production image: prod deps + build output, served by react-router-serve.
FROM node:24-alpine

WORKDIR /app
ENV PORT=8080

COPY package*.json ./
RUN npm ci --omit=dev

COPY --from=builder /app/build ./build

EXPOSE 8080
CMD ["npm", "run", "start"]
