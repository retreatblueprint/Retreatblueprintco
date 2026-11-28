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
           'photo-1777913319909-1d27d36db93e', 'photo-1767324672978-f26a05319e63'],
   hero=dict(eyebrow='Foundation Sprint &middot; retreat center systems setup',
             h1='Run on systems,<br><em>not memory.</em>',  # DRAFT
             promise='Bookings, payments, guest communication and your numbers, built once and connected.',  # DRAFT
             aud='For retreat centers, eco-lodges and wellness properties that host retreats.',
             price='Pieces from $100 USD &middot; no minimum &middot; 10% off 3 or more, 15% off the full package', jump=('#quote', 'Build your quote &darr;')),
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
     dict(kind='flow', id='quote', builder=True),
     dict(kind='close', eyebrow='Start with a conversation', h2='Build the foundation once.<br><em>Run on it every season.</em>',
          body='A free 30-minute call. No obligation, just a clear next step.'),
   ]),
 'concierge-ops': dict(
   name='Concierge Ops', acc='#4A6E4E', accd='#3A5A3E', soft='#E2EBE2', call=CAL + 'concierge-ops-call',
   photos=['photo-1762177446992-4cac5b44a05d', 'photo-1572511443032-a3cfe6823872', 'photo-1596436876625-091f67351709',
           'photo-1596436891234-ab1fbd9353e5', 'photo-1596436891234-ab1fbd9353e5', 'photo-1635248518288-2bdc4402fe37'],
   hero=dict(eyebrow='Concierge Ops &middot; retreat admin &amp; booking management',
             h1='Hand over<br><em>the inbox.</em>',  # DRAFT
             promise='A dedicated team, led by your Retreat Operations Director, answers every inquiry within 2 business hours, in your voice, in English and Spanish.',  # DRAFT (facts from the page)
             aud='For retreat centers, eco-lodges and wellness properties that host retreats.',
             price='From $250 USD / month &middot; 3-month minimum', jump=('#handover', 'See what you hand over &darr;')),
   stops=[
     dict(kind='signs', eyebrow='Is this you?', h2='When the admin waits for you, your guests wait too.',  # DRAFT
          sub='Every one of these is work your Concierge Ops team takes over.',
          cards=[('Inquiries wait until you have a free evening', 'Replies within 2 business hours, in your voice, including while a retreat is in session.'),
                 ('Interested guests go quiet', 'Well-timed, polite follow-ups until they book or decide.'),
                 ('Forms and reminders go out late, or not at all', 'Pre-arrival emails, forms and reminders sent on time.'),
                 ('Invoices and payments live in your head', 'Invoices sent, payments tracked, a month-end summary.')],
          cta=('#handover', 'See what you hand over &darr;')),
     dict(kind='roles', id='handover', eyebrow='Exactly what you hand over', h2='Four roles. <em>Every task named.</em>',
          roles=[('Inquiries and bookings', 'Remote Booking Assistant', ['Replies to every inquiry in your voice, within 2 business hours', 'Well-timed, polite follow-ups', 'Confirmations and reservation details sent', 'Calendar and booking sites kept current'], 'Pricing decisions and special requests.'),
                 ('Guest communication', 'Guest Experience Assistant', ['Pre-arrival emails and forms', 'Reminders sent on time, every time', 'Questions answered before and after the stay', 'Feedback and review requests'], 'The welcome and the experience itself.'),
                 ('Retreat coordination', 'Operations Coordinator', ['Organizers, guests and your team coordinated in one place', 'Rooming lists and schedules ready before arrival', 'Event preparation checklists'], 'Meeting retreat leaders and hosting.'),
                 ('Back office', 'Back Office Administrator', ['Invoices sent and payments tracked', 'Records organized in one place', 'A month-end summary of what came in'], 'Spending and strategy decisions.')]),
     dict(kind='together', eyebrow='How we&rsquo;ll work together', h2='From first call to a team that runs it, <em>with your inbox treated with care.</em>',  # DRAFT heading (merges two sections)
          sub='Handing over access takes trust. We protect and manage the privacy of your accounts, your access and your guests&rsquo; information, so you are never left wondering who can see what.',
          steps=[('Free call', 'Your bookings, your tools, and where the admin piles up.'),
                 ('Set-up', 'Access to your inbox and booking system; your voice, policies and templates handed over.'),
                 ('Your team takes over', 'Inquiries, guests, coordination and the back office, handled every day.'),
                 ('Monthly check-in', 'What came in, what got booked, and what to improve next.')],
          points=[('You own every account.', 'Nothing is moved or transferred. We work inside the inbox and booking system you already use.'),
                  ('Access only for the work.', 'Each team member gets what their role needs, and nothing more.'),
                  ('Guest information stays private.', 'Details are used only to look after your guests.'),
                  ('Access ends when you say so.', 'If you stop, access is removed and your accounts stay with you.')]),
     dict(kind='flow', id='faq'),
     dict(kind='close', eyebrow='Start with a conversation', h2='Give every guest your full attention.<br><em>We&rsquo;ll handle the admin.</em>',
          body='A free 30-minute call. No obligation, just a clear next step.'),
   ]),
 'fractional-operations-director': dict(
   name='Fractional Retreat Operations Director', acc='#2F6467', accd='#234D50', soft='#DCE8E8', call=CAL + 'fractional-director-call',
   photos=['photo-1587242778880-f5a1b727a006', 'photo-1590172815327-22cbf36dd2be', 'photo-1589982146187-a6cc277751ea',
           'photo-1567491634123-460945ea86dd', 'photo-1730815252343-f80770ec8eaa', 'photo-1791535771068-e0fa043957dc', 'photo-1788690732470-7a72a0a34d96'],
   hero=dict(eyebrow='Fractional Retreat Operations Director &middot; fractional COO for retreat centers',
             h1='Senior leadership,<br><em>without a full-time hire.</em>',
             promise='I manage your department leads, coordinate retreat delivery, and follow through on the improvements we agree on.',
             aud='For retreat centers, eco-lodges and wellness properties that host retreats.',
             price='From $1,800 USD / month &middot; 6-month minimum', jump=('#tiers', 'Compare packages &darr;')),
   stops=[
     dict(kind='signs', eyebrow='Who it&rsquo;s for', h2='When the business needs another level of leadership.',
          sub='Not every retreat needs a full-time operations director. But as a property develops, the decisions become more complex, and the need for experienced oversight becomes more important. This partnership may be right for you if:',
          list=['Your property is operating, but performance isn&rsquo;t where it should be.',
                'You have a capable team that needs clearer direction, accountability, or coordination.',
                'Revenue is coming in, but profitability and cash flow need closer attention.',
                'You&rsquo;re expanding, restructuring, or preparing for the next stage of growth.',
                'You need someone to connect business priorities with day-to-day execution.'],
          cta=('#tiers', 'Compare packages &darr;')),
     dict(kind='panel', eyebrow='What I oversee', h2='Connecting the decisions <em>that shape your business.</em>',
          sub='Pricing decisions affect occupancy and revenue. Staffing decisions influence service delivery and costs. Weak systems create work that shouldn&rsquo;t need to happen.',
          points=[('Business performance', 'Review revenue, operating costs, booking performance, and financial trends to identify risks and opportunities.'),
                  ('Operational systems', 'Evaluate and improve the processes, technology, and workflows that support the business.'),
                  ('Team and service delivery', 'Strengthen responsibilities, communication, operating standards, and accountability across teams.'),
                  ('Planning and implementation', 'Translate business priorities into actionable plans, coordinate progress, and evaluate results.')]),
     dict(kind='flow', id='tiers', faq=False, tiers=dict(
          label='How we work together', title='Choose the level of leadership your venue needs.',
          lead='I lead your department teams, coordinate retreat delivery, and follow through on the improvements we agree on. Choose how much responsibility you want me to take on.',
          cols=[('Essential', 'Operations leadership', '$1,800', 'I manage your department leads directly so your team knows what needs to happen before, during, and after each retreat.', None,
                 ['Departments I can lead include kitchen, housekeeping, maintenance, and guest care.',
                  'I set priorities and clarify responsibilities with department leads, check in typically every two weeks, and improve the handoffs and procedures your team relies on to deliver retreats.',
                  'Retreat readiness, including rooming, meals, logistics, and team briefings and debriefs.',
                  'Guest experience oversight during retreats. I set service expectations with department leads, follow up on guest and organiser concerns, and coordinate fixes with the team and vendors.',
                  'One operational improvement at a time and a monthly owner update on progress and priorities.']),
                ('Core', 'Operations + financial visibility', '$2,800', 'I lead your operation, improve the guest journey, and help you see what bookings, costs, and collections mean for the business.', 'Everything in Essential, plus',
                 ['A regular owner check-in to review decisions and follow-through.',
                  'Monthly performance summary covering bookings, collections, and retreat contribution, using your existing records, plus a budget-to-actual review where a working budget is in place.',
                  'Quarterly pricing and booking-mix review, plus a look at where retreat inquiries stall.',
                  'Guest journey improvement from pre-arrival through departure. I review guest and organiser feedback, identify recurring friction, and lead changes to team handoffs and service standards.',
                  'I use performance data, guest feedback, and a review of your workflows and tools to identify what&rsquo;s holding the operation back. I lead up to two agreed improvements at a time and check whether they&rsquo;re working.']),
                ('Embedded', 'Delegated operations', '$4,500', 'I take responsibility for operating and guest experience decisions within agreed limits.', 'Everything in Core, plus',
                 ['Decision authority over areas such as scheduling and vendor approvals.',
                  'Guest experience ownership across departments, including setting service standards, directing how escalated guest concerns are resolved, and approving remedies.',
                  'I set the quarterly operating plan, review a rolling 12-month cash-flow forecast with you each month, and adjust staffing, vendor, and service priorities within the authority we agree on.',
                  'Hiring and onboarding support for key roles.',
                  'Operational planning for expansion or a new offer, with up to three improvements at a time.',
                  'On-site support in Central America available as part of a tailored scope.'])],
          note='Six-month minimum. We agree on departments, retreat coverage, working hours, and escalation windows before we start. Your department leads carry out the work on site. Concierge Ops can be added to any tier for day-to-day admin, including inboxes, booking updates, guest messages, and payment tracking.')),
     dict(kind='metrics', eyebrow='The numbers &middot; part of Core and Embedded', h2='Performance is more <em>than occupancy.</em>',
          sub='A full calendar doesn&rsquo;t always translate into a healthy bottom line. I connect financial performance with the operational realities behind it, helping owners understand what is driving results and where changes can make the greatest difference.',
          groups=[('Revenue performance', ['Occupancy', 'ADR', 'RevPAR', 'Booking mix']),
                  ('Operating profitability', ['Cost per occupied room', 'Break-even occupancy', 'Operating margin']),
                  ('Financial planning', ['Cash flow', 'Budget versus actuals', 'Seasonal forecasting'])],
          note='For exclusive-use or package-based retreats, the measures are shaped around your business model.'),
     dict(kind='flow', id='faq'),
     dict(kind='close', eyebrow='Start with a conversation', h2='Tell me what you&rsquo;d like <em>to hand over.</em>',
          body='We&rsquo;ll talk through what your venue needs and which level of support fits.'),
   ]),
 'growth-marketing': dict(
   name='Growth Marketing', acc='#8A5414', accd='#6E420F', soft='#F2E6D3', call=CAL + 'growth-marketing-call',
   photos=['photo-1588504633950-9dc518941e93', 'photo-1772064901543-fb4a5d9f4736', 'photo-1772064901616-00264a6c4104',
           'photo-1782739249749-62de55c76535', 'photo-1782739249749-62de55c76535', 'photo-1762254923872-5bdc4210eb90'],
   hero=dict(eyebrow='Growth Marketing &middot; retreat center marketing',
             h1='Seen by the guests<br><em>who fit your retreat.</em>',
             promise='Scope built around what you actually need, from strategy only to full execution with a dedicated team, so the guests who fit your retreat find it, trust it and book.',  # DRAFT (joins two lines from the page)
             aud='For retreat centers, eco-lodges and wellness properties that host retreats.',
             price='From $500 USD &middot; strategy only or fully managed', jump=('#levels', 'Choose your level &darr;')),  # DRAFT price from Shila
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
     dict(kind='steps', eyebrow='How it starts', h2='From first call to campaigns going out.',
          steps=[('Free call', 'Your guests, your goals, and what&rsquo;s worked so far.'),
                 ('Strategy', 'Positioning, channels and a content plan.'),
                 ('Launch', 'Content, campaigns and outreach going out, reviewed month to month.')]),
     dict(kind='flow', id='faq'),
     dict(kind='close', eyebrow='Start with a conversation', h2='Fill the calendar <em>with the right guests.</em>',
          body='A free 30-minute call. No obligation, just a clear next step.'),
   ]),
 'buying-a-retreat': dict(
   name='Buying a Retreat', acc='#5B6B3A', accd='#47552C', soft='#E6EAD8', call=CAL + 'retreat-buyer-call',
   photos=['photo-1675432979329-e8f2ac1cd914', 'photo-1656039306242-0d36a34cda1d', 'photo-1710330758725-ff587bc14ffe',
           'photo-1711948728889-614d5d0030f8', 'photo-1789930153509-2c8a0c3ccec4', 'photo-1789930153694-14f21db66d1d',
           'photo-1772703003096-fe4096559f81', 'photo-1709390083401-4fdbc56970d9', 'photo-1731924823462-5614a26b4ede'],
   hero=dict(eyebrow='Buying a retreat center? &middot; pre-purchase operations review',
             h1='Know what you&rsquo;re buying.<br><em>Run it well from day one.</em>',
             promise='An independent operations review before you buy a retreat venue, and a hands-on 90-day plan after you get the keys. So the property you fell in love with becomes a business that works.',
             aud='For retreat centers, eco-lodges and wellness properties that host retreats.',
             price='Pre-purchase review from $1,200 USD', jump=('#packages', 'See the packages &darr;'), jump2=('#agents', 'Real estate agents &darr;')),
   stops=[
     dict(kind='gap', eyebrow='The gap', h2='Your lawyer checks the title. Your inspector checks the roof. <em>Nobody checks the operation.</em>',
          sub='When you buy a retreat venue, you&rsquo;re buying a business as much as a property. How well it runs depends on bookings, people and systems that never show up in a listing, and that&rsquo;s where buyers lose money.',
          roles=[('Lawyer or notary', 'Title, liens and transfer'), ('Inspector', 'The buildings'), ('Accountant', 'The books and taxes'), ('Retreat Blueprint Co.', 'How the business runs')]),
     dict(kind='flow', id='review', faq=False, extra_html='@@BUYTWO@@'),
     dict(kind='unseen', eyebrow='After closing', h2='What buyers often don&rsquo;t see <em>until after closing.</em>',
          items=['Bookings that depend on the owner&rsquo;s personal relationships', 'Know-how that lives only in the owner&rsquo;s head',
                 'Booking and payment accounts that don&rsquo;t transfer easily', 'Deposits already collected for retreats after closing']),
     dict(kind='flow', id='sample', faq=False, extra_html='@@BUYREPORT@@'),
     dict(kind='steps', eyebrow='How it works', h2='7 to 10 business days, <em>inside your due diligence window.</em>',
          steps=[('Kickoff call', 'Your goals, budget, timeline and concerns.', 'Day 1'), ('Data request', 'The seller shares records through your agent.', 'Days 1&ndash;3'),
                 ('Analysis', 'Financials, bookings, reviews and a mystery-shop inquiry.', 'Days 3&ndash;6'), ('Walk-through', 'On-Site: 2&ndash;3 days on the property with the owner and team. Desk: a video walk-through and owner call.', 'Days 6&ndash;8'),
                 ('Report &amp; debrief', 'Your 5-page report and a call on findings and negotiation points.', 'Days 9&ndash;10')],
          note='<b>The best time to start:</b> once your offer is accepted and before you sign the final purchase agreement. <span class="svnote-x">Ask your lawyer to make the review a condition of your offer, so you have time to act on what it finds.</span>'),
     dict(kind='flow', id='packages', faq=False, tiers=None, extra_html='@@BUYPACKAGES@@'),
     dict(kind='flow', id='agents', faq_page='buying-a-retreat', extra_html='@@BUYAGENTS@@'),
     dict(kind='close', eyebrow='Start with a conversation', h2='Tell me about the property <em>you&rsquo;re looking at.</em>',
          body='A free 30-minute call. No obligation, just a clear next step.'),
   ]),
}

