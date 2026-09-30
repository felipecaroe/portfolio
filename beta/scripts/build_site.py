from pathlib import Path
import json
import re
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://felipecaroe.github.io/portfolio/beta/"
EMAIL = "felipie@gmail.com"
SOCIALS = ["https://www.linkedin.com/in/felipecaroe/", "https://www.behance.net/felipecaroe"]
PAGES = []


def link(to, label, classes="text-link"):
    return f'<a class="{classes}" href="@@ROOT@@{to}">{label} <span class="arrow" aria-hidden="true">↗</span></a>'


def nav(current):
    items = [("work", "work.html", "Work"), ("services", "services.html", "Services"), ("leadership", "leadership.html", "About"), ("contact", "contact.html", "Contact")]
    return "".join(
        f'<a href="@@ROOT@@{path}" class="{("nav-contact" if key == "contact" else "")}"'
        f'{(" aria-current=page" if current == key else "")}>{label}</a>'
        for key, path, label in items
    )


def page(path, title, description, content, current="", schema=None):
    prefix = "../" if "/" in path else ""
    canonical = BASE + ("" if path == "index.html" else path)
    person = {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": BASE + "#felipe",
        "name": "Felipe Amorim",
        "alternateName": "Felipe Caroé Amorim",
        "url": BASE,
        "image": BASE + "img/felipe.png",
        "jobTitle": "Senior AI product designer and UX lead",
        "homeLocation": {"@type": "Place", "name": "Madrid, Spain"},
        "sameAs": SOCIALS,
    }
    nodes = [person, {"@context": "https://schema.org", "@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": title, "description": description, "author": {"@id": BASE + "#felipe"}}]
    if schema:
        nodes.append({"@context": "https://schema.org", **schema})
    ld = json.dumps(nodes, ensure_ascii=False).replace("<", "\\u003c")
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f5f1e9">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <meta name="robots" content="noindex,follow">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="@@ROOT@@img/favicon.ico">
  <link rel="stylesheet" href="@@ROOT@@assets/site.css">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{BASE}img/ogthumb.png">
  <meta property="og:image:alt" content="Felipe Amorim, senior freelance UX/UI designer for agency teams.">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="shell header-row">
  <a class="brand" href="@@ROOT@@index.html" aria-label="Felipe Amorim, home"><img class="brand-anchor" src="@@ROOT@@img/anchor.svg" alt="">Felipe Amorim</a>
  <nav class="nav" aria-label="Main navigation">{nav(current)}</nav>
</div></header>
<main id="main">
{content}
</main>
<div class="viewport-blur viewport-blur--top" aria-hidden="true"><div></div><div></div><div></div><div></div><div></div><div></div></div>
<div class="viewport-blur viewport-blur--bottom" aria-hidden="true"><div></div><div></div><div></div><div></div><div></div><div></div></div>
<footer class="site-footer"><div class="shell">
  <div class="footer-top"><div><div class="footer-kicker">Need senior design capacity?</div><h2>Bring me in for the <em>next brief.</em></h2></div>
    {link("contact.html?service=agency", "Discuss a client brief", "button button--light")}
  </div>
  <div class="footer-bottom"><span class="footer-signature"><img src="@@ROOT@@img/anchor_w.svg" alt=""><span>© 2026 Felipe Amorim · Madrid, Spain</span></span><nav class="footer-socials" aria-label="Contact and social links">
    <a href="mailto:{EMAIL}"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg><span>Email</span></a>
    <a href="https://www.linkedin.com/in/felipecaroe/" rel="me"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6Z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg><span>LinkedIn</span></a>
    <a href="https://www.behance.net/felipecaroe" rel="me"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 3h6v6M10 14 21 3"/><path d="M19 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h6"/></svg><span>Behance</span></a>
  </nav></div>
</div></footer>
<script src="@@ROOT@@assets/site.js" defer></script>
</body></html>
'''.replace("@@ROOT@@", prefix)
    destination = ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html, encoding="utf-8")
    PAGES.append(canonical)


def service_schema(name, description, price, page_path="services.html"):
    return {
        "@type": "Service",
        "name": name,
        "description": description,
        "provider": {"@id": BASE + "#felipe"},
        "areaServed": ["Europe", "United Kingdom"],
        "offers": {"@type": "Offer", "price": price, "priceCurrency": "EUR", "url": BASE + page_path},
    }


home = '''
<section class="hero"><div class="shell hero-grid">
  <div class="hero-copy"><div class="eyebrow">Freelance UX/UI partner · Madrid / Europe</div>
    <h1>Senior AI product design for your <span class="accent">next client brief.</span></h1>
    <p class="lead">I help agency teams turn AI capabilities into clear, useful product experiences, from conversational flows and edge cases to polished, developer-ready Figma. Hands-on AI product experience, backed by 20+ years in UX and product design.</p>
    <div class="hero-actions">''' + link("contact.html?service=agency", "Discuss a client brief", "button") + link("work.html", "See selected work") + '''</div>
    <div class="hero-foot">20+ years · Async-first · English / Español / Português / Italiano</div>
  </div>
  <div class="hero-visual"><img src="img/felipe.png" alt="Felipe Amorim, senior freelance product designer in Madrid" width="598" height="768" fetchpriority="high"><span class="portrait-credit">Felipe “Caroé” Amorim</span></div>
