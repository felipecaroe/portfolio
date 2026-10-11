const siteHeader = document.querySelector('.site-header');
const menuToggle = siteHeader?.querySelector('.menu-toggle');
const siteNavigation = siteHeader?.querySelector('#site-navigation');
if (menuToggle && siteNavigation) {
  const mobileHeader = window.matchMedia('(max-width:700px)');
  const closeMenu = (restoreFocus = false) => {
    if (restoreFocus) menuToggle.focus();
    menuToggle.setAttribute('aria-expanded', 'false');
    menuToggle.setAttribute('aria-label', 'Open menu');
    siteNavigation.hidden = mobileHeader.matches;
  };
  const updateHeader = () => {
    const focused = document.activeElement;
    const focusInMenu = siteNavigation.contains(focused);
    const contactLink = siteHeader.querySelector('.nav-contact');
    if (mobileHeader.matches) {
      menuToggle.after(siteNavigation);
    } else {
      contactLink.before(siteNavigation);
    }
    menuToggle.hidden = !mobileHeader.matches;
    closeMenu(mobileHeader.matches && focusInMenu);
    if (!mobileHeader.matches) {
      if (focused === menuToggle) siteNavigation.querySelector('a').focus();
      else if (focusInMenu) focused.focus();
    }
  };
  siteHeader.dataset.menuReady = '';
  menuToggle.addEventListener('click', () => {
    const open = menuToggle.getAttribute('aria-expanded') !== 'true';
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    siteNavigation.hidden = !open;
  });
  siteNavigation.addEventListener('click', event => {
    if (event.target.closest('a') && mobileHeader.matches) closeMenu(true);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') {
      closeMenu(true);
    }
  });
  document.addEventListener('click', event => {
    if (!siteHeader.contains(event.target) && menuToggle.getAttribute('aria-expanded') === 'true') {
      closeMenu(siteNavigation.contains(document.activeElement));
    }
  });
  siteHeader.addEventListener('focusout', event => {
    if (event.relatedTarget && !siteHeader.contains(event.relatedTarget)
        && menuToggle.getAttribute('aria-expanded') === 'true') closeMenu();
  });
  mobileHeader.addEventListener('change', updateHeader);
  updateHeader();
}

const backgroundVideo = document.querySelector('.site-background-video');
if (backgroundVideo) {
  const motion = window.matchMedia('(min-width:769px) and (prefers-reduced-motion:no-preference)');
  const sources = [...backgroundVideo.querySelectorAll('source[data-src]')];
  const updateBackground = () => {
    if (motion.matches) {
      sources.forEach(source => { source.src = source.dataset.src; });
      backgroundVideo.load();
      backgroundVideo.play().catch(() => {});
    } else {
      backgroundVideo.pause();
      sources.forEach(source => source.removeAttribute('src'));
      backgroundVideo.load();
    }
  };
  motion.addEventListener('change', updateBackground);
  updateBackground();
}

const copyEmail = document.querySelector('[data-copy-email]');
if (copyEmail) {
  copyEmail.addEventListener('click', async () => {
    const status = document.querySelector('.copy-email-status');
    try {
      await navigator.clipboard.writeText(copyEmail.dataset.copyEmail);
      status.textContent = 'Email address copied.';
    } catch {
      status.textContent = `Copy this address: ${copyEmail.dataset.copyEmail}`;
    }
  });
}

const form = document.querySelector('#brief-form');

if (form) {
  const requestedService = new URLSearchParams(window.location.search).get('service');
  if (requestedService === 'agency') form.elements.service.value = 'Agency or studio client brief';
  if (requestedService === 'brief') form.elements.service.value = 'Focused UX/UI brief';
  if (requestedService === 'monthly') form.elements.service.value = 'Monthly design support';
  if (requestedService === 'product') form.elements.service.value = 'Product team project';

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const status = document.querySelector('#form-status');
    const submit = form.querySelector('[type="submit"]');
    const apiKey = form.elements.apiKey.value;
    if (!apiKey || apiKey === 'STATIC_FORMS_API_KEY_TO_ADD') {
      status.textContent = 'The contact form is being connected. Please email me directly for now.';
      status.dataset.state = 'error';
      return;
    }

    submit.disabled = true;
    form.setAttribute('aria-busy', 'true');
    status.textContent = 'Sending your enquiry…';
    status.dataset.state = 'pending';

    try {
      const response = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
      });
      const result = await response.json();
      if (!response.ok || !result.success) throw new Error(result.message || 'Submission failed.');
      form.reset();
      status.textContent = 'Thanks. Your enquiry has been sent. I’ll reply within two working days.';
      status.dataset.state = 'success';
    } catch {
      status.replaceChildren('I couldn’t send your enquiry. Please try again or ', Object.assign(document.createElement('a'), { href: 'mailto:felipie@gmail.com?subject=Product%20design%20brief', textContent: 'email me directly' }), '.');
      status.dataset.state = 'error';
    } finally {
      submit.disabled = false;
      form.removeAttribute('aria-busy');
    }
  });
}

const offerTrack = document.querySelector('[data-offer-track]');
if (offerTrack) {
  const cards = [...offerTrack.querySelectorAll('.offer-card')];
  const count = document.querySelector('[data-offer-count]');
  const progress = document.querySelector('[data-offer-progress]');
  const previous = document.querySelector('[data-offer-prev]');
  const next = document.querySelector('[data-offer-next]');
  const step = () => cards[0].getBoundingClientRect().width + parseFloat(getComputedStyle(offerTrack).columnGap || '0');
  const update = () => {
    const maxScroll = Math.max(0, offerTrack.scrollWidth - offerTrack.clientWidth);
    const visibleCards = Math.max(1, Math.ceil(offerTrack.clientWidth / step()));
    const maxStart = Math.max(1, cards.length - visibleCards + 1);
    const first = Math.min(maxStart, Math.floor((offerTrack.scrollLeft + 1) / step()) + 1);
    const last = Math.min(cards.length, first + visibleCards - 1);
    const percentage = maxScroll ? Math.min(1, offerTrack.scrollLeft / maxScroll) : 1;
    count.textContent = `${String(first).padStart(2, '0')}–${String(last).padStart(2, '0')} / ${String(cards.length).padStart(2, '0')}`;
    progress.style.width = `${percentage * 100}%`;
    previous.disabled = offerTrack.scrollLeft <= 1;
    next.disabled = offerTrack.scrollLeft >= maxScroll - 1;
  };
  previous.addEventListener('click', () => offerTrack.scrollBy({ left: -step(), behavior: 'smooth' }));
  next.addEventListener('click', () => offerTrack.scrollBy({ left: step(), behavior: 'smooth' }));
  offerTrack.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
}
