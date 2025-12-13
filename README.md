# Karabük 2025 Orman Yangınları Uzaktan Algılama Analizi

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Sentinel-2](https://img.shields.io/badge/Data-Sentinel--2-green)
![GEE](https://img.shields.io/badge/Platform-Google%20Earth%20Engine-orange)
![License](https://img.shields.io/badge/Lisans-MIT-lightgrey)

> **Sayısal Görüntü İşleme (Digital Image Processing) teknikleri kullanılarak, Sentinel-2 uydu görüntüleri üzerinden 2025 Karabük orman yangınlarının hasar tespit ve sınıflandırma çalışması.**

---

## 📌 Proje Hakkında

Bu proje, 2025 yaz sezonunda Karabük ilinde (özellikle Ovacık, Safranbolu ve Eflani bölgelerinde) meydana gelen orman yangınlarının çevresel etkilerini **sayısal yöntemlerle** analiz etmek için geliştirilmiştir. **Google Earth Engine (GEE) Python API** kullanılarak, yangın öncesi ve sonrası uydu görüntüleri işlenmiş ve **dNBR (Normalized Burn Ratio Difference)** algoritması ile hasar şiddeti haritalanmıştır.

Çalışma, geleneksel haber takibinin ötesine geçerek, yangın izlerini piksel tabanlı matematiksel modellerle doğrulamayı ve mühendislik yaklaşımıyla raporlamayı hedefler.

### 🔬 Teknik Özellikler
*   **Veri Seti:** Sentinel-2 L2A (10m Çözünürlük, Atmosferik Düzeltilmiş).
*   **İndeksler:**
    *   **dNBR:** Yanmış alan tespiti ve şiddet sınıflandırması.
    *   **dNDVI:** Vejetasyon sağlığı ve klorofil kaybı analizi.
*   **Filtreleme:** Bulut maskeleme, su maskeleme (Water Mask) ve gürültü giderme (Median Filtering).
*   **Referans Veriler:** OGM kayıtları ve yerel haber kaynakları (Ground Truth).

---

## 📚 Dokümantasyon ve Raporlar

Bu projenin teknik detayları, akademik raporu ve veri doğrulama kayıtları `dokumanlar/` klasöründe titizlikle arşivlenmiştir.

| Dosya / Klasör | İçerik ve Açıklama |
| :--- | :--- |
| 📄 **[TEKNIK_YONTEM.md](dokumanlar/TEKNIK_YONTEM.md)** | Kullanılan algoritmalar, formüller (NBR, NDVI) ve görüntü işleme akışı (Pipeline). |
| 🗺️ **[CIKTI_OKUMA_REHBERI.md](dokumanlar/CIKTI_OKUMA_REHBERI.md)** | Üretilen haritaların renk skalaları, lejantları ve nasıl yorumlanacağı. |
| 📰 **[YANGIN_HABER_ARSIVI.md](dokumanlar/YANGIN_HABER_ARSIVI.md)** | Basına yansıyan haberler, olay kronolojisi ve resmi açıklamalar. |
| 🛠️ **[GELISTIRICI_NOTLARI.md](dokumanlar/GELISTIRICI_NOTLARI.md)** | Analiz sırasında karşılaşılan GEE API limitleri, çözüm yolları ve optimizasyon günlüğü. |
| 🎓 **[rapor/rapor.pdf](rapor/rapor.pdf)** | Projenin çıktılarını içeren, akademik formatta hazırlanmış **Nihai Proje Raporu**. |

---

## 🚀 Kurulum ve Kullanım

Kendi bilgisayarınızda bu analizleri tekrar etmek için aşağıdaki adımları izleyebilirsiniz.

### Ön Hazırlık
*   Python 3.8 veya üzeri yüklü olmalıdır.
*   Aktif bir [Google Earth Engine](https://earthengine.google.com/) hesabı gereklidir.

### 1. Projeyi Klonlayın
```bash
git clone https://github.com/yusufarbc/karabuk-2025-sentinel2-yangin-analizi.git
cd karabuk-2025-sentinel2-yangin-analizi
```

### 2. Sanal Ortam Oluşturun (Önerilen)
```bash
python -m venv .venv
# Windows için:
.venv\Scripts\activate
# Linux/Mac için:
source .venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. GEE Yetkilendirmesi
Analiz scriptlerinin uydu verilerine erişebilmesi için giriş yapın:
```bash
earthengine authenticate
```

### 5. Analizi Başlatın
Jupyter Notebook üzerinden adım adım ilerleyebilirsiniz:
```bash
jupyter notebook analysis.ipynb
```

---

## 📊 Örnek Çıktı

> *Aşağıdaki gibi dNBR haritaları, yangının en şiddetli olduğu merkez noktalarını (Kırmızı) ve çevreye yayılımını (Sarı/Turuncu) sayısal olarak gösterir.*

*(Buraya `gorseller/` klasöründen örnek bir analiz görseli eklenebilir)*

---

## 📝 Lisans ve İletişim

Bu proje **MIT Lisansı** ile sunulmuştur. Akademik ve eğitim amaçlı kullanıma açıktır.

**Geliştirici:** Yusuf Talha ARABACI - *Karabük Üniversitesi*
