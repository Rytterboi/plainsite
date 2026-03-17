# CLAUDE.md – Aktivpsykologerne

## What this is

Simple Flask marketing site for psykolog Astrid Skovgaard Bjørnekær, Aarhus.
Intentionally no database, no CMS, no JavaScript framework. Hard to hack, fast to load.

## Stack

- Python / Flask – server-rendered Jinja2 templates
- `markdown` – blog posts parsed from `.md` files in `blog/`
- Plain CSS in `static/style.css`
- No JS (except optional booking embeds from third parties)
- Nix shell for reproducible environment (`shell.nix`)

## Run locally

```bash
nix-shell
python3 run.py
```

## Key files

| File | Purpose |
|------|---------|
| `run.py` | All routes + blog parser + SEO endpoints |
| `templates/base.html` | Shared layout, nav, JSON-LD, Open Graph |
| `templates/*.html` | One file per page |
| `static/style.css` | All styles, single file |
| `blog/*.md` | Blog posts (frontmatter: title, date, description) |
| `NOTES.md` | Outstanding client tasks |

## Adding a blog post

Create a file in `blog/` with this format:

```markdown
---
title: Titel på artiklen
date: 2025-06-01
description: En sætning der vises i oversigter og meta-beskrivelse.
---

Indhold i almindelig markdown...
```

Future-dated posts are automatically hidden until that date. No restart needed if running with a process manager; with `debug=True` Flask auto-reloads on file changes.

## Adding a new page

1. Add a route in `run.py`
2. Create `templates/yourpage.html` extending `base.html`
3. Add to nav in `templates/base.html` if needed
4. Add to `SITEMAP_PAGES` list in `run.py`

## Google Search Console

Set `GOOGLE_VERIFICATION_CODE` in `run.py`. The value goes in two places automatically:
- `<meta name="google-site-verification">` on every page
- Served at `/google{code}.html` for file-based verification

After verifying, submit `https://www.aktivpsykologerne.dk/sitemap.xml` in Search Console.

## Twilio SMS (planned)

When the contact form is built, Twilio will send an SMS to the client's phone on each
submission. Config will live in `run.py`:

```python
TWILIO_ACCOUNT_SID = "..."
TWILIO_AUTH_TOKEN  = "..."
TWILIO_FROM        = "+45..."
NOTIFY_PHONE       = "+45..."   # client's number
NOTIFY_EMAIL       = "..."      # optional fallback
```

The form POST handler will call Twilio's REST API (no extra library needed, just `urllib`
or `requests`) and optionally send an email via SMTP.

## Deployment (Railway)

Railway is the deploy target. No VPS, no Nginx, no certbot, no SSH.

1. Push repo to GitHub
2. New project on railway.app → "Deploy from GitHub repo"
3. Railway auto-detects Python, runs `gunicorn run:app` via `Procfile`
4. Add custom domain in Railway dashboard → client points DNS there
5. SSL is automatic

Each client site is a separate Railway service. $5/month hobby plan covers many sites.
Push to GitHub → live in ~60 seconds. Rollback is one click in the dashboard.

Requires `Procfile` and `runtime.txt` in repo root (both present).

## Content style

- Language: Danish throughout
- Tone: warm, professional, not clinical
- No jargon without explanation
- Blog posts should be helpful and findable via Google — write for the person searching
  "hvad er stress symptomer" not for other psychologists
