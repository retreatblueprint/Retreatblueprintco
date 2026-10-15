#!/usr/bin/env python3
"""Builds the four service pages (concierge-ops, foundation-sprint, strategy-retainer, growth-marketing).

They share the Buying a Retreat page's base styles, nav and footer, plus one service-page template.
Each page has its own theme (accent colour, photos, band pattern) and its own sections.
Run from the repo root:  python3 scripts/build_service_pages.py
"""
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
.svc-name{font-family:var(--serif);font-weight:400;font-size:clamp(3.2rem,8vw,6.2rem);line-height:.98;letter-spacing:-.02em;margin:0 0 1rem;color:var(--earth);text-wrap:balance}
.svc-tag{font-family:var(--serif);font-size:clamp(1.35rem,2.5vw,1.85rem);line-height:1.25;color:var(--earth-mid);margin:0 0 1.5rem;max-width:30ch}
.co-price{background:var(--warm-white);border:1px solid var(--border);border-radius:8px;padding:28px;display:grid;gap:10px;box-shadow:0 18px 40px rgba(42,34,24,.10)}
.co-price .k{font-size:.68rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--terracotta)}
.co-price .amt{font-family:var(--serif);font-size:2.5rem;line-height:1.05}
.co-price .amt small{font-family:var(--sans);font-size:.9rem;color:var(--muted);white-space:nowrap}
.co-price p{font-size:.88rem;color:var(--earth-mid)}
.co-price ul{list-style:none;display:grid;gap:8px;border-top:1px solid var(--border);padding-top:14px;margin-top:4px}
.co-price li{display:flex;gap:10px;font-size:.9rem}
.co-price li::before{content:"\\2713";color:var(--acc);font-weight:600}
.outcomes{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-top:2.5rem}
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
.proof li::before{color:var(--acc)}
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


def outcomes(items):
    return "".join(f"<div><b>{b}</b><p>{p}</p></div>" for b, p in items)


def steps(items):
    return "".join(f"<li><h4>{h}</h4><p>{p}</p></li>" for h, p in items)