</div></section>
<section class="client-proof" aria-label="Selected client work"><div class="shell client-proof__row"><span class="client-proof__label">Selected client work</span><div class="client-proof__logos"><span class="client-proof__wordmark"><img src="img/logo_atm.svg" alt="" loading="lazy"><span>Atlético de Madrid</span></span><span class="client-proof__wordmark"><img src="img/logo_cd.svg" alt="" loading="lazy"><span>Card Dynamics</span></span><img src="img/logo_out.svg" alt="Outback" loading="lazy"><img src="img/logo_pizza.png" alt="Pizza Hut" loading="lazy"></div><span class="client-proof__years">20+ years in design</span></div></section>
<section class="section section--line"><div class="shell">
  <div class="section-index">01 / Selected work</div>
  <div class="section-head"><h2>Good design holds up in the details and the business.</h2><p class="body-copy">Mobile products, fintech and service experiences. See how I work through the brief, connect the journey and make the next move usable.</p></div>
  <div class="work-list">
    <a class="work-card" href="work/atletico-de-madrid.html"><div class="work-image"><img src="img/atm_case.png" alt="Atlético de Madrid app marketplace and fan card screens" width="771" height="709" loading="lazy"></div><div class="work-details"><div><h3>Atlético de Madrid</h3><p>Fan services · Mobile product · +€350k reported monthly revenue</p></div><span class="arrow" aria-hidden="true">↗</span></div></a>
    <a class="work-card" href="work/card-dynamics.html"><div class="work-image"><img src="img/card_case.png" alt="Card Dynamics identity shown on a tablet" width="771" height="709" loading="lazy"></div><div class="work-details"><div><h3>Card Dynamics</h3><p>Fintech · Product direction · Partner-ready banking flows</p></div><span class="arrow" aria-hidden="true">↗</span></div></a>
    <a class="work-card" href="work/outback.html"><div class="work-image work-image--device"><img src="img/parallax-4.png" alt="Outback mobile dining experience shown in a rounded phone mockup" width="541" height="980" loading="lazy"></div><div class="work-details"><div><h3>Outback</h3><p>Customer experience · Service design · +29% reported sales</p></div><span class="arrow" aria-hidden="true">↗</span></div></a>
    <a class="work-card" href="work/pizza-hut.html"><div class="work-image work-image--device"><img src="img/home_pizza.png" alt="Pizza Hut mobile ordering shown in a rounded phone mockup" width="1109" height="2283" loading="lazy"></div><div class="work-details"><div><h3>Pizza Hut</h3><p>Service design · Team leadership · Satisfaction 82% → 95%</p></div><span class="arrow" aria-hidden="true">↗</span></div></a>
  </div><p style="margin:32px 0 0">''' + link("work.html", "Explore all selected work") + '''</p>
