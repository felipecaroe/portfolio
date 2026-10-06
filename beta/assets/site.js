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

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    const values = Object.fromEntries(new FormData(form).entries());
    const subject = `Freelance UX/UI enquiry: ${values.service}`;
    const body = [
      `Hello Felipe,`,
      '',
      `My name: ${values.name}`,
      `My email: ${values.email}`,
      `I'm interested in: ${values.service}`,
      '',
      `Product and problem:`,
      values.problem,
      '',
      `Deadline and budget: ${values.timing || 'To discuss'}`,
      `How I found you: ${values.source || 'Not specified'}`,
    ].join('\n');

    const url = `mailto:felipie@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    const status = document.querySelector('#form-status');
    status.replaceChildren('Your email draft is ready. If it does not open, ', Object.assign(document.createElement('a'), { href: url, textContent: 'open it here' }), '. Please review and send it from your mail app.');
    window.location.href = url;
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
