# Aktivpsykologerne – Flask website

Enkel, statisk Flask-app som erstatning for den hackede WordPress-side.

## Struktur

```
aktivpsykologerne/
├── app.py              # Flask routes (én fil)
├── requirements.txt    # flask>=3.0
├── templates/          # Jinja2 HTML-sider
│   ├── base.html       # Fælles header/footer/nav
│   ├── index.html
│   ├── profil.html
│   ├── ydelser.html
│   ├── terapiformer.html
│   ├── praktisk_info.html
│   ├── pris_og_betaling.html
│   ├── afbud.html
│   ├── kontakt.html
│   ├── book_en_tid.html
│   ├── vilkaar.html
│   └── bliv_aktivpsykolog.html
└── static/
    └── style.css       # Alt CSS i én fil
```

## Kør lokalt

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Åbn http://localhost:5000

## Opdater indhold

Al tekst ligger direkte i HTML-filerne under `templates/`. Ingen database, ingen CMS.
Rediger den relevante `.html`-fil og genstart appen (eller brug `debug=True` under udvikling).

## Deploy til produktion

**Med Gunicorn bag Nginx (anbefalet):**

```bash
pip install gunicorn
gunicorn -w 2 -b 127.0.0.1:8000 app:app
```

Nginx-config (eksempel):
```nginx
server {
    listen 80;
    server_name aktivpsykologerne.dk www.aktivpsykologerne.dk;

    location /static/ {
        alias /path/to/aktivpsykologerne/static/;
        expires 7d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Tilføj SSL med `certbot --nginx`.

## Booking

`templates/book_en_tid.html` har en placeholder til dit bookingsystem (Calendly, Planway,
Cliniko el.lign.). Indsæt embed-koden i den markerede sektion i filen.