</div></section>
<section class="section offer-section" id="services"><div class="shell"><div class="section-index">02 / Ways to work together</div><div class="section-head"><h2>Flexible senior capacity. Clear scope from day one.</h2><p class="body-copy">Choose a focused brief or a recurring block of design time. I agree the outcome, schedule and handover with you before the work starts.</p></div><div class="home-offers">
<article class="home-offer"><span class="meta-label">A contained client brief</span><h3>One clear design problem.</h3><p>A flow, a small set of screens or a focused UX review. Up to four hours of senior design, scoped together.</p><div class="home-offer__price">€500 <span>· excluding applicable VAT</span></div><a class="text-link" href="services/ux-ui-brief.html">See the focused brief <span class="arrow" aria-hidden="true">↗</span></a></article>
<article class="home-offer"><span class="meta-label">For recurring agency work</span><h3>Sixteen hours, every month.</h3><p>Reliable design capacity for live client projects, with one active brief and agreed priorities.</p><div class="home-offer__price">€1,600 <span>· per month · excluding applicable VAT</span></div><a class="text-link" href="services/monthly-design.html">See monthly support <span class="arrow" aria-hidden="true">↗</span></a></article>
</div><p class="home-offers__secondary">Building an in-house product team? <a href="services.html">Explore support for product teams <span aria-hidden="true">↗</span></a></p></div></section>
<section class="quote-band"><div class="shell"><div class="section-index">A senior partner who stays close to the work</div><h2>Clear thinking in the brief. Care in every screen.</h2><p class="body-copy">I work directly with your team, bring the wider product journey into view and hand over decisions your designers and developers can use.</p></div></section>
<section class="section"><div class="shell split"><div class="about-image"><img src="img/felipe.png" alt="Felipe Amorim" loading="lazy" width="598" height="768"></div><div class="about-copy"><div class="section-index">03 / Meet your design partner</div><h2>Twenty years of perspective. Still making the work.</h2><p class="body-copy">I’m Felipe “Caroé” Amorim, a Madrid-based senior product designer. I’ve founded studios, led design teams and worked hands-on across UX, service design, brand and digital products.</p><p class="body-copy">I work in English, Spanish, Portuguese and Italian with agencies and product teams across Europe and the UK.</p>''' + link("leadership.html", "More about my experience") + '''</div></div></section>
'''
page("index.html", "Senior AI product designer for agencies | Felipe Amorim", "Senior AI product design and UX/UI for agencies and studios in Madrid, Europe and the UK. Clear conversational experiences, considered edge cases and developer-ready design.", home)

services = '''
<section class="page-hero"><div class="shell"><div class="eyebrow">Freelance UX/UI · Agencies first · Madrid / Europe</div><h1>Extra design capacity. <span class="accent">Senior from day one.</span></h1><p class="lead">I partner with agencies and studios on client briefs that need experienced UX thinking and polished interface design. Product teams can bring me a focused problem, too.</p></div></section>
<section class="section"><div class="shell"><div class="section-index">What I can take on</div><div class="service-menu">
<article><div class="service-menu__number">01 / User flows</div><div><h2>Help people complete the task.</h2><p>Improve onboarding, checkout, account setup, booking or another important journey. I map the steps, find the points of friction and shape a more direct path.</p><p class="service-output"><strong>You get:</strong> a clarified flow, key states and a prototype or annotated screens.</p></div></article>
<article><div class="service-menu__number">02 / Interface design</div><div><h2>Turn requirements into useful screens.</h2><p>Design new features or refine existing mobile and web interfaces. I work within your brand and components, or help establish patterns where they are missing.</p><p class="service-output"><strong>You get:</strong> responsive Figma screens, interaction states and developer-ready notes.</p></div></article>
<article><div class="service-menu__number">03 / Product review</div><div><h2>Know what to improve first.</h2><p>Get an experienced review of a product area, flow or prototype. I identify usability issues and separate the urgent fixes from the longer-term opportunities.</p><p class="service-output"><strong>You get:</strong> prioritised findings, annotated examples and clear next actions.</p></div></article>
<article><div class="service-menu__number">04 / AI product design</div><div><h2>Make AI useful, clear and trustworthy.</h2><p>Shape conversational and AI-powered product experiences, including generated responses, loading and uncertainty, correction and fallback states. I design the full interaction around the model so people know what is happening and what they can do next.</p><p class="service-output"><strong>You get:</strong> AI interaction flows, key interface states and a prototype or developer-ready handover.</p></div></article>
<article><div class="service-menu__number">05 / Product direction</div><div><h2>Give the team a shared way forward.</h2><p>Frame an unclear problem, align user and business needs, and turn early ideas into options a team can discuss or test.</p><p class="service-output"><strong>You get:</strong> a decision framework, concept direction or testable prototype.</p></div></article>
</div></div></section>
<section class="section section--line"><div class="shell"><div class="section-index">How to engage</div><div class="section-head"><h2>Start with the brief in front of you.</h2><p class="body-copy">Choose a contained piece of work or reserve a recurring block. I confirm scope and timing before you commit, so you can plan the client delivery with confidence.</p></div><div class="engagement-options"><a href="services/ux-ui-brief.html"><span class="meta-label">One focused client brief</span><h3>UX/UI brief</h3><p>Up to four hours on one agreed user flow, small screen set or product review. One feedback pass is included.</p><strong>€500 <small>excluding applicable VAT</small></strong><span class="text-link">Explore the focused brief ↗</span></a><a href="services/monthly-design.html"><span class="meta-label">Recurring agency capacity</span><h3>Monthly design support</h3><p>Sixteen hours of senior design capacity each month, with one active brief and agreed priorities.</p><strong>€1,600 <small>per month · excluding applicable VAT</small></strong><span class="text-link">Explore monthly support ↗</span></a></div><p class="direct-team-link">Building your own product? <a href="contact.html?service=product">Get in touch about direct product support <span aria-hidden="true">↗</span></a></p></div></section>
<section class="section section--line"><div class="shell split"><div><div class="section-index">A practical working rhythm</div><h2>Clear scope. Direct collaboration.</h2></div><div><p class="body-copy">I work mostly asynchronously with occasional planned calls. Share your current screens or product context, the user need, the decision that is stuck and your deadline. I’ll confirm the scope and delivery date before we begin.</p><p class="body-copy">For AI work, that includes the moments around the generated answer: waiting, uncertainty, correction and recovery. I work in English, Spanish, Portuguese and Italian with agencies and product teams across Europe and the UK.</p>''' + link("contact.html", "Tell me what you need") + '''</div></div></section>'''
service_catalog_schema = {
    "@type": "Service",
    "name": "AI and freelance product design support",
    "description": "Senior product design for AI interactions, UX/UI flows, mobile and web interfaces, product reviews and early product direction.",
    "serviceType": ["AI product design", "AI interaction design", "UX/UI design", "Product design", "Product experience review", "Product strategy"],
    "provider": {"@id": BASE + "#felipe"},
    "areaServed": ["Europe", "United Kingdom"],
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Ways to engage",
        "itemListElement": [
            {"@type": "Offer", "name": "Focused UX/UI and AI interaction design brief", "price": "500", "priceCurrency": "EUR", "url": BASE + "services/ux-ui-brief.html"},
            {"@type": "Offer", "name": "Monthly product design support", "price": "1600", "priceCurrency": "EUR", "url": BASE + "services/monthly-design.html"},
        ],
    },
}
page("services.html", "AI product design and UX/UI for agencies | Felipe Amorim", "Senior AI product design and UX/UI support for agencies and studios in Madrid, Europe and the UK. Focused briefs from €500; monthly capacity from €1,600.", services, "services", service_catalog_schema)

brief = '''
<section class="page-hero page-hero--compact"><div class="shell"><div class="bread"><a href="../services.html">Services</a> / Focused UX/UI brief</div><div class="eyebrow">One focused client brief · €500</div><h1>Move one important design decision <span class="accent">forward.</span></h1><p class="lead">Bring a live client flow, a set of screens or a UX question. I’ll help you clarify the next move and leave the agency team with design it can take into delivery.</p></div></section>
<section class="section"><div class="shell detail-layout"><div>
  <div class="detail-block"><div class="section-index">A fit for</div><h2>A client brief that needs senior hands.</h2><p>Bring an onboarding step, checkout, AI interaction, feature flow, important screen or UX question. I’ll work within the agreed scope and your existing product context to make a clear next version.</p><p>Useful when the agency has the brief and direction, and needs experienced design capacity to move the work into Figma and development handover.</p></div>
  <div class="detail-block"><div class="section-index">What you receive</div><h2>Design you can act on.</h2><ul><li>One agreed design outcome, usually a flow or small set of screens.</li><li>For AI work, the surrounding interaction states such as waiting, uncertainty, correction and recovery.</li><li>Editable Figma files or a documented review, agreed before work starts.</li><li>A short explanation of decisions, open questions and suggested next steps.</li><li>One feedback pass within the four-hour allowance.</li></ul></div>
  <div class="detail-block"><div class="section-index">How it works</div><h2>Scope it. Design it. Hand it over.</h2><p>Send the brief and existing product context. I’ll confirm what fits within four hours and agree a delivery date before we start. If it needs deeper research or a larger screen set, I’ll scope that separately rather than squeeze it into the brief.</p></div>
