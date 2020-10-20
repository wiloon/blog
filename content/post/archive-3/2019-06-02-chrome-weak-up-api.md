---
title: chrome weak up api
author: wiloon
type: post
date: 2019-06-02T14:19:27+00:00
url: /?p=14434
categories:
  - Uncategorized

---
### chrome 74
chrome://flags/#enable-experimental-web-platform-features

Note: Like most other powerful web APIs, the Wake Lock API is only available when served over HTTPS.

```
let wakeLock;
let wakeLockRequest;

async function toggleWakeLock() {
  if ('getWakeLock' in navigator) {
    console.log('', 'navigator.getWakeLock is supported');
    try {
      wakeLock = await navigator.getWakeLock("screen");
      updateStatus(wakeLock);
      // Listen for changes to the wakeLock
      wakeLock.addEventListener('activechange', (e) => {
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

```

### chrome 79+
https://www.infoq.com/news/2019/11/chrome-wakelock-api/#:~:text=The%20Wake%20Lock%20API%20prevents%20some%20aspect%20of,this%20feature%2C%20adding%20promises%20and%20wake%20lock%20types.
#### demo 
    https://wake-lock-demo.glitch.me/

#### code 
    https://glitch.com/edit/#!/wake-lock-demo?path=script.js%3A1%3A0
#### w3c wake lock
https://www.w3.org/TR/screen-wake-lock/
https://github.com/w3c/screen-wake-lock

https://developers.google.com/web/updates/2018/12/wakelock
https://chromestatus.com/features/4636879949398016
https://wake-lock.glitch.me/screen.html
https://medium.com/dev-channel/experimenting-with-the-wake-lock-api-b6f42e0a089f
https://bugs.chromium.org/p/chromium/issues/detail?id=257511

