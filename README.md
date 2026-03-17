# plainsite

**A Flask template for small business marketing sites that can't be hacked, load instantly, and cost almost nothing to run.**

`aktivpsykologerne/` is the working reference implementation — a real psychology practice site rebuilt after their WordPress got hacked. It serves as both a live example and the template for new clients.

---

## The problem this solves

Small businesses pay web agencies to maintain WordPress sites. Those sites:

- Get hacked constantly (PHP, plugins, outdated themes, brute-forced logins)
- Are slow without expensive caching infrastructure
- Break silently when a plugin updates
- Cost 2–5k DKK/month to maintain properly
- Are confusing for clients to edit, so they don't, and the content rots

The pattern of "WordPress site gets infected with malware/spam/redirects" is so common it's basically inevitable over a long enough timeline. This project started when exactly that happened — a psychologist's site started serving porn to some percentage of visitors.

---

## Why Flask + server-rendered HTML is the right answer

- **Zero attack surface.** No PHP, no plugin ecosystem, no CMS login page to brute-force, no SQL injection vector, no database to dump. The entire thing is Python rendering HTML templates. There is nothing to exploit.
- **Blazing fast.** Server-rendered HTML with no client-side JS framework. First byte is the full page. Faster than almost anything on the internet at this price point.
- **Runs on nothing.** A €5/month VPS handles 10–20 sites comfortably behind Nginx + Gunicorn. Most of the cost is profit.
- **Stable as a rock.** No moving parts. No cron jobs to update plugins. No compatibility matrix of PHP version × WordPress version × plugin versions. It just runs.
- **Perfect to work with alongside an LLM.** All content is in plain HTML templates and `.md` files. Any change is a one-shot edit. No abstractions to navigate, no build toolchain, no state to reason about.

---

## Business model

Charge **500–1000 DKK/month** per client as a retainer. Client texts or emails changes. You apply them with Claude in minutes and push. That's the entire workflow.

Target clients: **small professional practices** — psychologists, lawyers, accountants, physiotherapists, architects. People who need a credible web presence, have been burned by WordPress, and have no interest in maintaining it themselves.

**Economics per client:**
- Hosting: ~30 DKK/month (shared VPS)
- Time per month: 15–30 min average (most months: zero changes)
- Revenue: 500–1000 DKK/month
- Margin: ~95%

**New client workflow:**
1. `gh repo create clientname --template Rytterboi/plainsite`
2. Swap content, update 4–5 CSS variables for brand colours
3. Deploy to VPS, point DNS, `certbot --nginx`
4. Done in half a day

---

## What's built

- Server-rendered HTML with Jinja2 templates
- Blog from `.md` files — drop a file in `blog/`, it appears. Future-dated posts stay hidden.
- Full SEO stack: `sitemap.xml`, `robots.txt`, canonical URLs, Open Graph, JSON-LD structured data (Person, LocalBusiness, WebPage, WebSite)
- Google Search Console integration — one string in `run.py`
- Mobile-responsive, no JS
- Nix shell for reproducible dev environment (`nix-shell && python3 run.py`)
- Clean deploy path: Gunicorn + Nginx + certbot

---

## Roadmap

### Twilio contact form (next)
Contact form POSTs to Flask. Flask sends an SMS to the client's phone via Twilio REST API and optionally an email via SMTP. Client gets a notification within seconds of a lead coming in. No third-party form service, no data leaving your infrastructure, no monthly SaaS fee.

Config will just be four lines in `run.py`:
```python
TWILIO_ACCOUNT_SID = "..."
TWILIO_AUTH_TOKEN  = "..."
TWILIO_FROM        = "+45..."
NOTIFY_PHONE       = "+45..."
```

### Multi-outlet notifications
Route contact form submissions to wherever the client wants — SMS, email, Slack, WhatsApp. Client shouldn't have to check anything; the lead comes to them.

### Image handling
Lightweight image serving with automatic resizing/compression. Clients send photos, we drop them in `static/img/`, done.

### Analytics
Self-hosted (Plausible or Umami) or just Google Analytics tag — one include in `base.html`. No cookies for basic pageview counting.

### Per-client theming
A handful of CSS variables in `style.css` cover 90% of brand customisation (colours, fonts). Document the variables so swapping a theme is a 5-minute job.

### One-command deploy script
`./deploy.sh` that pulls latest, restarts Gunicorn, done. For clients on a VPS.

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

No VPS, no Nginx, no certbot, no SSH.

1. Push repo to GitHub
2. New project on [railway.app](https://railway.app) → "Deploy from GitHub repo"
3. Add custom domain in Railway dashboard → client points their DNS there
4. SSL is automatic

Push to GitHub → live in ~60 seconds. $5/month hobby plan runs many sites.
`Procfile` and `runtime.txt` are already in the repo.

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

Drop it in `blog/`. That's it.
