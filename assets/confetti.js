// Confetti burst from a letter of the name when it's hovered or tapped.
(function () {
  var colors = ["#9b0a0a", "#c4262e", "#eb8d5f", "#29adc0", "#2e3c96", "#f6eee3", "#6a8a4c", "#5a6fd8", "#121212"];
  var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function burst(el) {
    if (still || !document.body.animate) return;
    var r = el.getBoundingClientRect();
    var cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    for (var i = 0; i < 42; i++) {
      var p = document.createElement("span");
      p.className = "confetto";
      var w = 5 + Math.random() * 7, h = Math.random() < 0.5 ? w : w * 0.45;
      p.style.cssText = "left:" + cx + "px;top:" + cy + "px;width:" + w + "px;height:" + h +
        "px;background:" + colors[i % colors.length] + (Math.random() < 0.3 ? ";border-radius:50%" : "");
      document.body.appendChild(p);
      var ang = Math.random() * Math.PI * 2, dist = 70 + Math.random() * 130;
      var dx = Math.cos(ang) * dist, dy = Math.sin(ang) * dist - 60;
      p.animate([
        { transform: "translate(-50%,-50%) rotate(0deg)", opacity: 1 },
        { transform: "translate(" + dx + "px," + dy + "px) rotate(" + (Math.random() * 720 - 360) + "deg)", opacity: 1, offset: 0.6 },
        { transform: "translate(" + dx * 1.1 + "px," + (dy + 120) + "px) rotate(" + (Math.random() * 720) + "deg)", opacity: 0 }
      ], { duration: 1100 + Math.random() * 500, easing: "cubic-bezier(.2,.7,.4,1)" }).onfinish = (function (n) {
        return function () { n.remove(); };
      })(p);
    }
  }

  document.querySelectorAll(".ransom .cut").forEach(function (el) {
    el.addEventListener("mouseenter", function () { burst(el); });
    el.addEventListener("click", function () {           // phones: tap to show, tap again to hide
      var open = el.classList.toggle("open");
      document.querySelectorAll(".ransom .cut.open").forEach(function (o) { if (o !== el) o.classList.remove("open"); });
      if (open) burst(el);
    });
  });
})();
