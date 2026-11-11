// The pause/play button for everything that moves on its own: the flickering
// letters, the swirling jars, the rippling spill, autoplaying videos and the
// bubbles. It starts paused for people whose device asks for reduced motion,
// and remembers the visitor's choice on this browser.
(function () {
  var root = document.documentElement;
  var btn = document.querySelector(".motion-toggle");

  function svgs(fn) {
    document.querySelectorAll("svg").forEach(function (s) { if (s[fn]) s[fn](); });
  }
  function apply(off, remember) {
    root.classList.toggle("motion-off", off);
    root.classList.toggle("motion-on", !off);
    svgs(off ? "pauseAnimations" : "unpauseAnimations");
    document.querySelectorAll("video[autoplay]").forEach(function (v) {
      if (off) v.pause(); else { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
    });
    if (btn) {
      btn.setAttribute("aria-pressed", off ? "true" : "false");
      btn.setAttribute("aria-label", off ? "Play animations" : "Pause animations");
      btn.title = off ? "Play animations" : "Pause animations";
    }
    if (remember) { try { localStorage.setItem("motion", off ? "off" : "on"); } catch (e) {} }
  }

  apply(root.classList.contains("motion-off"), false);   // the <head> script already chose
  if (!btn) return;
  btn.addEventListener("click", function () { apply(!root.classList.contains("motion-off"), true); });

  // keep the button in the lower-right corner, but lift it above the footer
  var footer = document.querySelector(".colophon");
  function place() {
    var lift = footer ? Math.max(0, window.innerHeight - footer.getBoundingClientRect().top) : 0;
    btn.style.bottom = (16 + lift) + "px";
  }
  var queued = false;
  function onScroll() { if (!queued) { queued = true; requestAnimationFrame(function () { queued = false; place(); }); } }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  place();
})();
