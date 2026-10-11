(() => {
  const demo = document.querySelector('.rcde-demo');
  if (!demo) return;
  const toggle = demo.querySelector('.rcde-demo__toggle');
  const close = demo.querySelector('.rcde-demo__close');
  let preview;
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const transitionTime = 680;
  const setOpen = open => {
    demo.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', `${open ? 'Close' : 'Open'} Espanyol navigation`);
    close.hidden = !open;
    close.tabIndex = open ? 0 : -1;
  };
  const schedule = (open, delay) => {
    clearTimeout(preview);
    preview = setTimeout(() => {
      setOpen(open);
      schedule(!open, transitionTime + (open ? 3000 : 2000));
    }, delay);
  };
  const interact = open => {
    clearTimeout(preview);
    setOpen(open);
    if (!motion.matches) schedule(!open, transitionTime + (open ? 3000 : 2000));
  };
  toggle.addEventListener('click', () => interact(!demo.classList.contains('is-open')));
  close.addEventListener('click', () => interact(false));
  demo.addEventListener('keydown', event => { if (event.key === 'Escape') interact(false); });
  if (!motion.matches) schedule(true, 1000);
})();