AREAS = [('Revenue &amp; bookings', '24 months by revenue line, repeat business and future bookings.'), ('Demand &amp; channels', 'Where guests come from, and how much rests on one source.'),
         ('Pricing &amp; margins', 'Rates against nearby venues and the true cost of a retreat week.'), ('Guest experience', 'Review trends, response times, leader contracts and deposits.'),
         ('Team &amp; owner dependence', 'Who does what, and what lives only in the owner&rsquo;s head.'), ('Systems &amp; tools', 'Booking, payments and accounts, and whether they transfer.'),
         ('Operations &amp; suppliers', 'Kitchen, housekeeping, transport and maintenance routines.'), ('Compliance &amp; risk', 'Licenses and insurance, flagged for your lawyer.')]
RP = [('Score &amp; summary', 'Your Operations Health Score across 8 areas, the verified revenue and the true cost at a glance.'),
      ('Findings', 'Key business metrics, the listing checked against real records, and each risk with a suggested next step.'),
      ('Costs &amp; upside', 'The true monthly cost to operate, what the venue could earn with stronger operations, and the bottom line.'),
      ('Roadmap: before closing to day 30', 'What to secure before you sign, and how to protect bookings, accounts and the team in month one.'),
      ('Roadmap: days 31 to 90', 'Systems, procedures and training, then the plan to fill the calendar, with targets to track.')]
