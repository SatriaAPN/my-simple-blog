# Dockerfile for React Frontend
FROM node:16-alpine

# Set working directory inside the container
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the app files
COPY . .

# Expose port 3000 (default React development server port)
EXPOSE 3000

# Start the development server
CMD ["npm", "start"]
