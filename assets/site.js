const form = document.querySelector('#brief-form');

if (form) {
  const requestedService = new URLSearchParams(window.location.search).get('service');
  if (requestedService === 'brief') form.elements.service.value = 'Focused UX/UI brief';
  if (requestedService === 'monthly') form.elements.service.value = 'Monthly design support';

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    const values = Object.fromEntries(new FormData(form).entries());
    const subject = `Product design enquiry: ${values.service}`;
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
