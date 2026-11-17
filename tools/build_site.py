#!/usr/bin/env python3
"""Küçükağa Tarım sitesinin HTML sayfalarını üretir.

Kullanım:  python3 tools/build_site.py
Ortak başlık, alt bilgi ve iletişim bilgileri bu dosyadan tüm sayfalara yazılır.
Bu klasör (tools/) hosting'e yüklenmez.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://kucukagatarim.com"
VERSION = "20261117"

# ---------------------------------------------------------------- bilgiler
WA = "905422525226"
WA_URL = f"https://wa.me/{WA}"
PHONES = [
    ("+90 542 252 52 26", "+905422525226", "Yetkili · WhatsApp"),
    ("+90 542 537 61 07", "+905425376107", "Yetkili"),
    ("+90 552 738 63 81", "+905527386381", "Muhasebe"),
]
EMAILS = [("info@kucukagatarim.com", "Genel bilgi"), ("muhasebe@kucukagatarim.com", "Muhasebe")]
INSTAGRAM = "https://www.instagram.com/kucuk_aga_tarim.aydin?igsh=cGRrMXJ0emNpb3h1"
FACEBOOK = "https://www.facebook.com/share/18U8bR2U88/"
BRANCHES = [
    ("Aydın Şubesi", "Acarlar Adnan Menderes Toptancı Hali No: 41-46", "İncirliova, Aydın",
     "Acarlar Adnan Menderes Toptancı Hali İncirliova Aydın"),
    ("Kaş Şubesi", "Çavdır Mahallesi Merkez Sokak No: 58/2", "Kaş, Antalya",
     "Çavdır Mahallesi Merkez Sokak Kaş Antalya"),
    ("Burdur Şubesi", "Çavdır Toptancı Sebze Meyve Hali B Blok No: 6", "Çavdır, Burdur",
     "Çavdır Toptancı Sebze Meyve Hali Çavdır Burdur"),
    ("Elmalı Şubesi", "Elmalı Yuva Mahallesi, Hoppa Oğlu Kantarı", "Elmalı, Antalya",
     "Yuva Mahallesi Elmalı Antalya"),
]

NAV = [
    ("index.html", "Ana Sayfa"),
    ("urunler.html", "Ürünler"),
    ("hizmetler.html", "Hizmetler"),
    ("neden-biz.html", "Neden Biz"),
    ("galeri.html", "Galeri"),
    ("hakkimizda.html", "Hakkımızda"),
    ("iletisim.html", "İletişim"),
]

PRODUCTS = [
    ("salkim-domates", "Salkım Domates", "Sera",
     "Salkımıyla birlikte, dalında tam olgunlaşarak hasat edilir. Yoğun aroması ve canlı rengiyle hem sofrada hem tezgâhta öne çıkar."),
    ("verty-domates", "Verty Kokteyl Domates", "Sera",
     "Küçük boyu ve tatlı lezzetiyle salata, kahvaltı ve sunumlar için ideal. Dalında olgunlaşır, aromasını korur."),
    ("kemer-patlican", "Kemer Patlıcan", "Sebze",
     "İnce, uzun ve parlak kabuklu. Közleme, kızartma ve dolma için tercih edilen yöresel bir lezzet."),
    ("bif-domates", "Bif Domates", "Sera",
     "İri ve etli yapısıyla dilimlemeye uygun; salata, sandviç ve restoran mutfakları için güçlü bir seçenek."),
    ("sivri-biber", "Sivri Biber", "Sebze",
     "İnce kabuklu, taze ve diri. Kızartma, kahvaltı ve salatalar için günlük hasat."),
    ("tane-domates", "Tane Domates", "Sera",
     "Sofralık, tane tane seçilmiş domates. Günlük mutfak kullanımı ve toptan siparişler için düzenli tedarik."),
]

# (dosya, açıklama, kategori)
GALLERY = [
    ("salkim-domates", "Salkım domates hasadı", "domates"),
    ("hasat-2", "Dalında olgunlaşan domatesler", "sera"),
    ("bif-domates", "Kasada bif domates", "domates"),
    ("sera-7", "Seradan salkım domates", "sera"),
    ("sivri-biber", "Taze sivri biber", "sebze"),
    ("verty-domates", "Verty kokteyl domates", "domates"),
    ("sera-2", "Sera üretimi", "sera"),
    ("kemer-patlican", "Kemer patlıcan", "sebze"),
    ("cavdir-kasa", "Çavdır kasalarında sevkiyata hazır ürün", "sevkiyat"),
    ("sera-4", "Salkım domates, sera", "sera"),
    ("tane-domates", "Tane domates", "domates"),
    ("patlican-sera", "Dalında patlıcan", "sebze"),
    ("salkim-kasa", "Kasalanmış salkım domates", "sevkiyat"),
    ("sera-1", "Sera domatesi yakın çekim", "sera"),
    ("hasat-1", "Hasat sonrası kasalama", "sevkiyat"),
    ("bif-domates-3", "Bif domates", "domates"),
    ("sera-3", "Seradan taze hasat", "sera"),
    ("salkim-kasa-2", "Salkım domates kasaları", "sevkiyat"),
    ("sera-6", "Kasada salkım domates", "sevkiyat"),
    ("tane-domates-detay", "Kasalar ve ürün detayı", "sevkiyat"),
    ("sera-5", "Salkım domates", "sera"),
]
CATS = [("hepsi", "Tümü"), ("domates", "Domates"), ("sebze", "Biber & Patlıcan"), ("sera", "Sera"), ("sevkiyat", "Kasa & Sevkiyat")]

# ---------------------------------------------------------------- ikonlar
def ic(path, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>')

I = {
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<circle cx="12" cy="12" r="10"/><path d="m8 12 3 3 5-6"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10Z"/><path d="M2 21c0-3 1.9-5.4 5.1-6C9.5 14.5 12 13 13 12"/>',
    "sprout": '<path d="M7 20h10M10 20c5.5-2.5.8-6.4 3-10"/><path d="M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4 0 5.5.8Z"/><path d="M14.1 6a7 7 0 0 0-1.1 4c1.9-.1 3.3-.6 4.3-1.4 1-1 1.6-2.3 1.7-4.6-2.7.1-4 1-4.9 2Z"/>',
    "truck": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.6a1 1 0 0 0-.2-.6l-3.5-4.4A1 1 0 0 0 17.5 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
    "box": '<path d="M21 8a2 2 0 0 0-1-1.7l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.7l7 4a2 2 0 0 0 2 0l7-4a2 2 0 0 0 1-1.7Z"/><path d="m3.3 7 8.7 5 8.7-5M12 22V12"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.7 9a1 1 0 0 1-.6 0C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.2-2.7a1.2 1.2 0 0 1 1.6 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1Z"/><path d="m9 12 2 2 4-4"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    "chat": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "tag": '<path d="M12.6 2.6A2 2 0 0 0 11.2 2H4a2 2 0 0 0-2 2v7.2a2 2 0 0 0 .6 1.4l8.7 8.7a2.4 2.4 0 0 0 3.4 0l6.6-6.6a2.4 2.4 0 0 0 0-3.4Z"/><circle cx="7.5" cy="7.5" r=".5" fill="currentColor"/>',
    "snow": '<path d="M2 12h20M12 2v20m8-16-16 12m16 0L4 6"/>',
    "award": '<circle cx="12" cy="8" r="6"/><path d="M15.5 12.9 17 22l-5-3-5 3 1.5-9.1"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "map": '<path d="M14.1 4.6 9.9 2.4a2 2 0 0 0-1.8 0L3.6 4.7A1 1 0 0 0 3 5.6v14.8a1 1 0 0 0 1.4.9l3.7-1.9a2 2 0 0 1 1.8 0l4.2 2.2a2 2 0 0 0 1.8 0l4.5-2.3a1 1 0 0 0 .6-.9V3.6a1 1 0 0 0-1.4-.9l-3.7 1.9a2 2 0 0 1-1.8 0ZM15 5v16M9 3v16"/>',
}
WA_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3Z"/>'
          '<path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.1-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-3-.2-.3A8.2 8.2 0 1 1 12 20.2Z"/></svg>')
IG_SVG = ic('<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".6" fill="currentColor"/>')
FB_SVG = ic('<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>')


def e(s):
    return html.escape(s, quote=True)


def img(name, alt, sm=True, cls="", eager=False, w=None, h=None, extra=""):
    src = f"assets/img/{name}-sm.jpg" if sm else f"assets/img/{name}.jpg"
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    dims = f' width="{w}" height="{h}"' if w and h else ""
    return f'<img src="{src}" alt="{e(alt)}"{c}{dims} {loading}{extra}>'


def full(name):
    return f"assets/img/{name}.jpg"


# ---------------------------------------------------------------- şablon
def head(page, title, desc, og_image="assets/img/salkim-domates.jpg", extra_ld=None):
    url = SITE + "/" + ("" if page == "index.html" else page)
    ld = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Küçükağa Tarım",
        "legalName": "Küçükağa Tarım Ürünleri Gıda İnşaat İthalat İhracat Sanayi ve Ticaret Ltd. Şti.",
        "url": SITE + "/",
        "logo": SITE + "/assets/img/logo.jpg",
        "email": "info@kucukagatarim.com",
        "foundingDate": "2001",
        "sameAs": [INSTAGRAM, FACEBOOK],
        "contactPoint": [{"@type": "ContactPoint", "telephone": "+90-542-252-52-26", "contactType": "customer service",
                          "areaServed": "TR", "availableLanguage": "Turkish"}],
        "address": {"@type": "PostalAddress", "streetAddress": "Acarlar Adnan Menderes Toptancı Hali No: 41-46",
                    "addressLocality": "İncirliova", "addressRegion": "Aydın", "addressCountry": "TR"},
    }
    lds = [ld] + (extra_ld or [])
    ld_html = "\n".join(f'  <script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    return f"""<!doctype html>
