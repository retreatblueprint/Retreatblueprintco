#!/usr/bin/env python3
"""Builds the Field Notes section: field-notes/index.html and one page per article.

Each article is ONE file in content/field-notes/<slug>.html:
  - a JSON block inside an HTML comment at the top (title, date, status, description...)
  - then the article body as plain HTML.

Placeholders you can use in an article body:
  {{mid_cta}}          the short call to action after the short-answer box
  {{chart:<id>}}       a chart from CHARTS below

Status:
  "draft"      not built, not listed, not in the sitemap (use --preview to see drafts locally)
  "published"  built, listed on /field-notes/ and added to sitemap.xml

A published article must not contain any <mark class="todo"> or "[SHILA" placeholders:
the build stops with an error if it does.

Run from the repo root:
  python3 scripts/build_field_notes.py            # what goes live
  python3 scripts/build_field_notes.py --preview  # also builds drafts, for checking locally
"""
import datetime
import glob
import html
import json
import os
import re
import sys

SITE = "https://retreatblueprintco.com"
CAL = "https://calendly.com/hello-retreatblueprint/30min"
PREVIEW = "--preview" in sys.argv

AUTHOR = {
    "name": "Shila Kandiah",
    "role": "Retreat Operations Director, Retreat Blueprint Co.",
    "bio": "Shila has 10 years of operations management experience across healthcare, wellness and hospitality, and works with retreat centers, eco-lodges and wellness venues on their systems, teams and growth.",
    "avatar": "/assets/img/shila-avatar.jpg",
}

# ---------------------------------------------------------------- charts
CHARTS = {
    "cr-air-arrivals-2025": dict(
        title="Low season: September brought a third as many visitors as December",
        alt="Bar chart of international tourist arrivals to Costa Rica by air in 2025, by month. December was highest at 316,226 and September lowest at 104,246, about a third. The green season runs May to November.",
        caption='Source: <a href="https://www.ict.go.cr/en/documents/estad%C3%ADsticas/informes-estad%C3%ADsticos/recientes/3276-2025-12-llegadas-internacionales/file.html">ICT with DGME data</a>, international tourist arrivals by air, January to December 2025.',
        unit="air arrivals",
        rows=[("Jan", 266675), ("Feb", 270810), ("Mar", 312844), ("Apr", 231678), ("May", 189881), ("Jun", 217120),
              ("Jul", 242408), ("Aug", 182342), ("Sep", 104246), ("Oct", 129369), ("Nov", 225679), ("Dec", 316226)],
        band=(4, 10, "Green (low) season, May to November"),
        vmax=350000, ticks=(100000, 200000, 300000),
    ),
}


def _bar_svg(c, w, h, fs, short, cls):
    rows = c["rows"]
    left, right, top, bottom = (40, 68, 40, 30) if short else (52, 84, 44, 34)
    pw, ph = w - left - right, h - top - bottom
    band = pw / len(rows)
    bw = band * 0.62
    base = top + ph
    y = lambda v: base - v / c["vmax"] * ph
    peak = max(rows, key=lambda r: r[1])
    low = min(rows, key=lambda r: r[1])
    avg = sum(v for _, v in rows) / len(rows)
    k = lambda v: f"{round(v / 1000)}k"
    out = [f'<svg class="{cls}" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(c["alt"])}" font-size="{fs}">']
    b0, b1, blabel = c["band"]
    bx = left + b0 * band
    out.append(f'<rect x="{bx:.1f}" y="{top - 26}" width="{(b1 - b0 + 1) * band:.1f}" height="{ph + 26}" fill="#EEF4EE"/>')
    out.append(f'<text x="{bx + 6:.1f}" y="{top - 10}" fill="#4A6E4E">{"Green season" if short else blabel}</text>')
    for t in c["ticks"]:
        out.append(f'<line x1="{left}" x2="{left + pw}" y1="{y(t):.1f}" y2="{y(t):.1f}" stroke="rgba(90,72,50,.12)"/>')
        out.append(f'<text x="{left - 8}" y="{y(t) + 4:.1f}" text-anchor="end" fill="#6B6252">{k(t)}</text>')
    out.append(f'<line x1="{left}" x2="{left + pw}" y1="{base}" y2="{base}" stroke="rgba(90,72,50,.35)"/>')
    for i, (m, v) in enumerate(rows):
        x = left + i * band + (band - bw) / 2
        fill = "#985033" if (m, v) == low else "#CFC6B6"
        out.append(f'<rect x="{x:.1f}" y="{y(v):.1f}" width="{bw:.1f}" height="{base - y(v):.1f}" fill="{fill}" rx="2"><title>{m} 2025: {v:,} {c["unit"]}</title></rect>')
        out.append(f'<text x="{x + bw / 2:.1f}" y="{base + 20}" text-anchor="middle" fill="#6B6252">{m[0] if short else m}</text>')
        if (m, v) in (peak, low):
            col = "#985033" if (m, v) == low else "#2A2218"
            out.append(f'<text x="{x + bw / 2:.1f}" y="{y(v) - 7:.1f}" text-anchor="middle" font-weight="600" fill="{col}">{k(v)}</text>')
    out.append(f'<line x1="{left}" x2="{left + pw}" y1="{y(avg):.1f}" y2="{y(avg):.1f}" stroke="#5A4832" stroke-dasharray="4 4" stroke-opacity=".6"/>')
    out.append(f'<text x="{left + pw + 8}" y="{y(avg) + 4:.1f}" fill="#5A4832">Avg {k(avg)}</text>')
    out.append("</svg>")
    return "".join(out)


