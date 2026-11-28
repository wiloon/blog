# wiloon.com

Personal knowledge base and blog, live at **[wiloon.com](https://wiloon.com)**.

## About Me

Backend Engineer / Full-Stack Developer

- Languages: Java · Go · Python
- Databases: PostgreSQL · Redis · InfluxDB · MySQL
- Infrastructure: Docker · Kubernetes · AWS · Ansible · OpenTofu
- Daily driver: Arch Linux + KDE

## About This Blog

A long-running collection of notes, references, and write-ups accumulated over years of engineering work.
Content ranges from carefully curated technical guides to raw bookmarks — continuously being organized.

- **[About page](https://wiloon.com/about)** — full introduction and contact info

## Tech Stack

| | |
| --- | --- |
| Generator | Hugo Extended (version pinned in `Containerfile`) |
| Theme | PaperMod |
| Hosting | Cloudflare Pages |
| CI/CD | Cloudflare Pages build (`bash build.sh`), managed by OpenTofu |

## Local Development

```bash
# Live preview (Hugo Extended required)
task preview
# → http://localhost:1313/
```

文章插图（Page Bundle、PaperMod 封面）见 [`.ai/page-bundle-images.md`](.ai/page-bundle-images.md)。
