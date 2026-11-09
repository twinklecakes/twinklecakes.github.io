// Soap bubbles float up from a letter of the name when it's hovered or tapped.
(function () {
  var tints = ["#29adc0", "#5a6fd8", "#eb8d5f", "#c4262e", "#6a8a4c", "#2e3c96"];
  var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function burst(el) {
    if (still || !document.body.animate) return;
    var r = el.getBoundingClientRect();
    for (var i = 0; i < 16; i++) {
      var b = document.createElement("span");
      var size = 10 + Math.random() * 30;
      b.className = "bubble";
      b.style.cssText = "left:" + (r.left + Math.random() * r.width) + "px;top:" + (r.top + r.height * 0.6) +
        "px;width:" + size + "px;height:" + size + "px;--tint:" + tints[i % tints.length];
      document.body.appendChild(b);
      var rise = 90 + Math.random() * 160, drift = (Math.random() - 0.5) * 120, sway = 10 + Math.random() * 18;
      var anim = b.animate([
        { transform: "translate(-50%,-50%) scale(0.3)", opacity: 0 },
        { transform: "translate(calc(-50% + " + sway + "px)," + (-rise * 0.3) + "px) scale(1)", opacity: 1, offset: 0.25 },
        { transform: "translate(calc(-50% - " + sway + "px)," + (-rise * 0.65) + "px) scale(1)", opacity: 1, offset: 0.6 },
        { transform: "translate(calc(-50% + " + drift + "px)," + (-rise * 0.92) + "px) scale(1.05)", opacity: 0.9, offset: 0.9 },
        { transform: "translate(calc(-50% + " + drift + "px)," + (-rise) + "px) scale(1.5)", opacity: 0 }   // pop
      ], { duration: 1400 + Math.random() * 1200, delay: Math.random() * 250, easing: "ease-out", fill: "backwards" });
      anim.onfinish = (function (n) { return function () { n.remove(); }; })(b);
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
