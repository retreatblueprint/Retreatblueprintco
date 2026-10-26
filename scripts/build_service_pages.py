#!/usr/bin/env python3
"""Builds the four service pages (concierge-ops, foundation-sprint, fractional-operations-director, growth-marketing).

They share the Buying a Retreat page's base styles, nav and footer, plus one service-page template.
Each page has its own theme (accent colour, photos, band pattern) and its own sections.
Run from the repo root:  python3 scripts/build_service_pages.py
"""
import json
import re
import urllib.parse

BASE = open("buying-a-retreat.html").read()
HEAD = BASE[: BASE.index('<header class="hero')]
CAL = "https://calendly.com/hello-retreatblueprint/30min"
U = "https://images.unsplash.com/"

ICONS = {
    "mail": "M4 6h16v12H4z M4 6l8 7 8-7",
    "bell": "M12 3a6 6 0 0 0-6 6v4l-2 3h16l-2-3V9a6 6 0 0 0-6-6z M10 19a2 2 0 0 0 4 0",
    "grid": "M5 4h14v16H5z M5 9h14 M9 4v16",
    "receipt": "M7 3h10v18l-2.5-1.5L12 21l-2.5-1.5L7 21z M10 8h4 M10 12h4",
    "compass": "M12 3a9 9 0 1 0 0 18a9 9 0 0 0 0-18z M15.5 8.5l-2 5-5 2 2-5z",
    "card": "M3 6h18v12H3z M3 10h18 M7 15h4",
    "chart": "M4 20V10 M10 20V4 M16 20v-7 M3 20h18",
    "people": "M9 11a3 3 0 1 0 0-6a3 3 0 0 0 0 6z M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6 M16 5.5a3 3 0 0 1 0 5.5 M18 14.5c1.8.8 3 2.7 3 5",
}


def svg_bg(body):
    return "url(\"data:image/svg+xml," + urllib.parse.quote(body) + "\")"


