# Build Stage
FROM node:18 AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Baked into the bundle at build time. Defaults to localhost for dev builds.
ARG VUE_APP_API_URL=http://localhost:5050
ENV VUE_APP_API_URL=$VUE_APP_API_URL

RUN npm run build

# Serve with NGINX. The nginx:alpine image auto-runs envsubst on any
# /etc/nginx/templates/*.template file, substituting $PORT (and any other
# env vars) before nginx starts. Set PORT to whatever your host expects
# (80 locally, $PORT on Render, etc).
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf.template /etc/nginx/templates/default.conf.template
ENV PORT=80
CMD ["nginx", "-g", "daemon off;"]
