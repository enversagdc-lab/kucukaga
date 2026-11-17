# kucukagatarim.com

Küçükağa Tarım'ın web sitesi (statik HTML).

## Yapı

- `*.html` — 7 sayfa (ana sayfa, ürünler, hizmetler, neden biz, galeri, hakkımızda, iletişim)
- `assets/css/site.css` — ortak tasarım
- `assets/js/site.js` — mobil menü, galeri filtresi, fotoğraf görüntüleyici, WhatsApp teklif formu
- `assets/img/` — web için küçültülmüş fotoğraflar (`-sm` = küçük boy)
- `tools/build_site.py` — sayfaları üretir. Telefon, adres, ürün ve galeri bilgileri bu dosyanın başındadır.
  Bir bilgiyi değiştirmek için dosyayı düzenleyip `python3 tools/build_site.py` çalıştırın.

Kök dizindeki eski fotoğraflar (ör. `SALKIM.jpeg`) dışarıdan verilmiş bağlantılar bozulmasın diye duruyor.

## Yayına alma

Site İsimtescil hosting'inde (FTP) yayınlanır; GitHub'a gönderilen değişiklik siteye kendiliğinden geçmez.
Yüklenecekler: `*.html`, `assets/`, `robots.txt`, `sitemap.xml`, `logo.ico`. `tools/` yüklenmez.