</div><aside class="detail-aside"><div class="meta-label">Focused UX/UI brief</div><span class="price">€500</span><p class="small-copy">Up to four hours. Excludes applicable VAT.</p><div class="fact"><span>Working style</span><strong>Mostly async</strong></div><div class="fact"><span>Input</span><strong>One clear brief</strong></div><div class="fact"><span>Output</span><strong>Agreed before start</strong></div><div class="fact"><span>Feedback</span><strong>Within the allowance</strong></div>''' + link("contact.html?service=brief", "Discuss your brief", "button") + '''</aside></div></section>
<section class="section section--line faq"><div class="shell"><div class="section-index">Good to know</div><h2>Common questions</h2><details><summary>Can you design screens from our brief?</summary><p>Yes. Share the product goal, users, current files and constraints. I’ll confirm what can be designed within the available time.</p></details><details><summary>Does this include development?</summary><p>This offer covers design and handover. Production development would need its own scope.</p></details><details><summary>What if we need more than four hours?</summary><p>We can agree an additional four-hour block or move to monthly support before the scope changes.</p></details></div></section>'''
page("services/ux-ui-brief.html", "Focused AI product design and UX/UI brief | Felipe Amorim", "A focused four-hour UX/UI or AI interaction design brief for agency and studio teams, from €500. Senior design on one agreed flow, screen set or product review.", brief, "services", service_schema("Focused UX/UI and AI interaction design brief", "Up to four hours of senior UX/UI or AI interaction design for one agreed agency or product team brief, including handover and feedback within the allowance.", "500", "services/ux-ui-brief.html"))

monthly = '''
<section class="page-hero page-hero--compact"><div class="shell"><div class="bread"><a href="../services.html">Services</a> / Monthly design support</div><div class="eyebrow">16 hours a month · €1,600</div><h1>A senior design partner for your <span class="accent">busy months.</span></h1><p class="lead">Steady UX/UI capacity for agencies with recurring client work. I join one live brief at a time, with scope, priority and delivery dates agreed before each piece starts.</p></div></section>
<section class="section"><div class="shell detail-layout"><div>
  <div class="detail-block"><div class="section-index">A fit for</div><h2>More client work than in-house design time.</h2><p>Use the allocation for new screens, improving existing flows, prototypes, interface reviews, design-system decisions and developer handover. Your team sets the client priorities; I bring senior design thinking and make the agreed work.</p><p>It suits an agency that needs a reliable extra pair of hands and a direct line to the designer doing the work.</p></div>
  <div class="detail-block"><div class="section-index">How the allocation works</div><h2>Known capacity. Agreed priorities.</h2><ul><li>16 hours of design time within a calendar month.</li><li>We agree the outcome, time estimate and delivery date for each brief.</li><li>Calls, feedback, revisions and handover count towards the allocation.</li><li>One active brief at a time; new priorities can replace queued work.</li><li>Unused hours expire at month-end. Extra four-hour blocks are €500 by agreement.</li></ul></div>
  <div class="detail-block"><div class="section-index">Working together</div><h2>Thoughtful, mostly async.</h2><p>I work primarily asynchronously, with planned calls where they move a decision forward. I respond to project messages within two working days and agree delivery dates per brief. Monthly payment is in advance; scope and start date are confirmed in writing.</p></div>