IMG = 'assets/img/buying-a-retreat/'

EXTRA = {
 '@@BUYTWO@@': """<div class="svbuy"><p class="label">Two ways I help</p><h2 class="title">Before you buy, and after you get the keys.</h2>
 <div class="svpaths">
  <div class="svpath"><p class="svrk">For buyers and investors &middot; thinking of buying</p><h3>Pre-Purchase Operations Review</h3>
   <p class="svpath-d">An independent, neutral picture of how the venue runs, so you can decide with confidence and plan from day one.</p>
   <ul><li>Operations Health Score across 8 areas</li><li>Key numbers verified against records</li><li>Risks to address, each with a suggested next step</li><li>The true monthly cost to operate</li><li>The upside: what the venue could earn with stronger operations</li><li>A week-by-week 90-day roadmap</li></ul>
   <a class="svlink" href="assets/docs/sample-report.pdf" data-viewer="report" data-page="1">See what the 5-page report looks like &rarr;</a></div>
  <div class="svpath svpath--acc" id="ninety"><p class="svrk">After the acquisition &middot; just bought</p><h3>The First 90 Days</h3>
   <p class="svpath-d">Hands-on support through the acquisition of your new retreat property, across the whole business:</p>
   <p class="svcovers"><span>Financial management</span><span>Operational planning</span><span>Technology</span><span>Marketing</span><span>Training</span><span>Guest experience</span><span>Next stage of growth</span></p>
   <ul><li><b>Days 1&ndash;30, Protect:</b> the P&amp;L tracked from day one, the seller&rsquo;s know-how captured, every booked guest and retreat leader kept, and the team steadied</li><li><b>Days 31&ndash;60, Build:</b> a budget and forecast, an operational plan, one system for administration, finances and client relationships, the team trained, and the guest experience defined from inquiry to checkout</li><li><b>Days 61&ndash;90, Grow:</b> your marketing relaunched, past guests and leaders reconnected, and the next stage of growth mapped in a 12-month plan</li></ul></div>
 </div></div>
 <div class="svbuy svbuy--areas" id="areas"><p class="label">What I review</p><h2 class="title">Eight areas, each scored and explained.</h2>
 <p class="lead">An outside view that gives buyer and seller the same clear picture of how the business runs, explained in plain language.</p>
 <ol class="svareas">""" + ''.join(f'<li><span>{n+1:02d}</span><b>{a}</b><p>{b}</p></li>' for n, (a, b) in enumerate(AREAS)) + """</ol></div>""",
 '@@BUYREPORT@@': """<div class="svbuy"><p class="label">What you receive</p><h2 class="title">A detailed 5-page report, so you know exactly what you&rsquo;re buying.</h2>
 <p class="lead">Every review ends with a detailed 5-page report. You&rsquo;ll know what the business really earns and costs, what could go wrong after closing and what to ask for before you sign, plus a week-by-week plan for your first 90 days. Written in plain language and ready to share with your lawyer, accountant and agent.</p>
 <div class="svrp">""" + ''.join(
    f'<figure><button type="button" data-viewer="report" data-page="{n+1}" aria-label="Open page {n+1} of the sample report"><img src="{IMG}sample-report-page-{n+1}.jpg" alt="Page {n+1} of the sample report: {a}" loading="lazy"></button><span>Page {n+1}</span><b>{a}</b><p>{b}</p></figure>'
    for n, (a, b) in enumerate(RP)) + """</div>
 <p class="svrp-cta"><a class="btn svtb" href="assets/docs/sample-report.pdf" target="_blank" rel="noopener" data-viewer="report" data-page="1">View the sample report</a></p>
 <p class="svpk-note">Sample report for a fictional venue, prepared as an On-Site Review. Every report is prepared under NDA and released only with your permission.</p></div>""",
 '@@BUYPACKAGES@@': """<div class="svpkwrap"><p class="label">Packages</p><h2 class="title">A small cost against a six- or seven-figure decision.</h2>
 <div class="svpks">
  <div class="svpk"><div class="svpk-top"><p class="svrk">Remote &middot; anywhere in the world</p><h3>Desk Review</h3><p class="svpk-price"><b>$1,200</b> <span>USD</span></p><p class="svpk-desc">Know what you&rsquo;re really buying, without getting on a plane.</p><a class="btn svtb" href="@@CALL@@" target="_blank" rel="noopener">Book a free call</a></div>
   <p class="svpk-plus">What you get</p><ul><li>An Operations Health Score across all 8 areas</li><li>The listing&rsquo;s numbers checked against real records</li><li>The true monthly cost to run it under new ownership</li><li>Every risk flagged, with a suggested next step</li><li>A mystery-shop inquiry, so you see what guests see</li><li>A 5-page report with a week-by-week 90-day roadmap</li><li>A 60-minute debrief on findings and negotiation points</li><li>Delivered in 7 business days</li></ul></div>
  <div class="svpk svpk--mid"><div class="svpk-top"><p class="svrk">Most complete &middot; before you make an offer</p><h3>On-Site Review</h3><p class="svpk-price"><b>$2,500</b> <span>USD + travel</span></p><p class="svpk-desc">See the operation running before you sign.</p><a class="btn svtb" href="@@CALL@@" target="_blank" rel="noopener">Book a free call</a></div>
   <p class="svpk-plus">Everything in the Desk Review, plus</p><ul><li>2&ndash;3 days on the property with the owner and team</li><li>A changeover or live retreat observed first-hand</li><li>The guest experience tested in person</li><li>Team interviews: who owns what, and any flags to watch</li><li>An upside plan: what the venue could earn with stronger operations</li><li>Delivered in 10 business days</li></ul></div>
  <div class="svpk"><div class="svpk-top"><p class="svrk">Post-acquisition</p><h3>The First 90 Days</h3><p class="svpk-price"><b>Priced on scope</b> <span>half your review fee credited</span></p><p class="svpk-desc">Take over without losing a season.</p><a class="btn svtb" href="@@CALL@@" target="_blank" rel="noopener">Book a free call</a></div>
   <p class="svpk-plus">From financial management and operational planning to technology, marketing, training, guest experience and the next stage of growth.</p>
   <p class="svpk-ph">Days 1&ndash;30 &middot; Protect</p><ul><li>The P&amp;L tracked: revenue, ROI, EBITDA and guest retention</li><li>The seller&rsquo;s know-how, booked guests and team kept</li></ul>
   <p class="svpk-ph">Days 31&ndash;60 &middot; Build</p><ul><li>A budget, forecast and operational plan</li><li>One system, a trained team and the guest experience defined</li></ul>
   <p class="svpk-ph">Days 61&ndash;90 &middot; Grow</p><ul><li>Marketing relaunched and past guests reconnected</li><li>The next stage of growth: a 12-month plan</li></ul>
   <p class="svpk-after">After day 90, keep it running with a <a href="/preview/svc/fractional-operations-director.html">part-time retreat operations director</a>, or hand the daily admin to <a href="/preview/svc/concierge-ops.html">Concierge Ops</a>.</p></div>
 </div>
 <div class="svworld-note"><b>Buying a retreat property anywhere in the world?</b><p>The Desk Review is fully remote, so it works for retreat venues in any country, and for buyers who can&rsquo;t be on site yet.</p></div>
 <p class="svpk-note">This review covers operations only. Legal, structural and tax checks stay with your lawyer, inspector and accountant.</p></div>""",
 '@@BUYAGENTS@@': """<div class="svind"><p class="label">Independent and confidential</p><h2 class="title">A clear picture you can trust, on both sides of the deal.</h2>
 <div class="svind-g"><div><b>Independent</b><p>You hire me, and my findings are the same whether or not the sale goes ahead. If an agent referred you, any referral fee is disclosed to you in writing and never depends on what I find.</p></div>
 <div><b>Confidential</b><p>Everything shared by buyers and sellers is protected and kept confidential. An NDA is signed before any records are shared, and reports are released only with your permission.</p></div>
 <div><b>Fair to both sides</b><p>The review isn&rsquo;t about catching anyone out. It gives buyer and seller the same clear picture, which helps good deals close.</p></div></div></div>
 <div class="svagents"><p class="label">For real estate agents</p><h2 class="title">Help retreat deals close, on both sides.</h2>
 <p class="lead">Whether you&rsquo;re listing a retreat property or representing a buyer, I add an independent view of how the business runs, without slowing the deal down.</p>
 <div class="svlanes">
  <div class="svlane" id="listing-snapshot"><button class="svlane-pages" type="button" data-viewer="snapshot" data-page="1" aria-label="Open the sample Listing Snapshot"><img src="@@IMG@@sample-listing-snapshot-page-1.jpg" alt="Page 1 of the sample Listing Snapshot" loading="lazy"><img src="@@IMG@@sample-listing-snapshot-page-2.jpg" alt="Page 2 of the sample Listing Snapshot" loading="lazy"></button>
   <p class="svrk">For your sellers &middot; Listing Snapshot</p><h3>Help your listing sell</h3><p>A 2-page independent summary of how the business runs, checked against records. Share it with serious buyers before they make an offer.</p>
   <ul><li>Key numbers checked against records</li><li>Handover readiness across 8 areas</li><li>Gaps fixed before listing</li></ul><p class="svlane-price">Priced per property</p>
   <button class="btn svtb" type="button" data-viewer="snapshot" data-page="1">See a sample Listing Snapshot</button></div>
  <div class="svlane"><button class="svlane-pages" type="button" data-viewer="report" data-page="1" aria-label="Open the sample Pre-Purchase report"><img src="@@IMG@@sample-report-page-1.jpg" alt="Page 1 of the sample Pre-Purchase report" loading="lazy"><img src="@@IMG@@sample-report-page-4.jpg" alt="Page 4 of the sample Pre-Purchase report" loading="lazy"></button>
   <p class="svrk">For your buyers &middot; Pre-Purchase Review</p><h3>Help your buyers close with confidence</h3><p>I don&rsquo;t tell buyers whether to buy. I give them a clear picture and a plan, inside their due diligence window.</p>
   <ul><li>A detailed 5-page report</li><li>Delivered within 10 business days</li><li>Support through their first 90 days</li></ul><p class="svlane-price">From $1,200 USD</p>
   <button class="btn svtb" type="button" data-viewer="report" data-page="1">See the sample report</button></div>
 </div>
 <div class="svind-g svind-g--2"><div><b>Referral fee</b><p>Paid on every review, Listing Snapshot and 90-day plan you refer, and always disclosed to your client. Details on a partner call.</p></div>
 <div><b>Happy owners</b><p>Buyers who succeed send you their friends.</p></div></div>
 <p class="svag-h">How it works for you</p>
 <ol class="svtl svtl--row"><li><span class="svtl-dot">1</span><div><b>You introduce the buyer or seller</b><p>A quick email or WhatsApp intro is all it takes.</p></div></li><li><span class="svtl-dot">2</span><div><b>I deliver within 10 business days</b><p>I work through you to request records, so the deal stays on track.</p></div></li><li><span class="svtl-dot">3</span><div><b>You receive your referral fee</b><p>Paid as soon as your client pays for their service.</p></div></li></ol>
 <p><a class="btn svtb" href="https://cal.com/shila-kandiah/agent-partner-call" target="_blank" rel="noopener">Book a partner call</a></p></div>""",
 '@@BUYREAD@@': """<div class="svread"><p class="label">Further reading &middot; Field Notes</p><a href="/field-notes/buying-a-retreat-center-costa-rica">Buying a Retreat Center in Costa Rica: 9 Checks Before You Sign &rarr;</a></div>""",
}
for k in EXTRA: EXTRA[k] = EXTRA[k].replace('@@IMG@@', IMG)

