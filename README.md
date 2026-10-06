# Retreat Blueprint Co. website

One-page marketing site for Retreat Blueprint Co. Plain HTML, CSS and a little JavaScript.
There is nothing to install and no build step: what you see in this folder is what gets published.

Live address (once connected): https://retreatblueprintco.com
Contact: hello.retreatblueprint@gmail.com

## What's in here

| Path | What it is |
| --- | --- |
| `index.html` | The page itself: all the text and structure |
| `css/styles.css` | Colours, fonts, layout |
| `js/main.js` | Testimonial cards and the voice-note players |
| `assets/img/` | Photos, favicon, and the social share image |
| `assets/audio/` | The two testimonial voice notes (`.ogg`) |
| `404.html` | Page shown for a broken link |
| `sitemap.xml`, `robots.txt` | Help Google find and index the site |
| `.nojekyll` | Tells GitHub Pages to publish the files exactly as they are |

## Preview on your computer

```bash
python3 scripts/serve.py 4173 .
```

Then open http://localhost:4173. Use this script rather than double-clicking `index.html`,
because the voice-note progress bars need a server that supports partial file requests.

## Publishing (GitHub Pages + custom domain)

The repo is `retreatblueprint/Retreatblueprintco`. Publishing is just pushing to `main`.
GitHub Pages rebuilds in about a minute.

Connect the domain after buying `retreatblueprintco.com`:

1. In the Cloudflare dashboard for the domain, open **DNS** and add these records, all set to **DNS only** (grey cloud):
   - Four `A` records for `@` pointing to `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - One `CNAME` record for `www` pointing to `retreatblueprint.github.io`
2. On GitHub, go to the repo's **Settings > Pages**, set **Custom domain** to `retreatblueprintco.com`, and save.
3. When the DNS check passes, tick **Enforce HTTPS**.

Setting the custom domain makes GitHub add a `CNAME` file to the repo. Run `git pull` before your next push.

## Changing things

- **Text:** edit `index.html`. Search for a phrase and change it.
- **Colours and fonts:** the variables at the top of `css/styles.css`.
- **A photo:** replace the file in `assets/img/` and keep the same filename. Keep each under about 300 KB.
  The `-1200` versions are what phones load, so replace those too.
- **Booking link:** search `calendly.com` in `index.html` (it appears in the nav and twice on the page).
- **Email:** search `hello.retreatblueprint@gmail.com` in `index.html` (CTA section and footer).

## Known limitations

- The voice notes are `.ogg` files (WhatsApp's format, same as the original page). They play in Chrome, Edge and Firefox,
  but Safari and iPhones may not play them. Re-exporting them as `.m4a` or `.mp3` and adding a second `<source>` line
  in `index.html` would cover those. This is worth testing on a real iPhone once the site is live.