PAGES = [
    dict(
        slug="concierge-ops", menu="/concierge-ops", name="Concierge Ops",
        title="Concierge Ops · Retreat Blueprint Co.",
        desc="A dedicated team, led by your Retreat Operations Director, runs your retreat's day-to-day admin: inquiries, guests, coordination and the back office. From $250 a month.",
        og="Concierge Ops: your day-to-day admin, handled.",
        theme=dict(name="Concierge Ops", acc="#4A6E4E", acc_dark="#3A5A3E", acc_soft="#7A9E7E", on_band="#C2D6C2", on_band_soft="#B8D0BA",
                   hero="photo-1777913308049-a2c79af7380a", hero_pos="60% 55%", hero_fill="#3B4A33",
                   cta="photo-1644612105654-b6b0a941ecde", cta_pos="center 60%",
                   cta_tint="linear-gradient(180deg,rgba(18,30,21,.78) 0%,rgba(18,30,21,.70) 50%,rgba(18,30,21,.82) 100%)", cta_btn="#985033",
                   band_pattern=topo("#B8D0BA"), band_grad="linear-gradient(160deg,#25402B 0%,#1A2E1F 55%,#132217 100%)", band_glow="rgba(122,158,126,.22)"),
        label="Service · Monthly", tag="Your day-to-day admin, <em>handled.</em>",
        lead="Every inquiry answered fast, every guest looked after, every invoice tracked. A dedicated team, led by your Retreat Operations Director, runs your day-to-day admin so you can focus on the experience and on selling.",
        jump=("#team", "Meet your team ↓"),
        price=dict(k="Monthly", amt="From $250 <small>/ month</small>", note="Priced on your average monthly bookings and retreat capacity.",
                   items=["Inquiries and bookings", "Guest communication", "Retreat coordination", "Invoices and records"]),
        changes=("What changes", "Less time in the inbox. More time on <em>the experience.</em>", [
            ("No more missed bookings", "Inquiries answered within hours, with follow-ups until they book or say no."),
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
        cta_title="Hand off the admin. Keep the experience.",
    ),
    dict(
        slug="foundation-sprint", menu="/foundation-sprint", name="Foundation Sprint",
        title="Foundation Sprint · Retreat Blueprint Co.",
        desc="One focused build that gives your retreat the systems it runs on: bookings, payments, numbers, guest communication and SOPs. $3,000 to $6,000, fixed fee.",
        og="Foundation Sprint: the systems your retreat runs on, built in one go.",
        theme=dict(name="Foundation Sprint", acc="#985033", acc_dark="#7E4029", acc_soft="#C98A63", on_band="#E6D3C3", on_band_soft="#DDB797",
                   hero="photo-1777913319909-1d27d36db93e", hero_pos="65% 50%", hero_fill="#5A4832",
                   cta="photo-1565214988145-8e826f79d8c2", cta_pos="center",
                   cta_tint="linear-gradient(180deg,rgba(42,26,17,.80) 0%,rgba(42,26,17,.70) 50%,rgba(42,26,17,.84) 100%)", cta_btn="#985033",
                   band_pattern=blueprint("#DDB797"), band_grad="linear-gradient(160deg,#4A3021 0%,#3A251A 55%,#2A1A11 100%)", band_glow="rgba(221,183,151,.18)"),
        label="Service · Fixed fee", tag="Everything your retreat needs to run like a <em>real business.</em>",
        lead="Built, integrated, and ready to run without you in every detail. One focused build that gives your retreat its systems: bookings and payments, your numbers, guest communication and the tools your team uses every day.",
        jump=("#build", "What gets built ↓"),
        price=dict(k="Fixed fee · Most owners start here", amt="$3,000 – $6,000", note="One project, one price, agreed before the build starts.",
                   items=["Business audit and strategy brief", "Bookings, payments and website", "Dashboards and financial tracking", "Guest communication and SOPs"]),
        changes=("What changes", "From running on memory to running on <em>systems.</em>", [
            ("One booking flow", "Inquiry to confirmed booking to payment, set up and connected."),
            ("Numbers you can see", "Financial tracking and dashboards that show how the business is doing at a glance."),
            ("Guests looked after automatically", "A guest communication playbook, automations and a welcome package."),
            ("A team that knows what to do", "SOPs and operational tools, so the business doesn't depend on you for every detail.")]),
        band=("build", "What gets built", "Ten pieces, built and connected", "roles", [
            ("compass", "Strategy", ["Business audit and strategy brief"]),
            ("card", "Bookings and payments", ["Booking system setup and configuration", "Payment processing system", "Website build or optimization"]),
            ("chart", "Your numbers", ["Financial tracking system", "Business overview dashboards"]),
            ("people", "Guests and team", ["Guest communication playbook and automations", "Guest welcome package", "SOPs and operational tools"])],
            "<b>All connected:</b> application integration across every system, so nothing is typed in twice."),
        proof=("In practice", "Built for retreats like yours", [
            ("Systemize · Dominical, Costa Rica", "A system that replaced a full-time admin role", ["A full salary saved", "Full financial clarity", "Every past guest contact in one place"],
             "Someone who takes big challenges, and turns them into simple systems that just work.", "Jonathon Conant, Founder, Airborne Arts"),
            ("Revive · Ometepe, Nicaragua", "An inactive venue rebuilt and taking bookings again", ["Every booking in one streamlined system", "Guest communication automated", "Relaunched with a new brand and paid ads"],
             "Shila took on the nearly impossible task of building our entire digital backend from the ground up.", "Cris Ketch, Founder, Infinity Retreat")]),
        how=("How it works", "Audit, build, hand over", [
            ("Audit", "How the business runs today: bookings, money, guests and team."),
            ("Plan", "A strategy brief and a build plan, agreed before anything changes."),
            ("Build", "Systems set up, connected and tested."),
            ("Handover", "SOPs, training and a walk-through so your team can run it.")]),
        cta_title="Build the foundation once. Run on it every season.",
    ),
    dict(
        slug="strategy-retainer", menu="/strategy-retainer", name="Strategy Retainer",
        title="Strategy Retainer · Retreat Blueprint Co.",
        desc="An ongoing strategic partner for your retreat: monthly strategy sessions, metrics and priorities, team clarity, SOP refinements and growth planning. $1,000 to $2,000 a month.",
        og="Strategy Retainer: a partner who keeps your retreat moving forward.",
        theme=dict(name="Strategy Retainer", acc="#2F6467", acc_dark="#234D50", acc_soft="#6E9EA0", on_band="#C4DADB", on_band_soft="#9CC4C6",
                   hero="photo-1782139186009-6fcc4f2326ea", hero_pos="60% 60%", hero_fill="#2F4A4C",
                   cta="photo-1782061419033-591356402cd4", cta_pos="center 55%",
                   cta_tint="linear-gradient(180deg,rgba(12,34,36,.78) 0%,rgba(12,34,36,.66) 50%,rgba(12,34,36,.82) 100%)", cta_btn="#985033",
                   band_pattern=topo("#9CC4C6"), band_grad="linear-gradient(160deg,#1E4547 0%,#163638 55%,#0F2829 100%)", band_glow="rgba(156,196,198,.18)"),
        label="Service · Monthly", tag="A partner who keeps the business <em>moving forward.</em>",
        lead="An ongoing strategic partner who sets direction, tracks what's working, and keeps the business moving forward. Every month: the numbers reviewed, priorities set, and a clear plan for what comes next.",
        jump=("#rhythm", "Your monthly rhythm ↓"),
        price=dict(k="Monthly", amt="$1,000&nbsp;–&nbsp;$2,000 <small>/ month</small>", note="Ongoing direction once your systems are in place.",
                   items=["Monthly strategy sessions", "Metrics review and priority setting", "Team management and clarity", "SOP refinements and growth planning"]),
        changes=("What changes", "Fewer guesses. <em>Clearer decisions.</em>", [
            ("Know your numbers", "Metrics reviewed every month, so decisions start from what's actually happening."),
            ("Focus on what matters", "Priorities set together, so the month goes to the work that moves the business."),
            ("A team that's clear", "Roles and expectations kept clear as the business and the team grow."),
            ("Systems that keep up", "SOPs refined as things change, so nothing drifts back to how it was.")]),
        band=("rhythm", "Every month", "Your monthly rhythm", "cycle", [
            ("Review the numbers", "Bookings, revenue and costs, against last month and your goals."),
            ("Set priorities", "The few things that will move the business most this month."),
            ("Strategy session", "Decisions made together, with clear owners and next steps."),
            ("Team and SOPs", "Roles clarified and procedures updated where things changed."),
            ("Plan growth", "The next season, the next offer, the next hire.")]),
        proof=("In practice", "The work doesn't stop at the build", [
            ("Infinity Retreat · Ometepe, Nicaragua", "Kept on as an ongoing consultant after the build", ["Bookings, guests and payments in one system", "Relaunched with a new brand, website and paid ads", "Retained as an ongoing consultant"],
             "Shila has continued working with me as a consultant, a testament to the value she brings and the confidence I have in her abilities.", "Cris Ketch, Founder, Infinity Retreat")]),
        how=("How it starts", "Three steps to a steady rhythm", [
            ("Free call", "Where the business is now, and where you want it to go."),
            ("First session", "Your baseline numbers and the first set of priorities."),
            ("Monthly rhythm", "Review, decide, act, repeat.")], 3),
        cta_title="Keep the business moving forward.",
    ),
    dict(
        slug="growth-marketing", menu="/growth-marketing", name="Growth Marketing",
        title="Growth Marketing · Retreat Blueprint Co.",
        desc="Marketing for retreat venues: strategy and positioning, content, social media systems, outreach and lead generation, from strategy only to fully managed. Pricing on inquiry.",
        og="Growth Marketing: get your retreat seen by the right people.",
        theme=dict(name="Growth Marketing", acc="#8A5414", acc_dark="#6E420F", acc_soft="#C9934A", on_band="#D6D3E2", on_band_soft="#E2B877",
                   hero="photo-1699694927472-46a4fcf68973", hero_pos="62% 40%", hero_fill="#4A4430",
                   cta="photo-1760774714285-61ff516f86c5", cta_pos="center 60%",
                   cta_tint="linear-gradient(180deg,rgba(28,26,44,.72) 0%,rgba(28,26,44,.58) 50%,rgba(28,26,44,.80) 100%)", cta_btn="#985033",
                   band_pattern=topo("#E2B877"), band_grad="linear-gradient(160deg,#2C2F4A 0%,#232640 55%,#191B30 100%)", band_glow="rgba(226,184,119,.20)"),
        label="Service · Fully managed", tag="Getting your retreat seen by <em>the right people.</em>",
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
             "Shila took on the nearly impossible task of building our entire digital backend from the ground up.", "Cris Ketch, Founder, Infinity Retreat")]),
        how=("How it starts", "From first call to campaigns going out", [
            ("Free call", "Your guests, your goals, and what's worked so far."),
            ("Strategy", "Positioning, channels and a content plan."),
            ("Launch", "Content, campaigns and outreach going out, reviewed month to month.")], 3),
        cta_title="Fill the calendar with the right guests.",
    ),
]