</div><aside class="detail-aside"><div class="meta-label">Monthly design support</div><span class="price">€1,600 <small>/ month</small></span><p class="small-copy">16 hours. Excludes applicable VAT.</p><div class="fact"><span>Capacity</span><strong>16 hours/month</strong></div><div class="fact"><span>Briefs</span><strong>One active at a time</strong></div><div class="fact"><span>Communication</span><strong>Async, planned calls</strong></div><div class="fact"><span>Start</span><strong>By agreement</strong></div>''' + link("contact.html?service=monthly", "Discuss monthly support", "button") + '''</aside></div></section>
<section class="section section--line faq"><div class="shell"><div class="section-index">Good to know</div><h2>Common questions</h2><details><summary>Can you work from our existing Figma files?</summary><p>Yes. Existing components, content and developer constraints help me make work that fits your product.</p></details><details><summary>Can priorities change during the month?</summary><p>Yes, provided we pause or finish the current brief and agree what the remaining time can cover.</p></details><details><summary>Can you attend regular team meetings?</summary><p>Occasional planned calls can fit within the allocation. If you need daily availability, we should discuss a different arrangement.</p></details></div></section>'''
page("services/monthly-design.html", "Monthly freelance UX/UI for agencies | Felipe Amorim", "Sixteen hours of senior freelance UX/UI capacity for €1,600 per month. Design support for agency and studio client projects in Europe and the UK.", monthly, "services", service_schema("Monthly product design support", "Sixteen hours per month of senior UX/UI design for agency client projects, including flows, screens, reviews and developer handover.", "1600", "services/monthly-design.html"))

work = '''
<section class="page-hero"><div class="shell"><div class="eyebrow">Selected client work · Product · Service · UX/UI</div><h1>Thoughtful work for <span class="accent">real-world complexity.</span></h1><p class="lead">Explore agency and client projects across fintech, sport, hospitality and digital services. Each case shows the problem, my role and what the work changed.</p></div></section>
<section class="section"><div class="shell work-list">
<a class="work-card" href="work/luzia-new-chat/plan.html"><div class="work-image work-image--device"><img src="work/luzia-new-chat/assets/first-entrance.jpg" alt="Luzia new-chat experience with a short welcome and suggested prompts" width="465" height="900" loading="lazy"></div><div class="work-details"><div><h3>Luzia · New chat</h3><p>AI product · Product strategy · Experience design</p></div><span class="arrow" aria-hidden="true">↗</span></div></a>
<a class="work-card" href="work/atletico-de-madrid.html"><div class="work-image work-image--device"><img src="img/parallax-3.png" alt="Atlético de Madrid mobile shop shown in a rounded phone mockup" width="542" height="993"></div><div class="work-details"><div><h3>Atlético de Madrid</h3><p>Fan services · Mobile product · +€350k monthly revenue reported</p></div><span class="arrow" aria-hidden="true">↗</span></div></a>
<a class="work-card" href="work/card-dynamics.html"><div class="work-image work-image--device"><img src="img/parallax-6.png" alt="Card Dynamics mobile banking flow shown in a rounded phone mockup" width="463" height="893"></div><div class="work-details"><div><h3>Card Dynamics</h3><p>Fintech · Product and brand direction · Partner-ready flows</p></div><span class="arrow" aria-hidden="true">↗</span></div></a>
<a class="work-card" href="work/outback.html"><div class="work-image work-image--device"><img src="img/parallax-4.png" alt="Outback mobile dining experience shown in a rounded phone mockup" width="541" height="980" loading="lazy"></div><div class="work-details"><div><h3>Outback</h3><p>Customer experience · Service design · +29% sales reported</p></div><span class="arrow" aria-hidden="true">↗</span></div></a>
<a class="work-card" href="work/pizza-hut.html"><div class="work-image work-image--device"><img src="img/home_pizza.png" alt="Pizza Hut mobile ordering shown in a rounded phone mockup" width="1109" height="2283" loading="lazy"></div><div class="work-details"><div><h3>Pizza Hut</h3><p>Service design · Satisfaction reported from 82% to 95%</p></div><span class="arrow" aria-hidden="true">↗</span></div></a>
<a class="work-card work-card--concept" href="work/invisipayment.html"><div class="work-image"><img src="img/inv_case.png" alt="Invisipayment speculative payment design concept" width="771" height="709" loading="lazy"><span class="work-image__label">Independent concept</span></div><div class="work-details"><div><h3>Invisipayment</h3><p>Speculative design · Future of payments</p></div><span class="arrow" aria-hidden="true">↗</span></div></a>
<a class="work-card work-card--concept" href="cases/impulse.html"><div class="work-image"><img src="cases/img/hero.png" alt="Impulse speculative payment experience concept" width="3000" height="1477" loading="lazy"><span class="work-image__label">Independent concept</span></div><div class="work-details"><div><h3>Impulse</h3><p>Speculative design · Personal finance</p></div><span class="arrow" aria-hidden="true">↗</span></div></a>
</div></section>
<section class="section section--line"><div class="shell split"><div><div class="section-index">How I work</div><h2>A senior partner who stays close to the delivery.</h2></div><div><p class="body-copy">I’ve founded studios, led design teams and worked hands-on across UX, service design and digital products. That perspective helps me collaborate with agency teams and make the design useful for both clients and developers.</p>''' + link("leadership.html", "Meet Felipe and see his experience") + '''</div></div></section>'''
page("work.html", "Product and UX/UI case studies | Felipe Amorim", "Selected product, AI experience, UX/UI and service design work by Felipe Amorim, including Luzia, Atlético de Madrid, Card Dynamics, Outback and Pizza Hut.", work, "work")

def project_page(slug, name, title, description, category, lead, hero, hero_alt, client, role, focus, challenge, approach, impact, impact_label, stage_label, stage_caption, mockups, tags, source_url):
    hero_mockups = {
        "work/atletico-de-madrid.html": "parallax-3.png",
        "work/card-dynamics.html": "parallax-6.png",
        "work/outback.html": "parallax-4.png",
        "work/pizza-hut.html": "home_pizza.png",
    }
    hero_visual = hero_mockups.get(slug, hero)
    hero_class = "case-cover case-cover--device" if slug in hero_mockups else "case-cover"
    media_items = "".join(
        f'<figure class="case-gallery__item case-gallery__item--{("one", "two", "three")[i]}"><img src="../img/{src}" alt="{escape(alt)}" loading="lazy"><figcaption><span>0{i + 1}</span><span>{escape(caption)}</span></figcaption></figure>'
        for i, (src, alt, caption) in enumerate(mockups)
    )
    pills = "".join(f"<span>{escape(tag)}</span>" for tag in tags)
    impact_html = f'<div class="case-outcome case-outcome--hero"><strong>{escape(impact)}</strong><span>{escape(impact_label)}</span></div>' if impact else f'<div class="case-outcome case-outcome--hero"><strong>Outcome</strong><span>{escape(impact_label)}</span></div>'
    content = f'''