def chart_html(cid):
    c = CHARTS[cid]
    return (f'<figure class="fn-chart"><p class="fn-chart-title">{c["title"]}</p>'
            + _bar_svg(c, 720, 340, 13, False, "wide")
            + _bar_svg(c, 360, 300, 13, True, "narrow")
            + f'<figcaption>{c["caption"]}</figcaption></figure>')


# ---------------------------------------------------------------- photos
U = "https://images.unsplash.com/"


def photo_url(pid, w, h=None):
    return f"{U}{pid}?auto=format&fit=crop&w={w}" + (f"&h={h}" if h else "") + "&q=72"


def photo_html(pid, alt, caption=""):
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return (f'<figure class="fn-photo"><img src="{photo_url(pid, 1440)}" '
            f'srcset="{photo_url(pid, 720)} 720w, {photo_url(pid, 1440)} 1440w" sizes="(max-width:760px) 100vw, 720px" '
            f'alt="{html.escape(alt)}" loading="lazy" width="1440" height="900">{cap}</figure>')


# ---------------------------------------------------------------- articles
def load_articles():
    arts = []
    for path in sorted(glob.glob("content/field-notes/*.html")):
        src = open(path, encoding="utf-8").read()
        m = re.match(r"\s*<!--(.*?)-->", src, re.S)
        if not m:
            sys.exit(f"{path}: missing the JSON block at the top")
        meta = json.loads(m.group(1))
        meta["body"] = src[m.end():].strip()
        meta["path"] = path
        if meta["status"] == "published" and ('class="todo"' in meta["body"] or "[SHILA" in meta["body"]):
            sys.exit(f"{path}: still has [SHILA] placeholders; fill them in before publishing")
        if meta["status"] == "published" or PREVIEW:
            arts.append(meta)
    arts.sort(key=lambda a: a["date"], reverse=True)
    return arts


def words(body):
    return len(re.sub(r"<[^>]+>", " ", body).split())


def nice_date(d):
    dt = datetime.date.fromisoformat(d)
    return dt.strftime("%B %-d, %Y")


# ---------------------------------------------------------------- shared page head
BASE = open("buying-a-retreat.html", encoding="utf-8").read()
HEAD = BASE[: BASE.index('<header class="hero')]
MENU_V = re.search(r"js/menu\.js\?v=([\w-]+)", BASE).group(1)  # same version as the other pages
# pages live in /field-notes/, so every local path must start at the site root
HEAD = (HEAD.replace('href="css/', 'href="/css/').replace('href="assets/', 'href="/assets/')
        .replace("url('assets/", "url('/assets/").replace('src="js/', 'src="/js/'))
HEAD = HEAD.replace('<a href="/buying-a-retreat" class="dd-feature" aria-current="page">', '<a href="/buying-a-retreat" class="dd-feature">')
HEAD = HEAD.replace('<a href="/field-notes/">Field Notes</a>', '<a href="/field-notes/" aria-current="page">Field Notes</a>')

