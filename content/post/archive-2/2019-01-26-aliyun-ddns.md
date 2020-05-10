---
title: aliyun ddns
author: wiloon
type: post
date: 2019-01-26T09:51:46+00:00
url: /?p=13487
categories:
  - Uncategorized

---
https://github.com/honwen/aliyun-ddns-cli
  
https://github.com/chenhw2/aliyun-ddns-cli

<pre><code class="language-bash line-numbers">aliyun-ddns-cli --access-key-id=ak0 --access-key-secret=sk0  auto-update --domain=domain0.wiloon.com --redo=600

docker run -d \
    -e "AKID=[ALIYUN's AccessKey-ID]" \
    -e "AKSCT=[ALIYUN's AccessKey-Secret]" \
    -e "DOMAIN=ddns.aliyun.win" \
    -e "REDO=600" \
    chenhw2/aliyun-ddns-cli

</code></pre>