<html lang="tr" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="tr_TR">
  <meta property="og:site_name" content="Küçükağa Tarım">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/{og_image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#123d26">
  <link rel="icon" href="logo.ico" sizes="any">
  <link rel="icon" href="assets/img/icon-192.png" type="image/png">
  <link rel="apple-touch-icon" href="assets/img/icon-180.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap">
  <link rel="stylesheet" href="assets/css/site.css?v={VERSION}">
{ld_html}
</head>
<body>
<a class="skip" href="#icerik">İçeriğe geç</a>
"""


def header(page):
    links = "\n".join(
        f'      <a href="{href}"{" aria-current=\"page\"" if href == page else ""}>{label}</a>' for href, label in NAV)
    return f"""<div class="topbar">
  <div class="wrap">
    <div class="topbar-items">
      <a href="tel:{PHONES[0][1]}">{ic(I['phone'])}{PHONES[0][0]}</a>
      <a class="topbar-hide-sm" href="mailto:{EMAILS[0][0]}">{ic(I['mail'])}{EMAILS[0][0]}</a>
      <span class="topbar-hide-sm">{ic(I['pin'])}Aydın · Antalya · Burdur</span>
    </div>
    <div class="topbar-social">
      <a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram">{IG_SVG}</a>
      <a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook">{FB_SVG}</a>
    </div>
  </div>
</div>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Küçükağa Tarım ana sayfa">
      <img src="assets/img/logo-sm.jpg" alt="" width="52" height="52">
      <span><span class="brand-name">Küçükağa Tarım</span><span class="brand-sub">Tarladan Sofraya</span></span>
    </a>
    <button class="menu-toggle" type="button" aria-label="Menüyü aç" aria-expanded="false" aria-controls="site-nav">{ic(I['menu'])}</button>
    <nav class="nav" id="site-nav" aria-label="Ana menü">
{links}
      <a class="btn btn-primary header-cta" href="{WA_URL}" target="_blank" rel="noopener">{WA_SVG}Teklif Alın</a>
    </nav>
  </div>
</header>
<main id="icerik">
"""


def footer():
    nav = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in NAV)
    prods = "".join(f'<li><a href="urunler.html#{slug}">{name}</a></li>' for slug, name, *_ in PRODUCTS)
    phones = "".join(f'<li>{ic(I["phone"])}<span><a href="tel:{t}">{p}</a><br><small>{n}</small></span></li>' for p, t, n in PHONES)
    return f"""</main>
<footer class="site-footer">
  <div class="wrap footer-main">
    <div class="footer-brand">
      <a class="brand" href="index.html">
        <img src="assets/img/logo-sm.jpg" alt="" width="52" height="52" loading="lazy">
        <span><span class="brand-name">Küçükağa Tarım</span><span class="brand-sub">Tarladan Sofraya</span></span>
      </a>
      <p>30 yılı aşkın tarım tecrübesiyle yaş sebze ve meyvede üretim, toptan tedarik ve sevkiyat. 2001'den beri kurumsal.</p>
      <div class="social">
        <a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram">{IG_SVG}</a>
        <a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook">{FB_SVG}</a>
        <a href="{WA_URL}" target="_blank" rel="noopener" aria-label="WhatsApp">{WA_SVG}</a>
      </div>
    </div>
    <div>
      <h4>Sayfalar</h4>
      <ul>{nav}</ul>
    </div>
    <div>
      <h4>Ürünler</h4>
      <ul>{prods}</ul>
    </div>
    <div>
      <h4>İletişim</h4>
      <ul class="footer-contact">
        {phones}
        <li>{ic(I["mail"])}<a href="mailto:{EMAILS[0][0]}">{EMAILS[0][0]}</a></li>
        <li>{ic(I["pin"])}<span>Acarlar Adnan Menderes Toptancı Hali No: 41-46, İncirliova / Aydın</span></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="wrap">
      <span>© <span data-year>2026</span> Küçükağa Tarım Ürünleri. Tüm hakları saklıdır.</span>
      <span>Küçükağa Tarım ve Çavdır Fresh tescilli markalardır.</span>
    </div>
  </div>
</footer>
<a class="wa-float" href="{WA_URL}" target="_blank" rel="noopener" aria-label="WhatsApp ile yazın">{WA_SVG}</a>
<script src="assets/js/site.js?v={VERSION}" defer></script>
</body>
</html>
"""


def page_hero(title, text, crumb):
    return f"""<section class="page-hero">
  <div class="wrap">
    <nav class="breadcrumb" aria-label="Konum"><a href="index.html">Ana Sayfa</a><span aria-hidden="true">/</span><span>{crumb}</span></nav>
    <h1>{title}</h1>
    <p>{text}</p>
  </div>
</section>
"""


def cta_band(title="Toptan sipariş ve fiyat bilgisi için bize ulaşın",
             text="Ürün, miktar ve teslimat yerini yazın; size en kısa sürede dönüş yapalım."):
    return f"""<section class="section-sm">
  <div class="wrap">
    <div class="cta-band reveal">
      <div>
        <h2>{title}</h2>
        <p>{text}</p>
      </div>
      <div class="hero-actions">
        <a class="btn btn-primary" href="{WA_URL}" target="_blank" rel="noopener">{WA_SVG}WhatsApp'tan Yazın</a>
        <a class="btn btn-ghost" href="tel:{PHONES[0][1]}">{ic(I['phone'])}Hemen Arayın</a>
      </div>
    </div>
  </div>
</section>
"""


def product_cards(items, link_to_page):
    out = []
    for slug, name, tag, text in items:
        link = (f'<a class="product-link" href="urunler.html#{slug}">Detaylar {ic(I["arrow"])}</a>' if link_to_page else
                f'<a class="product-link" href="{WA_URL}?text={e(name + " için fiyat bilgisi almak istiyorum.").replace(" ", "%20")}" target="_blank" rel="noopener">Fiyat sorun {ic(I["arrow"])}</a>')
        out.append(f"""      <article class="product reveal" id="{slug}">
        <div class="product-img" data-full="{full(slug)}" data-caption="{e(name)}">
          {img(slug, name, w=720, h=960)}
          <span class="tag">{tag}</span>
        </div>
        <div class="product-body">
          <h3>{name}</h3>
          <div class="product-meta"><span class="chip">Dalından taze</span><span class="chip">Toptan</span></div>
          <p>{text}</p>
          {link}
        </div>
      </article>""")
    return "\n".join(out)


def features(items, cols=3):
    out = []
    for icon, title, text, *rest in items:
        red = " red" if rest and rest[0] else ""
        out.append(f"""      <div class="feature reveal">
        <div class="icon{red}">{ic(I[icon])}</div>
        <h3>{title}</h3>
        <p>{text}</p>
      </div>""")
    return f'<div class="grid grid-{cols}">\n' + "\n".join(out) + "\n    </div>"


WHY = [
    ("sprout", "Doğal Sera Üretimi", "Kontrollü ortamda doğal yöntemlerle üretilen ürünlerimiz hem canlı hem de sağlıklı bir lezzet sunar."),
    ("calendar", "Günlük Hasat", "Günlük hasat edilen ürünlerimiz 24 saat içinde sofranızda. Tazelik garantili.", True),
    ("tag", "Toptan Fiyatlandırma", "Yüksek miktarlı siparişlerde özel fiyatlar ve hızlı sevkiyat sunuyoruz."),
    ("truck", "Güvenilir Teslimat", "Ürünlerimiz koruma altında, uygun şekilde ambalajlanarak teslim edilir."),
    ("users", "Aile İşletmesi", "Kuşaktan kuşağa devam eden aile işletmemizde her ürüne özenle bakılır."),
    ("chat", "7/24 İletişim", "WhatsApp üzerinden 7/24 ulaşabilir, sorularınıza hızlı yanıt alabilirsiniz.", True),
]

STATS = """<section class="stats" aria-label="Rakamlarla Küçükağa Tarım">
  <div class="wrap">
    <div class="stat"><strong>30+</strong><span>Yıllık tarım tecrübesi</span></div>
    <div class="stat"><strong>2001</strong><span>Kurumsal yapı</span></div>
    <div class="stat"><strong>4</strong><span>Şube: Aydın, Kaş, Burdur, Elmalı</span></div>
    <div class="stat"><strong>2</strong><span>Tescilli marka</span></div>
  </div>
</section>
"""


def brands_section():
    return f"""<section class="section section-sand">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Markalarımız</span>
      <h2>Tescilli markalarla güvenilir tedarik</h2>
      <p>Ürünlerimizi Türk Patent ve Marka Kurumu tescilli Küçükağa Tarım ve Çavdır Fresh markalarıyla sunuyoruz.</p>
    </div>
    <div class="brands">
      <div class="brand-card reveal">
        {img("logo", "Küçükağa Tarım logosu", w=128, h=128)}
        <h3>Küçükağa Tarım</h3>
        <p>Aydın merkezli üretim, toptan tedarik ve sevkiyat.</p>
      </div>
      <div class="brand-card reveal">
        {img("cavdir-fresh-logo", "Çavdır Fresh logosu", w=128, h=128)}
        <h3>Çavdır Fresh</h3>
        <p>Çavdır ve Elmalı bölgesinden taze ürün markamız.</p>
      </div>
      <div class="brand-card doc reveal">
        <span data-full="{full('marka-tescil-belgesi')}" data-caption="Türk Patent marka tescil belgesi">{img("marka-tescil-belgesi", "Türk Patent marka tescil belgesi", w=490, h=720)}</span>
        <h3>Marka Tescil Belgesi</h3>
        <p>Türk Patent ve Marka Kurumu, tescil no: 2022 189003.</p>
      </div>
    </div>
  </div>
</section>
"""


# ---------------------------------------------------------------- sayfalar
def page_index():
    p = "index.html"
    strip_items = ["sera-7", "bif-domates", "sivri-biber", "sera-2", "verty-domates", "cavdir-kasa", "kemer-patlican", "sera-4", "salkim-kasa", "tane-domates"]
    strip = "\n".join(
        f'      <a href="{full(n)}" data-full="{full(n)}" data-caption="{e(c)}">{img(n, c, w=360, h=360)}</a>'
        for n, c, _ in [g for g in GALLERY if g[0] in strip_items])
    body = f"""<section class="hero">
  <div class="wrap">
    <div class="hero-inner">
      <span class="eyebrow">Aydın · Antalya · Burdur</span>
      <h1>Tarladan sofraya <em>taze</em> ve güvenilir tedarik</h1>
      <p class="lead">Küçükağa Tarım; salkım, bif ve kokteyl domatesten biber ve patlıcana kadar yöresel sera ürünlerini dalında olgunlaştırır, toptan olarak Türkiye'nin her yerine ulaştırır.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="urunler.html">Ürünlerimizi İnceleyin {ic(I['arrow'])}</a>
        <a class="btn btn-ghost" href="{WA_URL}" target="_blank" rel="noopener">{WA_SVG}Teklif Alın</a>
      </div>
      <div class="hero-badges">
        <div>{ic(I['award'])}30+ yıllık tecrübe</div>
        <div>{ic(I['snow'])}Soğuk hava depolama</div>
        <div>{ic(I['truck'])}Türkiye geneli sevkiyat</div>
      </div>
    </div>
    <div class="hero-media" aria-hidden="true">
      <img class="m1" src="assets/img/hasat-2.jpg" alt="" fetchpriority="high">
      <img class="m2" src="assets/img/bif-domates-sm.jpg" alt="">
      <img class="seal" src="assets/img/logo-sm.jpg" alt="">
    </div>
  </div>
</section>
{STATS}
<section class="section">
  <div class="wrap split">
    <div class="split-media reveal">
      {img("sera-4", "Serada dalında olgunlaşan salkım domatesler", w=720, h=1280)}
      <div class="media-card">
        {img("cavdir-fresh-logo", "Çavdır Fresh", w=54, h=54)}
        <div><strong>Çavdır Fresh</strong><span>Tescilli markamız</span></div>
      </div>
    </div>
    <div class="split-body reveal">
      <span class="eyebrow">Kaliteli üretim, güvenilir tedarik</span>
      <h2>Hasattan teslimata kadar her adım bizde</h2>
      <p>Türkiye'nin en verimli tarım bölgelerinde hasadını yaptığımız ürünleri modern soğuk hava depolama sistemleriyle saklıyor, maksimum tazelikle teslim ediyoruz.</p>
      <p>Doğrudan çiftçiden alım yaparak ürün kalitesini ve müşteri memnuniyetini en uygun fiyatlarla sunuyoruz.</p>
      <ul class="checks">
        <li>{ic(I['check'])}Dalında olgunlaşan ürün</li>
        <li>{ic(I['check'])}Doğrudan çiftçiden alım</li>
        <li>{ic(I['check'])}Soğuk hava depolama</li>
        <li>{ic(I['check'])}Geniş araç filosu</li>
      </ul>
      <a class="btn btn-green" href="hakkimizda.html">Bizi Tanıyın {ic(I['arrow'])}</a>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Ürünlerimiz</span>
      <h2>Seradan ve tarladan taze ürünler</h2>
      <p>Dalında tam olgunlaşarak hasat edilen ürünlerimizi toptan olarak tedarik ediyoruz.</p>
    </div>
    <div class="grid grid-3">
{product_cards(PRODUCTS[:3], True)}
    </div>
    <div class="section-foot"><a class="btn btn-outline" href="urunler.html">Tüm Ürünler {ic(I['arrow'])}</a></div>
  </div>
</section>

<section class="section section-dark">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Neden Küçükağa?</span>
      <h2>Kalite, lezzet ve güvenilirlik</h2>
      <p>Üretimden teslimata kadar her aşamayı titizlikle yönetiyoruz.</p>
    </div>
    {features(WHY)}
  </div>
</section>

{brands_section()}
<section class="section">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Galeri</span>
      <h2>Seradan ve hasattan kareler</h2>
    </div>
    <div class="strip reveal">
{strip}
    </div>
    <div class="section-foot"><a class="btn btn-outline" href="galeri.html">Galeriyi Gör {ic(I['arrow'])}</a></div>
  </div>
</section>
{cta_band()}"""
    return (head(p, "Küçükağa Tarım | Taze Domates & Sera Ürünleri – Toptan Tedarik",
                 "Küçükağa Tarım: salkım, bif ve kokteyl domates, sivri biber ve kemer patlıcan. 30+ yıllık tecrübe, soğuk hava depolama ve Türkiye geneli toptan sevkiyat.",
                 "assets/img/hasat-2.jpg")
            + header(p) + body + footer())


def page_urunler():
    p = "urunler.html"
    items = [{"@type": "Product", "name": n, "description": t, "image": f"{SITE}/{full(s)}",
              "brand": {"@type": "Brand", "name": "Küçükağa Tarım"}} for s, n, _, t in PRODUCTS]
    ld = [{"@context": "https://schema.org", "@type": "ItemList",
           "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": it} for i, it in enumerate(items)]}]
    body = page_hero("Ürünlerimiz",
                     "Tarladan ve seradan seçilen, dalında olgunlaşan yöresel sebze ve meyveler. Tüm ürünlerimiz toptan olarak tedarik edilir.",
                     "Ürünler") + f"""<section class="section">
  <div class="wrap">
    <div class="grid grid-3">
{product_cards(PRODUCTS, False)}
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Toptan sipariş</span>
      <h2>Nasıl sipariş verilir?</h2>
      <p>Siparişinizi üç adımda tamamlıyoruz.</p>
    </div>
    {features([
        ("chat", "1. Bize yazın", "WhatsApp veya telefonla ürün, miktar ve teslimat yerini iletin."),
        ("tag", "2. Fiyat ve tarih", "Güncel fiyat ve sevkiyat tarihini size hemen bildirelim.", True),
        ("truck", "3. Sevkiyat", "Ürünleriniz kasalanıp araç filomuzla adresinize ulaştırılır."),
    ])}
  </div>
</section>
{cta_band("Aradığınız ürünü bulamadınız mı?", "Sezona göre ürün çeşitliliğimiz değişir. Güncel ürün listesi için bize ulaşın.")}"""
    return (head(p, "Ürünlerimiz | Salkım, Bif ve Kokteyl Domates, Biber, Patlıcan – Küçükağa Tarım",
                 "Salkım domates, verty kokteyl domates, bif domates, tane domates, sivri biber ve kemer patlıcan. Dalından taze, toptan tedarik.",
                 "assets/img/salkim-domates.jpg", ld)
            + header(p) + body + footer())


def page_hizmetler():
    p = "hizmetler.html"
    services = [
        ("sera-2", "Sera Üretimi", "Modern sera sistemleri ve tarım teknolojileriyle en kaliteli ürünleri üretiyoruz. Ürünlerimiz dalında tam olgunlaşarak hasat edilir.",
         ["Kontrollü sera ortamı", "Dalında olgunlaşma", "Titiz hasat süreci"]),
        ("salkim-kasa", "Toptan Meyve & Sebze Tedariki", "Tarladan doğrudan toptan fiyatlarla kaliteli sebze ve meyve tedarik ediyoruz. Doğrudan çiftçiden alım yaparak en uygun fiyatı sunuyoruz.",
         ["Doğrudan çiftçiden alım", "Toptan fiyatlandırma", "Geniş ürün çeşitliliği"]),
        ("cavdir-kasa", "Depolama & Kalite Kontrol", "Her adımda kaliteyi kontrol ediyor, modern soğuk hava depolama sistemleriyle ürünlerin tazeliğini koruyoruz.",
         ["Soğuk hava depolama", "Kalite kontrol", "Uygun ambalajlama"]),
        ("hasat-1", "Lojistik & Sevkiyat", "Geniş araç filomuz ve deneyimli ekibimizle Türkiye'nin dört bir yanına güvenli ve hızlı sevkiyat sağlıyoruz.",
         ["Geniş araç filosu", "Zamanında teslimat", "Türkiye geneli dağıtım"]),
    ]
    rows = []
    for i, (im, t, txt, lst) in enumerate(services, 1):
        li = "".join(f"<li>{ic(I['check'])}{x}</li>" for x in lst)
        rows.append(f"""    <div class="service reveal">
      <div class="service-media">{img(im, t, w=720, h=1280)}</div>
      <div>
        <span class="service-num">0{i}</span>
        <h2>{t}</h2>
        <p>{txt}</p>
        <ul class="checks" style="grid-template-columns:1fr">{li}</ul>
      </div>
    </div>""")
    body = page_hero("Hizmetlerimiz",
                     "Üretimden depolamaya, toptan satıştan sevkiyata kadar tüm süreci tek elden yönetiyoruz.",
                     "Hizmetler") + f"""<section class="section">
  <div class="wrap">
{chr(10).join(rows)}
  </div>
</section>
{cta_band("Firmanız için düzenli tedarik mi arıyorsunuz?", "Hal, market, restoran ve toptancılar için düzenli ürün tedariki sağlıyoruz.")}"""
    return (head(p, "Hizmetlerimiz | Sera Üretimi, Toptan Tedarik ve Sevkiyat – Küçükağa Tarım",
                 "Sera üretimi, toptan meyve ve sebze tedariki, soğuk hava depolama ve Türkiye geneli sevkiyat hizmetleri.",
                 "assets/img/sera-2.jpg")
            + header(p) + body + footer())


def page_neden():
    p = "neden-biz.html"
    body = page_hero("Neden Küçükağa?", "Kalite, lezzet ve güvenilirlik için bize güvenin.", "Neden Biz") + f"""<section class="section">
  <div class="wrap">
    {features(WHY)}
  </div>
</section>
{STATS}
<section class="section section-alt">
  <div class="wrap split reverse">
    <div class="split-media reveal">{img("sera-7", "Seradan salkım domates", w=720, h=1280)}</div>
    <div class="split-body reveal">
      <span class="eyebrow">Çalışma anlayışımız</span>
      <h2>Planlı, sürdürülebilir ve güvenilir</h2>
      <p>Tarladan depolama, sevkiyat ve teslimata kadar tüm süreci titizlikle yönetiyoruz. Farklı sektörlerin ve ölçeklerin ihtiyaçlarını zamanında ve sorunsuz teslimat anlayışıyla karşılıyoruz.</p>
      <ul class="checks">
        <li>{ic(I['check'])}Yerel ve ulusal ölçekte hizmet</li>
        <li>{ic(I['check'])}Deneyimli ekip</li>
        <li>{ic(I['check'])}Tescilli markalar</li>
        <li>{ic(I['check'])}4 şubeyle yakın hizmet</li>
      </ul>
      <a class="btn btn-green" href="iletisim.html">İletişime Geçin {ic(I['arrow'])}</a>
    </div>
  </div>
</section>
{cta_band()}"""
    return (head(p, "Neden Küçükağa Tarım? | Doğal Üretim, Günlük Hasat, Güvenilir Teslimat",
                 "Doğal sera üretimi, günlük hasat, toptan fiyatlandırma, güvenilir teslimat ve 7/24 WhatsApp iletişim. Kuşaktan kuşağa aile işletmesi.",
                 "assets/img/sera-7.jpg")
            + header(p) + body + footer())


def page_galeri():
    p = "galeri.html"
    filters = "".join(
        f'<button type="button" data-filter="{k}" aria-pressed="{"true" if k == "hepsi" else "false"}"{" class=\"active\"" if k == "hepsi" else ""}>{v}</button>'
        for k, v in CATS)
    figs = "\n".join(
        f'      <figure data-cat="{cat}" data-full="{full(n)}" data-caption="{e(c)}">{img(n, c)}<figcaption>{c}</figcaption></figure>'
        for n, c, cat in GALLERY)
    body = page_hero("Hasat Galerisi",
                     "Tarlalarımızdan ve seralarımızdan gerçek anlar: canlı, doğal ve yöresel ürünler.",
                     "Galeri") + f"""<section class="section">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Galeri filtresi">{filters}</div>
    <div class="gallery">
{figs}
    </div>
  </div>
</section>
{cta_band()}"""
    return (head(p, "Galeri | Seradan ve Hasattan Fotoğraflar – Küçükağa Tarım",
                 "Küçükağa Tarım seralarından ve hasadından fotoğraflar: salkım domates, bif domates, biber, patlıcan ve sevkiyat.",
                 "assets/img/sera-4.jpg")
            + header(p) + body + footer())


def page_hakkimizda():
    p = "hakkimizda.html"
    body = page_hero("Hakkımızda",
                     "30 yılı aşkın tarım tecrübesiyle yaş sebze ve meyvede güvenilir çözüm ortağınız.",
                     "Hakkımızda") + f"""<section class="section">
  <div class="wrap split">
    <div class="split-media reveal">
      {img("sera-1", "Küçükağa Tarım serasından domates", w=720, h=1280)}
      <div class="media-card">
        {img("logo", "Küçükağa Tarım", w=54, h=54)}
        <div><strong>2001'den beri</strong><span>Kurumsal yapı</span></div>
      </div>
    </div>
    <div class="split-body reveal">
      <span class="eyebrow">Hikâyemiz</span>
      <h2>Tarladan doğan, güçlü bir tedarik organizasyonu</h2>
      <p>Küçükağa Tarım, 30 yılı aşkın tarım tecrübesiyle temelleri atılan bir işletme olarak yaş sebze ve meyve üretiminden doğmuş; yıllar içinde güçlü bir tedarik ve lojistik organizasyonuna dönüşmüştür. 2001 itibarıyla kurumsal kimlik kazanarak planlı, sürdürülebilir ve güvenilir bir operasyon modeliyle çalışmaktayız.</p>
      <p>Tarladan depolama, sevkiyat ve teslimata kadar tüm süreci titizlikle yönetiyoruz. Geniş araç filomuz ve deneyimli ekibimiz sayesinde farklı sektörlerin ve ölçeklerin ihtiyaçlarını zamanında karşılayarak yerel ve ulusal ölçekte güvenilir bir çözüm ortağı olmayı hedefliyoruz.</p>
      <p>Doğal üretim yöntemlerimiz, modern sera teknolojileri ve titiz hasat sürecimiz her ürünün yüksek kalite standartlarını karşılamasını sağlar.</p>
    </div>
  </div>
</section>
{STATS}
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Değerlerimiz</span>
      <h2>Bizi biz yapanlar</h2>
    </div>
    {features([
        ("award", "30+ Yıl Deneyim", "Köklü bir tarım geleneğinden gelen bilgi birikimi."),
        ("shield", "Kurumsal Altyapı", "2001'den beri planlı ve sürdürülebilir üretim.", True),
        ("leaf", "Doğal Üretim", "Doğal üretim yöntemleri ve titiz hasat süreci."),
        ("truck", "Geniş Araç Filosu", "Sorunsuz teslimat ve lojistik."),
        ("box", "Geniş Ürün Çeşitliliği", "Salkım, cherry ve bif domates, biber, patlıcan ve daha fazlası.", True),
        ("map", "4 Şube", "Aydın, Kaş, Burdur ve Elmalı'da hizmet."),
    ])}
  </div>
</section>
{brands_section()}{cta_band()}"""
    return (head(p, "Hakkımızda | 30+ Yıllık Tarım Tecrübesi – Küçükağa Tarım",
                 "Küçükağa Tarım: 30 yılı aşkın tecrübe, 2001'den beri kurumsal yapı, Aydın, Kaş, Burdur ve Elmalı şubeleri, tescilli Küçükağa Tarım ve Çavdır Fresh markaları.",
                 "assets/img/sera-1.jpg")
            + header(p) + body + footer())


def page_iletisim():
    p = "iletisim.html"
    phones = "".join(f'<li><a href="tel:{t}">{p_}</a><small>{n}</small></li>' for p_, t, n in PHONES)
    mails = "".join(f'<li><a href="mailto:{m}">{m}</a><small>{n}</small></li>' for m, n in EMAILS)
    branches = "".join(f"""
        <div class="branch">
          <div class="icon">{ic(I['pin'])}</div>
          <div>
            <h4>{n}</h4>
            <p>{a}<br>{c}</p>
            <a href="https://www.google.com/maps/search/?api=1&amp;query={q.replace(' ', '+')}" target="_blank" rel="noopener">Haritada aç →</a>
          </div>
        </div>""" for n, a, c, q in BRANCHES)
    options = "".join(f"<option>{n}</option>" for _, n, *_ in PRODUCTS) + "<option>Diğer / birden fazla ürün</option>"
    ld = [{"@context": "https://schema.org", "@type": "LocalBusiness", "name": f"Küçükağa Tarım – {n}",
           "telephone": "+90-542-252-52-26", "image": f"{SITE}/assets/img/logo.jpg",
           "address": {"@type": "PostalAddress", "streetAddress": a, "addressLocality": c.split(",")[0].strip(),
                       "addressRegion": c.split(",")[-1].strip(), "addressCountry": "TR"}}
          for n, a, c, _ in BRANCHES]
    body = page_hero("İletişim",
                     "Toptan sipariş, fiyat ve sevkiyat bilgisi için bize telefon, WhatsApp veya e-posta ile ulaşın.",
                     "İletişim") + f"""<section class="section">
  <div class="wrap contact-grid">
    <div class="card reveal">
      <h2 style="font-size:1.7rem">Teklif ve sipariş formu</h2>
      <p style="color:var(--muted)">Formu doldurun, mesajınız WhatsApp üzerinden bize hazır olarak iletilsin.</p>
      <form class="form" id="teklif-formu">
        <div class="row">
          <div><label for="ad">Ad Soyad</label><input id="ad" name="ad" required autocomplete="name"></div>
          <div><label for="firma">Firma (isteğe bağlı)</label><input id="firma" name="firma" autocomplete="organization"></div>
        </div>
        <div class="row">
          <div><label for="telefon">Telefon</label><input id="telefon" name="telefon" type="tel" autocomplete="tel"></div>
          <div><label for="urun">Ürün</label><select id="urun" name="urun"><option value="">Seçiniz</option>{options}</select></div>
        </div>
        <label for="mesaj">Mesajınız</label>
        <textarea id="mesaj" name="mesaj" required placeholder="Miktar, teslimat yeri ve tarih gibi bilgileri yazabilirsiniz."></textarea>
        <button class="btn btn-primary" type="submit">{WA_SVG}WhatsApp ile Gönder</button>
        <p class="form-note">Gönder'e bastığınızda WhatsApp açılır; mesajı kontrol edip gönderebilirsiniz.</p>
      </form>
    </div>
    <div style="display:grid;gap:1.5rem">
      <div class="card reveal">
        <h3>{ic(I['phone'])}Telefon</h3>
        <ul class="contact-list">{phones}</ul>
        <p class="form-note">WhatsApp: {PHONES[0][0]} numarasından 7/24 ulaşabilirsiniz.</p>
      </div>
      <div class="card reveal">
        <h3>{ic(I['mail'])}E-posta</h3>
        <ul class="contact-list">{mails}</ul>
      </div>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="wrap contact-grid">
    <div class="card reveal">
      <h3>{ic(I['pin'])}Şubelerimiz</h3>{branches}
    </div>
    <div class="reveal">
      <iframe class="map" title="Aydın Şubesi haritası" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
        src="https://www.google.com/maps?q=Acarlar+Adnan+Menderes+Toptanc%C4%B1+Hali+%C4%B0ncirliova+Ayd%C4%B1n&amp;output=embed"></iframe>
      <p class="form-note">Harita: Aydın Şubesi – Acarlar Adnan Menderes Toptancı Hali, İncirliova.</p>
    </div>
  </div>
</section>"""
    return (head(p, "İletişim | Küçükağa Tarım – Aydın, Kaş, Burdur, Elmalı",
                 "Küçükağa Tarım iletişim: +90 542 252 52 26 (WhatsApp 7/24), info@kucukagatarim.com. Aydın, Kaş, Burdur ve Elmalı şubeleri.",
                 "assets/img/logo.jpg", ld)
            + header(p) + body + footer())


PAGES = {
    "index.html": page_index,
    "urunler.html": page_urunler,
    "hizmetler.html": page_hizmetler,
    "neden-biz.html": page_neden,
    "galeri.html": page_galeri,
    "hakkimizda.html": page_hakkimizda,
    "iletisim.html": page_iletisim,
}


def sitemap():
    pri = {"index.html": "1.0", "urunler.html": "0.9", "iletisim.html": "0.8"}
    urls = []
    for pg in PAGES:
        loc = SITE + "/" + ("" if pg == "index.html" else pg)
        urls.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-11-17</lastmod>\n    <priority>{pri.get(pg, '0.7')}</priority>\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


if __name__ == "__main__":
    for name, fn in PAGES.items():
        (ROOT / name).write_text(fn(), encoding="utf-8")
        print("yazıldı:", name)
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: https://kucukagatarim.com/sitemap.xml\n", encoding="utf-8")
    print("yazıldı: sitemap.xml, robots.txt")
