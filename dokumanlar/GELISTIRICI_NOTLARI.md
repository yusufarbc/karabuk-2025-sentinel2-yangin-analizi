# GELİŞTİRİCİ NOTLARI VE OPTİMİZASYON GÜNLÜĞÜ

Bu doküman, Karabük 2025 Sentinel-2 Yangın Analizi projesi süresince karşılaşılan teknik zorlukları, Google Earth Engine (GEE) platformunun kısıtlamalarını ve gelecek çalışmalar için hayati önem taşıyan tecrübeleri derlemektedir.

## 1. Google Earth Engine (GEE) Altyapı ve Planlama

### Python API vs. JavaScript API
- **Dokümantasyon ve Örnekler:** GEE'nin resmi dokümantasyonu ve topluluk örneklerinin %90'ı JavaScript Code Editor üzerine kuruludur. Python API (`geemap` veya doğrudan `ee`) kullanırken sürekli olarak JS kodunu Python'a "tercüme etmek" zaman kaybına yol açmıştır.
- **İnteraktiflik:** JS Code Editor, anlık görselleştirme ve hata ayıklama (debug) konusunda çok daha hızlıdır. Python tarafında (Jupyter Notebook) her değişiklikte haritayı yeniden render etmek ve yetkilendirme süreçlerini yönetmek daha hantal kalmaktadır.
- **Öneri:** Gelecek projelerde analiz ve algoritma geliştirme aşaması GEE JS Code Editor'de tamamlanmalı, sadece son ürün otomasyonu için Python kullanılmalıdır.

### Hesap Türleri ve Kısıtlamalar (Non-Commercial vs. Commercial)
- **Non-Commercial Plan:** Standart, ücretsiz akademik hesap ("Non-commercial") büyük ölçekli ve yüksek bellek gerektiren işlemlerde yetersiz kalmaktadır. İşlemci gücü (EECU) önceliği düşüktür.
- **Commercial Limited Plan:** Projenin ilerleyen aşamalarında kesintisiz çalışabilmek için Google Cloud Platform (GCP) üzerinden bir proje oluşturulması ve faturalandırma (Billing) hesabının bağlanması gerekmiştir. "Commercial Limited" veya ücretli planlar, daha yüksek işlem limiti ve öncelik sağlar. GCP'de kredi kartı tanımlamak, ücretsiz kota aşılmasa bile servisin "ciddiyeti" ve erişim izinleri açısından kritik bir adımdır.

### Bellek (Memory) Sınırları ve "UserMemoryLimitExceeded"
- **İl Geneli Analiz Sorunu:** Karabük ili genelinde (büyük bir ROI) yüksek çözünürlüklü (10m) Sentinel-2 verisiyle çalışırken, özellikle `dNDVI` veya sınıflandırma gibi karmaşık hesaplamalarda sık sık bellek taşması hataları alınmıştır.
- **Overlay Kısıtı:** Bu bellek sınırı yüzünden, il genelini kapsayan tek parça, yüksek çözünürlüklü "Overlay" (harita üzerine giydirilmiş saydam katman) görselleri üretilememiştir. Sadece daha küçük, bölgesel (patch) analizler veya düşük çözünürlüklü çıktılar alınabilmiştir.
- **Çözüm Denemeleri:** `.reproject()` kullanımından kaçınmak, `tileScale` parametresini artırmak gibi optimizasyonlar yapılsa da donanım limiti yine de belirleyici faktör olmuştur.

## 2. Görselleştirme ve Sunum (GitHub Pages Entegrasyonu)

### Dinamik vs. Statik Haritalar
- **Token Süresi:** GEE Python API ile üretilen dinamik harita katmanları (Tile Layers), geçici erişim token'ları (token expiration) kullanır. Bu haritalar Jupyter Notebook'ta çalışsa da, GitHub Pages gibi statik bir web sitesine konulduğunda birkaç saat içinde "kırık link" haline gelmektedir.
- **Zorunlu PNG Overlay:** Haritaların GitHub Pages üzerinde kalıcı olarak sergilenebilmesi için analiz sonuçları (dNDVI, dNBR) statik PNG resimlerine dönüştürülüp harita üzerine "resim" olarak yapıştırılmıştır (ImageOverlay).
- **Dezavantaj:** Bu yöntem, haritaya çok yaklaşıldığında (zoom-in) görüntünün pikselleşmesine (bulanıklaşmasına) neden olmaktadır. Vektör veya Tile tabanlı netlik kaybedilmiştir.

## 3. Yönetim ve Kimlik Doğrulama Süreçleri

### Yetkilendirme (Authentication) Karmaşası
- Proje başında `gcloud auth` ve `earthengine authenticate` komutları arasında uyumsuzluklar yaşanmış, yerel ortamdaki (Localhost) yetkilendirme ile "Notebook" yetkilendirmesi karışmıştır.
- Proje ID'sinin (`karabuk-2025...` veya `solar-bolt...`) kod içinde ve GEE tarafında tutarlı olması gerektiği, aksi takdirde "Project not found" veya 403 yetki hataları alındığı tecrübe edilmiştir.

## Özet ve Gelecek İçin Tavsiyeler
1. **Hibrit Yaklaşım:** Algoritmayı JS'de geliştir, otomasyonu Python'da yap. (istersen tamamen JS'de yap)
2. **Altyapı:** İşe başlamadan önce GCP üzerinde faturalandırması açık bir proje tanımla.
3. **Sunum:** Web sunumu için Mapbox veya GEE App gibi profesyonel çözümleri değerlendir; statik PNG overlay sadece hızlı prototipleme içindir.
4. **Veri:** Büyük alanlarda çalışırken görüntüyü parçalara (grid/tile) bölerek işle (Export to Drive) ve sonra birleştir; anlık (on-the-fly) hesaplama bellek sınırına takılır.