CSS = """
/* Field Notes */
.fn-head{background:var(--cream);padding:72px 24px 48px}
.fn-head .inner{max-width:760px}
.fn-crumb{font-size:.72rem;font-weight:500;letter-spacing:.13em;text-transform:uppercase;color:var(--terracotta);margin-bottom:1rem;display:flex;gap:.5rem;align-items:center}
.fn-crumb a{text-decoration:none}.fn-crumb a:hover{text-decoration:underline}
.fn-head h1{font-family:var(--serif);font-weight:400;font-size:clamp(2.1rem,5vw,3.3rem);line-height:1.12;letter-spacing:-.01em;text-wrap:balance;margin-bottom:1rem}
.fn-hero{max-width:1100px;margin:0 auto;padding:0 24px;transform:translateY(-1px)}
.fn-hero img{display:block;width:100%;height:clamp(220px,42vw,460px);object-fit:cover;border-radius:0 0 10px 10px;background:var(--cream-dark)}
.fn-photo{margin:1.75rem 0 2rem}
.fn-photo img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;border-radius:8px;background:var(--cream-dark)}
.fn-photo figcaption{font-size:.8rem;color:var(--muted);margin-top:.45rem}
.fn-dek{font-family:var(--serif);font-size:clamp(1.15rem,2.2vw,1.35rem);line-height:1.45;color:var(--earth-mid);max-width:36em;margin-bottom:1.5rem}
.fn-meta{display:flex;align-items:center;gap:12px;font-size:.88rem;color:var(--muted)}
.fn-meta img{width:40px;height:40px;border-radius:50%;object-fit:cover}
.fn-meta b{color:var(--earth);font-weight:500}
.fn-body{max-width:720px;margin:0 auto;padding:56px 24px 32px;font-size:1.07rem;line-height:1.75}
.fn-body > p,.fn-body > ul,.fn-body > ol{margin:0 0 1.15rem}
.fn-body h2{font-family:var(--serif);font-weight:400;font-size:clamp(1.5rem,3vw,1.85rem);line-height:1.25;margin:2.75rem 0 .85rem;text-wrap:balance}
.fn-body ul,.fn-body ol{padding-left:1.3rem}
.fn-body li{margin-bottom:.4rem}
.fn-body a{color:var(--sage-dark);text-underline-offset:3px}
.fn-body sup{font-size:.68em;line-height:0;margin-left:1px}
.fn-body sup a{text-decoration:none;color:var(--terracotta);font-weight:600}
.fn-k{font-size:.7rem;font-weight:600;letter-spacing:.13em;text-transform:uppercase;color:var(--terracotta);margin-bottom:.6rem}
.fn-answer{background:var(--sage-light);border-left:4px solid var(--sage-dark);border-radius:6px;padding:22px 26px;margin:1.75rem 0}
.fn-answer ol{margin:0;padding-left:1.2rem}.fn-answer li{margin-bottom:.35rem}
.fn-answer .fn-k{color:var(--sage-dark)}
.fn-mid{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;justify-content:space-between;border:1px dashed rgba(74,110,78,.45);border-radius:6px;padding:14px 18px;margin:0 0 2rem;font-size:.95rem;color:var(--earth-mid)}
.fn-mid a{font-weight:500;white-space:nowrap}
.fn-field{background:var(--cream-dark);border-left:4px solid var(--terracotta);border-radius:6px;padding:24px 28px;margin:2.5rem 0;font-family:var(--serif);font-size:1.12rem;line-height:1.6}
.fn-field .fn-k{font-family:var(--sans)}
.fn-table{overflow-x:auto;margin:1.25rem 0 1.25rem}
.fn-table table{width:100%;border-collapse:collapse;font-size:.92rem;line-height:1.5}
.fn-table th{text-align:left;font-weight:600;font-size:.75rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);border-bottom:2px solid var(--border);padding:10px 12px 8px 0}
.fn-table td{border-bottom:1px solid var(--border);padding:12px 12px 12px 0;vertical-align:top}
.fn-table td:nth-child(2){white-space:nowrap;font-weight:500}
.fn-chart{margin:1.75rem 0 2rem}
.fn-chart-title{font-family:var(--serif);font-size:1.15rem;line-height:1.35;margin-bottom:.5rem}
.fn-chart svg{display:block;width:100%;height:auto;font-family:var(--sans)}
.fn-chart svg.narrow{display:none}
.fn-chart figcaption{font-size:.8rem;color:var(--muted);margin-top:.4rem}
.fn-chart figcaption a{color:inherit}
@media (max-width:560px){.fn-chart svg.wide{display:none}.fn-chart svg.narrow{display:block}}
.fn-check{border:1px solid var(--border);border-radius:8px;padding:28px 28px 24px;margin:2.75rem 0;background:var(--warm-white);box-shadow:0 14px 34px rgba(42,34,24,.07)}
.fn-check h2{margin-top:0}
.fn-check ul{list-style:none;padding:0;margin:0 0 1.25rem}
.fn-check li{position:relative;padding-left:32px;margin-bottom:.7rem}
.fn-check li::before{content:"";position:absolute;left:0;top:.3em;width:18px;height:18px;border:1.5px solid var(--sage-dark);border-radius:3px}
.fn-print{font:inherit;font-size:.85rem;font-weight:500;color:var(--sage-dark);background:none;border:1px solid var(--sage-dark);border-radius:4px;padding:.5rem 1rem;cursor:pointer}
.fn-print:hover{background:var(--sage-light)}
.fn-next{background:#1E2F21;color:#EEF4EE;border-radius:8px;padding:30px;margin:2.75rem 0;display:grid;gap:14px;justify-items:start}
.fn-next .fn-k{color:#DDB797;margin:0}
.fn-next p{color:#C2D6C2}
.fn-next .btn{background:#fff;color:var(--sage-dark);border-color:#fff}
.fn-sources{margin-top:3rem;padding-top:1.5rem;border-top:1px solid var(--border);font-size:.86rem;line-height:1.6;color:var(--earth-mid)}
.fn-sources h2{font-size:1.15rem;margin:0 0 .75rem}
.fn-sources li{margin-bottom:.3rem}
.fn-sources li:target{background:#FFF6D6}
.fn-disclaimer{margin-top:1rem;font-style:italic;color:var(--muted)}
.fn-author{max-width:720px;margin:0 auto 72px;padding:0 24px}
.fn-author > div{display:grid;grid-template-columns:72px 1fr;gap:18px;align-items:center;border-top:1px solid var(--border);padding-top:28px}
.fn-author img{width:72px;height:72px;border-radius:50%;object-fit:cover}
.fn-author b{font-family:var(--serif);font-weight:500;font-size:1.1rem;display:block}
.fn-author span{font-size:.8rem;color:var(--muted);display:block;margin-bottom:4px}
.fn-author p{font-size:.92rem;color:var(--earth-mid)}
/* Editorial treatment (Oct 21): fewer boxes, labels and rails; reads like a printed field journal */
.fn-body > p:first-of-type::first-letter{font-family:var(--serif);float:left;font-size:3.6em;line-height:.82;padding:.08em .1em 0 0;color:var(--terracotta)}
.fn-k{font-family:var(--serif);font-style:italic;font-weight:400;font-size:1.05rem;letter-spacing:0;text-transform:none;color:var(--terracotta);margin-bottom:.5rem}
.fn-answer{background:none;border:0;border-top:1px solid var(--earth);border-bottom:1px solid var(--border);border-radius:0;padding:18px 0 20px;margin:2rem 0 2.25rem}
.fn-answer .fn-k{color:var(--earth)}
.fn-answer ol{list-style:none;padding:0;margin:0;counter-reset:a;display:grid;gap:.55rem}
.fn-answer li{counter-increment:a;display:grid;grid-template-columns:2rem 1fr;align-items:baseline;margin:0}
.fn-answer li::before{content:counter(a);font-family:var(--serif);font-size:1.35rem;line-height:1;color:var(--terracotta)}
.fn-mid{display:block;border:0;border-radius:0;padding:0;margin:0 0 2.25rem;font-size:.98rem;font-style:italic;color:var(--earth-mid)}
.fn-mid span{margin-right:.35rem}
.fn-mid a{font-style:normal;color:var(--sage-dark)}
.fn-field{background:none;border:0;border-top:1px solid var(--terracotta);border-bottom:1px solid var(--border);border-radius:0;padding:16px 0 18px;margin:2rem 0 2.25rem;font-family:var(--serif);font-size:1.12rem;line-height:1.6;color:var(--earth)}
.fn-field .fn-k{display:block;font-size:1rem;margin-bottom:.4rem}
.fn-field p+p{margin-top:.75rem}
.fn-check{border:0;border-top:3px double var(--earth);border-radius:0;box-shadow:none;background:none;padding:22px 0 8px;margin:3rem 0}
.fn-check ul{margin-bottom:1.25rem}
.fn-check li{padding:.7rem 0 .7rem 34px;margin:0;border-bottom:1px solid var(--border)}
.fn-check li::before{top:.95rem;border-radius:2px;border-color:var(--earth-mid)}
.fn-print{border-radius:3px}
.fn-next{background:var(--cream-dark);color:var(--earth);border-radius:0;padding:30px 30px 28px;gap:12px;margin:3rem 0}
.fn-next .fn-k{color:var(--earth);font-size:1.45rem;font-style:normal}
.fn-next p{color:var(--earth-mid)}
.fn-next .btn{background:var(--sage-dark);color:#fff;border-color:var(--sage-dark)}
.fn-photo img{border-radius:2px}
.fn-photo figcaption{font-style:italic}
.fn-hero img{border-radius:0}
@media (max-width:640px){.fn-field{font-size:1.06rem}.fn-next{padding:22px}}
mark.todo{background:#FFF0A8;color:var(--earth);padding:2px 5px;border-radius:3px;font-family:var(--sans);font-size:.92em}
.fn-draft{background:#FFF0A8;text-align:center;font-size:.85rem;padding:8px 16px}
/* index */
.fn-list{max-width:820px;margin:0 auto;padding:48px 24px 88px;display:grid;gap:18px}
.fn-card{display:grid;gap:8px;padding:28px;border:1px solid var(--border);border-radius:8px;background:var(--warm-white);text-decoration:none;color:var(--earth);transition:border-color .2s,transform .2s,box-shadow .2s}
.fn-card:hover{border-color:var(--sage-mid);transform:translateY(-2px);box-shadow:0 14px 34px rgba(42,34,24,.08)}
.fn-card.has-img{grid-template-columns:minmax(0,340px) minmax(0,1fr);gap:0;padding:0;overflow:hidden}
.fn-card.has-img img{display:block;width:100%;height:100%;min-height:240px;object-fit:cover;background:var(--cream-dark)}
.fn-card-txt{display:grid;gap:8px;align-content:center}
.fn-card.has-img .fn-card-txt{padding:28px}
@media (max-width:640px){.fn-card.has-img{grid-template-columns:1fr}.fn-card.has-img img{min-height:0;aspect-ratio:16/10;height:auto}.fn-card.has-img .fn-card-txt{padding:22px}}
.fn-card .fn-k{margin:0;font-size:.7rem;color:var(--terracotta)}
.fn-card h2{font-family:var(--serif);font-weight:400;font-size:1.55rem;line-height:1.25;text-wrap:balance}
.fn-card p{color:var(--earth-mid);font-size:.98rem}
.fn-card small{color:var(--muted);font-size:.82rem}
.fn-card em{font-style:normal;color:var(--sage-dark);font-weight:500;font-size:.9rem}
.fn-empty{color:var(--muted)}
@media (max-width:640px){.fn-hero{padding:0}.fn-hero img{border-radius:0}.fn-head{padding:48px 16px 36px}.fn-body{padding:40px 16px 24px;font-size:1.02rem}.fn-author,.fn-list{padding-left:16px;padding-right:16px}.fn-check,.fn-next{padding:22px}.fn-field,.fn-answer{padding:20px}}
@media print{
  html.print-check body > *:not(#fn-print-area){display:none!important}
  #fn-print-area{display:block!important}
  #fn-print-area .fn-check{margin:0;padding-top:12px}
  #fn-print-area .fn-print{display:none}
  .fn-print-src{margin-top:18px;font-size:10pt;color:#6B6252}
  .fn-print,.nav,footer,.cta,.wa-float{display:none!important}
}
#fn-print-area{display:none}
"""

