from pathlib import Path
import json
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://felipecaroe.github.io/portfolio/"
EMAIL = "felipie@gmail.com"
SOCIALS = ["https://www.linkedin.com/in/felipecaroe/", "https://www.behance.net/felipecaroe"]
PAGES = []


def link(to, label, classes="text-link"):
    return f'<a class="{classes}" href="@@ROOT@@{to}">{label} <span class="arrow" aria-hidden="true">↗</span></a>'


def nav(current):
    items = [("services", "services.html", "Services"), ("work", "work.html", "Work"), ("leadership", "leadership.html", "Leadership"), ("contact", "contact.html", "Contact")]
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
        "jobTitle": "Senior product designer",
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
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="@@ROOT@@img/favicon.ico">
  <link rel="stylesheet" href="@@ROOT@@assets/site.css">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{BASE}img/ogthumb.png">
  <meta property="og:image:alt" content="Felipe Amorim. Senior product design, on demand.">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="shell header-row">
  <a class="brand" href="@@ROOT@@index.html" aria-label="Felipe Amorim, home">Felipe Amorim<span class="brand-mark" aria-hidden="true"></span></a>
  <nav class="nav" aria-label="Main navigation">{nav(current)}</nav>
</div></header>
<main id="main">
{content}
</main>
<footer class="site-footer"><div class="shell">
  <div class="footer-top"><div><div class="footer-kicker">Have a product brief?</div><h2>Let’s make the next step <em>clear.</em></h2></div>
    {link("contact.html", "Discuss your brief", "button button--light")}
  </div>
  <div class="footer-bottom"><span>© 2026 Felipe Amorim · Madrid, Spain</span><span><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="https://www.linkedin.com/in/felipecaroe/" rel="me">LinkedIn</a> · <a href="https://www.behance.net/felipecaroe" rel="me">Behance</a></span></div>
</div></footer>
<script src="@@ROOT@@assets/site.js" defer></script>
</body></html>
'''.replace("@@ROOT@@", prefix)
    destination = ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html, encoding="utf-8")
    PAGES.append(canonical)


def service_schema(name, description, price):
    return {
        "@type": "Service",
        "name": name,
        "description": description,
        "provider": {"@id": BASE + "#felipe"},
        "areaServed": ["Europe", "United Kingdom"],
        "offers": {"@type": "Offer", "price": price, "priceCurrency": "EUR", "url": BASE + "services.html"},
    }


home = '''
<section class="hero"><div class="shell hero-grid">
  <div class="hero-copy"><div class="eyebrow">Senior product design · Madrid / Europe</div>
    <h1>Senior product design,<br><span class="accent">without a full-time hire.</span></h1>
    <p class="lead">I help teams turn product briefs into clear user flows, polished interfaces and Figma files ready for developers.</p>
    <div class="hero-actions">''' + link("contact.html", "Discuss a brief", "button") + link("work.html", "See selected work") + '''</div>
    <div class="hero-foot">Independent design support · Async-first · English / Español / Português</div>
  </div>
  <div class="hero-visual"><img src="img/felipe.png" alt="Portrait of Felipe Amorim" width="598" height="736" fetchpriority="high"><span class="portrait-credit">Felipe “Caroé” Amorim</span></div>
</div></section>
<div class="strap"><div class="shell"><p><strong>20+ years</strong> across product design, UX and digital strategy</p><p>Former founder and design leader · Hands-on by choice</p></div></div>
<section class="section" id="services"><div class="shell">
  <div class="section-index">01 / Ways to work together</div>
  <div class="section-head"><h2>The right amount of design, when you need it.</h2><p class="body-copy">One useful first brief or a small, steady allocation. Every engagement starts with a clear problem and a realistic amount of work.</p></div>
  <div class="cards">
    <article class="service-card"><div class="meta-label">01 / Start here</div><h3>A focused UX/UI brief</h3><p>One flow, screen set or interface problem. A defined piece of design work, with feedback and handover.</p><div class="service-bottom"><div class="price">€500 <small>/ up to 4 hours</small></div>''' + link("services/ux-ui-brief.html", "Explore", "text-link") + '''</div></article>
    <article class="service-card"><div class="meta-label">02 / Ongoing support</div><h3>A senior designer in your corner</h3><p>Allocated design time each month for briefs, screens, flow improvements, reviews and developer handover.</p><div class="service-bottom"><div class="price">€1,600 <small>/ month</small></div>''' + link("services/monthly-design.html", "Explore", "text-link") + '''</div></article>
  </div><p class="small-copy" style="margin-top:18px">Prices exclude applicable VAT. Scope and start date are confirmed before work begins.</p>
