---
title: redis pub sub
author: wiloon
type: post
date: 2017-12-18T13:47:16+00:00
url: /?p=11635
categories:
  - Uncategorized

---
<pre><code class="language-bash line-numbers">redis-cli -h redis.wiloon.com
SUBSCRIBE channel0
publish channel0 message0
</code></pre>

http://redisbook.readthedocs.io/en/latest/feature/pubsub.html