PRINT_JS = "<script>document.addEventListener('click',function(e){var btn=e.target.closest('.fn-print');if(!btn)return;e.preventDefault();var r=document.documentElement,src=btn.closest('.fn-check'),box=document.getElementById('fn-print-area');if(!box){box=document.createElement('div');box.id='fn-print-area';document.body.appendChild(box)}box.innerHTML='';box.appendChild(src.cloneNode(true));var f=document.createElement('p');f.className='fn-print-src';f.textContent='From Field Notes by Retreat Blueprint Co. \u00b7 '+location.hostname+location.pathname;box.appendChild(f);r.classList.add('print-check');window.addEventListener('afterprint',function(){r.classList.remove('print-check')},{once:true});window.print()})</script>"


def head(title, desc, url, og_image, jsonld, og_type="article"):
    h = HEAD
    h = re.sub(r"<title>[^<]*</title>", f"<title>{html.escape(title)}</title>", h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(desc)}">', h, count=1)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{html.escape(title)}">', h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{html.escape(desc)}">', h, count=1)
    h = re.sub(r'<meta property="og:type" content="[^"]*">', f'<meta property="og:type" content="{og_type}">', h, count=1)
    h = re.sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{og_image}">', h, count=1)
    h = h.replace(f"{SITE}/buying-a-retreat", url)
    extra = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>\n<style>{CSS}</style>\n'
    return h.replace("</head>", extra + "</head>", 1)


