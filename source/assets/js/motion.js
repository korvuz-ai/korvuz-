// Progressive enhancement: content is readable before JS and without observers.
export function initMotion(root = document) {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const desktop = matchMedia('(min-width: 900px) and (hover: hover) and (pointer: fine)');
  let dispose = () => {};
  const setup = () => {
    dispose();
    if (reduced.matches || !('IntersectionObserver' in window)) return;

    const events = new AbortController();
    const {signal} = events;
    const revealed = root.querySelectorAll('main > .section, .work-grid > .project-card, .blog-card, .case-cover, .case-body, .compact-cta');
    const headline = root.querySelector('h1');
    const lines = [...root.querySelectorAll('.timeline')].filter(el => el instanceof HTMLElement);
    /** @type {Set<HTMLElement>} */
    const activeLines = new Set();
    /** @typedef {{host: HTMLElement, surface: HTMLElement, limit: number, point: {x: number, y: number} | null, dirty: boolean}} PointerState */
    /** @type {PointerState[]} */
    const pointers = [];
    let frame = 0;

    const revealObserver = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        entry.target.classList.add('reveal-ready');
        revealObserver.unobserve(entry.target);
      }
    }, {threshold: 0, rootMargin: '0px 0px -24px 0px'});
    revealed.forEach(el => revealObserver.observe(el));
    headline?.classList.add('headline-ready');

    /** @param {number} value @param {number} min @param {number} max */
    const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
    const update = () => {
      frame = 0;
      // Read all geometry first, then write only transform variables.
      const progress = [...activeLines].map(el => {
        const rect = el.getBoundingClientRect();
        return {el, value: clamp((innerHeight * .85 - rect.top) / Math.max(1, rect.height), 0, 1)};
      });
      const offsets = pointers.filter(state => state.dirty).map(state => {
        state.dirty = false;
        const rect = state.host.getBoundingClientRect();
        const x = state.point ? clamp((state.point.x - rect.left) / Math.max(1, rect.width) * 2 - 1, -1, 1) * state.limit : 0;
        const y = state.point ? clamp((state.point.y - rect.top) / Math.max(1, rect.height) * 2 - 1, -1, 1) * state.limit : 0;
        return {state, x, y};
      });
      for (const {el, value} of progress) el.style.setProperty('--line-progress', value.toFixed(4));
      for (const {state, x, y} of offsets) {
        state.surface.style.setProperty('--parallax-x', `${x.toFixed(2)}px`);
        state.surface.style.setProperty('--parallax-y', `${y.toFixed(2)}px`);
      }
    };
    const schedule = () => {if (!frame && !document.hidden) frame = requestAnimationFrame(update)};
    const lineObserver = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!(entry.target instanceof HTMLElement)) continue;
        if (entry.isIntersecting) activeLines.add(entry.target);
        else {
          activeLines.delete(entry.target);
          entry.target.style.setProperty('--line-progress', entry.boundingClientRect.top < 0 ? '1' : '0');
        }
      }
      schedule();
    });
    lines.forEach(el => {el.style.setProperty('--line-progress', '0'); lineObserver.observe(el)});
    window.addEventListener('scroll', () => {if (activeLines.size) schedule()}, {passive: true, signal});
    window.addEventListener('resize', schedule, {passive: true, signal});
    document.addEventListener('visibilitychange', schedule, {signal});
    window.addEventListener('pageshow', schedule, {signal});

    if (desktop.matches) {
      const hosts = [...root.querySelectorAll('.hero-visual, .project-image-link')].filter(el => el instanceof HTMLElement);
      for (const host of hosts) {
        const isHero = host.classList.contains('hero-visual');
        const surface = host.querySelector(isHero ? '.hero-art' : '.project-media');
        if (!(surface instanceof HTMLElement)) continue;
        /** @type {PointerState} */
        const state = {host, surface, limit: isHero ? 6 : 4, point: null, dirty: false};
        pointers.push(state);
        surface.classList.add('parallax-surface');
        host.addEventListener('pointermove', event => {
          if (event.pointerType !== 'mouse' || host.matches(':focus-within')) return;
          state.point = {x: event.clientX, y: event.clientY};
          state.dirty = true;
          schedule();
        }, {passive: true, signal});
        const reset = () => {state.point = null; state.dirty = true; schedule()};
        host.addEventListener('pointerleave', reset, {passive: true, signal});
        host.addEventListener('pointercancel', reset, {passive: true, signal});
        host.addEventListener('focusin', reset, {signal});
      }
    }
    // Focusing content never waits for an entrance animation.
    root.addEventListener('focusin', event => {
      if (event.target instanceof Element) event.target.closest('.reveal-ready')?.classList.remove('reveal-ready');
    }, {signal});

    dispose = () => {
      events.abort();
      cancelAnimationFrame(frame);
      revealObserver.disconnect();
      lineObserver.disconnect();
      revealed.forEach(el => el.classList.remove('reveal-ready'));
      headline?.classList.remove('headline-ready');
      lines.forEach(el => el.style.removeProperty('--line-progress'));
      for (const {surface} of pointers) {
        surface.classList.remove('parallax-surface');
        surface.style.removeProperty('--parallax-x');
        surface.style.removeProperty('--parallax-y');
      }
      dispose = () => {};
    };
  };
  reduced.addEventListener('change', setup);
  desktop.addEventListener('change', setup);
  setup();
}
