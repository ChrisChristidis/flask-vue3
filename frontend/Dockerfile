# Use the official Node.js image
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# Build the Vue 3 app
RUN npm run build

# Expose port 8080 for the frontend application
EXPOSE 8080

# Serve the app with `npm run serve`
CMD ["npm", "run", "serve"]
