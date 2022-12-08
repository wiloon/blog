---
title: chrome weak up api, keep screen on, 屏幕常亮
author: "-"
date: 2022-11-08 15:45:12
url: chrome/weak/up/api
categories:
  - chrome
tags:
  - reprint
---
## chrome weak up api, keep screen on, 屏幕常亮

- chrome: enable-experimental-web-platform-features
- web 页面支持 https 才能使用 wake lock api
- android: 系统开启开发者模式

## chrome 74

chrome://flags/#enable-experimental-web-platform-features  
Note: Like most other powerful web APIs, the Wake Lock API is only available when served over HTTPS.  

## chrome 79+

Chrome Updates Experimental Wake Lock API Support  
<https://www.infoq.com/news/2019/11/chrome-wakelock-api/#:~:text=The%20Wake%20Lock%20API%20prevents%20some%20aspect%20of,this%20feature%2C%20adding%20promises%20and%20wake%20lock%20types>.

To use the Wake Lock API, developers need to enable the #enable-experimental-web-platform-features flag in chrome://flags.

chrome://flags
enable-experimental-web-platform-features

## keep-screen-on.js

```javascript
export function wakeLock () {
  if ('wakeLock' in navigator && 'request' in navigator.wakeLock) {
    console.log('wakeLock supported')
    try {
      navigator.wakeLock.request('screen')
      console.log('Wake Lock is active')
    } catch (e) {
      console.error(`${e.name}, ${e.message}`)
    }
  } else {
    console.log('no wakeLock support')
  }
}
```

### vue script

```typescript
<script lang="ts">
import HelloWorld from './components/HelloWorld.vue'
import { Component, Vue } from 'vue-property-decorator'
import { wakeLock } from './assets/keep-screen-on.js'

@Component({
  components: { HelloWorld }
})
export default class App extends Vue {
  drawer = false
  foo = ''

  mounted () {
    this.$vuetify.theme.dark = true
    wakeLock()
  }
}
</script>

```

#### demo

<https://wake-lock-demo.glitch.me/>

#### code

<https://glitch.com/edit/#!/wake-lock-demo?path=script.js%3A1%3A0>

#### w3c wake lock

<https://www.w3.org/TR/screen-wake-lock/>
<https://github.com/w3c/screen-wake-lock>

<https://developers.google.com/web/updates/2018/12/wakelock>
<https://chromestatus.com/features/4636879949398016>
<https://wake-lock.glitch.me/screen.html>
<https://medium.com/dev-channel/experimenting-with-the-wake-lock-api-b6f42e0a089f>
<https://bugs.chromium.org/p/chromium/issues/detail?id=257511>
