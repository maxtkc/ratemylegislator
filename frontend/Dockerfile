# Multi-stage build for Gatsby application
FROM node:18-alpine AS development

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Expose development port
EXPOSE 8000

# Development command
CMD ["npm", "run", "develop", "--", "--host", "0.0.0.0"]

# Production build stage
FROM node:18-alpine AS build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Deployment stage (includes dev dependencies for gh-pages)
FROM node:18-alpine AS deploy

WORKDIR /app

# Install git for gh-pages deployment
RUN apk add --no-cache git

# Copy package files
COPY package*.json ./

# Install ALL dependencies (including dev dependencies like gh-pages)
RUN npm ci && npm cache clean --force

# Copy source code
COPY . .

# Production stage
FROM nginx:alpine AS production

# Copy custom nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built application
COPY --from=build /app/public /usr/share/nginx/html

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]