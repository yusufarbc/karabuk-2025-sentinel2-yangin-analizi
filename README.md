# Karabük 2025 Orman Yangınları Uzaktan Algılama Analizi

> **Sentinel-2 Uydu Görüntüleri ve Google Earth Engine ile Hasar Tespit Raporu**

Bu proje, 2025 yaz sezonunda Karabük ilinde (özellikle Ovacık, Eflani ve Safranbolu bölgelerinde) meydana gelen orman yangınlarının çevresel etkilerini bilimsel yöntemlerle analiz etmek amacıyla geliştirilmiştir.

---

## 🌐 Canlı Demo ve Rapor

Projenin interaktif haritalarını ve detaylı analiz sonuçlarını web üzerinden inceleyebilirsiniz:

### [🚀 Analiz Platformunu Görüntüle](https://yusufarbc.github.io/karabuk-2025-sentinel2-yangin-analizi/)

---

## 🔍 Proje Hakkında

İklim değişikliğinin bir sonucu olarak 2025 yılında artan sıcaklıklar, Karabük ormanlarında ciddi yangınlara yol açmıştır. Bu çalışma, **Sentinel-2** uydusunun yüksek çözünürlüklü optik verilerini kullanarak yangın öncesi ve sonrası durumu karşılaştırmalı olarak sunar.

### Uygulanan Bilimsel Metodoloji
*   **dNDVI (Vejetasyon Fark İndeksi):** Bitki örtüsündeki yeşillik kaybını ve klorofil değişimini modeller.
*   **dNBR (Yanmışlık Oranı Farkı):** USGS standartlarına göre yanma şiddetini (Düşük, Orta, Yüksek) sınıflandırır.
*   **Maskeleme:** ESA WorldCover verisi kullanılarak tarım arazileri ve yerleşim yerleri analizden çıkarılmış, sadece ormanlık alanlara odaklanılmıştır.

Analizler, **Google Earth Engine (GEE)** Python API kullanılarak bulut tabanlı olarak gerçekleştirilmiş ve sonuçlar **QGIS** ortamında doğrulanmıştır.

---

## 📂 Proje Yapısı

| Klasör | İçerik ve Açıklama |
| :--- | :--- |
| `gee/` | **Analiz Motoru:** GEE pipeline kodları, indeks hesaplamaları ve görüntü işleme scriptleri. |
| `results/` | **Çıktılar:** Her bölge için üretilen HTML haritalar, PNG görseller ve CSV istatistikleri. |
| `paper/` | **Akademik Rapor:** LaTeX formatında yazılmış bilimsel makale ve derlenmiş PDF. |
| `analysis.ipynb` | **Jupyter Notebook:** Adım adım analiz sürecini çalıştıran ana defter. |
| `index.html` | **Web Arayüzü:** Sonuçların sunulduğu modern, responsive web sayfası. |

---

## ⚡ Kurulum ve Kullanım

Bu projeyi yerel ortamınızda çalıştırmak ve analizleri tekrar etmek için aşağıdaki adımları izleyin.

### Önkoşullar
*   Python 3.8+
*   Google Earth Engine hesabı

### 1. Kurulum

```bash
# Projeyi klonlayın
git clone https://github.com/yusufarbc/karabuk-2025-sentinel2-yangin-analizi.git

# Sanal ortam oluşturun (Önerilen)
python -m venv .venv

# Paketleri yükleyin
pip install -r requirements.txt
```

### 2. Kimlik Doğrulama
Google Earth Engine API'sini projenizde kullanabilmek için yetkilendirme yapın:
```bash
earthengine authenticate
```

### 3. Analizi Çalıştırma
Analiz sürecini başlatmak için Jupyter Notebook'u kullanabilirsiniz:
```bash
jupyter notebook analysis.ipynb
```
Alternatif olarak, `.py` scriptleri üzerinden doğrudan işlem yapabilirsiniz.

---

## 📝 Lisans

Bu proje **MIT Lisansı** ile lisanslanmıştır. Açık kaynaklıdır ve eğitim/araştırma amaçlı özgürce kullanılabilir.

---

*Yusuf Talha ARABACI - Karabük Üniversitesi*
