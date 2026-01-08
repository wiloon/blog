# Multi-stage build for Hugo blog

# Stage 1: Build the Hugo site
FROM docker.io/library/alpine:3.22.2 AS builder

# Install Hugo Extended (required for PaperMod theme - requires v0.146.0+)
ENV HUGO_VERSION=0.152.2
ARG TARGETARCH
RUN apk add --no-cache wget ca-certificates libc6-compat libstdc++ git && \
    case "$TARGETARCH" in \
        amd64) HUGO_ARCH="amd64" ;; \
        arm64) HUGO_ARCH="arm64" ;; \
        *) echo "Unsupported architecture: $TARGETARCH" && exit 1 ;; \
    esac && \
    wget -q https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-${HUGO_ARCH}.tar.gz && \
    tar -xzf hugo_extended_${HUGO_VERSION}_linux-${HUGO_ARCH}.tar.gz && \
    chmod +x hugo && \
    mv hugo /usr/local/bin/hugo && \
    rm hugo_extended_${HUGO_VERSION}_linux-${HUGO_ARCH}.tar.gz && \
    apk del wget && \
    hugo version

# Set working directory
WORKDIR /blog

# Copy blog source files
COPY . .

# Clone PaperMod theme directly (since git submodules don't work well in Docker without .git dir)
RUN git clone --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod && \
    rm -rf themes/PaperMod/.git

# Build the Hugo site
RUN hugo

# Stage 2: Create production image with Nginx
FROM docker.io/library/nginx:1.29.3-alpine

# Clean nginx default content (必须在复制前清理，否则 nginx 默认的 index.html 不会被覆盖)
RUN rm -rf /usr/share/nginx/html/*

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
