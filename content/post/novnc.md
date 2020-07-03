+++
author = "w1100n"
date = 2020-06-28T15:23:44Z
title = "novnc"

+++
    podman run  \
    -e REMOTE_HOST=192.168.50.114 \
    -e REMOTE_PORT=5900 \
    -p 8082:8081 \
    -d \
    --name novnc-dell \
    dougw/novnc