def topo(color):
    lines = "".join(f"<path d='M0 {y} C240 {y-50} 480 {y+70} 720 {y} S1200 {y-60} 1440 {y-5}'/>" for y in range(80, 900, 58))
    return svg_bg(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 900' preserveAspectRatio='none'><g fill='none' stroke='{color}' stroke-opacity='.10' stroke-width='1.2' vector-effect='non-scaling-stroke'>{lines}</g></svg>") + " center/100% 100% no-repeat"


def blueprint(color):
    return svg_bg(f"<svg xmlns='http://www.w3.org/2000/svg' width='48' height='48'><path d='M48 0H0V48' fill='none' stroke='{color}' stroke-opacity='.10' stroke-width='1'/><path d='M24 0V48M0 24H48' fill='none' stroke='{color}' stroke-opacity='.05' stroke-width='1'/></svg>") + " 0 0/48px 48px repeat"


SHARED_CSS = """
/* Service page template */
.svc-h1 .label{font-family:var(--sans)}.svc-h1 .svc-name{display:block;font-size:inherit;line-height:inherit;margin:0}
.svc-name{font-family:var(--serif);font-weight:400;font-size:clamp(3.2rem,8vw,6.2rem);line-height:.98;letter-spacing:-.02em;margin:0 0 1rem;color:var(--earth);text-wrap:balance}
.svc-tag{font-family:var(--serif);font-size:clamp(1.35rem,2.5vw,1.85rem);line-height:1.25;color:var(--earth-mid);margin:0 0 1.5rem;max-width:30ch}
.venue-hint{font-size:.85rem;color:var(--earth-mid);margin:-.25rem 0 1.5rem;display:flex;gap:8px;align-items:center}
.venue-hint::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--acc);flex:none}
.svc-tag em{white-space:nowrap}
.band-note a{color:#fff;text-decoration:underline;text-underline-offset:3px}
.co-price{background:var(--warm-white);border:1px solid var(--border);border-radius:8px;padding:28px;display:grid;gap:10px;box-shadow:0 18px 40px rgba(42,34,24,.10)}
.co-price .k{font-size:.68rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--terracotta)}
.co-price .amt{font-family:var(--serif);font-size:2.5rem;line-height:1.05}
.co-price .amt small{font-family:var(--sans);font-size:.9rem;color:var(--muted);white-space:nowrap}
.co-price p{font-size:.88rem;color:var(--earth-mid)}
.co-price ul{list-style:none;display:grid;gap:8px;border-top:1px solid var(--border);padding-top:14px;margin-top:4px}
.co-price li{display:flex;gap:10px;font-size:.9rem}
.co-price li::before{content:"\\2713";color:var(--acc);font-weight:600}
.outcomes{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-top:2.5rem}
.outcomes.three{grid-template-columns:repeat(3,minmax(0,1fr))}
.split-intro{margin-top:1rem;max-width:640px;color:var(--earth-mid);font-size:1rem}
.split{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr) minmax(0,1fr);gap:0;margin-top:2rem;border-radius:10px;overflow:hidden;border:1px solid var(--border);background:var(--warm-white)}
.split-col{padding:26px 26px 24px;display:grid;gap:12px;align-content:start;position:relative}
.split-col + .split-col{border-left:1px solid var(--border)}
.split-k{font-size:.7rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.split-col ul{list-style:none;display:grid;gap:9px}
.split-col li{font-family:var(--serif);font-size:1.12rem;line-height:1.3;color:var(--earth)}
.split-col.flex{background:repeating-linear-gradient(135deg,transparent 0 10px,rgba(47,100,103,.045) 10px 20px)}
.split-col.flex li{display:flex;gap:10px;align-items:baseline}
.split-col.flex li::before{content:"\\21C4";font-family:var(--sans);font-size:.8rem;color:var(--acc)}
.split-note{font-size:.85rem;color:var(--earth-mid)}
.split-col.mine{background:var(--acc);}
.split-col.mine .split-k{color:rgba(255,255,255,.75)}
.split-col.mine li{color:#fff}
.split-col.keep li::before,.split-col.mine li::before{content:"";display:inline-block;width:6px;height:6px;border-radius:50%;margin-right:10px;vertical-align:middle;background:var(--acc-soft)}
.split-col.mine li::before{background:rgba(255,255,255,.7)}
.split-then{margin-top:2.5rem;font-size:.7rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--terracotta)}
.split-then + .outcomes{margin-top:1rem}
@media (max-width:900px){.split{grid-template-columns:1fr}.split-col + .split-col{border-left:0;border-top:1px solid var(--border)}.outcomes.three{grid-template-columns:1fr}}
.outcomes > div{background:var(--warm-white);border:1px solid var(--border);border-top:3px solid var(--acc-soft);border-radius:6px;padding:22px;display:grid;gap:8px;align-content:start}
.outcomes b{font-family:var(--serif);font-weight:500;font-size:1.15rem;line-height:1.25}
.outcomes p{font-size:.9rem;color:var(--earth-mid)}
.roles{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;margin-top:2.5rem}
.role{display:grid;grid-template-columns:52px 1fr;gap:16px;align-items:start;padding:22px;border:1px solid rgba(255,255,255,.14);border-radius:8px;background:rgba(255,255,255,.06)}
.role svg{width:52px;height:52px;padding:12px;border-radius:50%;background:rgba(255,255,255,.10);fill:none;stroke:var(--on-band-soft);stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.role h3{font-family:var(--serif);font-weight:400;font-size:1.25rem;color:#F4F6F2;margin-bottom:4px}
.role p,.role li{font-size:.9rem;color:var(--on-band)}
.role ul{list-style:none;display:grid;gap:4px}
.role li::before{content:"\\2013  ";color:var(--on-band-soft)}
.band-note{margin-top:1.75rem;font-size:.92rem;color:var(--on-band);display:flex;gap:10px;align-items:center}
.band-note:has(.route){display:grid;grid-template-columns:1fr 1fr;gap:14px 20px;align-items:stretch}
.routes-h{grid-column:1/-1;font-size:.7rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--on-band-soft)}
.route{display:block;padding:16px 18px;border-radius:8px;border:1px dashed rgba(255,255,255,.25)}
.route b{display:block;margin-bottom:6px;color:#fff;font-weight:500;font-family:var(--serif);font-size:1.05rem}
@media (max-width:700px){.band-note:has(.route){grid-template-columns:1fr}}
.band-note b{color:#fff;font-weight:500}
.cycle{list-style:none;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px;margin-top:2.75rem;position:relative}
.cycle li{position:relative;display:grid;gap:8px;align-content:start;padding:22px 18px;border-radius:8px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14)}
.cycle li span{font-family:var(--serif);font-size:1.6rem;color:var(--on-band-soft);line-height:1}
.cycle li b{font-family:var(--serif);font-weight:400;font-size:1.15rem;color:#F4F6F2}
.cycle li p{font-size:.86rem;color:var(--on-band)}
.cycle li:not(:last-child)::after{content:"\\2192";position:absolute;right:-13px;top:26px;width:12px;text-align:center;color:var(--on-band-soft);font-size:.9rem}
.cycle-loop{margin-top:16px;font-size:.85rem;color:var(--on-band);display:flex;align-items:center;gap:8px}
.cycle-loop svg{width:18px;height:18px;fill:none;stroke:var(--on-band-soft);stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.levels{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:20px;margin-top:2.5rem}
.level{border-radius:8px;padding:28px;display:grid;gap:12px;align-content:start}
.level.lite{border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.06)}
.level.full{background:#FDFCF9;color:var(--earth);box-shadow:0 18px 40px rgba(0,0,0,.25)}
.level .k{font-size:.68rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--on-band-soft)}
.level.full .k{color:var(--acc)}
.level h3{font-family:var(--serif);font-weight:400;font-size:1.5rem;color:#F4F6F2}
.level.full h3{color:var(--earth)}
.level p{font-size:.92rem;color:var(--on-band)}
.level.full p{color:var(--earth-mid)}
.level ul{list-style:none;display:grid;gap:8px;border-top:1px solid rgba(255,255,255,.15);padding-top:14px}
.level.full ul{border-top-color:var(--border)}
.level li{display:flex;gap:10px;font-size:.92rem;color:#EEF2EC}
.level.full li{color:var(--earth)}
.level li::before{content:"\\2713";color:var(--on-band-soft);font-weight:600}
.level.full li::before{color:var(--acc)}
.level .plus{font-size:.86rem;font-weight:500;color:var(--acc)}
.compare{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.2fr) minmax(0,.9fr);gap:16px;margin-top:2.5rem;align-items:stretch}
.cmp{border:1px solid var(--border);border-radius:8px;padding:24px;background:var(--warm-white);display:grid;gap:12px;align-content:start}
.cmp h3{font-family:var(--serif);font-weight:400;font-size:1.2rem;color:var(--muted)}
.cmp ul{list-style:none;display:grid;gap:8px}
.cmp li{font-size:.9rem;color:var(--earth-mid);padding-left:18px;position:relative}
.cmp li::before{content:"\\2013";position:absolute;left:0;color:var(--muted)}
.cmp.on{border:2px solid var(--acc);box-shadow:0 18px 40px rgba(42,34,24,.10);transform:translateY(-6px)}
.cmp.on h3{color:var(--earth);font-size:1.4rem}
.cmp.on li{color:var(--earth)}
.cmp.on li::before{content:"\\2713";color:var(--acc);font-weight:600}
.cmp .pick{justify-self:start;font-size:.66rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:#fff;background:var(--acc);border-radius:4px;padding:3px 8px}
@media (max-width:900px){.compare{grid-template-columns:1fr}.cmp.on{transform:none}}
.proof li::before{color:var(--acc)}
.proof .built{font-size:.86rem;color:var(--earth-mid);line-height:1.55;margin:0 0 .9rem}.proof .built b{font-weight:600;color:var(--earth)}
.proof-more{margin-top:1.5rem;font-size:.9rem}
.proof-more a{color:var(--acc);font-weight:500;text-decoration:underline;text-underline-offset:3px}
.others{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-top:2rem}
.others a{display:grid;gap:6px;padding:20px;border:1px solid var(--border);border-radius:6px;background:var(--warm-white);text-decoration:none;color:var(--earth);transition:border-color .2s,transform .2s}
.others a:hover{border-color:var(--acc-soft);transform:translateY(-2px)}
.others b{font-family:var(--serif);font-weight:500;font-size:1.05rem}
.others span{font-size:.84rem;color:var(--muted)}
.others em{font-style:normal;font-size:.8rem;font-weight:500;color:var(--acc);margin-top:4px}
.how .steps{grid-template-columns:repeat(var(--cols,4),minmax(0,1fr))}
.steps li{border-top-color:var(--acc-soft)}
.steps li::before{color:var(--acc)}
.title em,.svc-tag em,.hero h1 em{color:var(--acc)}
.btn.primary{background:var(--acc);border-color:var(--acc)}
.btn.primary:hover{background:var(--acc-dark);border-color:var(--acc-dark)}
@media (max-width:900px){.outcomes,.others{grid-template-columns:repeat(2,minmax(0,1fr))}.roles,.levels{grid-template-columns:1fr}.cycle{grid-template-columns:1fr 1fr}.cycle li::after{display:none}.how .steps{grid-template-columns:1fr 1fr}}
@media (max-width:520px){.outcomes,.others,.cycle{grid-template-columns:1fr}.how .steps{grid-template-columns:1fr}}
"""


def theme_css(t):
    hero, cta = U + t["hero"] + "?auto=format&fit=crop&q=72", U + t["cta"] + "?auto=format&fit=crop&q=72"
    return f"""
/* Theme: {t['name']} */
:root{{--acc:{t['acc']};--acc-dark:{t['acc_dark']};--acc-soft:{t['acc_soft']};--on-band:{t['on_band']};--on-band-soft:{t['on_band_soft']}}}
.hero{{background:linear-gradient(100deg,rgba(250,248,243,.97) 0%,rgba(250,248,243,.9) 42%,rgba(250,248,243,.35) 72%,rgba(250,248,243,.08) 100%),{t['hero_fill']} url('{hero}&w=2000') {t['hero_pos']}/cover !important}}
@media (max-width:860px){{.hero{{background:linear-gradient(180deg,rgba(250,248,243,.93) 0%,rgba(250,248,243,.88) 100%),{t['hero_fill']} url('{hero}&w=1100') {t['hero_pos']}/cover !important}}}}
.band-bg{{background:{t['band_pattern']},{t['band_grad']} !important}}
.band-ov{{background:radial-gradient(60% 60% at 85% 10%, {t['band_glow']}, transparent 70%) !important}}
.band .label{{color:var(--on-band-soft)}}.band .lead{{color:var(--on-band)}}
.cta{{background:{t['hero_fill']} url('{cta}&w=2000') {t['cta_pos']}/cover !important}}
@media (max-width:860px){{.cta{{background-image:url('{cta}&w=1100') !important}}}}
.cta > .cta-ov{{background:{t['cta_tint']} !important}}
.cta .btn.primary{{background:{t['cta_btn']};border-color:{t['cta_btn']}}}
"""


def split_html(pg):
    if not pg.get("split"):
        return ""
    has_out = bool(pg["changes"][2])
    intro, cols = pg["split"]
    cells = []
    for col in cols:
        h, kind, items = col[0], col[1], col[2]
        note = f'<p class="split-note">{col[3]}</p>' if len(col) > 3 else ""
        cells.append(f'<div class="split-col {kind}"><span class="split-k">{h}</span><ul>' + "".join(f"<li>{x}</li>" for x in items) + f"</ul>{note}</div>")
    return f'<p class="split-intro">{intro}</p><div class="split">{"".join(cells)}</div>' + ('<p class="split-then">What changes for you</p>' if has_out else '')


def outcomes(items):
    return "".join(f"<div><b>{b}</b><p>{p}</p></div>" for b, p in items)


def steps(items):
    return "".join(f"<li><h4>{h}</h4><p>{p}</p></li>" for h, p in items)


PAGES = [
    dict(
        slug="concierge-ops", kw="Retreat center admin &amp; booking management", menu="/concierge-ops", name="Concierge Ops",
        title="Retreat Center Admin & Booking Management · Concierge Ops",
        desc="Retreat center admin and booking management by a dedicated team: inquiries, guest communication, coordination and back office. From $250 a month.",
        og="Concierge Ops: your day-to-day admin, handled.",
        theme=dict(name="Concierge Ops", acc="#4A6E4E", acc_dark="#3A5A3E", acc_soft="#7A9E7E", on_band="#C2D6C2", on_band_soft="#B8D0BA",
                   hero="photo-1777913308049-a2c79af7380a", hero_pos="60% 55%", hero_fill="#3B4A33",
                   cta="photo-1644612105654-b6b0a941ecde", cta_pos="center 60%",
                   cta_tint="linear-gradient(180deg,rgba(18,30,21,.78) 0%,rgba(18,30,21,.70) 50%,rgba(18,30,21,.82) 100%)", cta_btn="#985033",
                   band_pattern=topo("#B8D0BA"), band_grad="linear-gradient(160deg,#25402B 0%,#1A2E1F 55%,#132217 100%)", band_glow="rgba(122,158,126,.22)"),
        label="For retreat venues · Monthly", tag="Stop answering every inquiry yourself. <em>Hand it to a team that does it daily.</em>",
        lead="Every inquiry answered fast, every guest looked after, every invoice tracked. We are the experts in hospitality communications. A dedicated team, led by your Retreat Operations Director, runs your day-to-day admin in your voice, so you are not coordinating everything yourself while you host and build the parts only you can.",
        jump=("#handoff", "See what you hand over ↓"),
        price=dict(k="Monthly", amt="From $250 <small>USD / month</small>", note="Priced on your average monthly bookings, team size and retreat capacity. 3-month minimum.",
                   items=["Replies within 2 business hours", "Works inside your current inbox", "Your accounts and guest details kept private", "Led by your Retreat Operations Director"]),
        main="content/concierge-conversion.html",
        changes=("What changes", "Less time in the inbox. More time on <em>the experience.</em>", [
            ("No more missed bookings", "Inquiries answered within 2 business hours, with follow-ups until they book or say no."),
            ("Guests who feel looked after", "Pre-arrival emails, forms, reminders, and review requests sent on time, every time."),
            ("Retreats that run smoothly", "Organizers kept in the loop, with rooming lists and schedules ready before anyone arrives."),
            ("Books you can trust", "Invoices sent, payments tracked, and records organized in one place.")]),
        band=("team", "Your team", "Four roles, one team, led by your Retreat Operations Director", "roles", [
            ("mail", "Remote Booking Assistant", "Inquiry responses, follow-ups, reservations and confirmations."),
            ("bell", "Guest Experience Assistant", "Guest emails, forms, reminders, feedback and review requests."),
            ("grid", "Operations Coordinator", "Event preparation, organizer communication, rooming lists and schedules."),
            ("receipt", "Back Office Administrator", "Invoices, payment tracking, spreadsheets and digital records.")]),
        proof=None,
        how=("How it starts", "From first call to a team that runs it", [
            ("Free call", "Your bookings, your tools, and where the admin piles up."),
            ("Set-up", "Access to your inbox and booking system; your voice, policies and templates handed over."),
            ("Your team takes over", "Inquiries, guests, coordination and the back office, handled every day."),
            ("Monthly check-in", "What came in, what got booked, and what to improve next.")]),
        faq=[
            ("How fast are guests answered?", "Within 2 business hours, including while a retreat is in session. Interested guests also get a well-timed, polite follow-up in your voice, so they do not go quiet while you are hosting."),
            ("What decides the monthly price?", "Your average bookings per month, which sets how much time the work takes, plus your team size and retreat capacity. Pricing starts at $250 USD a month and is agreed on a free call."),
            ("Who will my guests be talking to?", "Your Concierge Ops team writes in your voice, using your policies and templates. I lead the team and I'm your point of contact, so you always know who is responsible."),
            ("Do I need to change my booking system or inbox?", "No. The team works inside the inbox and booking system you already use. If something is slowing you down, I'll suggest a better setup, and the <a href=\"/foundation-sprint\">Foundation Sprint</a> can build it."),
            ("How is this different from the Fractional Retreat Operations Director?", "Concierge Ops does the day-to-day admin. The <a href=\"/fractional-operations-director\">Fractional Retreat Operations Director</a> leads the operations: priorities, numbers, team and systems. Many venues combine the two."),
            ("Is there a minimum commitment?", "Three months, so the team has time to learn your voice, your guests and your policies, and you can see the difference it makes."),
            ("How are my accounts and guests' details protected?", "You own every account, and nothing is moved or transferred. Each team member only gets the access their role needs, guest information is used only to look after your guests, and access is removed if you stop."),
            ("Where do you work?", "Fully remote, so it works for retreat properties anywhere in the world."),
        ],
        cta_title="Give every guest your full attention. We'll handle the admin.",
    ),
    dict(
        slug="foundation-sprint", kw="Retreat center systems setup", menu="/foundation-sprint", name="Foundation Sprint",
        title="Retreat Center Systems Setup: Booking, Payments & SOPs · Foundation Sprint",
        desc="Set up your retreat center's booking system, payments, numbers, guest communication and SOPs in one focused build. From $100: build your own quote, no minimum.",
        og="Foundation Sprint: the systems your retreat runs on, built in one go.",
        theme=dict(name="Foundation Sprint", acc="#985033", acc_dark="#7E4029", acc_soft="#C98A63", on_band="#E6D3C3", on_band_soft="#DDB797",
                   hero="photo-1771526087720-e6fc37b442fe", hero_pos="70% 55%", hero_fill="#5A4832",
                   cta="photo-1565214988145-8e826f79d8c2", cta_pos="center",
                   cta_tint="linear-gradient(180deg,rgba(42,26,17,.80) 0%,rgba(42,26,17,.70) 50%,rgba(42,26,17,.84) 100%)", cta_btn="#985033",
                   band_pattern=blueprint("#DDB797"), band_grad="linear-gradient(160deg,#4A3021 0%,#3A251A 55%,#2A1A11 100%)", band_glow="rgba(221,183,151,.18)"),
        label="For retreat venues · One-time build", tag="Everything your retreat needs to run like a <em>real business.</em>",
        lead="Built, integrated, and ready to run without you in every detail. One focused build that gives your retreat its systems: bookings and payments, your numbers, guest communication and the tools your team uses every day.",
        jump=("#quote", "Build your quote ↓"),
        price=dict(k="Build your own · No minimum", amt="From $100 <small>USD</small>", note="Choose only the pieces you need, see the price as you go, and add more later. 10% off 3 or more pieces, 15% off the full package.",
                   items=["Business audit and strategy brief", "Bookings, payments and website", "Custom operating system and financial tracking", "Guest communication and SOPs"]),
        changes=("What changes", "From running on memory to running on <em>systems.</em>", [
            ("One booking flow", "Inquiry to confirmed booking to payment, set up and connected."),
            ("Numbers you can see", "Financial tracking and a custom operating system that show how the business is doing at a glance."),
            ("Guests looked after automatically", "A guest communication playbook, automations and a welcome package."),
            ("A team that knows what to do", "SOPs and operational tools, so the business doesn't depend on you for every detail.")]),
        band=None,
        proof=("In practice", "Built for retreats like yours", [
            ("Systemize · Dominical, Costa Rica", "A custom retreat operating system that replaced a full-time admin role", ["A full-time administrative salary saved", "Revenue, and what each retreat and participant owes, clear at a glance", "Kitchen messages in English and Spanish, sent from the same system", "Every past and present client in one place"],
             "Someone who takes big challenges, and turns them into simple systems that just work.", "Jonathon Conant, Founder, Airborne Arts", "One custom system connecting guest communication, financial status, bookings, kitchen communication, the client list, and guest, student and kitchen portals."),
            ("Revive · Ometepe, Nicaragua", "An inactive venue rebuilt and taking bookings again", ["Every booking in one streamlined system", "Guest communication automated", "Relaunched with a new brand and paid ads"],
             "Shila took on the nearly impossible task of building our entire digital backend from the ground up.", "Cris Ketch, Founder, Infinity Retreat", "Business audit and strategy brief, website build and optimization, booking sites, sales process and payment flows, guest communication and automations, and a guest welcome package.")]),
        how=("How it works", "Audit, plan, build, hand over", [
            ("Audit", "How the pieces you chose are handled today, so nothing is built on guesswork."),
            ("Plan", "What needs to change, the cost and the flow, agreed before anything is built."),
            ("Build", "A connected version of each piece, tested so it all works together."),
            ("Handover", "A walk-through and training so your team can run it.")]),
        faq=[
            ("How long does it take?", "A single piece can take days to a couple of weeks. The full build usually takes 1 to 3 months, depending on the scope and the size of your team. The timeline leaves room to hand everything over properly, with training, so your team can run it."),
            ("Are software subscriptions included?", "No. Booking, payment and other tools are billed to you directly by each provider, so you own every account. I help you choose tools that fit your size and budget."),
            ("How is it priced?", "Each piece has its own price, and you only pay for the pieces you pick. Use the quote builder above to see your total. Website optimization, a fully automated financial tracking system and a larger custom operating system are confirmed on a free call, because the work depends on what you already have. Choose 3 or more pieces for 10% off, or the full package for 15% off."),
            ("Can you work with the tools I already use?", "Yes. I audit before I build, so anything that already works stays, and only the gaps get built or replaced."),
            ("Is it remote or on-site?", "Remote for retreat properties anywhere in the world. On-site visits are available in Costa Rica, Panama, Nicaragua and Guatemala."),
            ("What happens after the build?", "Your team runs it from the SOPs and training. If you want ongoing support, the <a href=\"/fractional-operations-director\">Fractional Retreat Operations Director</a> or <a href=\"/concierge-ops\">Concierge Ops</a> picks up from there."),
        ],
        cta_title="Build the foundation once. Run on it every season.",
        builder="content/foundation-quote-builder.html",
    ),
    dict(
        slug="fractional-operations-director", kw="Fractional COO for retreat centers", menu="/fractional-operations-director", name="Fractional Retreat Operations Director", name_html="<span>Fractional Retreat</span><span>Operations Director</span>",
        title="Fractional COO for Retreat Centers · Part-Time Operations Director",
        desc="A part-time COO for your retreat center: operations leadership, numbers, team and systems without a full-time hire. From $1,000 a month.",
        og="Fractional Retreat Operations Director: your part-time COO.",
        name_css=".hero .svc-name{font-size:clamp(2.1rem,3.8vw,3.35rem);line-height:1.06;max-width:none}.svc-name span{display:block}@media (max-width:860px){.hero .svc-name{font-size:clamp(1.9rem,8.6vw,2.8rem)}}",
        theme=dict(name="Fractional Retreat Operations Director", acc="#2F6467", acc_dark="#234D50", acc_soft="#6E9EA0", on_band="#C4DADB", on_band_soft="#9CC4C6",
                   hero="photo-1782139186009-6fcc4f2326ea", hero_pos="60% 60%", hero_fill="#2F4A4C",
                   cta="photo-1782061419033-591356402cd4", cta_pos="center 55%",
                   cta_tint="linear-gradient(180deg,rgba(12,34,36,.78) 0%,rgba(12,34,36,.66) 50%,rgba(12,34,36,.82) 100%)", cta_btn="#985033",
                   band_pattern=topo("#9CC4C6"), band_grad="linear-gradient(160deg,#1E4547 0%,#163638 55%,#0F2829 100%)", band_glow="rgba(156,196,198,.18)"),
        label="For retreat venues · Monthly · Your part-time COO", tag="Senior operations leadership,<br><em>without a full-time hire.</em>",
        lead="I run the operations side of your venue with you: the automations, guest messages and coordination, and the digital systems behind them. I make sure it all runs efficiently, change the processes that stop making sense, and lead the team that does the work.",
        jump=("#role", "What the role covers ↓"),
        price=dict(k="Monthly retainer", amt="From $1,000 <small>USD / month</small>", note="Operations leadership at a fraction of a full-time salary. 6-month minimum.",
                   items=["Two scheduled touchpoints a month", "Owns operations priorities with you", "P&amp;L, budget and forecast owned", "Team leadership, SOPs and growth planning"]),
        changes=("How we work together", "You keep the vision. <em>I take the operations.</em>", []),
        split=("You decide where the line sits. Some owners keep the guest relationships close; others hand over everything but the vision.", [
            ("Always yours", "keep", ["The vision for your retreat", "The big decisions"]),
            ("Your call", "flex", ["Priorities for the month and the season", "Growth planning", "Guest experience", "Retreat leader relationships", "Hiring", "Marketing"], "Set these together, keep them, or hand them over. Support or ownership, whichever you prefer."),
            ("Always mine", "mine", ["Digital systems: booking, payments, website, automations and team tools, connected so nothing is typed in twice", "Financial management: P&amp;L, budget and forecast reviewed monthly, quarterly and annually", "The team and day-to-day operations, with clear roles and messages and coordination running smoothly", "The processes: SOPs kept current, season after season"])]),
        band=None,
        after_changes="<div class=\"routes-row\"><span class=\"routes-h\">Two ways to run it</span><span class=\"route\"><b>You have a team</b>I lead your in-house team and run the operations through them.</span><span class=\"route\"><b>You don't have one yet</b>The Retreat Blueprint <a href=\"/concierge-ops\">Concierge Ops</a> remote team handles the day-to-day, under my direction.</span></div>",
        compare=("Why fractional", "The leadership of a full&#8209;time hire, sized to your retreat", [
            ("Fractional director", ["Operations owned with you, every month", "Numbers reviewed on a set rhythm", "A leader the team can go to", "A plan for the season ahead", "A monthly retainer, no long hiring process"], True),
            ("Full-time hire", ["Operations owned, full time", "A full salary, every month of the year", "Months to recruit and onboard", "Hard to scale back in low season"], False)]),
        proof=("In practice", "The work doesn't stop at the build", [
            ("Infinity Retreat · Ometepe, Nicaragua", "Kept on as an ongoing consultant after the build", ["Bookings, guests and payments in one system", "Relaunched with a new brand, website and paid ads", "Retained as an ongoing consultant"],
             "Shila has continued working with me as a consultant, a testament to the value she brings and the confidence I have in her abilities.", "Cris Ketch, Founder, Infinity Retreat")]),
        how=("How it starts", "From first call to a steady rhythm", [
            ("Free call", "Where the business is now, and where you want it to go."),
            ("Operations review", "Your baseline numbers, team and systems, and the first set of priorities."),
            ("Monthly rhythm", "Review the numbers, set priorities, lead the team, refine the systems. Repeat.")], 3),
        faq=[
            ("How much of your time do I get?", "Two scheduled touchpoints a month, plus the operations work in between. Hours depend on what your retreat needs and the level you choose, and both are agreed before we start."),
            ("Is there a minimum commitment?", "Six months minimum. I recommend 12, so we work through a full season together, high and low."),
            ("Is it remote or on-site?", "Remote for retreat properties anywhere in the world. On-site time is available in Costa Rica, Panama, Nicaragua and Guatemala."),
            ("What if I don't have a team?", "The Retreat Blueprint <a href=\"/concierge-ops\">Concierge Ops</a> team can handle the day-to-day under my direction."),
            ("What if my systems are a mess?", "Most venues start with the <a href=\"/foundation-sprint\">Foundation Sprint</a> to build the systems, then move to the fractional role to run and improve them."),
            ("Who makes the final decisions?", "You do. You keep the vision and the big decisions, and you choose what else to hand over."),
        ],
        cta_title="Bring in your part-time COO.",
        builder="content/director-additions.html",
    ),
    dict(
        slug="growth-marketing", kw="Retreat center marketing", menu="/growth-marketing", name="Growth Marketing",
        title="Retreat Center Marketing to Get More Bookings · Growth Marketing",
        desc="Marketing for retreat centers and eco-lodges: strategy, content, social media and outreach to fill your calendar with the right guests. Pricing on inquiry.",
        og="Growth Marketing: get your retreat seen by the right people.",
        theme=dict(name="Growth Marketing", acc="#8A5414", acc_dark="#6E420F", acc_soft="#C9934A", on_band="#D6D3E2", on_band_soft="#E2B877",
                   hero="photo-1699694927472-46a4fcf68973", hero_pos="62% 40%", hero_fill="#4A4430",
                   cta="photo-1760774714285-61ff516f86c5", cta_pos="center 60%",
                   cta_tint="linear-gradient(180deg,rgba(28,26,44,.72) 0%,rgba(28,26,44,.58) 50%,rgba(28,26,44,.80) 100%)", cta_btn="#985033",
                   band_pattern=topo("#E2B877"), band_grad="linear-gradient(160deg,#2C2F4A 0%,#232640 55%,#191B30 100%)", band_glow="rgba(226,184,119,.20)"),
        label="For retreat venues · Strategy to fully managed", tag="Getting your retreat seen by <em>the right people.</em>",
        lead="Scope is built around what you actually need, from strategy only to full execution with a dedicated team. The goal is simple: the guests who fit your retreat find it, trust it and book.",
        jump=("#levels", "Choose your level ↓"),
        price=dict(k="Pricing", amt="On inquiry", note="Scope and price agreed on a free call, based on what you need.",
                   items=["Strategy and positioning", "Content direction and creation", "Social media systems", "Outreach and lead generation"]),
        changes=("What changes", "Seen by the guests who <em>fit your retreat.</em>", [
            ("A clear position", "Marketing strategy and positioning that says who your retreat is for."),
            ("Content that shows the experience", "Content direction and creation, handled end to end."),
            ("A consistent presence", "Social media systems and scheduling, so posting doesn't wait for a free afternoon."),
            ("A steady pipeline", "Outreach campaigns, a sales funnel and a custom lead generator.")]),
        band=("levels", "Choose your level", "From strategy only to fully managed", "levels", None),
        proof=("In practice", "A venue relaunched and back in front of guests", [
            ("Revive · Infinity Retreat, Ometepe", "Relaunched with a new brand, website and paid ads", ["Marketing rebrand and website", "Content strategy", "Paid ads across Costa Rica and Nicaragua", "Custom lead generation app"],
             None, None)]),
        how=("How it starts", "From first call to campaigns going out", [
            ("Free call", "Your guests, your goals, and what's worked so far."),
            ("Strategy", "Positioning, channels and a content plan."),
            ("Launch", "Content, campaigns and outreach going out, reviewed month to month.")], 3),
        faq=[
            ("How is it priced?", "Scope and price are agreed on a free call, based on what you need: strategy only, or strategy plus a dedicated team running it for you."),
            ("What's the difference between strategy only and fully managed?", "Strategy only gives your team the positioning, channels and content direction to run with. Fully managed adds a dedicated marketing lead who creates the content, runs your social media and outreach, and builds your lead pipeline."),
            ("Do I need my systems in place first?", "It helps. Marketing brings in more inquiries, so they need somewhere to land. If bookings still run through your inbox and memory, start with the <a href=\"/foundation-sprint\">Foundation Sprint</a> or pair marketing with <a href=\"/concierge-ops\">Concierge Ops</a>."),
            ("Where do you work?", "Remote for retreat properties anywhere in the world. On-site visits are available in Costa Rica, Panama, Nicaragua and Guatemala."),
        ],
        cta_title="Fill the calendar with the right guests.",
    ),
]

OTHERS = {
    "foundation-sprint": ("Foundation Sprint", "The systems your retreat runs on, built in one go.", "From $100 · build your own quote →"),
    "fractional-operations-director": ("Fractional Retreat Operations Director", "Your part-time COO, month to month.", "From $1,000 USD / month →"),
    "concierge-ops": ("Concierge Ops", "Your day-to-day admin, handled.", "From $250 USD / month →"),
    "growth-marketing": ("Growth Marketing", "Get your retreat seen by the right people.", "Pricing on inquiry →"),
    "buying-a-retreat": ("Buying a retreat?", "Pre-purchase review and your first 90 days.", "From $1,200 USD →"),
}

LEVELS_HTML = """<div class="levels">
        <div class="level lite"><span class="k">Strategy only</span><h3>The plan, ready for your team</h3><p>For venues with someone to run marketing day to day, who need the direction.</p>
          <ul><li>Marketing strategy and positioning</li><li>Content direction</li></ul></div>
        <div class="level full"><span class="k">Fully managed</span><h3>Strategy plus a dedicated team</h3><p>Everything in strategy only, then executed for you, end to end.</p>
          <ul><li>Dedicated marketing lead, fully managed</li><li>Content creation handled end to end</li><li>Social media systems and scheduling</li><li>Outreach campaigns and sales funnel</li><li>Custom lead generator</li></ul>
          <span class="plus">Scope discussed on inquiry</span></div>
      </div>"""


FAQ_JS = "<script>\n// FAQ: questions slide open and closed, and only one stays open at a time\n(function () {\n  var items = Array.prototype.slice.call(document.querySelectorAll('.faq details'));\n  var calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;\n  function animate(d, open) {\n    var summary = d.querySelector('summary');\n    if (d._anim) d._anim.cancel();\n    var start = d.offsetHeight;\n    if (open) d.open = true;\n    var end = open ? d.scrollHeight : summary.offsetHeight + parseFloat(getComputedStyle(d).paddingTop) + parseFloat(getComputedStyle(d).paddingBottom);\n    if (calm || !d.animate) { if (!open) d.open = false; return; }\n    d._anim = d.animate({ height: [start + 'px', end + 'px'] }, { duration: 280, easing: 'ease' });\n    d._anim.onfinish = function () { d._anim = null; if (!open) d.open = false; };\n    d._anim.oncancel = function () { d._anim = null; };\n  }\n  items.forEach(function (d) {\n    d.querySelector('summary').addEventListener('click', function (e) {\n      e.preventDefault();\n      var opening = !d.open || (d._anim && d._closing);\n      items.forEach(function (o) { if (o !== d && o.open) { o._closing = true; animate(o, false); } });\n      d._closing = !opening;\n      animate(d, opening);\n    });\n  });\n})();\n</script>"


def build(pg):
    head = HEAD
    head = re.sub(r"<title>[^<]*</title>", f"<title>{pg['title']}</title>", head, count=1)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{pg["desc"]}">', head, count=1)
    head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{pg["og"]}">', head, count=1)
    head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{pg["desc"]}">', head, count=1)
    head = head.replace("https://retreatblueprintco.com/buying-a-retreat", f"https://retreatblueprintco.com/{pg['slug']}")
    head = re.sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{U}{pg["theme"]["hero"]}?auto=format&fit=crop&w=1200&h=630&q=75">', head, count=1)
    # nav: mark this page as current
    head = head.replace('<a href="/buying-a-retreat" class="dd-feature" aria-current="page">', '<a href="/buying-a-retreat" class="dd-feature">')
    head = head.replace(f'<a href="{pg["menu"]}">', f'<a href="{pg["menu"]}" aria-current="page">')
    if 'href="https://images.unsplash.com"' not in head:
        head = head.replace('<link rel="preconnect" href="https://calendly.com">', '<link rel="preconnect" href="https://images.unsplash.com">\n<link rel="preconnect" href="https://calendly.com">', 1)
    # structured data: this page's service (Google reads it; nothing visible changes)
    ld = {"@context": "https://schema.org", "@type": "Service", "name": pg["name"],
          "serviceType": "Retreat center operations consulting", "description": pg["desc"],
          "url": f"https://retreatblueprintco.com/{pg['slug']}",
          "provider": {"@type": "ProfessionalService", "@id": "https://retreatblueprintco.com/#business", "name": "Retreat Blueprint Co."},
          "areaServed": {"@type": "Place", "name": "Worldwide"},
          "audience": {"@type": "Audience", "audienceType": "Retreat centers, eco-lodges and wellness properties that host retreats"}}
    if pg.get("faq"):
        ld = {"@context": "https://schema.org", "@graph": [ld, {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in pg["faq"]]}]}
        del ld["@graph"][0]["@context"]
    head = head.replace("</head>", '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>\n</head>", 1)
    head = head.replace("</head>", "<style>" + SHARED_CSS + theme_css(pg["theme"]) + pg.get("name_css", "") + "</style>\n</head>", 1)

    p = pg["price"]
    out = [f'''<header class="hero wb" id="top" style="--wave-b:var(--cream-dark)">
  <div class="inner">
    <div>
      <h1 class="svc-h1"><span class="label">{pg['kw']}</span> <span class="svc-name">{pg.get('name_html', pg['name'])}</span></h1>
      <p class="svc-tag">{pg['tag']}</p>
      <p class="lead">{pg['lead']}</p>
      <p class="venue-hint">For retreat centers, eco-lodges and wellness properties that host retreats.</p>
      <div class="row">
        <a class="btn primary" href="{CAL}" target="_blank" rel="noopener">Book a free call</a>
        <a class="btn text" href="{pg['jump'][0]}">{pg['jump'][1]}</a>
      </div>
    </div>
    <div class="co-price">
      <span class="k">{p['k']}</span>
      <p class="amt">{p['amt']}</p>
      <p>{p['note']}</p>
      <ul>{''.join(f'<li>{i}</li>' for i in p['items'])}</ul>
    </div>
  </div>
</header>

<section class="sec gap">
  <div class="inner">
    <p class="label">{pg['changes'][0]}</p>
    <h2 class="title">{pg['changes'][1]}</h2>
    {split_html(pg)}
    {('<div class="outcomes' + (' three' if len(pg['changes'][2]) == 3 else '') + '">' + outcomes(pg['changes'][2]) + '</div>') if pg['changes'][2] else ''}
    {pg.get("after_changes","")}
  </div>
</section>
''']
    if pg.get("band"):
        bid, blabel, btitle, kind, items, *note = pg["band"]
        if kind == "roles":
            cells = []
            for icon, h, body in items:
                body_html = f"<p>{body}</p>" if isinstance(body, str) else "<ul>" + "".join(f"<li>{x}</li>" for x in body) + "</ul>"
                cells.append(f'<div class="role"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{ICONS[icon]}"/></svg><div><h3>{h}</h3>{body_html}</div></div>')
            inner = f'<div class="roles">{"".join(cells)}</div>' + (f'<p class="band-note">{note[0]}</p>' if note else "")
        elif kind == "cycle":
            inner = '<ol class="cycle">' + "".join(f"<li><span>{i + 1:02d}</span><b>{h}</b><p>{t}</p></li>" for i, (h, t) in enumerate(items)) + "</ol>" \
                    '<p class="cycle-loop"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 12a8 8 0 1 1-2.3-5.6 M20 4v4h-4"/></svg>Then again next month, with the numbers to show what moved.</p>'
        else:
            inner = LEVELS_HTML
        out.append(f'''<div class="band wt wb" id="{bid}" style="--wave:var(--cream-dark);--wave-b:var(--warm-white)">
      <div class="band-bg" aria-hidden="true"></div>
      <div class="band-ov" aria-hidden="true"></div>
      <section class="sec">
        <div class="inner">
          <p class="label">{blabel}</p>
          <h2 class="title">{btitle}</h2>
          {inner}
        </div>
      </section>
    </div>
    ''')
    if pg.get("builder"):
        out.append(open(pg["builder"]).read())
    if pg.get("compare"):
        cl, ct, cols3 = pg["compare"]
        cells = "".join(('<div class="cmp on"><span class="pick">Best fit for most retreats</span>' if on else '<div class="cmp">') + f"<h3>{h}</h3><ul>" + "".join(f"<li>{x}</li>" for x in lis) + "</ul></div>" for h, lis, on in cols3)
        out.append(f'''<section class="sec proof-sec">
  <div class="inner">
    <p class="label">{cl}</p>
    <h2 class="title">{ct}</h2>
    <div class="compare">{cells}</div>
  </div>
</section>
''')
    if pg.get("main"):
        out = [out[0].split('<section class="sec gap">')[0], open(pg["main"]).read()]
    after_band = "var(--warm-white)"
    if pg["proof"]:
        plabel, ptitle, cards = pg["proof"]
        cells = "".join(f'''<div class="proof"><span class="loc">{loc}</span><h3>{h}</h3>{('<p class="built"><b>What was built:</b> ' + built[0] + '</p>') if built else ''}<ul>{''.join(f'<li>{x}</li>' for x in lis)}</ul>
        {f'<blockquote>"{q}"<cite>{c}</cite></blockquote>' if q else ''}</div>''' for loc, h, lis, q, c, *built in cards)
        grid_style = '' if len(cards) > 1 else ' style="grid-template-columns:minmax(0,640px)"'
        out.append(f'''<section class="sec proof-sec">
  <div class="inner">
    <p class="label">{plabel}</p>
    <h2 class="title">{ptitle}</h2>
    <div class="proof-grid"{grid_style}>{cells}</div>
    {'<p class="proof-more"><a href="/#testimonials">Hear the voice notes from these clients</a></p>' if any(c[3] for c in cards) else ''}
  </div>
</section>
''')
        how_wave = ' wt" style="--wave:var(--warm-white);--cols:{cols}"'
    else:
        how_wave = '" style="--cols:{cols}"'
    hl, ht, hs, *cols = pg["how"]
    cols = cols[0] if cols else 4
    how_bg = "background:var(--cream-dark)" if pg["proof"] else ""
    out.append(f'''<section class="sec how{' wt' if pg['proof'] else ''}" style="--cols:{cols};{('--wave:var(--warm-white);' + how_bg) if pg['proof'] else ''}">
  <div class="inner">
    <p class="label">{hl}</p>
    <h2 class="title">{ht}</h2>
    <ol class="steps">{steps(hs)}</ol>
  </div>
</section>
''')
    prev = "var(--cream-dark)" if pg["proof"] else "var(--warm-white)"
    if pg.get("faq"):
        qs = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in pg["faq"])
        out.append(f'''<section class="sec faq wt" style="--wave:{prev}">
  <div class="inner">
    <p class="label">Questions</p>
    <h2 class="title">Before you book</h2>
    {qs}
    <!-- field-notes:related --><!-- /field-notes:related -->
  </div>
</section>
''')
        prev = "var(--warm-white)"
    others = "".join(f'<a href="/{s}"><b>{n}</b><span>{d}</span><em>{pr}</em></a>' for s, (n, d, pr) in OTHERS.items() if s != pg["slug"])
    out.append(f'''<section class="sec trust wt" style="--wave:{prev}">
  <div class="inner">
    <p class="label">Other services</p>
    <h2 class="title">Need something different?</h2>
    <div class="others">{others}</div>
  </div>
</section>

<section class="sec cta wt" style="--wave:var(--sage-light)">
  <div class="cta-ov" aria-hidden="true"></div>
  <div class="inner">
    <p class="label">Start with a conversation</p>
    <h2 class="title">{pg['cta_title']}</h2>
    <p class="lead">A free 30-minute call. No obligation, just a clear next step.</p>
    <a class="btn primary" href="{CAL}" target="_blank" rel="noopener">Book a free call</a>
    <p class="email"><a href="mailto:hello@retreatblueprintco.com?subject={urllib.parse.quote(pg['name'])}%20inquiry">hello@retreatblueprintco.com</a> · <a href="https://wa.me/16479702759" target="_blank" rel="noopener">WhatsApp</a></p>
  </div>
</section>

<footer><span class="f-brand"><span class="f-logo">Retreat Blueprint Co.</span><a class="f-li" href="https://www.linkedin.com/in/shila-kandiah" target="_blank" rel="noopener me" aria-label="Shila Kandiah on LinkedIn"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M20.45 20.45h-3.55v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg></a></span><span>© 2026 · <a href="mailto:hello@retreatblueprintco.com">hello@retreatblueprintco.com</a></span></footer>
{FAQ_JS if pg.get("faq") else ""}
<script src="js/menu.js?v=2026-10-21a" defer></script>
</body>
</html>
''')
    open(f"{pg['slug']}.html", "w").write(head + "".join(out))


for pg in PAGES:
    build(pg)
    print("built", pg["slug"] + ".html")
