---
author: "-"
date: 2026-05-18T11:00:00+08:00
lastmod: 2026-05-18T12:52:24+08:00
title: "Pomodoro — A Minimal Timer PWA for Always-On Phone Display"
url: pomodoro
categories:
  - projects
tags:
  - original
  - vue
  - pwa
  - cloudflare
  - AI-assisted
---

**Live:** [https://pomodoro.wiloon.com](https://pomodoro.wiloon.com) · **Source:** [github.com/wiloon/pomodoro-vue](https://github.com/wiloon/pomodoro-vue)

---

## The Problem

Sitting for long periods is hard on your back and neck. I wanted a simple reminder to stand up and move every 30 minutes.

Most Pomodoro apps I tried were overly complex — they required accounts, had task lists, synced to the cloud, or sent too many notifications. I didn't need any of that. I just needed a countdown on a screen I could glance at.

My setup: an idle Google Pixel 3 placed next to my monitor, screen always on, running the timer. No distractions.

---

## What It Does

- Countdown timer with configurable focus and break intervals
- Audible alert when an interval ends — user can choose the alert sound
- Optional ambient sound (rain forest) playing throughout each interval
- Screen wake lock — keeps the phone screen on without touching it
- Works fully offline (PWA with Service Worker)
- No account, no sign-in, no data collection

---

## Tech Stack

| Layer          | Technology                                     |
|----------------|------------------------------------------------|
| Framework      | Vue 3 + TypeScript (Composition API)           |
| UI             | Vuetify 4 + Material Design Icons              |
| Router         | Vue Router 5                                   |
| Build          | Vite 8                                         |
| PWA            | vite-plugin-pwa (Workbox, auto-update)         |
| Analytics      | Umami (self-hosted, no cookies, privacy-first) |
| Hosting        | Cloudflare Pages                               |
| Infrastructure | OpenTofu (Cloudflare provider)                 |

---

## Key Design Decisions

**PWA over native app.** A web app avoids app store friction and works across all devices. The Wake Lock API handles keeping the screen on, and the Service Worker enables offline use — the two features that matter most for this use case.

**Pinia for shared state.** Timer state (current interval type, timestamp, pause status, session counts) lives in a Pinia store (`stores/timer.ts`) so it survives route navigation — switching to Settings and back no longer resets the countdown. Settings (alert sound, ding interval) are in a separate `stores/settings.ts` that auto-syncs to localStorage via `watch`, so changes apply immediately without a Save button. The core timer math stays in a plain TypeScript module (`src/utils/pomodoro.ts`), keeping the store free of formatting logic.

**Vuetify for UI.** I was already familiar with it and it ships a solid dark theme out of the box. The auto-import plugin keeps the bundle lean — only used components are included.

**Cloudflare Pages for hosting.** Static SPA, no backend, no server to maintain. Push to `main` → Cloudflare builds and deploys globally in under a minute. Infrastructure (DNS, custom domain, Pages project) is managed with OpenTofu for reproducibility.

---

## Battery Management

Running a phone plugged in 24/7 degrades the battery and can cause swelling. I use a smart USB switch paired with Macrodroid to do threshold-based charging:

- Battery drops below 20% → Macrodroid sends a command to the USB switch to start charging
- Battery rises above 80% → Macrodroid cuts power

This keeps the battery healthy long-term without any manual intervention.

---

## Infrastructure

The hosting stack is fully managed as code:

```hcl
resource "cloudflare_pages_project" "pomodoro" {
  name              = "pomodoro"
  production_branch = "main"

  source {
    type = "github"
    config {
      owner     = "wiloon"
      repo_name = "pomodoro-vue"
    }
  }

  build_config {
    build_command   = "pnpm build"
    destination_dir = "dist"
  }
}
```

A `cloudflare_record` CNAME points `pomodoro.wiloon.com` to the Pages subdomain. No manual DNS clicks, no console drift.

---

## Testing

- **Unit tests**: Vitest covers the core timer logic (`tick`, `pause`, `reset`, interval transitions)
- **E2E tests**: Playwright tests the full user flow in a real browser

```bash
pnpm test   # unit tests
pnpm e2e    # playwright e2e
```
