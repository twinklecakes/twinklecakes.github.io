// Click an image in a gallery piece or blog post to see it large.
// Arrow keys / on-screen arrows / swipe to move between images; Esc, the ×,
// or a click on the dark background closes it.
(function () {
  var imgs = Array.prototype.slice.call(document.querySelectorAll(".prose img"));
  var hero = document.querySelector(".jar-hero .jar");      // the big jar at the top of a piece
  var items = imgs.map(function (im) { return { src: im.currentSrc || im.src, alt: im.alt }; });
  if (hero) items.unshift({ src: hero.getAttribute("href"), alt: hero.title });
  if (!items.length) return;

  var box = document.createElement("div");
  box.className = "lightbox";
  box.setAttribute("role", "dialog");
  box.setAttribute("aria-modal", "true");
  box.setAttribute("aria-label", "Enlarged image");
  box.innerHTML =
    '<img class="lb-img" alt="">' +
    '<button class="lb-btn lb-close" type="button" aria-label="Close">×</button>' +
    '<button class="lb-btn lb-prev" type="button" aria-label="Previous image">‹</button>' +
    '<button class="lb-btn lb-next" type="button" aria-label="Next image">›</button>' +
    '<span class="lb-count"></span>';
  document.body.appendChild(box);
  var big = box.querySelector(".lb-img"), count = box.querySelector(".lb-count");
  var at = 0, lastFocus = null;

  function show(i) {
    at = (i + items.length) % items.length;
    big.src = items[at].src;
    big.alt = items[at].alt || "";
    count.textContent = items.length > 1 ? (at + 1) + " / " + items.length : "";
    // preload the neighbours so stepping through is instant
    [at + 1, at - 1].forEach(function (j) { new Image().src = items[(j + items.length) % items.length].src; });
  }
  function open(i) {
    lastFocus = document.activeElement;
    show(i);
    box.classList.add("on");
    box.classList.toggle("single", items.length < 2);
    document.documentElement.classList.add("lb-open");
    box.querySelector(".lb-close").focus();
  }
  function close() {
    box.classList.remove("on");
    document.documentElement.classList.remove("lb-open");
    if (lastFocus) lastFocus.focus();
  }

  imgs.forEach(function (im, i) {
    im.classList.add("zoomable");
    im.addEventListener("click", function () { open(hero ? i + 1 : i); });
  });
  if (hero) hero.addEventListener("click", function (e) { e.preventDefault(); open(0); });

  box.querySelector(".lb-close").addEventListener("click", close);
  box.querySelector(".lb-prev").addEventListener("click", function (e) { e.stopPropagation(); show(at - 1); });
  box.querySelector(".lb-next").addEventListener("click", function (e) { e.stopPropagation(); show(at + 1); });
  box.addEventListener("click", function (e) { if (e.target === box) close(); });
  big.addEventListener("click", function (e) { e.stopPropagation(); if (items.length > 1) show(at + 1); });
  document.addEventListener("keydown", function (e) {
    if (!box.classList.contains("on")) return;
    if (e.key === "Escape") close();
    else if (e.key === "ArrowRight") show(at + 1);
    else if (e.key === "ArrowLeft") show(at - 1);
  });

  // swipe on phones
  var x0 = null;
  box.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  box.addEventListener("touchend", function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 45) show(at + (dx < 0 ? 1 : -1));
    x0 = null;
  });
})();
