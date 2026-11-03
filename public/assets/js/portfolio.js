'use strict';

document.documentElement.classList.add('enhanced');

const menuButton = document.getElementById('menu-btn');
const mobileMenu = document.getElementById('mobile-nav');

function closeMenu() {
  mobileMenu.classList.remove('open');
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', 'Open menu');
}

menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  mobileMenu.classList.toggle('open', open);
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
});
mobileMenu.addEventListener('click', (event) => {
  if (event.target.closest('a')) closeMenu();
});
document.addEventListener('click', (event) => {
  if (!event.target.closest('.navbar')) closeMenu();
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menuButton.focus();
  }
});
const mobileBreakpoint = window.matchMedia('(max-width: 820px)');
mobileBreakpoint.addEventListener('change', closeMenu);

const stages = {
  source: 'A reviewed, version-controlled change is the starting point for a repeatable release.',
  delivery: 'Jenkins brings the build and release steps into a pipeline the team can inspect and maintain.',
  platform: 'Amazon EKS runs the service. Verification and operational follow-up continue after the deployment.',
};
document.querySelectorAll('[data-stage]').forEach((button) => {
  button.addEventListener('click', () => {
    document.querySelectorAll('[data-stage]').forEach((other) => {
      other.setAttribute('aria-pressed', String(other === button));
    });
    document.getElementById('pipeline-detail').textContent = stages[button.dataset.stage];
  });
});

const details = JSON.parse(document.getElementById('portfolio-details').textContent);
const dialog = document.getElementById('detail-dialog');
let detailTrigger;

function appendText(parent, tag, value) {
  const element = document.createElement(tag);
  element.textContent = value;
  parent.append(element);
}

if (typeof dialog.showModal === 'function') {
  document.querySelectorAll('[data-modal]').forEach((link) => {
    link.addEventListener('click', (event) => {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      const detail = details[link.dataset.modal];
      if (!detail) return;
      event.preventDefault();
      detailTrigger = link;
      document.getElementById('detail-title').textContent = detail.title;
      document.getElementById('detail-category').textContent = detail.type || detail.category;
      const body = document.getElementById('detail-body');
      body.replaceChildren();
      detail.paragraphs.forEach((text) => appendText(body, 'p', text));
      const list = document.createElement('ul');
      detail.bullets.forEach((text) => appendText(list, 'li', text));
      body.append(list);
      if (detail.closing) appendText(body, 'p', detail.closing);
      document.getElementById('detail-permalink').href = detail.route;
      dialog.showModal();
      dialog.scrollTop = 0;
      document.body.classList.add('lock');
    });
  });
  document.getElementById('modal-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('lock');
    detailTrigger?.focus();
  });
}

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
if ('IntersectionObserver' in window && !reducedMotion.matches) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('entered');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.reveal').forEach((element) => observer.observe(element));
}
document.getElementById('year').textContent = new Date().getFullYear();