def tail():
    return f'''<section class="sec cta wt" style="--wave:var(--warm-white)">
  <div class="cta-ov" aria-hidden="true"></div>
  <div class="inner">
    <p class="label">Start with a conversation</p>
    <h2 class="title">Questions about your retreat venue?</h2>
    <p class="lead">A free 30-minute call. No obligation, just a clear next step.</p>
    <a class="btn primary" href="{CAL}" target="_blank" rel="noopener">Book a free call</a>
    <p class="email"><a href="mailto:hello@retreatblueprintco.com?subject=Field%20Notes">hello@retreatblueprintco.com</a> · <a href="https://wa.me/16479702759" target="_blank" rel="noopener">WhatsApp</a></p>
  </div>
</section>

<footer><span class="f-brand"><span class="f-logo">Retreat Blueprint Co.</span><a class="f-li" href="https://www.linkedin.com/in/shila-kandiah" target="_blank" rel="noopener me" aria-label="Shila Kandiah on LinkedIn"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M20.45 20.45h-3.55v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg></a></span><span>© 2026 · <a href="mailto:hello@retreatblueprintco.com">hello@retreatblueprintco.com</a></span></footer>
<script src="/js/menu.js?v={MENU_V}" defer></script>
{PRINT_JS}
</body>
</html>
'''


