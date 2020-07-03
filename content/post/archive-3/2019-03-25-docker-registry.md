---
title: docker registry
author: wiloon
type: post
date: 2019-03-25T15:01:06+00:00
url: /?p=13951
categories:
  - Uncategorized

---
curl -XGET https://registry.docker-cn.com/v2/nextcloud/tags/list

```bash
podman run -d \
-p 5000:5000 \
--name registry \
-v docker-registry:/var/lib/registry \
registry:latest

docker push registry.wiloon.com/foo:v0.0.1
docker pull registry.wiloon.com/foo:v0.0.1
```

### nginx config

自签证书

<code class="line-numbers">upstream docker-registry {
    server 192.168.50.220:5000;
 }

  ## Set a variable to help us decide if we need to add the
  ## 'Docker-Distribution-Api-Version' header.
  ## The registry always sets this header.
  ## In the case of nginx performing auth, the header is unset
  ## since nginx is auth-ing before proxying.
# map $upstream_http_docker_distribution_api_version $docker_distribution_api_version {
#   '' 'registry/2.0';
# }

server {
    listen 443 ssl;
    server_name registry.wiloon.com;

    # SSL
    ssl_certificate /etc/nginx/cert/server.crt;
    ssl_certificate_key /etc/nginx/cert/server.key;

    # Recommendations from https://raymii.org/s/tutorials/Strong_SSL_Security_On_nginx.html
    ssl_protocols TLSv1.2;
    ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH';
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;

    # disable any limits to avoid HTTP 413 for large image uploads
    client_max_body_size 0;

    # required to avoid HTTP 411: see Issue #1486 (https://github.com/moby/moby/issues/1486)
    chunked_transfer_encoding on;

    location /v2/ {
      # Do not allow connections from docker 1.5 and earlier
      # docker pre-1.6.0 did not properly set the user agent on ping, catch "Go *" user agents
      if ($http_user_agent ~ "^(docker/1.(3|4|5(?!.[0-9]-dev))|Go ).*$" ) {
        return 404;
      }

      # To add basic authentication to v2 use auth_basic setting.
      #auth_basic "Registry realm";
      #auth_basic_user_file /etc/nginx/conf.d/nginx.htpasswd;

      ## If $docker_distribution_api_version is empty, the header is not added.
      ## See the map directive above where this variable is defined.
      # add_header 'Docker-Distribution-Api-Version' $docker_distribution_api_version always;

      proxy_pass                          http://docker-registry;
      proxy_set_header  Host              $http_host;   # required for docker client's sake
      proxy_set_header  X-Real-IP         $remote_addr; # pass on real client's IP
      proxy_set_header  X-Forwarded-For   $proxy_add_x_forwarded_for;
      proxy_set_header  X-Forwarded-Proto $scheme;
      proxy_read_timeout                  900;
    }
}
```

https://docs.docker.com/registry/recipes/nginx/