def _viewer():
    live = open('buying-a-retreat.html').read()
    a = live.index('<dialog class="rv"'); b = live.index('</script>', a) + len('</script>')
    return live[a:b]
VIEWER_HTML = _viewer()
ME = ('<div class="svme"><img src="assets/img/shila-avatar.jpg" alt="Shila Kandiah" width="56" height="56" loading="lazy">'
      '<p><b>Shila Kandiah, Retreat Operations Director.</b> 10 years in business operations management, now focused entirely on retreat venue operations. On-site across Central America, remote worldwide. '
      '<a href="/preview/zoom.html#about">Read my story &rarr;</a></p></div>')

OTHERS = {
 'foundation-sprint': ('Foundation Sprint', 'The systems behind a smooth stay, built piece by piece: bookings, payments, guest communication and your numbers.', 'From $100 &middot; build your own quote'),
 'concierge-ops': ('Concierge Ops', 'Every inquiry and guest message answered in your voice, so guests feel looked after from the first email.', 'From $250 USD / month'),
 'fractional-operations-director': ('Fractional Retreat Operations Director', 'Your part-time operations director for the guest experience, the numbers, the team and the systems.', 'From $1,800 USD / month'),
 'growth-marketing': ('Growth Marketing', 'Strategy, content and outreach so the right guests and retreat leaders find you and know what to expect.', 'From $500 USD'),
 'buying-a-retreat': ('Buying a retreat?', 'Pre-purchase review and your first 90 days.', 'From $1,200 USD'),
}
READING = {
 'foundation-sprint': [('/field-notes/retreat-center-high-season-preparation', '8 weeks to high season: a calmer season and guests who come back')],
 'concierge-ops': [('/field-notes/delegate-retreat-center-inbox', 'When to Hand Over Your Inbox So Your Retreat Center Can Grow'),
                   ('/field-notes/7-signs-youre-the-bottleneck-in-your-own-retreat-center', '7 signs you&rsquo;re the bottleneck in your own retreat center')],
 'buying-a-retreat': [('/field-notes/buying-a-retreat-center-costa-rica', 'Buying a Retreat Center in Costa Rica: 9 Checks Before You Sign')],
}
def more_html(slug, pg):
    me = ('<div class="svbio"><img src="assets/img/shila-avatar.jpg" alt="Shila Kandiah" width="120" height="120" loading="lazy">'
          '<div><p class="label">Who you&rsquo;ll work with</p><p class="svbio-t"><b>Shila Kandiah, Retreat Operations Director.</b> 10 years in business operations management, now focused entirely on retreat venue operations. On-site across Central America, remote worldwide.</p>'
          '<p class="svbio-l"><a href="/preview/zoom.html#about">Read my story &rarr;</a><a href="/preview/zoom.html#testimonials">See client results &rarr;</a></p></div></div>')
    cards = ''.join(f'<a class="svother" href="/preview/svc/{k}.html"><b>{n}</b><p>{d}</p><span>{pr} &rarr;</span></a>' for k, (n, d, pr) in OTHERS.items() if k != slug)
    others = f'<div class="svothers-w"><p class="label">Other services</p><h2 class="title">Need something different?</h2><div class="svothers">{cards}</div></div>'
    rd = ''
    if READING.get(slug):
        rd = '<div class="svread"><p class="label">Further reading &middot; Field Notes</p>' + ''.join(f'<a href="{h}">{t} &rarr;</a>' for h, t in READING[slug]) + '</div>'
    return me + others + rd

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
        inner = head() + '<ol class="svsteps">' + ''.join(f'<li><span class="svn{" svn--d" if len(x) > 2 else ""}">{x[2] if len(x) > 2 else f"{n+1:02d}"}</span><b>{x[0]}</b><p>{x[1]}</p></li>' for n, x in enumerate(st['steps'])) + '</ol>' + (f'<p class="svnote">{st["note"]}</p>' if st.get('note') else '')
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
        inner = head() + f'<div class="pcards{" pcards--1" if len(st["cards"]) == 1 else ""}">' + ''.join(proof_card(c) for c in st['cards']) + '</div>' + extra + (ME if st.get('me') else '')
        cls = 'svstop sv-center zp'
    elif k == 'together':
        tl = '<ol class="svtl">' + ''.join(f'<li><span class="svtl-dot">{n+1}</span><div><b>{a}</b><p>{b}</p></div></li>' for n, (a, b) in enumerate(st['steps'])) + '</ol>'
        tr = '<ul class="svtrust">' + ''.join(f'<li><b>{a}</b> {b}</li>' for a, b in st['points']) + '</ul>'
        inner = head() + f'<div class="svtogether"><div class="svcol"><p class="svcolk">How it starts</p>{tl}</div><div class="svcol svcol--trust"><p class="svcolk">Your accounts and your guests&rsquo; details</p>{tr}</div></div>'
        cls = 'svstop sv-center'
    elif k == 'panel':
        inner = head() + '<div class="svpanel">' + ''.join(f'<div><b>{a}</b><p>{b}</p></div>' for a, b in st['points']) + '</div>'
        cls = 'svstop sv-center'
    elif k == 'metrics':
        inner = head() + '<div class="svmetrics">' + ''.join(
            f'<div><b>{t}</b><p>' + ''.join(f'<span>{m}</span>' for m in ms) + '</p></div>' for t, ms in st['groups']) + '</div>' + (f'<p class="svnote">{st["note"]}</p>' if st.get('note') else '')
        cls = 'svstop sv-center'
    elif k == 'gap':
        inner = head() + '<div class="svgap">' + ''.join(f'<div class="svgap-i{" svgap-i--me" if n == 3 else ""}"><b>{a}</b><p>{b}</p></div>' for n, (a, b) in enumerate(st['roles'])) + '</div>'
        cls = 'svstop sv-center'
    elif k == 'two':
        inner = head() + '<div class="svtwo">' + ''.join(
            f'<div class="svtwo-c"><p class="svrk">{k1}</p><h3>{t}</h3><p class="svtwo-d">{d}</p><ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul></div>'
            for k1, t, d, items in st['cols']) + '</div>'
        cls = 'svstop sv-center'
    elif k == 'eight':
        inner = head() + '<ol class="sveight">' + ''.join(f'<li><span>{n+1:02d}</span><b>{a}</b><p>{b}</p></li>' for n, (a, b) in enumerate(st['areas'])) + '</ol>'
        cls = 'svstop sv-center'
    elif k == 'report':
        inner = head() + '<ol class="svreport">' + ''.join(f'<li><span>Page {n+1}</span><b>{a}</b><p>{b}</p></li>' for n, (a, b) in enumerate(st['pages'])) + '</ol>' + f'<a class="btn svcta svcta--c" href="{st["link"][0]}" target="_blank" rel="noopener">{st["link"][1]}</a>'
        cls = 'svstop sv-center'
    elif k == 'unseen':
        inner = head() + '<ol class="svunseen">' + ''.join(f'<li><span>{n+1:02d}</span><p>{x}</p></li>' for n, x in enumerate(st['items'])) + '</ol>'
        cls = 'svstop sv-center'
    elif k == 'flow':
        parts = []
        if st.get('builder'):
            parts.append(open('content/foundation-quote-builder.html').read())
        if st.get('tiers'):
            t = st['tiers']
            cols = ''
            for n, (name, lab, price, desc, plus, items) in enumerate(t['cols']):
                cols += (f'<div class="svpk{" svpk--mid" if n == 1 else ""}"><div class="svpk-top"><p class="svrk">{lab}</p><h3>{name}</h3>'
                         f'<p class="svpk-price">From <b>{price}</b> <span>USD / month</span></p><p class="svpk-desc">{desc}</p>'
                         f'<a class="btn svtb" href="{pg["call"]}" target="_blank" rel="noopener">Discuss {name}</a></div>'
                         + (f'<p class="svpk-plus">{plus}</p>' if plus else '<p class="svpk-plus">What&rsquo;s included</p>')
                         + '<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul></div>')
            parts.append(f'<div class="svpkwrap"><p class="label">{t["label"]}</p><h2 class="title">{t["title"]}</h2><p class="lead">{t["lead"]}</p><div class="svpks">{cols}</div><p class="svpk-note">{t["note"]}</p></div>')
        if st.get('extra_html'):
            parts.append(EXTRA.get(st['extra_html'], st['extra_html']).replace('@@CALL@@', pg['call']))
        if st.get('faq', True):
            parts.append('<div class="svfaq"><p class="label">Questions</p><h2 class="title">Before you book</h2>' + faq_from(st.get('faq_page') or slug_of[pg['name']]) + '</div>')
        if st.get('after_html'):
            parts.append(EXTRA[st['after_html']])
        if st.get('faq', True) or st.get('builder'):
            parts.append(more_html(slug_of[pg['name']], pg))
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
            f'<p class="eyebrow">{h["eyebrow"]}</p><h1>{h["h1"]}</h1><p class="zpromise">{h["promise"]}</p>' + (f'<p class="svaud">{h["aud"]}</p>' if h.get('aud') else '') + f'<p class="svhprice">{h["price"]}</p>'
            f'<div class="hero-actions"><a class="btn" href="{pg["call"]}" target="_blank" rel="noopener">Book a free call</a>'
            f'<a class="link-quiet" href="{h["jump"][0]}">{h["jump"][1]}</a>' + (f'<a class="link-quiet" href="{h["jump2"][0]}">{h["jump2"][1]}</a>' if h.get('jump2') else '') + '</div></div></header>')
    stops = ''.join(stop_html(st, pg, i) for i, st in enumerate(pg['stops']))
    world = (f'<div class="zworld svworld" id="top" style="--acc:{pg["acc"]};--acc-d:{pg["accd"]};--acc-soft:{pg["soft"]}">'
             f'<div class="zstick" aria-hidden="true">{imgs}<div class="zshade zshade--hero"></div><div class="svshade"></div></div>'
             f'{hero}{stops}</div>' + (VIEWER_HTML if 'data-viewer' in stops else ''))
    head = re.sub(r'<title>.*?</title>', f'<title>Preview · {pg["name"]} · Retreat Blueprint Co.</title>', shell_head, flags=re.S)
    head = re.sub(r'<link rel="canonical"[^>]*>\s*', '', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', head, flags=re.S)
    head = re.sub(r'preview/zoom\.css\?v=\d+', 'preview/zoom.css?v=60', head)
    head = head.replace('</head>', '<link rel="stylesheet" href="preview/svc.css?v=8">\n</head>')
    foot = re.sub(r'<script src="preview/zoom\.js[^"]*" defer></script>', '<script src="preview/svc.js?v=2" defer></script>', shell_foot)
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
