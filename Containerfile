# Multi-stage build for Hugo blog

# Stage 1: Build the Hugo site
FROM docker.io/library/alpine:3.18 AS builder

# Install Hugo
ENV HUGO_VERSION=0.70.0
RUN apk add --no-cache wget ca-certificates && \
    wget -q https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_${HUGO_VERSION}_Linux-64bit.tar.gz && \
    tar -xzf hugo_${HUGO_VERSION}_Linux-64bit.tar.gz && \
    mv hugo /usr/local/bin/ && \
    rm hugo_${HUGO_VERSION}_Linux-64bit.tar.gz && \
    apk del wget

# Set working directory
WORKDIR /blog

# Copy blog source files
COPY . .

# Build the Hugo site
RUN hugo --minify -v

# Stage 2: Create production image with Nginx
FROM docker.io/library/nginx:1.25-alpine

# Copy built static files from builder stage
COPY --from=builder /blog/public /usr/share/nginx/html

# Copy custom nginx configuration (optional)
# COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
