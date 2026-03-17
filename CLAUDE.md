# CLAUDE.md – plainsite

## What this is

A Flask template for small business marketing sites. No database, no CMS, no JS framework.
`aktivpsykologerne/` is the reference implementation — a real psychology practice rebuilt after their WordPress got hacked.

The guiding principle: **the complexity was never necessary.** Strip everything back to what the problem actually requires. A 5-page business site is just text, a phone number and a contact form. Flask + Jinja2 + markdown is the correct tool. Everything else is overhead.

## The business behind this

This is a micro web agency targeting small local businesses with broken/outdated/hacked WordPress sites. Psychologists, lawyers, dentists, accountants, tradespeople. The pitch:

> *"Your site stays as-is. I rebuild it, you compare. Free for 3 months. After that 500-1000 DKK/month — any change you need, just send a WhatsApp."*

**The product promise:** Send WhatsApp → change live same day. Never gets hacked. Never goes down. Blazing fast. Client thinks about their website zero times per month.

**Why this works as a business:**
- 95% margin per client (Railway hosting is cents)
- 15-30 min/month actual work per client at steady state
- Claude handles the mechanical work, developer handles the judgment
- Entire codebase fits in one context window — iteration is instant
- Stack never changes, never breaks, never needs updating

**Pricing:**
- 500 DKK/month — basic sites
- 1000 DKK/month — target for professional practices
- 1500 DKK/month — includes monthly SEO blog posts
- One-time fees for new pages, integrations, features

**Full time threshold:** ~35-40 clients at 1000 DKK = 35-40k DKK/month

## Why this stack

Python/Flask has been boring and stable for 20 years. Jinja2 templates from 2010 still work. No build step, no bundler, no `node_modules`, no hydration errors, no "server vs client component" confusion, no breaking changes. `gunicorn run:app` and it runs.

The entire codebase fits in one Claude context window. That's the superpower. Any change is a one-shot edit. Claude can see `run.py`, `base.html` and `style.css` simultaneously and understand the whole system. Try that with a Next.js app.

## Stack

- Python / Flask — server-rendered Jinja2 templates
- `markdown` — blog posts from `.md` files in `blog/`
- Plain CSS in `static/style.css` — single file, CSS variables for theming
- No client-side JS (except optional third-party booking embeds)
- Nix shell for reproducible local dev (`shell.nix`)
- Railway for deploy — push to GitHub → live in 60 seconds
- Docker for portability (`Dockerfile` in root)

## Run locally

```bash
nix-shell
python3 run.py
# → http://localhost:5000
```

## Key files

| File | Purpose |
|------|---------|
| `run.py` | All routes, blog parser, SEO endpoints. Start here. |
| `templates/base.html` | Shared layout, nav, JSON-LD, Open Graph, canonical URLs |
| `templates/*.html` | One file per page — edit directly for content changes |
| `static/style.css` | All styles in one file. CSS variables at the top for theming. |
| `blog/*.md` | Blog posts with frontmatter. Drop file → appears on site. |
| `NOTES.md` | Outstanding tasks for the current client |

## Adding a blog post

```markdown
---
title: Post title
date: 2025-06-01
description: One sentence for listings and meta tags.
---

Content in regular markdown.
```

Drop in `blog/`. Future-dated posts stay hidden automatically.

## Adding a new page

1. Add route in `run.py`
2. Create `templates/yourpage.html` extending `base.html`
3. Add to nav in `templates/base.html` if needed
4. Add to `SITEMAP_PAGES` in `run.py`

## New client setup

```bash
gh repo create clientname --template Rytterboi/plainsite
cd clientname
```

Then:
1. Edit page templates in `templates/` with client content
2. Update `SITE_URL` and contact details in `run.py`
3. Update primary colour in `static/style.css` (one line)
4. Drop client images in `static/img/`
5. Replace/add blog posts in `blog/`
6. Connect to Railway, point client DNS
7. Set `GOOGLE_VERIFICATION_CODE` once they verify Search Console

Half a day start to finish for a standard site.

## Syncing infrastructure from upstream

When plainsite template improves (new features, bug fixes, DaisyUI updates),
pull just the infrastructure files into a client fork — never the content files.

```bash
# Once: add upstream remote
git remote add upstream https://github.com/Rytterboi/plainsite

# Sync infrastructure (safe — these files don't contain client content)
git fetch upstream
git checkout upstream/main -- \
  run.py \
  templates/base.html \
  static/style.css \
  Procfile Dockerfile runtime.txt requirements.txt shell.nix CLAUDE.md

git commit -m "Sync infrastructure from upstream plainsite"
```

**What syncs:** routing, blog engine, SEO stack, navbar, footer, DaisyUI version, deploy config.
**What never syncs:** page templates, blog posts, client images, `SITE_URL`, `GOOGLE_VERIFICATION_CODE`.
No merge conflicts because you're explicitly checking out specific files, not merging.

## Per-client theming

One line in `static/style.css`:
```css
[data-theme="light"], :root {
  --color-primary: oklch(54% 0.08 155);  /* ← change this */
}
```
Use [oklch.com](https://oklch.com) to pick a colour. Dark mode is handled automatically by DaisyUI.

## Google Search Console

Set `GOOGLE_VERIFICATION_CODE` in `run.py`. Automatically:
- Renders `<meta name="google-site-verification">` on every page
- Serves `/google{code}.html` for file-based verification

After verifying, submit `/sitemap.xml` in Search Console.

## Twilio contact form (next to build)

Contact form POSTs to Flask → Twilio SMS to client's phone within seconds.
No third-party form service. No data leaving our infrastructure. Config in `run.py`:

```python
TWILIO_ACCOUNT_SID = "..."
TWILIO_AUTH_TOKEN  = "..."
TWILIO_FROM        = "+45..."
NOTIFY_PHONE       = "+45..."
NOTIFY_EMAIL       = "..."   # optional fallback
```

This is the single highest-value feature to add. Turns the site from a brochure into a
lead capture machine. Client gets notified the moment someone fills out the form.

## Deploy (Railway)

No VPS, no Nginx, no certbot, no SSH.

1. Push repo to GitHub
2. New project on railway.app → "Deploy from GitHub repo"
3. Add custom domain → client points DNS there
4. SSL automatic

`Procfile`, `runtime.txt` and `Dockerfile` already in repo.
Push to GitHub → live in ~60 seconds. Rollback is one click.

## Roadmap

- [ ] **plainsite business website** — fork this template, build the plainsite.dk marketing site
      Decisions needed before building:
      - Name confirmed? (plainsite or something else)
      - Danish or English first?
      - Show pricing publicly or "contact us"?
      - Name/face behind it or keep anonymous for now?
      - This is the demo — it sells itself by being the product

- [ ] **Twilio contact form** — highest value next feature
      Form POST → Flask → Twilio SMS to client's phone within seconds.
      Config: 4 lines in run.py (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM, NOTIFY_PHONE)
      No third-party form service. No data leaving our infra.

- [ ] **Multi-outlet notifications** — SMS, email, WhatsApp routing per client preference

- [ ] **Image pipeline** — drop in `static/img/`, auto-compress

- [ ] **Analytics** — GA4 or Plausible, one include in `base.html`

## Content style (Danish sites)

- Warm, professional, not clinical
- Write blog posts for the person googling the problem, not for peers
- No jargon without explanation
- CTA on every page pointing to booking/contact
