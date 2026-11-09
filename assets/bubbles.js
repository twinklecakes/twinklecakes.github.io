// Soap bubbles. Hovering (or tapping) anything with a bubble trigger blows a
// handful of bubbles that wander on a swirling breeze. Some pop after a while;
// others get caught by a gust and drift off the left, right or top edge.
(function () {
  var TRIGGERS = ".ransom .cut, .book, .jar, .stk-clock";
  var tints = ["#29adc0", "#5a6fd8", "#eb8d5f", "#c4262e", "#6a8a4c", "#2e3c96"];
  var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var live = [], running = false, MAX = 140;

  function rand(a, b) { return a + Math.random() * (b - a); }

  function blow(el) {
    if (still) return;
    var r = el.getBoundingClientRect();
    var n = Math.min(18, MAX - live.length);
    for (var i = 0; i < n; i++) {
      var big = Math.random() < 0.22;
      var size = big ? rand(42, 78) : rand(8, 34);
      var b = document.createElement("span");
      b.className = "bubble";
      b.style.width = b.style.height = size + "px";
      b.style.setProperty("--tint", tints[(Math.random() * tints.length) | 0]);
      document.body.appendChild(b);
      var edge = Math.random() < 0.38 ? ["left", "right", "top"][(Math.random() * 3) | 0] : null;
      live.push({
        el: b, size: size,
        x: r.left + rand(0.1, 0.9) * r.width, y: r.top + rand(0.3, 0.9) * r.height,
        vx: rand(-0.6, 0.6), vy: rand(-0.9, -0.35),   // px per frame (60fps), slow
        edge: edge, pull: rand(0.006, 0.02),
        phase: rand(0, 1000), born: performance.now() + rand(0, 300),
        life: edge ? Infinity : rand(4500, 9000), popAt: 0
      });
    }
    if (!running) { running = true; requestAnimationFrame(step); }
  }

  function step(now) {
    var W = window.innerWidth, H = window.innerHeight;
    for (var i = live.length - 1; i >= 0; i--) {
      var p = live[i], age = now - p.born;
      if (age < 0) { p.el.style.opacity = 0; continue; }
      // the breeze: a slowly turning swirl that depends on where the bubble is
      var t = now * 0.001;
      var ax = Math.sin(p.y * 0.011 + t * 0.9 + p.phase) * 0.028 + Math.cos(t * 0.37 + p.phase) * 0.012;
      var ay = Math.cos(p.x * 0.009 - t * 0.7 + p.phase) * 0.022 - 0.004;   // a little lift
      if (p.edge === "left") ax -= p.pull;
      if (p.edge === "right") ax += p.pull;
      if (p.edge === "top") ay -= p.pull;
      p.vx = (p.vx + ax) * 0.992;
      p.vy = (p.vy + ay) * 0.992;
      p.x += p.vx; p.y += p.vy;

      var gone = p.x < -p.size * 2 || p.x > W + p.size * 2 || p.y < -p.size * 2 || p.y > H + p.size * 2;
      if (!p.popAt && age > p.life) p.popAt = now;
      var scale = 1 + Math.sin(age * 0.004 + p.phase) * 0.03, op = Math.min(1, age / 400);
      if (p.popAt) {
        var k = (now - p.popAt) / 180;                  // pop: swell and vanish
        scale *= 1 + k * 0.5; op = 1 - k;
        if (k >= 1) gone = true;
      }
      if (gone) { p.el.remove(); live.splice(i, 1); continue; }
      p.el.style.opacity = op;
      p.el.style.transform = "translate3d(" + (p.x - p.size / 2) + "px," + (p.y - p.size / 2) + "px,0) scale(" +
        scale + "," + (2 - scale) + ")";
    }
    if (live.length) requestAnimationFrame(step); else running = false;
  }

  window.blowBubbles = blow;
  document.querySelectorAll(TRIGGERS).forEach(function (el) {
    el.addEventListener("mouseenter", function () { blow(el); });
  });

  // name letters: on phones, tap to show the photo (tap again to hide)
  document.querySelectorAll(".ransom .cut").forEach(function (el) {
    el.addEventListener("click", function () {
      var open = el.classList.toggle("open");
      document.querySelectorAll(".ransom .cut.open").forEach(function (o) { if (o !== el) o.classList.remove("open"); });
      if (open && matchMedia("(hover: none)").matches) blow(el);
    });
  });
})();
