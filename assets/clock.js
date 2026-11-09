// Hovering (or tapping) the grandfather clock plays the clock video, looping
// only the part between data-start and data-end seconds.
(function () {
  var clock = document.querySelector(".stk-clock");
  var fig = document.querySelector(".clock-video");
  if (!clock || !fig) return;
  var v = fig.querySelector("video");
  var start = parseFloat(v.dataset.start) || 0, end = parseFloat(v.dataset.end) || 0;

  function seekIn() {
    if (v.currentTime < start || (end && v.currentTime >= end)) v.currentTime = start;
  }
  function play() {
    fig.classList.add("on");
    if (v.readyState >= 1) seekIn(); else v.addEventListener("loadedmetadata", seekIn, { once: true });
    var p = v.play(); if (p && p.catch) p.catch(function () {});
  }
  function stop() { fig.classList.remove("on"); v.pause(); }

  v.addEventListener("timeupdate", function () {
    if ((end && v.currentTime >= end) || v.currentTime < start - 0.3) v.currentTime = start;
  });
  // mouse: play while hovering. touch: tap to start, tap again to stop.
  clock.addEventListener("pointerenter", function (e) { if (e.pointerType === "mouse") play(); });
  clock.addEventListener("pointerleave", function (e) { if (e.pointerType === "mouse") stop(); });
  var lastType = "mouse";
  clock.addEventListener("pointerdown", function (e) { lastType = e.pointerType; });
  clock.addEventListener("click", function () {
    if (lastType === "mouse") return;
    if (fig.classList.contains("on")) stop(); else play();
  });
})();