</div></section>
<section class="section section--line"><div class="shell">
  <div class="section-index">02 / Selected work</div>
  <div class="section-head"><h2>Interface craft with a wider view of the product.</h2><p class="body-copy">A few examples of complex products made easier to understand and use.</p></div>
  <div class="work-list">
    <a class="work-card" href="work/atletico-de-madrid.html"><div class="work-image"><img src="img/atm_case.png" alt="Atlético de Madrid app marketplace and fan card screens" width="771" height="709" loading="lazy"></div><div class="work-details"><div><h3>Atlético de Madrid</h3><p>Fan experience · Mobile product</p></div><span class="arrow" aria-hidden="true">↗</span></div></a>
    <a class="work-card" href="work/card-dynamics.html"><div class="work-image"><img src="img/card_case.png" alt="Card Dynamics identity shown on a tablet" width="771" height="709" loading="lazy"></div><div class="work-details"><div><h3>Card Dynamics</h3><p>Fintech · Product and brand</p></div><span class="arrow" aria-hidden="true">↗</span></div></a>
  </div><p style="margin:32px 0 0">''' + link("work.html", "See all selected work") + '''</p>
</div></section>
<section class="quote-band"><div class="shell"><div class="section-index">A useful way to work</div><h2>Give me the brief. I’ll make the product decision visible.</h2><p class="body-copy">A good design handover explains what changed, why it changed and what needs to happen next. I work mostly asynchronously, with calls when they help the work move forward.</p></div></section>
<section class="section"><div class="shell split"><div class="about-image"><img src="img/felipe.png" alt="Felipe Amorim" loading="lazy" width="598" height="736"></div><div class="about-copy"><div class="section-index">03 / Who you’ll work with</div><h2>Experienced enough to lead. Close enough to the work to make it.</h2><p class="body-copy">I’m Felipe, a Madrid-based product designer with more than 20 years in UX, digital products and strategy. I’ve founded studios, led teams and stayed hands-on with the design itself.</p><p class="body-copy">I work in English, Spanish and Portuguese, and bring both product thinking and interface craft to small, well-defined engagements.</p>''' + link("leadership.html", "Explore my leadership experience") + '''</div></div></section>
'''
page("index.html", "Felipe Amorim | Freelance product designer in Madrid", "Senior freelance product designer in Madrid. UX/UI briefs and monthly product design support for European and UK teams, from €500.", home)

services = '''
<section class="page-hero"><div class="shell"><div class="eyebrow">Work with Felipe</div><h1>Product design that fits the <span class="accent">work in front of you.</span></h1><p class="lead">A senior design partner for agencies and product teams who need considered UX/UI work without adding a full-time role.</p></div></section>
<section class="section"><div class="shell"><div class="section-index">Choose the right starting point</div><div class="cards">
<article class="service-card"><div class="meta-label">A focused first brief</div><h3>One product problem. A useful next step.</h3><p>Use a short engagement for a screen set, flow improvement, prototype or thoughtful review. A good fit when the problem is already framed.</p><div class="service-bottom"><div class="price">€500 <small>/ up to 4 hours</small></div>''' + link("services/ux-ui-brief.html", "See details") + '''</div></article>
<article class="service-card"><div class="meta-label">Small monthly allocation</div><h3>Senior design support, built into your rhythm.</h3><p>Reserve time for briefs, interface design, product thinking, review and handover across the month. One active brief at a time.</p><div class="service-bottom"><div class="price">€1,600 <small>/ 16 hours</small></div>''' + link("services/monthly-design.html", "See details") + '''</div></article></div>
<p class="small-copy" style="margin-top:18px">Prices exclude applicable VAT. Additional scope is quoted separately.</p></div></section>
<section class="section section--line"><div class="shell"><div class="section-index">How I work</div><div class="split"><div><h2>A clear brief gives us a better start.</h2></div><div><p class="body-copy">Tell me what product you’re working on, what decision or screen is stuck, your deadline and what you already know. I’ll confirm the work that fits the available time before it starts.</p><p class="body-copy">Delivery is primarily asynchronous. We agree on review points and handover format up front so the work can move without constant meetings.</p>''' + link("contact.html", "Tell me about your brief") + '''</div></div></div></section>'''
page("services.html", "Product design services | Felipe Amorim", "Focused UX/UI briefs and monthly senior product design support for agencies and product teams across Europe and the UK.", services, "services")

brief = '''
<section class="page-hero page-hero--compact"><div class="shell"><div class="bread"><a href="../services.html">Services</a> / Focused UX/UI brief</div><div class="eyebrow">A useful first project</div><h1>Make one product problem <span class="accent">clearer.</span></h1><p class="lead">A focused piece of senior UX/UI work when you have a brief, a product question and a need to move forward.</p></div></section>
<section class="section"><div class="shell detail-layout"><div>
  <div class="detail-block"><div class="section-index">What this is for</div><h2>Small scope. Real progress.</h2><p>Bring an onboarding step, checkout moment, feature flow, important screen or interface decision. I’ll use the agreed time to examine the problem, design a sensible next version and explain the choices.</p><p>This is particularly useful when your team has direction and needs an experienced designer to turn it into screens or a clearer path for development.</p></div>
  <div class="detail-block"><div class="section-index">What you receive</div><h2>Design you can act on.</h2><ul><li>One agreed design outcome, usually a flow or small set of screens.</li><li>Editable Figma files or a documented review, agreed before work starts.</li><li>A short explanation of decisions, open questions and suggested next steps.</li><li>One feedback pass within the four-hour allowance.</li></ul></div>
  <div class="detail-block"><div class="section-index">Process</div><h2>Brief → estimate → make → hand over.</h2><p>Send the brief and any existing product context. I’ll identify what fits in four hours and agree a delivery date. If the brief needs deeper research or a larger screen set, I’ll suggest a separate scope instead of stretching this one.</p></div>
