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
    // SVG ripples are written with begin="indefinite", so they never start on
    // their own: a paused or reduced-motion visitor never sees them move at all
    if (!off) document.querySelectorAll("animate[begin=indefinite]").forEach(function (an) {
      if (!an.dataset.started) { an.dataset.started = "1"; an.beginElement(); }
    });
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
    document.dispatchEvent(new CustomEvent("motionchange", { detail: { off: off } }));
  }

  // big decorative pictures inside SVGs (the spilled jar): attach them unless
  // this is the lite version, where they're skipped to save the download
  if (!root.classList.contains("lite")) {
    document.querySelectorAll("image[data-href]").forEach(function (im) { im.setAttribute("href", im.getAttribute("data-href")); });
  }

  apply(root.classList.contains("motion-off"), false);   // the <head> script already chose

  // if the visitor turns reduced motion on (or off) in their device settings while
  // the page is open, follow it, unless they've used the button on this site
  if (window.matchMedia) {
    var mq = matchMedia("(prefers-reduced-motion: reduce)");
    var follow = function (e) {
      var saved = null; try { saved = localStorage.getItem("motion"); } catch (err) {}
      if (!saved) apply(e.matches, false);
    };
    if (mq.addEventListener) mq.addEventListener("change", follow); else if (mq.addListener) mq.addListener(follow);
  }
  if (!btn) return;
  btn.addEventListener("click", function () { apply(!root.classList.contains("motion-off"), true); });

  // keep the button in the lower-right corner, but lift it above the footer
  var footer = document.querySelector(".colophon");
  function place() {
    var lift = footer ? Math.max(0, window.innerHeight - footer.getBoundingClientRect().top) : 0;
    btn.style.bottom = (48 + lift) + "px";   // see .motion-toggle in style.css
  }
  var queued = false;
  function onScroll() { if (!queued) { queued = true; requestAnimationFrame(function () { queued = false; place(); }); } }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  place();
})();
