FROM node:13.12.0-alpine as build
WORKDIR /app

COPY package.json package.json
COPY package-lock.json package-lock.json

RUN npm install --legacy-peer-deps

COPY . .
RUN npm run build

CMD ["npx", "-y", "http-server", "-p", "9000", "/app/build"]