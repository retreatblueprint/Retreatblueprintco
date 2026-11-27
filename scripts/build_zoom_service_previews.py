#!/usr/bin/env python3
"""Build the hidden zoom-style previews of the four service pages (preview/svc/<slug>.html).

Uses the homepage zoom preview (preview/zoom.html) as the shell for head, nav and footer,
so every page shares the same look. Each page: a wide hero photo, then pinned stops that
zoom through its own photo journey, a calm-scroll card for long parts (quote builder, FAQ),
and a closing stop. Copy marked DRAFT in comments is new wording for Shila to approve.
Run from the repo root:  python3 scripts/build_zoom_service_previews.py
"""
import re, os, html as H

U = 'https://images.unsplash.com/'
def src(i, w): return f'{U}{i}?auto=format&fit=crop&w={w}&q=80'
def srcset(i): return ', '.join(f'{src(i, w)} {w}w' for w in (1200, 2000, 2800))

CAL = 'https://cal.com/shila-kandiah/'
VN = {'jon': ('Jonathon', '0:53'), 'cris': ('Cris', '0:59')}
PROOF = {
  'airborne': dict(place='Airborne Arts &middot; Dominical, Costa Rica', big='Full-time administrative salary avoided.',
     cap='A custom operating system replaced the need for a full-time administrative assistant, with clearer financial oversight for the owner.',
     q='&ldquo;Someone who takes big challenges, and turns them into simple systems that just work.&rdquo;', who='Jonathon Conant', role='Founder, Airborne Arts', vn='jon'),
  'infinity': dict(place='Infinity Retreat &middot; Ometepe, Nicaragua', big='+37% occupancy in 6 months',
     cap='An inactive venue rebuilt and taking bookings again, with no further double bookings reported.',
     q='&ldquo;Shila took on the nearly impossible task of building our entire digital backend from the ground up.&rdquo;', who='Cris Ketch', role='Founder, Infinity Retreat', vn='cris'),
}

def faq_from(page):
    s = open(page + '.html').read()
    items = re.findall(r'<details.*?</details>', s, re.S)
    out = []
    for d in items:
        d = re.sub(r'href="/(?=[a-z])', 'href="/preview/svc/', d)  # keep links inside the preview where a preview page exists
        out.append(d)
    return '\n'.join(out)