def build_article(a):
    url = f"{SITE}/field-notes/{a['slug']}"
    body = a["body"]
    svc_href, svc_text = a["service"]
    body = body.replace('<p class="fn-k">From the field</p>', '<p class="fn-k">A note from the field</p>')
    body = body.replace('<p class="fn-k">The next step</p>', '<p class="fn-k">Want a second pair of eyes?</p>')
    body = body.replace(' onclick="window.print()"', '')
    body = body.replace("{{mid_cta}}", f'<p class="fn-mid"><span>{a["mid_cta"]}</span><a href="{svc_href}">{svc_text} →</a></p>')
    body = re.sub(r"\{\{chart:([\w-]+)\}\}", lambda m: chart_html(m.group(1)), body)
    body = re.sub(r"\{\{photo:([^|}]+)\|([^|}]+)(?:\|([^}]*))?\}\}", lambda m: photo_html(m.group(1).strip(), m.group(2).strip(), (m.group(3) or "").strip()), body)
    hero = a.get("hero")
    og_image = photo_url(hero["photo"], 1200, 630) if hero else f"{SITE}/assets/img/og-image.jpg"
    hero_html = (f'<div class="fn-hero"><img src="{photo_url(hero["photo"], 1600, 760)}" srcset="{photo_url(hero["photo"], 800, 520)} 800w, {photo_url(hero["photo"], 1600, 760)} 1600w" '
                 f'sizes="(max-width:1100px) 100vw, 1100px" alt="{html.escape(hero["alt"])}" width="1600" height="760" fetchpriority="high"></div>') if hero else ""
    minutes = max(1, round(words(a["body"]) / 220))
    jsonld = {
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": a["title"], "description": a["description"],
        "datePublished": a["date"], "dateModified": a.get("updated") or a["date"],
        "mainEntityOfPage": url, "image": og_image,
        "author": {"@type": "Person", "name": AUTHOR["name"], "jobTitle": AUTHOR["role"], "url": f"{SITE}/#about", "sameAs": ["https://www.linkedin.com/in/shila-kandiah"]},
        "publisher": {"@type": "Organization", "name": "Retreat Blueprint Co.", "url": SITE},
    }
    upd = f' · Updated {nice_date(a["updated"])}' if a.get("updated") else ""
    draft = '<div class="fn-draft">Draft preview: not published. Highlighted text still needs your input.</div>' if a["status"] != "published" else ""
    page = head(a.get("seo_title", a["title"]) + " · Retreat Blueprint Co.", a["description"], url, og_image, jsonld)
    page += f'''{draft}
<header class="fn-head">
  <div class="inner">
    <p class="fn-crumb"><a href="/field-notes/">Field Notes</a><span aria-hidden="true">·</span><span>{a["topic"]}</span></p>
    <h1>{a["title"]}</h1>
    <p class="fn-dek">{a["dek"]}</p>
    <p class="fn-meta"><img src="{AUTHOR["avatar"]}" alt="" width="40" height="40"><span>By <b>{AUTHOR["name"]}</b> · {nice_date(a["date"])}{upd} · {minutes} min read</span></p>
  </div>
</header>
{hero_html}
<article class="fn-body">
{body}
</article>

<aside class="fn-author" aria-label="About the author">
  <div><img src="{AUTHOR["avatar"]}" alt="{AUTHOR["name"]}" width="72" height="72"><div><b>{AUTHOR["name"]}</b><span>{AUTHOR["role"]}</span><p>{AUTHOR["bio"]}</p></div></div>
</aside>

'''
    page += tail()
    os.makedirs("field-notes", exist_ok=True)
    open(f"field-notes/{a['slug']}.html", "w", encoding="utf-8").write(page)
    print("built", f"field-notes/{a['slug']}.html", "(draft)" if a["status"] != "published" else "")


