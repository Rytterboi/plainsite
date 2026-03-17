from flask import Flask, render_template, Response, abort
from datetime import date
from pathlib import Path
import markdown
import re

app = Flask(__name__)

SITE_URL = "https://www.aktivpsykologerne.dk"

# Paste your Google Search Console verification code here.
# Get it from Search Console → Settings → Ownership verification → HTML tag.
# Copy only the value from content="..." – e.g. "abc123XYZ"
GOOGLE_VERIFICATION_CODE = ""

app.config["GOOGLE_VERIFICATION_CODE"] = GOOGLE_VERIFICATION_CODE

BLOG_DIR = Path(__file__).parent / "blog"


# ── Blog helpers ─────────────────────────────────────────────────────────────

def parse_post(path: Path) -> dict | None:
    """Parse a markdown file with optional YAML-style frontmatter (--- blocks)."""
    text = path.read_text(encoding="utf-8")
    meta = {"title": path.stem, "date": None, "description": ""}
    body = text

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                if ":" in line:
                    key, _, val = line.partition(":")
                    meta[key.strip()] = val.strip()
            body = parts[2]

    if meta["date"]:
        try:
            meta["date"] = date.fromisoformat(str(meta["date"]))
        except ValueError:
            meta["date"] = None

    meta["slug"] = path.stem
    meta["html"] = markdown.markdown(
        body,
        extensions=["extra", "nl2br", "sane_lists"],
    )
    return meta


def get_posts(published_only=True) -> list[dict]:
    posts = [parse_post(p) for p in sorted(BLOG_DIR.glob("*.md"))]
    posts = [p for p in posts if p]
    if published_only:
        posts = [p for p in posts if p["date"] and p["date"] <= date.today()]
    return sorted(posts, key=lambda p: p["date"] or date.min, reverse=True)


# ── Pages ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html", recent_posts=get_posts()[:3])

@app.route("/profil/")
def profil():
    return render_template("profil.html")

@app.route("/ydelser/")
def ydelser():
    return render_template("ydelser.html")

@app.route("/terapiformer/")
def terapiformer():
    return render_template("terapiformer.html")

@app.route("/praktisk-info/")
def praktisk_info():
    return render_template("praktisk_info.html")

@app.route("/pris-og-betaling/")
def pris_og_betaling():
    return render_template("pris_og_betaling.html")

@app.route("/afbud/")
def afbud():
    return render_template("afbud.html")

@app.route("/kontakt/")
def kontakt():
    return render_template("kontakt.html")

@app.route("/book-en-tid/")
def book_en_tid():
    return render_template("book_en_tid.html")

@app.route("/vilkaar-og-betingelser/")
def vilkaar():
    return render_template("vilkaar.html")

@app.route("/bliv-en-aktivpsykolog/")
def bliv_aktivpsykolog():
    return render_template("bliv_aktivpsykolog.html")


# ── Blog ─────────────────────────────────────────────────────────────────────

@app.route("/blog/")
def blog_index():
    return render_template("blog_index.html", posts=get_posts())

@app.route("/blog/<slug>/")
def blog_post(slug):
    # Only allow safe slugs
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", slug):
        abort(404)
    path = BLOG_DIR / f"{slug}.md"
    if not path.exists():
        abort(404)
    post = parse_post(path)
    if not post or not post["date"] or post["date"] > date.today():
        abort(404)
    return render_template("blog_post.html", post=post)


# ── SEO ──────────────────────────────────────────────────────────────────────

@app.route("/sitemap.xml")
def sitemap():
    today = date.today().isoformat()
    static_pages = [
        ("/",                        "weekly",  "1.0"),
        ("/profil/",                 "monthly", "0.9"),
        ("/ydelser/",                "monthly", "0.9"),
        ("/terapiformer/",           "monthly", "0.8"),
        ("/praktisk-info/",          "monthly", "0.7"),
        ("/pris-og-betaling/",       "monthly", "0.7"),
        ("/afbud/",                  "monthly", "0.5"),
        ("/kontakt/",                "monthly", "0.8"),
        ("/book-en-tid/",            "weekly",  "0.9"),
        ("/blog/",                   "weekly",  "0.8"),
        ("/vilkaar-og-betingelser/", "yearly",  "0.3"),
        ("/bliv-en-aktivpsykolog/",  "monthly", "0.5"),
    ]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, freq, priority in static_pages:
        lines.append(f"""  <url>
    <loc>{SITE_URL}{path}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>""")
    for post in get_posts():
        lines.append(f"""  <url>
    <loc>{SITE_URL}/blog/{post['slug']}/</loc>
    <lastmod>{post['date'].isoformat()}</lastmod>
    <changefreq>never</changefreq>
    <priority>0.7</priority>
  </url>""")
    lines.append("</urlset>")
    return Response("\n".join(lines), mimetype="application/xml")

@app.route("/robots.txt")
def robots():
    return Response(
        f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n",
        mimetype="text/plain",
    )

@app.route("/google<code>.html")
def google_verify(code):
    if GOOGLE_VERIFICATION_CODE and code == GOOGLE_VERIFICATION_CODE:
        return Response(f"google-site-verification: google{code}.html",
                        mimetype="text/plain")
    abort(404)


if __name__ == "__main__":
    app.run(debug=True)