PAGES = {
 'foundation-sprint': dict(
   name='Foundation Sprint', acc='#985033', accd='#7E4029', soft='#F3E4D9', call=CAL + 'foundation-sprint-call',
   photos=['photo-1754078219069-7565df2033b0', 'photo-1775283537748-4fc2b5fb28c0', 'photo-1791535766539-32200ac0ba30',
           'photo-1777913319909-1d27d36db93e', 'photo-1777913319909-1d27d36db93e', 'photo-1767324672978-f26a05319e63'],
   hero=dict(eyebrow='Foundation Sprint &middot; retreat center systems setup',
             h1='Run on systems,<br><em>not memory.</em>',  # DRAFT
             promise='Bookings, payments, guest communication and your numbers, built once and connected.',  # DRAFT
             price='From $100 USD &middot; build your own quote, no minimum', jump=('#quote', 'Build your quote &darr;')),
   stops=[
     dict(kind='signs', eyebrow='Is this you?', h2='When the business runs on memory, everything waits for you.',  # DRAFT
          sub='Each piece of the Foundation Sprint replaces a gap like these with a system.',  # DRAFT
          cards=[('Bookings live in your inbox and your head', 'One booking flow, from inquiry to confirmed booking to payment.'),
                 ('You can&rsquo;t tell if last month made money', 'Numbers you can see at a glance.'),
                 ('Every guest gets a different answer', 'Guest communication that sends itself, on time.'),
                 ('Nothing happens unless you&rsquo;re there', 'SOPs so your team knows what to do.')],
          cta=('#quote', 'Build your quote &darr;')),
     dict(kind='steps', eyebrow='How it works', h2='Audit, plan, build, hand over.',
          steps=[('Audit', 'How the pieces you chose are handled today, so nothing is built on guesswork.'),
                 ('Plan', 'What needs to change, the cost and the flow, agreed before anything is built.'),
                 ('Build', 'A connected version of each piece, tested so it all works together.'),
                 ('Handover', 'A walk-through and training so your team can run it.')],
          note='A single piece can take days to a couple of weeks. The full build usually takes 1 to 3 months, with training so your team can run it.'),
     dict(kind='proof', eyebrow='In practice', h2='Built for retreats <em>like yours.</em>', cards=['airborne', 'infinity']),
     dict(kind='flow', id='quote', builder=True),
     dict(kind='close', eyebrow='Start with a conversation', h2='Build the foundation once.<br><em>Run on it every season.</em>',
          body='A free 30-minute call. No obligation, just a clear next step.'),
   ]),
 'concierge-ops': dict(
   name='Concierge Ops', acc='#4A6E4E', accd='#3A5A3E', soft='#E2EBE2', call=CAL + 'concierge-ops-call',
   photos=['photo-1762177446992-4cac5b44a05d', 'photo-1572511443032-a3cfe6823872', 'photo-1596436876625-091f67351709',
           'photo-1596436891234-ab1fbd9353e5', 'photo-1606194017837-97658d442c49', 'photo-1606194017837-97658d442c49', 'photo-1635248518288-2bdc4402fe37'],
   hero=dict(eyebrow='Concierge Ops &middot; retreat admin &amp; booking management',
             h1='Hand over<br><em>the inbox.</em>',  # DRAFT
             promise='Every inquiry answered within 2 business hours, in your voice, while you host.',  # DRAFT (facts from the page)
             price='From $250 USD / month &middot; 3-month minimum', jump=('#handover', 'See what you hand over &darr;')),
   stops=[
     dict(kind='signs', eyebrow='Is this you?', h2='When the admin waits for you, your guests wait too.',  # DRAFT
          sub='Every one of these is work your Concierge Ops team takes over.',
          cards=[('Inquiries wait until you have a free evening', 'Replies within 2 business hours, in your voice.'),
                 ('Interested guests go quiet', 'Well-timed, polite follow-ups until they book or decide.'),
                 ('Forms and reminders go out late, or not at all', 'Pre-arrival emails, forms and reminders sent on time.'),
                 ('Invoices and payments live in your head', 'Invoices sent, payments tracked, a month-end summary.')],
          cta=('#handover', 'See what you hand over &darr;')),
     dict(kind='roles', id='handover', eyebrow='Exactly what you hand over', h2='Four roles. <em>Every task named.</em>',
          roles=[('Inquiries and bookings', 'Remote Booking Assistant', ['Replies to every inquiry in your voice, within 2 business hours', 'Well-timed, polite follow-ups', 'Calendar and booking sites kept current'], 'Pricing decisions and special requests.'),
                 ('Guest communication', 'Guest Experience Assistant', ['Pre-arrival emails and forms', 'Reminders sent on time, every time', 'Feedback and review requests'], 'The welcome and the experience itself.'),
                 ('Retreat coordination', 'Operations Coordinator', ['Organizers, guests and your team coordinated in one place', 'Rooming lists and schedules ready before arrival', 'Event preparation checklists'], 'Meeting retreat leaders and hosting.'),
                 ('Back office', 'Back Office Administrator', ['Invoices sent and payments tracked', 'Records organized in one place', 'A month-end summary of what came in'], 'Spending and strategy decisions.')]),
     dict(kind='points', eyebrow='Your accounts and your guests&rsquo; details', h2='Trusted with your inbox, <em>treated with care.</em>',
          points=[('You own every account.', 'Nothing is moved or transferred. We work inside the inbox and booking system you already use.'),
                  ('Access only for the work.', 'Each team member gets what their role needs, and nothing more.'),
                  ('Guest information stays private.', 'Details are used only to look after your guests.'),
                  ('Access ends when you say so.', 'If you stop, access is removed and your accounts stay with you.')]),
     dict(kind='steps', eyebrow='How it starts', h2='From first call to a team that runs it.',
          steps=[('Free call', 'Your bookings, your tools, and where the admin piles up.'),
                 ('Set-up', 'Access to your inbox and booking system; your voice, policies and templates handed over.'),
                 ('Your team takes over', 'Inquiries, guests, coordination and the back office, handled every day.'),
                 ('Monthly check-in', 'What came in, what got booked, and what to improve next.')]),
     dict(kind='flow', id='faq'),
     dict(kind='close', eyebrow='Start with a conversation', h2='Give every guest your full attention.<br><em>We&rsquo;ll handle the admin.</em>',
          body='A free 30-minute call. No obligation, just a clear next step.'),
   ]),
 'fractional-operations-director': dict(
   name='Fractional Retreat Operations Director', acc='#2F6467', accd='#234D50', soft='#DCE8E8', call=CAL + 'fractional-director-call',
   photos=['photo-1587242778880-f5a1b727a006', 'photo-1590172815327-22cbf36dd2be', 'photo-1589982146187-a6cc277751ea',
           'photo-1567491634123-460945ea86dd', 'photo-1730815252343-f80770ec8eaa', 'photo-1791535771068-e0fa043957dc', 'photo-1791535771068-e0fa043957dc', 'photo-1788690732470-7a72a0a34d96'],
   hero=dict(eyebrow='Fractional Retreat Operations Director &middot; fractional COO for retreat centers',
             h1='Senior leadership,<br><em>without a full-time hire.</em>',
             promise='I manage your department leads, coordinate retreat delivery, and follow through on the improvements we agree on.',
             price='From $1,800 USD / month', jump=('#tiers', 'Compare packages &darr;')),
   stops=[
     dict(kind='signs', eyebrow='Who it&rsquo;s for', h2='When the business needs another level of leadership.',
          sub='This partnership may be right for you if:',
          list=['Your property is operating, but performance isn&rsquo;t where it should be.',
                'You have a capable team that needs clearer direction, accountability, or coordination.',
                'Revenue is coming in, but profitability and cash flow need closer attention.',
                'You&rsquo;re expanding, restructuring, or preparing for the next stage of growth.',
                'You need someone to connect business priorities with day-to-day execution.'],
          cta=('#tiers', 'Compare packages &darr;')),
     dict(kind='points', eyebrow='What I oversee', h2='Connecting the decisions <em>that shape your business.</em>',
          points=[('Business performance', 'Review revenue, operating costs, booking performance, and financial trends to identify risks and opportunities.'),
                  ('Operational systems', 'Evaluate and improve the processes, technology, and workflows that support the business.'),
                  ('Team and service delivery', 'Strengthen responsibilities, communication, operating standards, and accountability across teams.'),
                  ('Planning and implementation', 'Translate business priorities into actionable plans, coordinate progress, and evaluate results.')]),
     dict(kind='tiers', id='tiers', eyebrow='How we work together', h2='Choose the level of leadership <em>your venue needs.</em>',
          tiers=[('Essential', 'Operations leadership', 'From $1,800 USD / month', 'I manage your department leads directly so your team knows what needs to happen before, during, and after each retreat.'),
                 ('Core', 'Operations + financial visibility', 'From $2,800 USD / month', 'I lead your operation, improve the guest journey, and help you see what bookings, costs, and collections mean for the business.'),
                 ('Embedded', 'Delegated operations', 'From $4,500 USD / month', 'I take responsibility for operating and guest experience decisions within agreed limits.')],
          note='Six-month minimum. Concierge Ops can be added to any tier for day-to-day admin.'),
     dict(kind='points', eyebrow='The numbers &middot; part of Core and Embedded', h2='Performance is more <em>than occupancy.</em>',
          sub='I connect financial performance with the operational realities behind it, so you can see what is driving results.',
          points=[('Revenue performance', 'Occupancy &middot; ADR &middot; RevPAR &middot; Booking mix'),
                  ('Operating profitability', 'Cost per occupied room &middot; Break-even occupancy &middot; Operating margin'),
                  ('Financial planning', 'Cash flow &middot; Budget versus actuals &middot; Seasonal forecasting')]),
     dict(kind='proof', eyebrow='In practice', h2='Systems and implementation, <em>in practice.</em>', cards=['airborne']),
     dict(kind='flow', id='faq'),
     dict(kind='close', eyebrow='Start with a conversation', h2='Tell me what you&rsquo;d like <em>to hand over.</em>',
          body='We&rsquo;ll talk through what your venue needs and which level of support fits.'),
   ]),
 'growth-marketing': dict(
   name='Growth Marketing', acc='#8A5414', accd='#6E420F', soft='#F2E6D3', call=CAL + 'growth-marketing-call',
   photos=['photo-1588504633950-9dc518941e93', 'photo-1772064901543-fb4a5d9f4736', 'photo-1772064901616-00264a6c4104',
           'photo-1758448756167-88dc934c58e4', 'photo-1782739249749-62de55c76535', 'photo-1782739249749-62de55c76535', 'photo-1762254923872-5bdc4210eb90'],
   hero=dict(eyebrow='Growth Marketing &middot; retreat center marketing',
             h1='Seen by the guests<br><em>who fit your retreat.</em>',
             promise='The guests who fit your retreat find it, trust it and book.',
             price='Pricing on inquiry &middot; strategy only or fully managed', jump=('#levels', 'Choose your level &darr;')),
   stops=[
     dict(kind='signs', eyebrow='Is this you?', h2='Great retreats stay quiet when the right people can&rsquo;t find them.',  # DRAFT
          sub='Growth Marketing closes each of these gaps.',  # DRAFT
          cards=[('Your website says what you have, not who it&rsquo;s for', 'A clear position: who your retreat is for.'),
                 ('Your best moments never make it online', 'Content that shows the experience.'),
                 ('Posting waits for a free afternoon', 'A consistent presence, scheduled.'),
                 ('Inquiries come in waves, then stop', 'A steady pipeline from outreach and a lead generator.')],
          cta=('#levels', 'Choose your level &darr;')),
     dict(kind='levels', id='levels', eyebrow='Choose your level', h2='From strategy only <em>to fully managed.</em>',
          levels=[('Strategy only', 'The plan, ready for your team', 'For venues with someone to run marketing day to day, who need the direction.', ['Marketing strategy and positioning', 'Content direction']),
                  ('Fully managed', 'Strategy plus a dedicated team', 'Everything in strategy only, then executed for you, end to end.', ['Dedicated marketing lead, fully managed', 'Content creation handled end to end', 'Social media systems and scheduling', 'Outreach campaigns and sales funnel', 'Custom lead generator'])],
          note='Scope discussed on inquiry.'),
     dict(kind='proof', eyebrow='In practice', h2='A venue relaunched <em>and back in front of guests.</em>', cards=['infinity'],
          extra=['Marketing rebrand and website', 'Content strategy', 'Paid ads across Costa Rica and Nicaragua', 'Custom lead generation app']),
     dict(kind='steps', eyebrow='How it starts', h2='From first call to campaigns going out.',
          steps=[('Free call', 'Your guests, your goals, and what&rsquo;s worked so far.'),
                 ('Strategy', 'Positioning, channels and a content plan.'),
                 ('Launch', 'Content, campaigns and outreach going out, reviewed month to month.')]),
     dict(kind='flow', id='faq'),
     dict(kind='close', eyebrow='Start with a conversation', h2='Fill the calendar <em>with the right guests.</em>',
          body='A free 30-minute call. No obligation, just a clear next step.'),
   ]),
}

PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>'

def proof_card(key):
    p = PROOF[key]; n, t = VN[p['vn']]
    return (f'<article class="pcard"><p class="pplace">{p["place"]}</p><p class="pbig">{p["big"]}</p><p class="pcap">{p["cap"]}</p>'
            f'<blockquote class="pq">{p["q"]}</blockquote><p class="pwho"><b>{p["who"]}</b>{p["role"]}</p>'
            f'<div class="vnote" data-src="assets/audio/voice-note-{p["vn"]}.m4a"><button class="vplay" type="button" aria-label="Play {n}&rsquo;s voice note">{PLAY}</button>'
            f'<div class="vmeta"><b>Hear from {n}</b><span class="vbar"><i></i></span></div><span class="vtime">{t}</span></div></article>')

def stop_html(st, pg, i):
    k = st['kind']; sid = f' id="{st["id"]}"' if st.get('id') else ''
    head = lambda: f'<div class="svh"><p class="eyebrow">{st["eyebrow"]}</p><h2>{st["h2"]}</h2>' + (f'<p class="svsub">{st["sub"]}</p>' if st.get('sub') else '') + '</div>'
    if k == 'signs':
        if st.get('cards'):
            body = '<div class="svsigns">' + ''.join(f'<div class="svsign"><p class="svp">{a}</p><p class="svfix">{b}</p></div>' for a, b in st['cards']) + '</div>'
        else:
            body = '<ul class="svlist">' + ''.join(f'<li>{x}</li>' for x in st['list']) + '</ul>'
        cta = f'<a class="btn svcta" href="{st["cta"][0]}">{st["cta"][1]}</a>' if st.get('cta') else ''
        inner = head() + body + cta
        cls = 'svstop sv-left'
    elif k == 'steps':
        inner = head() + '<ol class="svsteps">' + ''.join(f'<li><span class="svn">{n+1:02d}</span><b>{a}</b><p>{b}</p></li>' for n, (a, b) in enumerate(st['steps'])) + '</ol>' + (f'<p class="svnote">{st["note"]}</p>' if st.get('note') else '')
        cls = 'svstop sv-card'
    elif k == 'points':
        inner = head() + '<div class="svpoints">' + ''.join(f'<div class="svpt"><b>{a}</b><p>{b}</p></div>' for a, b in st['points']) + '</div>'
        cls = 'svstop sv-card'
    elif k == 'roles':
        inner = head() + '<div class="svroles">' + ''.join(
            f'<div class="svrole"><p class="svrk">{r}</p><b>{t}</b><ul>' + ''.join(f'<li>{x}</li>' for x in tasks) + f'</ul><p class="svkeep"><span>You keep:</span> {keep}</p></div>'
            for t, r, tasks, keep in st['roles']) + '</div>'
        cls = 'svstop sv-center'
    elif k == 'tiers':
        inner = head() + '<div class="svtiers">' + ''.join(
            f'<div class="svtier"><p class="svrk">{lab}</p><h3>{n}</h3><p class="svprice">{pr}</p><p>{d}</p><a class="btn svtb" href="{pg["call"]}" target="_blank" rel="noopener">Discuss {n}</a></div>'
            for n, lab, pr, d in st['tiers']) + '</div>' + f'<p class="svnote">{st["note"]}</p>'
        cls = 'svstop sv-center'
    elif k == 'levels':
        inner = head() + '<div class="svtiers svtiers--2">' + ''.join(
            f'<div class="svtier"><p class="svrk">{n}</p><h3>{t}</h3><p>{d}</p><ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul></div>'
            for n, t, d, items in st['levels']) + '</div>' + f'<p class="svnote">{st["note"]}</p>'
        cls = 'svstop sv-center'
    elif k == 'proof':
        extra = ('<ul class="svextra">' + ''.join(f'<li>{x}</li>' for x in st['extra']) + '</ul>') if st.get('extra') else ''
        inner = head() + f'<div class="pcards{" pcards--1" if len(st["cards"]) == 1 else ""}">' + ''.join(proof_card(c) for c in st['cards']) + '</div>' + extra
        cls = 'svstop sv-center zp'
    elif k == 'flow':
        parts = []
        if st.get('builder'):
            parts.append(open('content/foundation-quote-builder.html').read())
        parts.append('<div class="svfaq"><p class="label">Questions</p><h2 class="title">Before you book</h2>' + faq_from(slug_of[pg['name']]) + '</div>')
        return f'<section class="svflow"{sid}><div class="wrap"><div class="svflow-card">' + ''.join(parts) + '</div></div></section>'
    elif k == 'close':
        inner = (f'<p class="eyebrow">{st["eyebrow"]}</p><h2>{st["h2"]}</h2><p class="body">{st["body"]}</p>'
                 f'<a class="btn btn--light" href="{pg["call"]}" target="_blank" rel="noopener">Book a free call</a>'
                 '<div class="note-block"><p>Prefer to write first? <a href="mailto:hello@retreatblueprintco.com?subject=Retreat%20Blueprint%20Co.%20inquiry">hello@retreatblueprintco.com</a> or <a href="https://wa.me/16479702759" target="_blank" rel="noopener">WhatsApp</a></p></div>')
        cls = 'svstop sv-close'
    return f'<section class="{cls}"{sid}><div class="wrap">{inner}</div></section>'

