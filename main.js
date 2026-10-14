(function () {
  "use strict";

  /* ---------- story viewer: the nine nights + the tenth day ---------- */
  var items = Array.prototype.slice.call(document.querySelectorAll("[data-index]"))
    .sort(function (a, b) { return +a.dataset.index - +b.dataset.index; })
    .map(function (el) {
      return {
        slug: el.id,
        detail: el.querySelector(".detail"),
        img: "/img/" + el.id + ".webp",
        alt: (el.querySelector("img") || {}).alt || ""
      };
    });

  var dialog = document.getElementById("viewer");
  var vImg = document.getElementById("viewer-img");
  var vContent = document.getElementById("viewer-content");
  var vPos = document.getElementById("viewer-pos");
  var current = -1;
  var opener = null;

  function show(i) {
    if (!dialog || !items.length) return;
    current = (i + items.length) % items.length;
    var it = items[current];
    vImg.src = it.img;
    vImg.alt = it.alt;
    vContent.innerHTML = it.detail.innerHTML;
    var h = vContent.querySelector("h3");
    if (h) h.id = "viewer-title";
    vPos.textContent = (current + 1) + " of " + items.length;
    var body = dialog.querySelector(".viewer-body");
    if (body) body.scrollTop = 0;
    var txt = dialog.querySelector(".viewer-text");
    if (txt) txt.scrollTop = 0;
    try { history.replaceState(null, "", "#" + it.slug); } catch (e) {}
    if (!dialog.open) {
      if (typeof dialog.showModal === "function") dialog.showModal();
      else dialog.setAttribute("open", "");
    }
  }

  function close() {
    if (!dialog) return;
    if (dialog.open) dialog.close();
  }

  if (dialog) {
    dialog.addEventListener("close", function () {
      try { history.replaceState(null, "", location.pathname); } catch (e) {}
      if (opener) opener.focus();
    });
    dialog.addEventListener("click", function (ev) {
      if (ev.target === dialog) close(); // click on the backdrop
      var step = ev.target.closest("[data-step]");
      if (step) show(current + +step.dataset.step);
      if (ev.target.closest("[data-close]")) close();
    });
    dialog.addEventListener("keydown", function (ev) {
      if (ev.key === "ArrowRight") show(current + 1);
      if (ev.key === "ArrowLeft") show(current - 1);
    });
  }

  document.querySelectorAll(".card button").forEach(function (btn) {
    btn.addEventListener("click", function () {
      opener = btn;
      show(+btn.closest("[data-index]").dataset.index);
    });
  });
  document.querySelectorAll("[data-open]").forEach(function (btn) {
    btn.addEventListener("click", function () { opener = btn; show(+btn.dataset.open); });
  });

  // open a form directly from a shared link, e.g. /#kalaratri
  var hash = location.hash.replace("#", "");
  if (hash) {
    var idx = items.findIndex(function (it) { return it.slug === hash; });
    if (idx > -1) show(idx);
  }

  /* ---------- embers on Kalaratri's side of the hero ---------- */
  var canvas = document.getElementById("embers");
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!canvas || reduce || !canvas.getContext) return;
  var ctx = canvas.getContext("2d");
  var hero = canvas.parentElement;
  var W = 0, H = 0, dpr = Math.min(window.devicePixelRatio || 1, 2);
  var sparks = [];
  var running = true, looping = false;
  function start() { running = true; if (!looping) { looping = true; requestAnimationFrame(tick); } }

  function size() {
    W = hero.clientWidth; H = hero.clientHeight;
    canvas.width = W * dpr; canvas.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  function spawn(initial) {
    // born on the left (fire) half, mostly low down
    return {
      x: W * (0.06 + Math.random() * 0.42),
      y: initial ? Math.random() * H : H * (0.7 + Math.random() * 0.35),
      r: 0.6 + Math.random() * 1.8,
      vy: 0.25 + Math.random() * 0.7,
      sway: Math.random() * Math.PI * 2,
      life: 0,
      max: 260 + Math.random() * 360,
      hue: 18 + Math.random() * 22
    };
  }
  function tick() {
    if (!running) { looping = false; return; }
    ctx.clearRect(0, 0, W, H);
    ctx.globalCompositeOperation = "lighter";
    for (var i = 0; i < sparks.length; i++) {
      var s = sparks[i];
      s.life++;
      s.sway += 0.02;
      s.y -= s.vy;
      s.x += Math.sin(s.sway) * 0.35 + 0.08;
      var t = s.life / s.max;
      var a = t < 0.15 ? t / 0.15 : 1 - (t - 0.15) / 0.85;
      if (a <= 0 || s.y < -10) { sparks[i] = spawn(false); continue; }
      var g = ctx.createRadialGradient(s.x, s.y, 0, s.x, s.y, s.r * 4);
      g.addColorStop(0, "hsla(" + s.hue + ",95%,68%," + (0.85 * a) + ")");
      g.addColorStop(1, "hsla(" + s.hue + ",95%,50%,0)");
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.arc(s.x, s.y, s.r * 4, 0, Math.PI * 2); ctx.fill();
    }
    requestAnimationFrame(tick);
  }
  size();
  var count = W < 600 ? 26 : 48;
  for (var k = 0; k < count; k++) sparks.push(spawn(true));
  window.addEventListener("resize", size);
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      var vis = entries[0].isIntersecting;
      if (vis) start(); else running = false;
    }).observe(hero);
  }
  document.addEventListener("visibilitychange", function () {
    if (document.hidden) running = false;
    else start();
  });
  start();
})();
