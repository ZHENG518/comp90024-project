FROM node:10
# RUN npm config set https-proxy http://wwwproxy.unimelb.edu.au:8000
COPY ./ /app
WORKDIR /app
RUN npm install && npm run build

FROM nginx
RUN mkdir /app
COPY --from=0 /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf