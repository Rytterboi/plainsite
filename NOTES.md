# Client notes – Aktivpsykologerne

## Things still needed from client

Send these questions to Astrid / the client and come back with answers:

1. **Priser** – hvad koster en session?
   - Individuel voksen
   - Individuel barn/ung
   - Parterapi
   - Familiesamtale
   - Første/afklarende samtale

2. **Booking system** – bruger de et online bookingværktøj?
   (Calendly, Planway, Cliniko, MindBody, andet?)
   Hvis ja: hvad er embed-koden eller linket?

3. **Profilbillede** – et foto af Astrid til profil-siden.
   JPG/PNG er fint. Bare send filen.

4. **Google Search Console** – gå til search.google.com/search-console,
   tilføj domænet, vælg "HTML tag"-verificering, og send
   `content="..."` værdien her.

5. **Google Maps** – bekræft at adressen er præcis "Aldersrovej 38, 8200 Aarhus N"
   så kortet på kontakt-siden virker korrekt.

6. **Blog-artikler** – de tre eksempelartikler er placeholder-tekster på godt dansk.
   Astrid bør læse dem og markere hvad der skal rettes, tilføjes eller fjernes.
   Flere artikler = bedre SEO. Bare send emner eller tekst.

7. **"Bliv en aktivpsykolog"-siden** – er dette reel rekruttering, eller bare en placeholder?
   Hvis reel: hvad skal der stå?

8. **SMS/notifikationer (Twilio)** – kontaktformularen er ikke bygget endnu.
   Når den er klar: hvilken(e) numre/adresser skal notifikationer sendes til?
   (telefon til SMS via Twilio, og/eller mail)

---

## Deployment huskeliste

- [ ] Domæne peger på serveren
- [ ] SSL via certbot (`certbot --nginx`)
- [ ] Gunicorn kører bag Nginx
- [ ] Google Search Console verificeret og sitemap indsendt
- [ ] Priser udfyldt
- [ ] Booking-embed indsat
- [ ] Profilbillede tilføjet
- [ ] Blog-artikler godkendt af Astrid
