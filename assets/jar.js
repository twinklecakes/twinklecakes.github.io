// Redraws each jar photo onto a canvas, warped like it's seen through
// curved glass: the middle is magnified, the sides squeeze, and the
// middle of each column swells a little. If this script fails, the
// plain photo still shows.
(function () {
  var STRENGTH = 0.55; // 0 = flat, 1 = very strong
  var SWELL = 0.07;    // how much taller the middle looks than the edges

  function warp(img) {
    var box = img.parentElement;
    var W = Math.round(box.clientWidth * 2), H = Math.round(box.clientHeight * 2);
    if (!W || !H || !img.naturalWidth) return;

    // cover-fit the photo into the jar
    var iw = img.naturalWidth, ih = img.naturalHeight;
    var scale = Math.max(W / iw, H / ih);
    var sw = W / scale, sh = H / scale;
    var sx0 = (iw - sw) / 2, sy0 = (ih - sh) / 2;

    var c = document.createElement("canvas");
    c.width = W; c.height = H;
    c.className = "jar-photo jar-canvas";
    c.setAttribute("role", "img");
    c.setAttribute("aria-label", img.alt);
    var g = c.getContext("2d");

    for (var x = 0; x < W; x++) {
      var u = (2 * (x + 0.5)) / W - 1;                 // -1 .. 1 across the jar
      var bent = (2 / Math.PI) * Math.asin(u);          // cylinder lens
      var us = u + (bent - u) * STRENGTH;
      var srcX = sx0 + ((us + 1) / 2) * sw;
      var swell = 1 + SWELL * Math.cos((u * Math.PI) / 2);
      var colH = sh / swell;
      g.drawImage(img, srcX, sy0 + (sh - colH) / 2, Math.max(sw / W, 1), colH, x, 0, 1, H);
    }
    img.replaceWith(c);
  }

  function run(img) {
    if (img.complete && img.naturalWidth) warp(img);
    else img.addEventListener("load", function () { warp(img); }, { once: true });
  }

  document.querySelectorAll("img.jar-photo").forEach(run);
})();
