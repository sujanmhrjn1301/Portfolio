# Build stage
FROM node:18-alpine as builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Build the application
RUN npm run build && rm -rf node_modules

# Production stage
FROM node:18-alpine

# Security: Create non-root user
RUN addgroup -g 1000 appuser && adduser -D -u 1000 -G appuser appuser

WORKDIR /app

# Install serve in production stage only
RUN npm install -g serve

# Copy built application from builder
COPY --from=builder --chown=appuser:appuser /app/build ./build

# Security: Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000/ || exit 1

# Expose port
EXPOSE 3000

# Set environment (will be overridden)
ENV REACT_APP_API_URL=http://localhost:8000

# Start the application
CMD ["serve", "-s", "build", "-l", "3000"]