</div><aside class="detail-aside"><div class="meta-label">Focused UX/UI brief</div><span class="price">€500</span><p class="small-copy">Up to four hours. Excludes applicable VAT.</p><div class="fact"><span>Working style</span><strong>Mostly async</strong></div><div class="fact"><span>Input</span><strong>One clear brief</strong></div><div class="fact"><span>Output</span><strong>Agreed before start</strong></div><div class="fact"><span>Feedback</span><strong>Within the allowance</strong></div>''' + link("contact.html?service=brief", "Discuss your brief", "button") + '''</aside></div></section>
<section class="section section--line faq"><div class="shell"><div class="section-index">Good to know</div><h2>Common questions</h2><details><summary>Can you design screens from our brief?</summary><p>Yes. Share the product goal, users, current files and constraints. I’ll confirm what can be designed within the available time.</p></details><details><summary>Does this include development?</summary><p>This offer covers design and handover. Production development would need its own scope.</p></details><details><summary>What if we need more than four hours?</summary><p>We can agree an additional four-hour block or move to monthly support before the scope changes.</p></details></div></section>'''
page("services/ux-ui-brief.html", "Focused UX/UI design brief | Felipe Amorim", "A focused UX/UI brief from €500: senior product design for one agreed flow, screen set or interface problem, with Figma handover.", brief, "services", service_schema("Focused UX/UI design brief", "Up to four hours of senior UX/UI design for one agreed product brief, including handover and feedback within the allowance.", "500"))

monthly = '''
<section class="page-hero page-hero--compact"><div class="shell"><div class="bread"><a href="../services.html">Services</a> / Monthly design support</div><div class="eyebrow">A little senior capacity, every month</div><h1>Your product team’s <span class="accent">design partner.</span></h1><p class="lead">A monthly allocation for the flows, screens and product decisions that need experienced attention, without a full-time hire.</p></div></section>
<section class="section"><div class="shell detail-layout"><div>
  <div class="detail-block"><div class="section-index">What this is for</div><h2>Steady progress on real briefs.</h2><p>Use the allocation for new screens, improving existing flows, prototyping, interface reviews, design-system decisions and developer handover. It works well for a product or agency team that can provide context and keep one brief active at a time.</p><p>I’ll consider the user journey and business goal while making the design itself. You retain a direct line to the person doing the work.</p></div>
  <div class="detail-block"><div class="section-index">How the allocation works</div><h2>Clear time, clear priorities.</h2><ul><li>16 hours of design time within a calendar month.</li><li>We agree a priority and estimate for each brief before it starts.</li><li>Calls, feedback, revisions and handover use the same allocation.</li><li>One active brief at a time; new priorities can replace queued work.</li><li>Unused hours expire at month-end. Extra four-hour blocks are €500 by agreement.</li></ul></div>
  <div class="detail-block"><div class="section-index">Working together</div><h2>Thoughtful, mostly async.</h2><p>I work primarily asynchronously, with planned calls where they move a decision forward. I respond to project messages within two working days and agree delivery dates per brief. Monthly payment is in advance; scope and start date are confirmed in writing.</p></div>