def card_img(a):
    h = a.get("hero")
    if not h:
        return ""
    return (f'<img src="{photo_url(h["photo"], 760, 520)}" srcset="{photo_url(h["photo"], 380, 260)} 380w, {photo_url(h["photo"], 760, 520)} 760w" '
            f'sizes="(max-width:640px) 100vw, 340px" alt="{html.escape(h["alt"])}" width="760" height="520" loading="lazy">')


def build_index(arts):
    url = f"{SITE}/field-notes/"
    desc = "Practical notes for retreat venue owners and buyers: operations, buying, low season and growth, from Retreat Blueprint Co."
    jsonld = {"@context": "https://schema.org", "@type": "Blog", "name": "Field Notes", "url": url, "description": desc,
              "publisher": {"@type": "Organization", "name": "Retreat Blueprint Co.", "url": SITE}}
    page = head("Field Notes · Retreat Blueprint Co.", desc, url, f"{SITE}/assets/img/og-image.jpg", jsonld, "website")
    cards = "".join(
        f'''<a class="fn-card{' has-img' if a.get('hero') else ''}" href="/field-notes/{a["slug"]}">{card_img(a)}<div class="fn-card-txt"><p class="fn-k">{a["topic"]}{" · Draft" if a["status"] != "published" else ""}</p>
<h2>{a["title"]}</h2><p>{a["dek"]}</p><small>{nice_date(a["date"])} · {max(1, round(words(a["body"]) / 220))} min read</small><em>Read →</em></div></a>'''
        for a in arts) or '<p class="fn-empty">The first notes are on their way.</p>'
    page += f'''<header class="fn-head">
  <div class="inner">
    <p class="fn-crumb">Retreat Blueprint Co.</p>
    <h1>Field Notes</h1>
    <p class="fn-dek">Practical notes on running, buying and growing a retreat venue.</p>
  </div>
</header>
<main class="fn-list">{cards}</main>
'''
    page += tail()
    os.makedirs("field-notes", exist_ok=True)
    open("field-notes/index.html", "w", encoding="utf-8").write(page)
    print("built field-notes/index.html")


def update_sitemap(arts):
    sm = open("sitemap.xml", encoding="utf-8").read()
    sm = re.sub(r"\s*<url>\s*<loc>https://retreatblueprintco\.com/field-notes/[^<]*</loc>.*?</url>", "", sm, flags=re.S)
    live = [a for a in arts if a["status"] == "published"]
    if live:
        entries = [f"  <url>\n    <loc>{SITE}/field-notes/</loc>\n    <lastmod>{live[0]['date']}</lastmod>\n  </url>"]
        entries += [f"  <url>\n    <loc>{SITE}/field-notes/{a['slug']}</loc>\n    <lastmod>{a.get('updated') or a['date']}</lastmod>\n  </url>" for a in live]
        sm = sm.replace("</urlset>", "\n".join(entries) + "\n</urlset>")
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    print("sitemap:", len(live), "article(s) listed")


