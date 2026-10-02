// Scene runtime. The renderer sets window.__SCENE__ = {d, presenter} before this runs and calls
// window.__seek(seconds, speak) once per frame; nothing here uses real time.
(() => {
  const cfg = window.__SCENE__ || { d: 10 };
  document.documentElement.lang = 'en';
  document.documentElement.style.setProperty('--d', String(cfg.d));

  const apply = () => {
    const text = window.TEXT || {};
    document.querySelectorAll('[data-i]').forEach((el) => {
      const v = text[el.dataset.i];
      if (v !== undefined) el.innerHTML = v;
    });
    const p = cfg.presenter;
    if (p && !document.body.hasAttribute('data-no-presenter')) {
      const box = document.createElement('div');
      box.className = 'presenter';
      const photo = p.photo ? `<img src="${p.photo}" alt="">` : p.initials;
      box.innerHTML = `<div class="face"><div class="ring"></div><div class="photo">${photo}</div></div><div class="who"><b>${p.name}</b><span>${p.title}</span></div>`;
      document.body.appendChild(box);
    }
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', apply);
  else apply();

  window.__seek = (t, speak) => {
    document.documentElement.style.setProperty('--speak', String(speak || 0));
    document.getAnimations().forEach((a) => {
      a.pause();
      a.currentTime = t * 1000;
    });
  };
})();
