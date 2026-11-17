/* Küçükağa Tarım — ortak site betiği */
(function () {
  "use strict";
  document.documentElement.classList.remove("no-js");

  // Mobil menü
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") { nav.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); }
    });
  }

  // Kaydırınca başlık gölgesi
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () { header.classList.toggle("scrolled", window.scrollY > 8); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // Görünür olunca belirme
  var items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -60px 0px" });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("in"); });
  }

  // Galeri filtreleri
  var filterBar = document.querySelector(".filters");
  if (filterBar) {
    filterBar.addEventListener("click", function (e) {
      var btn = e.target.closest("button");
      if (!btn) return;
      filterBar.querySelectorAll("button").forEach(function (b) { b.classList.toggle("active", b === btn); b.setAttribute("aria-pressed", b === btn ? "true" : "false"); });
      var f = btn.getAttribute("data-filter");
      document.querySelectorAll(".gallery figure").forEach(function (fig) {
        fig.classList.toggle("hide", f !== "hepsi" && fig.getAttribute("data-cat") !== f);
      });
    });
  }

  // Lightbox
  var triggers = Array.prototype.slice.call(document.querySelectorAll("[data-full]"));
  if (triggers.length) {
    var lb = document.createElement("div");
    lb.className = "lightbox";
    lb.setAttribute("role", "dialog");
    lb.setAttribute("aria-modal", "true");
    lb.setAttribute("aria-label", "Fotoğraf görüntüleyici");
    var icon = function (d) { return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + "</svg>"; };
    lb.innerHTML =
      '<figure style="margin:0;max-width:100%;max-height:100%;display:flex"><img alt=""><figcaption></figcaption></figure>' +
      '<button class="lb-btn lb-close" type="button" aria-label="Kapat">' + icon('<path d="M18 6 6 18M6 6l12 12"/>') + "</button>" +
      '<button class="lb-btn lb-prev" type="button" aria-label="Önceki">' + icon('<path d="m15 18-6-6 6-6"/>') + "</button>" +
      '<button class="lb-btn lb-next" type="button" aria-label="Sonraki">' + icon('<path d="m9 18 6-6-6-6"/>') + "</button>";
    document.body.appendChild(lb);
    var img = lb.querySelector("img"), cap = lb.querySelector("figcaption"), idx = 0, last = null;
    var visible = function () { return triggers.filter(function (t) { return t.offsetParent !== null; }); };
    var show = function (i) {
      var list = visible(); if (!list.length) return;
      idx = (i + list.length) % list.length;
      var t = list[idx];
      img.src = t.getAttribute("data-full");
      img.alt = t.getAttribute("data-caption") || "";
      cap.textContent = t.getAttribute("data-caption") || "";
    };
    var open = function (t) { last = t; show(visible().indexOf(t)); lb.classList.add("open"); document.body.style.overflow = "hidden"; lb.querySelector(".lb-close").focus(); };
    var close = function () { lb.classList.remove("open"); document.body.style.overflow = ""; img.src = ""; if (last) last.focus(); };
    triggers.forEach(function (t) {
      if (!t.hasAttribute("tabindex") && t.tagName !== "A" && t.tagName !== "BUTTON") t.setAttribute("tabindex", "0");
      t.setAttribute("role", "button");
      t.addEventListener("click", function (e) { e.preventDefault(); open(t); });
      t.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(t); } });
    });
    lb.querySelector(".lb-close").addEventListener("click", close);
    lb.querySelector(".lb-prev").addEventListener("click", function () { show(idx - 1); });
    lb.querySelector(".lb-next").addEventListener("click", function () { show(idx + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(idx - 1);
      if (e.key === "ArrowRight") show(idx + 1);
    });
  }

  // İletişim formu -> WhatsApp mesajı
  var form = document.getElementById("teklif-formu");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var v = function (n) { var el = form.elements[n]; return el ? el.value.trim() : ""; };
      var lines = [
        "Merhaba, web sitenizden yazıyorum.",
        "Ad Soyad: " + v("ad"),
        v("firma") ? "Firma: " + v("firma") : "",
        v("telefon") ? "Telefon: " + v("telefon") : "",
        v("urun") ? "İlgilendiğim ürün: " + v("urun") : "",
        "",
        v("mesaj")
      ].filter(function (l, i, a) { return l !== "" || (i > 0 && a[i - 1] !== ""); });
      var url = "https://wa.me/905422525226?text=" + encodeURIComponent(lines.join("\n"));
      window.open(url, "_blank", "noopener");
    });
  }

  // Yıl
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
