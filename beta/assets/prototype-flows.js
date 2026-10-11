(() => {
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('[data-prototype-flow]').forEach(flow => {
    const frames = JSON.parse(flow.dataset.prototypeFlow);
    const screen = flow.querySelector('.device-mockup__screen');
    const image = screen.querySelector('img');
    const incoming = image.cloneNode();
    incoming.alt = '';
    incoming.setAttribute('aria-hidden', 'true');
    incoming.classList.add('flow-frame--incoming');
    screen.append(incoming);
    const tap = document.createElement('span');
    tap.className = 'prototype-flow__tap';
    tap.setAttribute('aria-hidden', 'true');
    screen.append(tap);
    const label = flow.querySelector('.prototype-flow__state');
    let index = 0;
    let timer;
    let visible = false;
    let paused = motion.matches;
    let generation = 0;
    const clear = () => {
      clearTimeout(timer);
      generation++;
      tap.classList.remove('is-tapping');
      incoming.classList.remove('is-visible');
    };
    const announce = () => {
      if (label) label.textContent = frames[index].label;
      image.alt = frames[index].alt || frames[index].label;
    };
    const schedule = delay => {
      clearTimeout(timer);
      if (paused || !visible || document.hidden) return;
      timer = setTimeout(advance, delay);
    };
    const waitForFade = () => new Promise(resolve => {
      let settled = false;
      const finish = () => {
        if (settled) return;
        settled = true;
        clearTimeout(fallback);
        incoming.removeEventListener('transitionend', onEnd);
        resolve();
      };
      const onEnd = event => {
        if (event.target === incoming && event.propertyName === 'opacity') finish();
      };
      const fallback = setTimeout(finish, motion.matches ? 0 : 1000);
      incoming.addEventListener('transitionend', onEnd);
    });
    const nextFrame = () => new Promise(resolve => requestAnimationFrame(resolve));
    const advance = async () => {
      const current = generation;
      const next = (index + 1) % frames.length;
      incoming.classList.remove('is-visible');
      incoming.src = frames[next].src;
      try { await incoming.decode(); } catch { schedule(3000); return; }
      if (current !== generation || paused || !visible || document.hidden) return;
      const transition = async () => {
        tap.classList.remove('is-tapping');
        // Give the browser a painted hidden state before revealing the decoded frame.
        await nextFrame();
        await nextFrame();
        if (current !== generation || paused || !visible || document.hidden) return;
        incoming.classList.add('is-visible');
        if (!motion.matches) await waitForFade();
        if (current !== generation || paused || !visible || document.hidden) return;
        image.src = frames[next].src;
        try { await image.decode(); } catch { return; }
        if (current !== generation) return;
        index = next;
        announce();
        incoming.style.transition = 'none';
        incoming.classList.remove('is-visible');
        incoming.getBoundingClientRect();
        requestAnimationFrame(() => { incoming.style.transition = ''; });
        schedule(frames[index].hold || 3400);
      };
      if (frames[index].tap && !motion.matches) {
        tap.style.left = frames[index].tap[0] + '%';
        tap.style.top = frames[index].tap[1] + '%';
        tap.classList.add('is-tapping');
        timer = setTimeout(transition, 500);
      } else transition();
    };
    new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting;
      clear();
      incoming.classList.remove('is-visible');
      schedule(1500);
    }, { threshold: .2 }).observe(flow);
    document.addEventListener('visibilitychange', () => { clear(); schedule(1500); });
    motion.addEventListener('change', () => {
      paused = motion.matches;
      clear();
      schedule(1000);
    });
    announce();
  });
})();
