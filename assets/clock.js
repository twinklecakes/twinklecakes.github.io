// Hovering (or tapping) the grandfather clock plays its video, on a loop,
// inside the front panel of the clock case.
(function () {
  var clock = document.querySelector(".stk-clock");
  var fig = document.querySelector(".clock-video");
  if (!clock || !fig) return;
  var v = fig.querySelector("video");

  function play() {
    if (!v.src && v.dataset.src) v.src = v.dataset.src;   // fetched only the first time it plays
    fig.classList.add("on");
    var p = v.play(); if (p && p.catch) p.catch(function () {});
  }
  function stop() { fig.classList.remove("on"); v.pause(); }

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
