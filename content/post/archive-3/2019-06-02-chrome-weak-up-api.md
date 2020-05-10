---
title: chrome weak up api
author: wiloon
type: post
date: 2019-06-02T14:19:27+00:00
url: /?p=14434
categories:
  - Uncategorized

---
chrome://flags/#enable-experimental-web-platform-features

Note: Like most other powerful web APIs, the Wake Lock API is only available when served over HTTPS.

<pre><code class="language-javascript line-numbers">let wakeLock;
let wakeLockRequest;

async function toggleWakeLock() {
  if ('getWakeLock' in navigator) {
    console.log('', 'navigator.getWakeLock is supported');
    try {
      wakeLock = await navigator.getWakeLock("screen");
      updateStatus(wakeLock);
      // Listen for changes to the wakeLock
      wakeLock.addEventListener('activechange', (e) =&gt; {
        updateStatus(wakeLock);
      });
      wakeLockRequest = wakeLock.createRequest();
    } catch (ex) {

      console.error(ex);
    }
  } else {
    console.warn('navigator.getWakeLock is not supported');

  }

}

function updateStatus(wakeLock) {
  console.log(wakeLock);
}

</code></pre>

https://developers.google.com/web/updates/2018/12/wakelock
  
https://chromestatus.com/features/4636879949398016
  
https://wake-lock.glitch.me/screen.html

https://medium.com/dev-channel/experimenting-with-the-wake-lock-api-b6f42e0a089f
  
https://bugs.chromium.org/p/chromium/issues/detail?id=257511