<section class="case-hero"><div class="shell"><div class="bread"><a href="../work.html">Selected work</a> / {escape(name)}</div><div class="case-hero-grid"><div class="case-hero-copy"><div class="eyebrow">{escape(category)}</div><h1>{title}</h1><p class="lead">{escape(lead)}</p>{impact_html}</div><div class="{hero_class}"><img src="../img/{hero_visual}" alt="{escape(hero_alt)}" loading="eager"></div></div><div class="case-facts"><div><span class="meta-label">Client</span><strong>{escape(client)}</strong></div><div><span class="meta-label">My contribution</span><strong>{escape(role)}</strong></div><div><span class="meta-label">Focus</span><strong>{escape(focus)}</strong></div></div></div></section>
<section class="section section--tight"><div class="shell detail-layout"><div>
<div class="detail-block"><div class="section-index">The challenge</div><h2>{escape(challenge[0])}</h2><p>{escape(challenge[1])}</p></div>
<div class="detail-block"><div class="section-index">My approach</div><h2>{escape(approach[0])}</h2><p>{escape(approach[1])}</p></div>
</div><aside class="detail-aside"><div class="meta-label">Project at a glance</div><div class="fact"><span>Discipline</span><strong>{escape(category)}</strong></div><div class="fact"><span>Contribution</span><strong>{escape(role)}</strong></div><div class="case-tags">{pills}</div><p style="margin-top:28px"><a class="text-link" href="{escape(source_url)}" target="_blank" rel="noopener noreferrer">View original project <span class="arrow" aria-hidden="true">↗</span></a></p></aside></div></section>
<section class="section section--line case-gallery-section case-gallery-section--{slug.split('/')[-1]}"><div class="shell"><div class="case-gallery-heading"><div><div class="section-index">Inside the work</div><h2>{escape(stage_label)}</h2><p>{escape(stage_caption)}</p></div></div><div class="case-gallery case-gallery--{len(mockups)}" role="group" aria-label="{escape(name)} product mockups">{media_items}</div></div></section>
<section class="case-close section"><div class="shell case-close__inner"><div class="case-close__proof"><div class="section-index">Next client brief</div><h2>Need senior design capacity for the delivery?</h2></div><a class="button button--glass" href="../contact.html?service=agency">Scope an agency brief <span aria-hidden="true">↗</span></a></div><div class="shell case-back"><a href="../work.html">← Back to selected work</a><a href="{escape(source_url)}" target="_blank" rel="noopener noreferrer">View original case study ↗</a></div></section>'''
    title_text = re.sub(r"<[^>]*>", "", title)
    page(slug, title_text + " | Felipe Amorim", description, content, "work")

project_page(
    "work/atletico-de-madrid.html", "Atlético de Madrid", "Bringing the fan journey <span class=\"accent\">into one app.</span>",
    "Felipe Amorim helped improve Atlético de Madrid's official mobile app, connecting fan services and card benefits in one experience.",
    "Mobile product · Fan experience", "A clearer mobile experience for the many moments around match day and club life.",
    "atm_case.png", "Atlético de Madrid mobile shop in a rounded phone mockup", "Atlético de Madrid", "Product and experience design", "Mobile services, navigation and fan benefits",
    ("Many fan needs. One mobile entry point.", "The official app brings together tickets, food, merchandise, club information and payment. I worked on an experience that makes these practical services easier to discover and use on the move."),
    ("Make the next useful action easy to find.", "The service hub gives everyday tasks clear entry points. A related card experience makes member benefits and payment feel like part of the same product, rather than a disconnected destination."),
    "€350k+", "monthly revenue boost reported for the project", "A connected match-day experience", "The app brings everyday club services and fan benefits into one mobile experience.",
    [("parallax-3.png", "Atlético de Madrid mobile merchandise shop with team kits and player products", "Fan services and merchandise"), ("parallax-1.png", "Atlético de Madrid mobile checkout with merchandise, payment methods and order total", "Checkout and mobile payment")],
    ["Fan experience", "Mobile product", "Service design"], "https://www.behance.net/gallery/201717263/Atletico-de-Madrid-Cashless-Marketplace")

project_page(
    "work/card-dynamics.html", "Card Dynamics", "Making financial flows <span class=\"accent\">feel navigable.</span>",
    "Design leadership and product revamp for Card Dynamics, connecting fintech product operations, brand direction and partner-ready mobile flows.",
    "Fintech · Product and brand", "A clearer design system for a financial product built to work across partners.",
    "card_case.png", "Card Dynamics home-loan application in a rounded phone mockup", "Card Dynamics", "Design operations, product and brand revamp", "White-label mobile banking flows",
    ("Trust is built one step at a time.", "Connecting a bank account asks people to share sensitive information and understand what happens next. Card Dynamics needed a product direction that felt coherent across its own experience and partner-branded flows."),
    ("Keep the task and reassurance together.", "I led design operations and the broader product and branding revamp. The account connection, account selection and verification screens use familiar patterns, direct language and a visible next action."),
    "White-label", "product and design direction prepared for partner-branded experiences", "A consistent flow across partner brands", "Clear steps and partner identity help people stay oriented during sensitive financial tasks.",
    [("parallax-6.png", "Card Dynamics partner-branded home-loan application screen", "Home-loan application"), ("parallax-7.png", "Card Dynamics partner-branded account selection screen", "Partner-branded account selection"), ("parallax-8.png", "Card Dynamics identity verification screen with one-time SMS code entry", "Identity verification")],
    ["Fintech", "Design operations", "White-label UX"], "https://www.behance.net/gallery/234892939/Card-Dynamics-Revamp")

project_page(
    "work/outback.html", "Outback", "A better dining journey, <span class=\"accent\">from first tap to table.</span>",
    "Customer experience design for Outback, bringing digital ordering and the in-restaurant experience into one joined-up journey.",
    "Customer experience · Food and hospitality", "A joined-up dining service shaped by customer interviews and observing the experience first-hand.",
    "outback_case.png", "Outback mobile dining experience in a rounded phone mockup", "Outback", "Customer research and experience design", "Digital ordering and on-premise service",
    ("The experience continues after the order.", "I interviewed more than 20 customers across Brazil and experienced the journey myself. The work looked across on-premise and off-premise dining to surface recurring needs and points where the service could feel fragmented."),
    ("Join the digital and physical moments.", "The redesigned experience brings delivery, collection, reservations and queueing into a clearer set of choices. The mobile concept keeps food discovery and practical service actions close together, while acknowledging the real restaurant journey around them."),
    "29%", "increase in sales reported for the project", "One joined-up dining journey", "Ordering, collection and the in-restaurant experience work together across the journey.",
    [("parallax-4.png", "Outback mobile app for menu browsing, delivery, collection, reservations and queueing", "Browse, order and dine"), ("parallax-5.png", "Outback menu and ordering screens shown together in two angled phones", "Menu and ordering flows")],
    ["Customer research", "Service design", "Hospitality"], "https://www.behance.net/gallery/201713907/Outback-Customer-Experience")

project_page(
    "work/pizza-hut.html", "Pizza Hut", "Easing the wait between <span class=\"accent\">order and arrival.</span>",
    "Pizza Hut service design led by Felipe Amorim: an eight-person team audited 25+ channels, identified 65 experience gaps and improved the Brazilian digital ecosystem.",
    "Service design · Food and delivery", "A service-wide response to delivery anxiety, shaped from an audit of Pizza Hut's digital ecosystem in Brazil.",
    "pizzahut_case.png", "Pizza Hut mobile ordering in a rounded phone mockup", "Pizza Hut · Brazil", "Service design leadership for an eight-person team", "Digital ecosystem, delivery and checkout",
    ("Delivery anxiety was a system problem.", "Customers moved across more than 25 digital channels before and after ordering. The audit surfaced 65 experience gaps, including unclear progress, inconsistent information and uncertainty about when food would arrive."),
    ("Prioritise the moments that change confidence.", "I led an eight-person team through the audit and service design work. Applying familiar usability principles, we organised the gaps into a roadmap focused on the order journey, clear status and more reassuring delivery communication."),
    "62% → 40%", "reported checkout-friction score; satisfaction rose from 82% to 95%", "A service roadmap across 25+ touchpoints", "Ordering, tracking and delivery reassurance become part of one joined-up service.",
    [("home_pizza.png", "Pizza Hut Brazil mobile ordering app with restaurant selection, offer and menu", "Restaurant discovery and order status"), ("pizzahut2.png", "Pizza Hut menu, item detail and checkout screens composed across three phones", "Menu, item details and checkout")],
    ["Service design", "Team leadership", "E-commerce"], "https://www.behance.net/gallery/241661977/Service-Design-for-Pizza-Hut")

project_page(
    "work/invisipayment.html", "Invisipayment", "A more human future <span class=\"accent\">for everyday payments.</span>",
    "A speculative design project using futures thinking and AI interaction design to imagine payment experiences that feel more human.",
    "Speculative design · Future of payments", "An exploration of payment beyond the familiar card terminal and checkout screen.",
    "inv_case.png", "Invisipayment concept with a voice interface and payment terminal", "Independent concept", "Futures thinking and interaction design", "Voice, ambient computing and payment",
    ("What if payment disappeared into the experience?", "The project asks how emerging technologies could reduce the friction of everyday transactions without making people feel less in control. Rather than treating a payment as a standalone screen, it considers the moment, environment and confidence around it."),
    ("Keep people informed and in control.", "The concept explores voice and ambient interfaces for confirming a purchase, while making the amount and the choice visible. A watch, a spoken confirmation and a familiar display each offer a different way to notice, approve or question a transaction."),
    "Concept", "a futures-thinking exploration, not a shipped product", "Payment cues across devices and environments", "From wrist to counter, each cue is designed to keep the person informed and in control.",
    [("parallax-10.png", "Smartwatch concept showing purchase amount and options to approve or reject a payment", "Review and approve a payment"), ("parallax-11.png", "Illustrated concept exploring a voice interaction between shopper and store assistant", "A payment conversation"), ("parallax-12.png", "Countertop display concept asking a shopper to confirm a purchase", "Confirm before purchase")],
    ["Futures thinking", "AI interaction design", "Concept design"], "https://www.behance.net/gallery/221562325/Invisipayment-A-concept-for-the-future-of-payments")

offerings = [
    ("Product design", "Research, UX/UI, prototyping and design systems that turn a product brief into a useful experience.", "product-design.png", ["UX/UI", "Research", "Prototyping"]),
    ("Innovation and strategy", "Find the opportunity, frame the right question and turn early ideas into something a team can test.", None, ["Futures thinking", "Product strategy", "Validation"]),
    ("AI product design", "Design useful AI interactions from the first prompt to waiting, uncertainty, correction and recovery. Turn model capability into an experience people can understand and trust.", "image-10.png", ["AI interaction design", "Conversational UX", "AI product flows"]),
    ("Design leadership", "Build a stronger design practice through clear direction, team coaching and close collaboration with the business.", "image-11.png", ["Team leadership", "Design operations", "Mentoring"]),
    ("Revenue-driven design", "Connect interface improvements to the commercial outcomes the product needs to deliver.", "parallax-1.png", ["Conversion", "E-commerce", "Service journeys"]),
    ("Brand and experience", "Make identity and digital experience work together across the moments customers remember.", "branding.png", ["Branding", "Customer experience", "Digital products"]),
]
def offer_card(index, name, description, src, tags):
    visual = f'<div class="offer-card__visual" data-number="{index:02}"><img src="img/{src}" alt="" loading="lazy"></div>' if src else f'<div class="offer-card__visual offer-card__visual--statement" data-number="{index:02}"><span>Design for what comes next.</span></div>'
    chips = "".join(f"<span>{escape(tag)}</span>" for tag in tags)
    return f'<article class="offer-card">{visual}<div class="offer-card__body"><h3>{escape(name)}</h3><p>{escape(description)}</p><div class="case-tags">{chips}</div></div></article>'

offer_cards = "".join(offer_card(index, *offering) for index, offering in enumerate(offerings, start=1))
impact_stats = [
    ("20+", "years as a designer", "Industrial and graphic design, with specialisations in branding, UX and usability."),
    ("5", "companies founded", "Two startups as a solo founder and three ventures as business architect."),
    ("4", "languages I speak", "Portuguese, English, Spanish and Italian."),
    ("30+", "designers mentored", "Helping designers build confidence, take on responsibility and grow their careers."),
    ("1,000+", "projects delivered", "Across UX, product and innovation, for more than 200 clients."),
    ("€10m+", "business value generated", "Reported across recent projects through strategic design and product work."),
]
impact_cards = "".join(f'<article class="impact-card"><strong>{escape(number)}</strong><h3>{escape(label)}</h3><p>{escape(description)}</p></article>' for number, label, description in impact_stats)

leadership = f'''
<section class="page-hero"><div class="shell"><div class="eyebrow">About Felipe · Madrid / Europe</div><h1>Design leader by experience. <span class="accent">Designer by practice.</span></h1><p class="lead">I’m Felipe “Caroé” Amorim, a senior product designer with 20+ years across UX, service design, brand and digital products.</p></div></section>
<section class="section"><div class="shell split"><div><div class="section-index">Who you work with</div><h2>Senior perspective. Hands-on delivery.</h2></div><div><p class="body-copy">I’ve founded design ventures, led teams and worked with organisations as they built or improved products. I bring that commercial and team perspective into the work itself: framing the problem, shaping the experience and making the interface.</p><p class="body-copy">Most recently, I worked on AI-powered product experiences at Luzia. I now take on a limited number of well-scoped freelance briefs, drawing on 20+ years in UX, service design and product delivery.</p><p class="body-copy">Before that, I led design at 4all, founded Brava Digital and co-founded Pipe Digital. I work in Portuguese, English, Spanish and Italian with agencies, studios and product teams across Europe and the UK.</p></div></div></section>
<section class="section offer-section" id="expertise"><div class="shell"><div class="offer-heading"><div><div class="section-index">Ways I can help</div><h2>Hire me if you need…</h2></div><div class="offer-controls"><button type="button" data-offer-prev aria-label="Previous capabilities">←</button><button type="button" data-offer-next aria-label="Next capabilities">→</button></div></div><div class="offer-track" data-offer-track role="region" aria-label="Capabilities carousel" tabindex="0">{offer_cards}</div><div class="offer-progress"><span data-offer-count aria-live="polite">01 / 06</span><span class="offer-progress__track" aria-hidden="true"><span data-offer-progress></span></span><span>Drag or use the arrows</span></div></div></section>
<section class="section impact-section"><div class="shell"><div class="impact-heading"><div class="section-index">A few markers along the way</div><h2>Experience you can put to work.</h2><p>Years in the field are useful when they help a team make better decisions, deliver with confidence and build something people value.</p></div><div class="impact-grid">{impact_cards}</div></div></section>
<section class="section section--line"><div class="shell"><div class="section-index">Selected experience</div><div class="detail-layout"><div>
<div class="detail-block"><h2>Design leadership</h2><p>At 4all, I led UX/UI and strategic consulting work for digital products and client projects. That meant managing designers and connecting design processes to business goals while remaining close to delivery.</p></div>
<div class="detail-block"><h2>Building ventures</h2><p>I founded Brava Digital, a design studio focused on branding and digital experiences, and co-founded Pipe Digital, a UX and front-end venture. These roles gave me direct responsibility for teams, clients and the work itself.</p></div>
<div class="detail-block"><h2>Product and future thinking</h2><p>My work spans research, service design, interface design, business strategy and emerging technologies. I’ve continued learning through UX and futures-thinking studies while working on digital products.</p></div>
</div><aside class="detail-aside"><div class="meta-label">Experience at a glance</div><div class="fact"><span>Location</span><strong>Madrid, Spain</strong></div><div class="fact"><span>Languages</span><strong>Portuguese, English, Spanish, Italian</strong></div><div class="fact"><span>Focus</span><strong>Product, UX and design leadership</strong></div><p style="margin-top:28px">''' + link("resume.html", "View résumé") + '''</p><p>''' + link("contact.html", "Start a conversation") + '''</p></aside></div></div></section>'''
page("leadership.html", "Senior AI product designer and UX lead | Felipe Amorim", "Felipe Amorim is a Madrid-based senior AI product designer with 20+ years across AI product experience, UX, service design and digital products. He works in Portuguese, English, Spanish and Italian.", leadership, "leadership")

if not (ROOT / "resume.html").is_file():
    raise FileNotFoundError("The detailed resume.html must be preserved")
PAGES.append(BASE + "resume.html")

contact = '''
<section class="section"><div class="shell contact-grid"><div class="contact-details"><div class="eyebrow">Agency projects · Product teams welcome</div><h1>What are you looking to <span class="accent">move forward?</span></h1><p class="lead">Tell me about the brief, the delivery date and where the team needs senior design. I’ll reply within two working days to confirm whether the scope and timing fit.</p><p class="body-copy">Based in Madrid, working across Europe and the UK. Async-first, with planned calls when they help. English, Spanish, Portuguese and Italian.</p><p><a href="mailto:felipie@gmail.com">felipie@gmail.com</a></p><p class="small-copy">Prefer to write directly? Email me instead.</p></div>
<form class="contact-form" id="brief-form"><h2>Start with the project.</h2>
<label class="field">Your name<input name="name" autocomplete="name" required placeholder="Your name"></label>
<label class="field">Work email<input name="email" type="email" autocomplete="email" required placeholder="you@company.com"></label>
<label class="field">Project type<select name="service" required><option value="">Choose a starting point</option><option value="Agency or studio client brief">Agency or studio client brief</option><option value="Focused UX/UI brief">Focused UX/UI brief · €500 / up to 4h</option><option value="Monthly design support">Monthly support · €1,600 / 16h</option><option value="Product team project">Product team project</option><option value="Not sure yet">Not sure yet</option></select></label>
<label class="field">What needs to move forward?<textarea name="problem" required placeholder="A sentence or two about the product, the design challenge and where you need help."></textarea></label>
<label class="field">Delivery date and budget<input name="timing" placeholder="When do you need it? A budget range helps me suggest the right scope."></label>
<label class="field">How did you find me? <span class="small-copy">(optional)</span><input name="source" placeholder="Search, LinkedIn, Behance, referral…"></label>
<button class="button" type="submit">Continue in email <span class="arrow" aria-hidden="true">↗</span></button>
<p class="form-status" id="form-status" role="status" aria-live="polite">Your email app will open with the details ready for you to review and send.</p>
<noscript><p><a href="mailto:felipie@gmail.com?subject=Product%20design%20brief">Email Felipe directly</a></p></noscript>
</form></div></section>'''
page("contact.html", "Hire freelance UX/UI design support | Felipe Amorim", "Contact Felipe Amorim for senior freelance UX/UI design support on agency client briefs or product team projects in Europe and the UK.", contact, "contact")

urls = "\n".join(f"  <url><loc>{escape(url)}</loc></url>" for url in PAGES)
(ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n', encoding="utf-8")
print(f"Built {len(PAGES) - 1} pages and sitemap.xml; preserved resume.html")