</div><aside class="detail-aside"><div class="meta-label">Monthly design support</div><span class="price">€1,600 <small>/ month</small></span><p class="small-copy">16 hours. Excludes applicable VAT.</p><div class="fact"><span>Capacity</span><strong>16 hours/month</strong></div><div class="fact"><span>Briefs</span><strong>One active at a time</strong></div><div class="fact"><span>Communication</span><strong>Async, planned calls</strong></div><div class="fact"><span>Start</span><strong>By agreement</strong></div>''' + link("contact.html?service=monthly", "Discuss monthly support", "button") + '''</aside></div></section>
<section class="section section--line faq"><div class="shell"><div class="section-index">Good to know</div><h2>Common questions</h2><details><summary>Can you work from our existing Figma files?</summary><p>Yes. Existing components, content and developer constraints help me make work that fits your product.</p></details><details><summary>Can priorities change during the month?</summary><p>Yes, provided we pause or finish the current brief and agree what the remaining time can cover.</p></details><details><summary>Can you attend regular team meetings?</summary><p>Occasional planned calls can fit within the allocation. If you need daily availability, we should discuss a different arrangement.</p></details></div></section>'''
page("services/monthly-design.html", "Monthly product design support | Felipe Amorim", "16 hours of senior product design support for €1,600 per month. UX/UI screens, flows, reviews and Figma handover for European and UK teams.", monthly, "services", service_schema("Monthly product design support", "Sixteen hours per month of senior UX/UI design for product teams, including flows, screens, reviews and developer handover.", "1600"))

work = '''
<section class="page-hero"><div class="shell"><div class="eyebrow">Selected work</div><h1>Work that connects the <span class="accent">details to the whole.</span></h1><p class="lead">Product design has to make sense on the screen and across the journey. Here are two examples from my experience.</p></div></section>
<section class="section"><div class="shell work-list">
<a class="work-card" href="work/atletico-de-madrid.html"><div class="work-image"><img src="img/atm_case.png" alt="Atlético de Madrid mobile fan experience screens" width="771" height="709"></div><div class="work-details"><div><h3>Atlético de Madrid</h3><p>Connecting fan services in a mobile experience</p></div><span class="arrow" aria-hidden="true">↗</span></div></a>
<a class="work-card" href="work/card-dynamics.html"><div class="work-image"><img src="img/card_case.png" alt="Card Dynamics product identity shown on a tablet" width="771" height="709"></div><div class="work-details"><div><h3>Card Dynamics</h3><p>Design direction for a fintech product and its interfaces</p></div><span class="arrow" aria-hidden="true">↗</span></div></a>
</div></section>
<section class="section section--line"><div class="shell split"><div><div class="section-index">More selected work</div><h2>A wider range of product questions.</h2></div><div><p>''' + link("cases/impulse.html", "Impulse · Speculative future of payments") + '''</p><p><a class="text-link" href="https://www.behance.net/gallery/241661977/Service-Design-for-Pizza-Hut">Pizza Hut · Service design <span class="arrow" aria-hidden="true">↗</span></a></p><p><a class="text-link" href="https://www.behance.net/gallery/201713907/Outback-Customer-Experience">Outback · Customer experience <span class="arrow" aria-hidden="true">↗</span></a></p></div></div></section>
<section class="section section--line"><div class="shell split"><div><div class="section-index">More of the story</div><h2>From product work to design leadership.</h2></div><div><p class="body-copy">These projects sit within a wider career across service design, studios, innovation and teams. My leadership experience is available separately for employers and collaborators.</p>''' + link("leadership.html", "Explore leadership experience") + '''</div></div></section>'''
page("work.html", "Selected UX/UI work | Felipe Amorim", "Selected product design work by Felipe Amorim, including Atlético de Madrid mobile fan experience and Card Dynamics fintech interfaces.", work, "work")

atletico = '''
<section class="page-hero page-hero--compact"><div class="shell"><div class="bread"><a href="../work.html">Selected work</a> / Atlético de Madrid</div><div class="eyebrow">Mobile product · Fan experience</div><h1>Bringing the fan journey <span class="accent">into one app.</span></h1><p class="lead">A product direction for the official Atlético de Madrid app, connecting practical services and fan benefits in a clearer mobile experience.</p><div class="case-cover"><img src="../img/atm_case.png" alt="Two Atlético de Madrid app screens showing fan services and a card" width="771" height="709"></div><div class="case-facts"><div><span class="meta-label">Client</span><strong>Atlético de Madrid</strong></div><div><span class="meta-label">My contribution</span><strong>Product and experience design</strong></div><div><span class="meta-label">Focus</span><strong>Mobile navigation, services and card experience</strong></div></div></div></section>
<section class="section"><div class="shell detail-layout"><div>
<div class="detail-block"><div class="section-index">Context</div><h2>Many fan needs. One mobile entry point.</h2><p>Club apps can pull in several directions at once: tickets, matchday information, food, merchandise, benefits and payment. The design challenge was to give those services a place that felt coherent to a fan using a phone, often in a time-sensitive setting.</p><p>The public screens show a compact service hub and a card area. Together, they make the relationship between everyday club activities and member benefits easier to understand.</p></div>
<div class="detail-block"><div class="section-index">Design decisions</div><h2>Make actions visible at the moment of need.</h2><p>The marketplace screen gives prominent positions to the actions fans may seek quickly: store, tour, food and drink, and tickets. The card screen puts the membership or payment card in the same product environment, rather than treating it as an unrelated destination.</p><p>This approach keeps the interface familiar across different tasks. It also gives the team a structure in which new services can be added without asking users to learn a new interaction pattern each time.</p></div>
<div class="detail-block"><div class="section-index">Takeaway</div><h2>Useful screens start with the journey.</h2><p>The most valuable product decision here was not a single visual treatment. It was framing several club touchpoints as one connected fan experience, then making that direction legible in mobile screens.</p></div>
</div><aside class="detail-aside"><div class="meta-label">What this demonstrates</div><p>Mapping a multi-service experience into a focused mobile interface, with clear paths to the actions users need.</p><a class="text-link" href="https://www.behance.net/gallery/201717263/Atletico-de-Madrid-Cashless-Marketplace">View the original Behance project <span class="arrow" aria-hidden="true">↗</span></a></aside></div></section>'''
page("work/atletico-de-madrid.html", "Atlético de Madrid app case study | Felipe Amorim", "Felipe Amorim's product design contribution to the Atlético de Madrid mobile fan experience, connecting services and card benefits.", atletico, "work")

card = '''
<section class="page-hero page-hero--compact"><div class="shell"><div class="bread"><a href="../work.html">Selected work</a> / Card Dynamics</div><div class="eyebrow">Fintech · Product and brand</div><h1>Making a complex financial journey <span class="accent">feel navigable.</span></h1><p class="lead">Design direction for Card Dynamics, bringing product, brand and mobile interface decisions into a more consistent experience.</p><div class="case-cover"><img src="../img/card_case.png" alt="Card Dynamics product identity shown on a tablet" width="771" height="709"></div><div class="case-facts"><div><span class="meta-label">Client</span><strong>Card Dynamics</strong></div><div><span class="meta-label">My contribution</span><strong>Design direction and product revamp</strong></div><div><span class="meta-label">Focus</span><strong>Fintech interface and brand coherence</strong></div></div></div></section>
<section class="section"><div class="shell detail-layout"><div>
<div class="detail-block"><div class="section-index">Context</div><h2>Clarity matters when money is involved.</h2><p>Financial tasks ask users to understand a process, trust what will happen and complete it without mistakes. Card Dynamics needed design direction that could work across its own product and partner experiences.</p><p>My role covered design operations and a wider product and brand revamp. The public screen examples show this direction applied to account connection, selection and verification flows.</p></div>
<div class="detail-block"><div class="section-index">Interface work</div><h2>Help people see where they are.</h2><p>The account-connection screens use a prominent primary action and short, benefit-led explanations. Account selection places options in a familiar card format, while the confirmation screen separates the code task from the background journey.</p><p>Across these states, labels, actions and the supporting visual language need to remain legible even when partner branding changes. That is the practical design challenge behind a white-label product.</p></div>
<div class="detail-block"><div class="section-index">Takeaway</div><h2>A system has to survive real screens.</h2><p>Brand direction becomes useful when it helps people make decisions in the product. This work demonstrates the connection between design operations, interface consistency and the details of a financial flow.</p></div>
</div><aside class="detail-aside"><div class="meta-label">What this demonstrates</div><p>Designing across product and identity while keeping high-stakes mobile tasks understandable.</p><a class="text-link" href="https://www.behance.net/gallery/234892939/Card-Dynamics-Revamp">View the original Behance project <span class="arrow" aria-hidden="true">↗</span></a></aside></div>
<div class="shell case-visuals"><figure><img src="../img/card_dynamics/3.png" alt="Card Dynamics partner-branded account connection screen" loading="lazy"><figcaption>A partner-branded account connection step, with the action and reassurance grouped in one view.</figcaption></figure><figure><img src="../img/card_dynamics/4.png" alt="Card Dynamics SMS verification state" loading="lazy"><figcaption>A verification state that isolates the code entry task and next action.</figcaption></figure></div></section>'''
page("work/card-dynamics.html", "Card Dynamics design case study | Felipe Amorim", "Card Dynamics fintech case study by Felipe Amorim: design direction for product, brand and mobile account connection interfaces.", card, "work")

leadership = '''
<section class="page-hero"><div class="shell"><div class="eyebrow">Experience and leadership</div><h1>A career built across <span class="accent">design, teams and products.</span></h1><p class="lead">I’m Felipe “Caroé” Amorim, a Madrid-based product designer with over 20 years across UX, service design, branding and digital product strategy.</p></div></section>
<section class="section"><div class="shell split"><div><div class="section-index">About me</div><h2>Hands-on craft, with a leader’s perspective.</h2></div><div><p class="body-copy">I’ve founded design ventures, led teams and worked with organisations as they built or improved products. That experience helps me connect interface details to commercial and organisational realities.</p><p class="body-copy">I currently work at Luzia. Before that, I led design at 4all and founded Brava Digital. My freelance work is a small, separate allocation for well-defined projects.</p><p class="body-copy">I work in English, Spanish and Portuguese.</p></div></div></section>
<section class="section section--line"><div class="shell"><div class="section-index">Selected experience</div><div class="detail-layout"><div>
<div class="detail-block"><h2>Design leadership</h2><p>At 4all, I led UX/UI and strategic consulting work for digital products and client projects. That meant managing designers and connecting design processes to business goals while remaining close to delivery.</p></div>
<div class="detail-block"><h2>Building ventures</h2><p>I founded Brava Digital, a design studio focused on branding and digital experiences, and co-founded Pipe Digital, a UX and front-end venture. These roles gave me direct responsibility for teams, clients and the work itself.</p></div>
<div class="detail-block"><h2>Product and future thinking</h2><p>My work spans research, service design, interface design, business strategy and emerging technologies. I’ve continued learning through UX and futures-thinking studies while working on digital products.</p></div>
</div><aside class="detail-aside"><div class="meta-label">Experience at a glance</div><div class="fact"><span>Location</span><strong>Madrid, Spain</strong></div><div class="fact"><span>Languages</span><strong>Portuguese, English, Spanish</strong></div><div class="fact"><span>Focus</span><strong>Product, UX and design leadership</strong></div><p style="margin-top:28px">''' + link("resume.html", "View résumé") + '''</p><p>''' + link("contact.html", "Start a conversation") + '''</p></aside></div></div></section>'''
page("leadership.html", "Design leadership and experience | Felipe Amorim", "Felipe Amorim is a Madrid-based senior product designer and former design leader with 20+ years across UX, strategy and digital products.", leadership, "leadership")

if not (ROOT / "resume.html").is_file():
    raise FileNotFoundError("The detailed resume.html must be preserved")
PAGES.append(BASE + "resume.html")

contact = '''
<section class="section"><div class="shell contact-grid"><div class="contact-details"><div class="eyebrow">Let’s talk about the work</div><h1>Have a brief? <span class="accent">Tell me.</span></h1><p class="lead">A few details about your product and the decision in front of you will help us see whether a focused brief or monthly support is the right fit.</p><p class="body-copy">I work mainly asynchronously, with planned calls when they help. English, Spanish and Portuguese are all welcome.</p><p><a href="mailto:felipie@gmail.com">felipie@gmail.com</a></p><p class="small-copy">Prefer a direct email? That works too.</p></div>
<form class="contact-form" id="brief-form"><h2>Start with the essentials.</h2>
<label class="field">Your name<input name="name" autocomplete="name" required placeholder="Your name"></label>
<label class="field">Your email<input name="email" type="email" autocomplete="email" required placeholder="you@company.com"></label>
<label class="field">What do you need?<select name="service" required><option value="">Choose a starting point</option><option value="Focused UX/UI brief">A focused UX/UI brief · from €500</option><option value="Monthly design support">Monthly design support · €1,600/month</option><option value="Not sure yet">Not sure yet</option></select></label>
<label class="field">Product and problem<textarea name="problem" required placeholder="What are you building, and what needs to change?"></textarea></label>
<label class="field">Deadline and budget<input name="timing" placeholder="When do you need it, and what budget have you set?"></label>
<label class="field">How did you find me?<input name="source" placeholder="Search, LinkedIn, Behance, a job post…"></label>
<button class="button" type="submit">Prepare my email <span class="arrow" aria-hidden="true">↗</span></button>
<p class="form-status" id="form-status" role="status" aria-live="polite">This prepares an email in your mail app. You’ll review and send it yourself.</p>
<noscript><p><a href="mailto:felipie@gmail.com?subject=Product%20design%20brief">Email Felipe directly</a></p></noscript>
</form></div></section>'''
page("contact.html", "Contact Felipe Amorim | Product design brief", "Discuss a UX/UI design brief or monthly senior product design support with Felipe Amorim in Madrid.", contact, "contact")

urls = "\n".join(f"  <url><loc>{escape(url)}</loc></url>" for url in PAGES)
(ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n', encoding="utf-8")
print(f"Built {len(PAGES) - 1} pages and sitemap.xml; preserved resume.html")