slug_of = {v['name']: k for k, v in PAGES.items()}

def build(slug, pg, shell_head, shell_nav, shell_foot):
    imgs = ''.join(f'<img class="svimg" data-i="{n}" src="{src(p, 2000)}" srcset="{srcset(p)}" sizes="(max-width: 760px) 260vw, 120vw" alt=""{" fetchpriority=\"high\"" if n == 0 else " loading=\"lazy\""}>'
                   for n, p in enumerate(pg['photos']))
    h = pg['hero']
    hero = (f'<header class="zs zs1 svhero"><div class="zsnap" style="top:0" aria-hidden="true"></div><div class="zcopy">'
            f'<p class="eyebrow">{h["eyebrow"]}</p><h1>{h["h1"]}</h1><p class="zpromise">{h["promise"]}</p><p class="svhprice">{h["price"]}</p>'
            f'<div class="hero-actions"><a class="btn" href="{pg["call"]}" target="_blank" rel="noopener">Book a free call</a>'
            f'<a class="link-quiet" href="{h["jump"][0]}">{h["jump"][1]}</a></div></div></header>')
    stops = ''.join(stop_html(st, pg, i) for i, st in enumerate(pg['stops']))
    world = (f'<div class="zworld svworld" id="top" style="--acc:{pg["acc"]};--acc-d:{pg["accd"]};--acc-soft:{pg["soft"]}">'
             f'<div class="zstick" aria-hidden="true">{imgs}<div class="zshade zshade--hero"></div><div class="svshade"></div></div>'
             f'{hero}{stops}</div>')
    head = re.sub(r'<title>.*?</title>', f'<title>Preview · {pg["name"]} · Retreat Blueprint Co.</title>', shell_head, flags=re.S)
    head = re.sub(r'<link rel="canonical"[^>]*>\s*', '', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', head, flags=re.S)
    head = re.sub(r'preview/zoom\.css\?v=\d+', 'preview/zoom.css?v=60', head)
    head = head.replace('</head>', '<link rel="stylesheet" href="preview/svc.css?v=2">\n</head>')
    foot = re.sub(r'<script src="preview/zoom\.js[^"]*" defer></script>', '<script src="preview/svc.js?v=1" defer></script>', shell_foot)
    page = head + shell_nav + world + foot
    page = page.replace('href="/preview/zoom.html#', 'href="/preview/zoom.html#')
    os.makedirs('preview/svc', exist_ok=True)
    open(f'preview/svc/{slug}.html', 'w').write(page)

def main():
    s = open('preview/zoom.html').read()
    a = s.index('</head>') + len('</head>')
    shell_head = s[:a]
    w = s.index('<div class="zworld"')
    shell_nav = s[a:w]
    f = s.index('<footer')
    # page ends: footer and scripts
    shell_foot = s[f:]
    # service links in nav/footer point at the preview versions
    for slug in PAGES:
        shell_nav = shell_nav.replace(f'href="/{slug}"', f'href="/preview/svc/{slug}.html"')
        shell_foot = shell_foot.replace(f'href="/{slug}"', f'href="/preview/svc/{slug}.html"')
    for slug, pg in PAGES.items():
        build(slug, pg, shell_head, shell_nav, shell_foot)
        print('built preview/svc/' + slug + '.html')

if __name__ == '__main__':
    main()