# ---------------------------------------------------------------- related Field Notes on service pages
# Each article's "service" field names the page it supports. That page gets a small
# "Further reading" block (inside its FAQ section, between the field-notes:related markers)
# listing the published articles for it, newest first. Run AFTER build_service_pages.py.
RELATED_PAGES = ["buying-a-retreat", "foundation-sprint", "fractional-operations-director", "concierge-ops", "growth-marketing"]
REL_RE = re.compile(r"<!-- field-notes:related -->.*?<!-- /field-notes:related -->", re.S)


def related_block(items):
    if not items:
        return "<!-- field-notes:related --><!-- /field-notes:related -->"
    links = "".join(
        f'<li style="margin:.35rem 0"><a href="/field-notes/{a["slug"]}" style="color:var(--sage-dark);font-weight:500;text-underline-offset:3px">{html.escape(a["title"])}</a></li>'
        for a in items)
    return ('<!-- field-notes:related --><div class="fn-related" style="margin-top:2.25rem">'
            '<p style="font-size:.7rem;font-weight:600;letter-spacing:.13em;text-transform:uppercase;color:var(--terracotta);margin-bottom:.4rem">Further reading · Field Notes</p>'
            f'<ul style="list-style:none;padding:0;margin:0">{links}</ul></div><!-- /field-notes:related -->')


def update_related(arts):
    for slug in RELATED_PAGES:
        path = f"{slug}.html"
        if not os.path.exists(path):
            continue
        src = open(path, encoding="utf-8").read()
        if not REL_RE.search(src):
            print("related: no markers in", path)
            continue
        items = [a for a in arts if a.get("service") and a["service"][0].rstrip("/") == f"/{slug}"]
        new = REL_RE.sub(lambda m: related_block(items), src, count=1)
        if new != src:
            open(path, "w", encoding="utf-8").write(new)
        print(f"related: {path} lists {len(items)} article(s)")



# ---------------------------------------------------------------- latest Field Notes on the homepage
# index.html has a "Field Notes" section; the 3 newest published articles go between the field-notes:latest markers
LATEST_RE = re.compile(r"<!-- field-notes:latest -->.*?<!-- /field-notes:latest -->", re.S)


def update_latest(arts):
    path = "index.html"
    src = open(path, encoding="utf-8").read()
    if not LATEST_RE.search(src):
        print("latest: no markers in", path)
        return
    live = [a for a in arts if a["status"] == "published"][:3]
    # two large cards: 3:2 photo with the topic as a pill, the serif title, the article's meta description, a quiet link
    cards = "".join(
        f'<a class="fl-card" href="/field-notes/{a["slug"]}">'
        f'<div class="fl-media">'
        + (f'<img src="{photo_url(a["hero"]["photo"], 760, 507)}" alt="{html.escape(a["hero"]["alt"])}" width="760" height="507" loading="lazy">' if a.get("hero") else "")
        + f'<span class="fl-k">{html.escape(a["topic"])}</span></div>'
        f'<div class="fl-txt"><h3>{html.escape(a["title"])}</h3><p class="fl-desc">{html.escape(a["description"])}</p><em>Read the note →</em></div></a>'
        for a in live)
    block = f'<!-- field-notes:latest --><div class="fl-grid">{cards}</div><!-- /field-notes:latest -->'
    new = LATEST_RE.sub(lambda m: block, src, count=1)
    if new != src:
        open(path, "w", encoding="utf-8").write(new)
    print(f"latest: {path} lists {len(live)} article(s)")

if __name__ == "__main__":
    articles = load_articles()
    # remove pages from earlier builds that shouldn't be live (e.g. a draft built with --preview)
    keep = {f"field-notes/{a['slug']}.html" for a in articles} | {"field-notes/index.html"}
    for old in glob.glob("field-notes/*.html"):
        if old not in keep:
            os.remove(old)
            print("removed", old)
    for art in articles:
        build_article(art)
    build_index(articles)
    update_related(articles)
    update_latest(articles)
    if not PREVIEW:
        update_sitemap(articles)