OTHERS = {
    "foundation-sprint": ("Foundation sprint", "The systems your retreat runs on, built in one go.", "$3,000 – $6,000 →"),
    "strategy-retainer": ("Strategy retainer", "A monthly partner for direction and growth.", "From $1,000 / month →"),
    "concierge-ops": ("Concierge ops", "Your day-to-day admin, handled.", "From $250 / month →"),
    "growth-marketing": ("Growth marketing", "Get your retreat seen by the right people.", "Pricing on inquiry →"),
    "buying-a-retreat": ("Buying a retreat?", "Pre-purchase review and your first 90 days.", "From $1,200 →"),
}

LEVELS_HTML = """<div class="levels">
        <div class="level lite"><span class="k">Strategy only</span><h3>The plan, ready for your team</h3><p>For venues with someone to run marketing day to day, who need the direction.</p>
          <ul><li>Marketing strategy and positioning</li><li>Content direction</li></ul></div>
        <div class="level full"><span class="k">Fully managed</span><h3>Strategy plus a dedicated team</h3><p>Everything in strategy only, then executed for you, end to end.</p>
          <ul><li>Dedicated marketing lead, fully managed</li><li>Content creation handled end to end</li><li>Social media systems and scheduling</li><li>Outreach campaigns and sales funnel</li><li>Custom lead generator</li></ul>
          <span class="plus">Scope discussed on inquiry</span></div>
      </div>"""


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
    head = head.replace("</head>", "<style>" + SHARED_CSS + theme_css(pg["theme"]) + "</style>\n</head>", 1)

    p = pg["price"]
    out = [f'''<header class="hero wb" id="top" style="--wave-b:var(--cream-dark)">
  <div class="inner">
    <div>
      <p class="label">{pg['label']}</p>
      <h1 class="svc-name">{pg['name']}</h1>
      <p class="svc-tag">{pg['tag']}</p>
      <p class="lead">{pg['lead']}</p>
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
    <div class="outcomes">{outcomes(pg['changes'][2])}</div>
  </div>
</section>
''']
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
    after_band = "var(--warm-white)"
    if pg["proof"]:
        plabel, ptitle, cards = pg["proof"]
        cells = "".join(f'''<div class="proof"><span class="loc">{loc}</span><h3>{h}</h3><ul>{''.join(f'<li>{x}</li>' for x in lis)}</ul>
        <blockquote>"{q}"<cite>{c}</cite></blockquote></div>''' for loc, h, lis, q, c in cards)
        grid_style = '' if len(cards) > 1 else ' style="grid-template-columns:minmax(0,640px)"'
        out.append(f'''<section class="sec proof-sec">
  <div class="inner">
    <p class="label">{plabel}</p>
    <h2 class="title">{ptitle}</h2>
    <div class="proof-grid"{grid_style}>{cells}</div>
    <p class="proof-more"><a href="/#testimonials">Hear the voice notes from these clients</a></p>
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
    <p class="email"><a href="mailto:hello@retreatblueprintco.com?subject={urllib.parse.quote(pg['name'])}%20inquiry">hello@retreatblueprintco.com</a></p>
  </div>
</section>

<footer><span class="f-logo">Retreat Blueprint Co.</span><span>© 2026 · <a href="mailto:hello@retreatblueprintco.com">hello@retreatblueprintco.com</a></span></footer>
<script src="js/menu.js?v=2026-10-16a" defer></script>
</body>
</html>
''')
    open(f"{pg['slug']}.html", "w").write(head + "".join(out))


for pg in PAGES:
    build(pg)
    print("built", pg["slug"] + ".html")
