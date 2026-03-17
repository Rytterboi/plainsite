# plainsite

**A Flask template for small business marketing sites that can't be hacked, load instantly, and cost almost nothing to run.**

The reference implementation is a real psychology practice site (`aktivpsykologerne.dk`) rebuilt after their WordPress got hacked and started serving porn to visitors. It took one afternoon. It now scores 100 on PageSpeed and has never had a security incident.

---

## The pitch

> *"Your website is slow, broken, and probably already compromised. I'll rebuild it properly, host it, and maintain it. Free for 3 months. After that, 500 DKK/month — and any change you need, just send me a message."*

That's the entire sales conversation. The downside risk for the client is zero. Most say yes.

**Target clients:** small local businesses with bad websites — psychologists, lawyers, dentists, physiotherapists, accountants, architects, tradespeople. The kind of site that was built in 2015, hasn't been touched since, runs on an outdated WordPress install, and is one plugin update away from disaster. There are millions of them.

---

## Why this beats WordPress for 90% of sites

Most small business websites are fundamentally just: a few pages of text, a contact form, maybe a blog. That's it. WordPress is a database-backed CMS with a plugin ecosystem and an admin panel to serve... a few pages of text, a contact form, and maybe a blog.

The mismatch is absurd. Here's what you get rid of:

| WordPress | plainsite |
|-----------|-----------|
| PHP runtime | Python renders HTML, done |
| MySQL database | No database |
| Plugin ecosystem | No plugins |
| CMS admin login (brute-force target) | No login page |
| Caching plugins to make it fast | Fast by default |
| Security plugins | Nothing to secure |
| Monthly plugin/theme updates | Nothing to update |
| Eventual hack (basically inevitable) | Structurally cannot happen |

The speed difference is visceral. Server-rendered HTML with no JS framework hits the browser as a complete page. PageSpeed 100 is realistic out of the box. Google notices. Users notice.

---

## The security story

WordPress powers ~43% of the web and is the most-attacked platform on the internet. PHP, plugins, themes, admin panels, XML-RPC endpoints, SQL injection, brute-forced logins — the attack surface is enormous and grows every time a plugin updates.

plainsite has no login page. No database. No PHP. No plugins. No XML-RPC. The attack surface is: a Python process rendering Jinja2 templates. There is genuinely nothing to exploit. "Can't be hacked" sounds like marketing but it's just structurally true here.

The psychologist site that started this project was serving porn to some percentage of visitors for an unknown period before anyone noticed. That's the real cost of WordPress for a client who doesn't have IT support.

---

## The business model

**Per client:**
- Setup: half a day to fork repo, swap content, deploy, point DNS
- Hosting: ~$0.25/month (Railway, shared across sites)
- Monthly time: 15–30 min average (most months zero — client has no changes)
- Revenue: 500–1000 DKK/month

**Client change workflow:**
1. Client sends a message (text, email, WhatsApp) with what they want changed
2. You tell Claude, it edits the file
3. `git push` → live in 60 seconds

That's it. No ticket system. No staging environment. No deployment pipeline. Just a text message and a git push.

**At 10 clients:** ~7000 DKK/month, ~3 hours/month of actual work. The rest is margin.

**New client setup:**
```bash
gh repo create clientname --template Rytterboi/plainsite
# swap content, update CSS variables, push
# connect to Railway, point DNS
# done
```

---

## Honest assessment of limitations

**UI/design:** Claude generates clean, professional HTML/CSS but it's not a bespoke designer. For most small local businesses this is more than sufficient — they're coming from a broken WordPress site that hasn't been updated since 2017. If a client needs something more polished, a one-time CSS pass from a freelance designer (3–5 hours) levels it up significantly, and you charge accordingly.

**Complex functionality:** Webshops, booking systems with real backend logic, membership areas, user accounts — wrong tool. plainsite is for marketing sites. Clients who need a webshop need something else. This is actually fine: that segment is harder to support and lower margin anyway.

**Client expectations around "self-editing":** Some clients will ask if they can edit the site themselves. The honest answer is no — but the counter is that they don't need to. They send a message, it's done same day. That's a better experience than fumbling in Gutenberg and accidentally breaking the layout.

**Not invented here risk:** Some clients or their IT people will be suspicious of anything that isn't WordPress/Squarespace/Wix. "What happens if you get hit by a bus?" is a real question. Answer: it's Python, Flask, and HTML files on GitHub. Any developer can pick it up in 20 minutes. The bus risk is actually lower than with a bespoke WordPress theme.

**Vendor dependency:** Railway is a dependency. If they raise prices or shut down, migration to any other Python host (Render, Fly.io, a VPS) is a one-hour job. The Dockerfile means it runs anywhere.

---

## What's built

- Server-rendered HTML, Jinja2 templates, zero client-side JS
- Blog from `.md` files — drop a file in `blog/`, it's live. Future-dated posts auto-hidden.
- Full SEO: `sitemap.xml`, `robots.txt`, canonical URLs, Open Graph, JSON-LD structured data
- Google Search Console: one string in `run.py`
- Mobile-responsive
- Dockerfile + Procfile — deploys anywhere
- Nix shell for local dev (`nix-shell && python3 run.py`)

---

## Roadmap

**Twilio contact form** *(next)*
Form POSTs to Flask → Twilio SMS to client's phone within seconds. No third-party form service. Config is 4 lines in `run.py`. This turns the site from a brochure into a lead capture machine and is probably the single highest-value feature to add.

**Multi-outlet notifications**
Route leads to SMS, email, Slack, WhatsApp — wherever the client actually looks.

**Image pipeline**
Client sends a photo → drop in `static/img/` → reference in template. Auto-compression would be nice but even without it the workflow is simple.

**Analytics**
Google Analytics or self-hosted Plausible — one include in `base.html`. Clients like seeing traffic numbers.

**Theme variables**
Document the 5–6 CSS variables that control brand colours and fonts. New client theming becomes a 10-minute job.

---

## Running locally

```bash
nix-shell
python3 run.py
# → http://localhost:5000
```

Without Nix:
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 run.py
```

## Deploy (Railway)

1. Push repo to GitHub
2. New project on [railway.app](https://railway.app) → "Deploy from GitHub repo"
3. Add custom domain → client points DNS there
4. SSL is automatic

`Procfile`, `runtime.txt` and `Dockerfile` are already in the repo. Push to GitHub → live in ~60 seconds.

---

## Adding a blog post

```markdown
---
title: Post title
date: 2025-06-01
description: One sentence shown in listings and meta tags.
---

Content in regular markdown.
```

Drop it in `blog/`. Done. Future-dated posts stay hidden automatically.
