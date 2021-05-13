FROM node
WORKDIR /app
COPY package.json .
RUN npm install --legacy-peer-deps --registry=https://registry.npm.taobao.org
COPY . .
EXPOSE 3000
CMD ["npm", "start"]