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
  clock.addEventListener("mouseenter", play);
  clock.addEventListener("mouseleave", stop);
  clock.addEventListener("click", function () {
    if (fig.classList.contains("on")) stop();
    else { play(); if (window.blowBubbles && matchMedia("(hover: none)").matches) window.blowBubbles(clock); }
  });
})();
