# Security

## TL;DR

There is no database. There is no login page. There is no CMS. There is no PHP.
There is no user input being processed or persisted anywhere.

The attack surface is: a Python process that receives a URL and returns an HTML string.

Hackers are welcome to try. There is genuinely nothing here.

---

## What doesn't exist (and why that matters)

| Attack vector | WordPress | plainsite |
|---|---|---|
| SQL injection | ✅ MySQL database | ❌ No database |
| Brute force login | ✅ /wp-admin login page | ❌ No login page |
| Plugin CVEs | ✅ Thousands of plugins | ❌ No plugins |
| PHP exploits | ✅ PHP runtime | ❌ No PHP |
| XML-RPC attacks | ✅ Enabled by default | ❌ Doesn't exist |
| File upload exploits | ✅ Media uploads | ❌ No file uploads |
| Session hijacking | ✅ User sessions | ❌ No sessions |
| Credential stuffing | ✅ Admin accounts | ❌ No accounts |
| Database dumps | ✅ User data, passwords | ❌ No database |
| Malware injection | ✅ Plugin/theme files | ❌ Immutable source files |
| Crypto mining injection | ✅ Common WordPress attack | ❌ Nothing to inject into |
| SEO spam injection | ✅ Very common | ❌ No write access |

---

## What the actual attack surface is

**1. Blog post slug parameter**

The only user-controlled input in the entire application is the URL slug
for blog posts (`/blog/<slug>/`). It is sanitised with a strict whitelist
before anything happens:

```python
if not re.fullmatch(r"[a-zA-Z0-9_-]+", slug):
    abort(404)
```

Anything that isn't letters, numbers, hyphens or underscores gets a hard 404
before it touches the filesystem. No path traversal. No injection. No creative
Unicode shenanigans.

**2. The contact form (not yet built)**

When built, the form will accept name, email and message fields. These will be:
- Validated server-side before processing
- Passed to the Twilio API as strings (no eval, no shell exec, no DB write)
- Never rendered back to any user (no XSS vector)
- Never persisted anywhere

The entire processing chain is: validate → send SMS → done.

**3. Jinja2 template rendering**

Jinja2 auto-escapes all variables by default. Even if user input somehow
reached a template, it would be escaped to plain text. Template injection
requires `{{ }}` syntax to reach the renderer unescaped — which requires
a developer to explicitly mark input as `| safe`, which we never do with
user-controlled data.

---

## The economic argument

WordPress sites get compromised at scale not because attackers care about
your dentist's website — but because exploitation is automated. Bots scan
millions of sites simultaneously, fingerprint the WordPress version and
installed plugins, cross-reference against CVE databases, and execute known
exploits automatically. No human involvement required. The payoff is:

- Stolen credit card data (WooCommerce)
- Spam and phishing infrastructure
- Crypto mining
- SEO spam injection (black hat link building)
- Ransomware staging

plainsite sites are not in any of these pipelines because:

1. They don't fingerprint as WordPress — no `/wp-admin`, no `wp-content`,
   no `generator` meta tag, no `X-Powered-By: PHP`
2. They have no database to dump
3. They have no credentials to steal
4. They have no compute to mine
5. They have no write access to inject SEO spam into
6. They serve no financial transactions

The ROI on attacking a plainsite site is effectively zero.
An attacker would have to specifically target one site, manually,
for no payoff. That doesn't happen.

---

## What could theoretically go wrong

**Denial of Service**
A flood of requests could slow the server. Mitigation: Railway's infrastructure
handles traffic spikes, and a rate limiter can be added to Flask in 5 lines if needed.
Impact: temporary slowdown. No data loss. No compromise.

**Dependency vulnerability**
Flask or one of its dependencies could have a CVE. Mitigation: minimal dependency
surface (`flask`, `markdown`, `gunicorn` — that's it), and updates are trivial.
This is orders of magnitude smaller than the WordPress plugin ecosystem.

**Server compromise at the infrastructure level**
If Railway itself were compromised, all hosted apps would be at risk.
This is true of any hosted platform. Mitigation: source of truth is always GitHub.
Recovery is a redeploy — minutes, not days.

**Developer error**
A future developer marks user input as `| safe` in a template, creating an XSS vector.
Mitigation: code review, and the surface is so small that this is easy to audit.

---

## Summary

plainsite didn't achieve security through clever engineering or exotic hardening.
It achieved security by not building the things that cause insecurity in the first place.

No database → no SQL injection.
No login → no brute force.
No plugins → no plugin CVEs.
No PHP → no PHP exploits.
No user sessions → no session attacks.
No persistent user input → no injection of any kind.

The most secure code is code that doesn't exist.
We deleted 20 years of WordPress complexity and got security for free as a side effect.

The hackers can absolutely come have a look.
There's just nothing here for them.
