# Sonuçların ve Çıktıların Yorumlanması

Analiz tamamlandığında `results/` klasörü altında HTML haritalar, PNG görseller ve CSV özet tabloları oluşturulur. Bu doküman, elde edilen çıktıların nasıl yorumlanacağını açıklar.

## 1. Çıktı Klasör Yapısı

*   `results/il_geneli/`: Tüm Karabük ili için yapılan geniş ölçekli (100m) tarama sonuçları.
*   `results/yanginlar/[BOLGE_ADI]/`: Tespit edilen 6 kritik bölge (Aladağlar, Ovacık vb.) için yapılan yüksek çözünürlüklü (10m) detaylı analiz sonuçları.

## 2. Harita Türleri

### A. dNBR Haritası (`dNBR.html` / `dNBR.png`)
Yangın öncesi ve sonrası arasındaki ham değişimi gösterir.
*   **Mavi/Yeşil:** Değişim yok veya bitki örtüsü artışı (yenilenme).
*   **Sarı/Turuncu:** Hafif hasar.
*   **Kırmızı:** şiddetli hasar.

### B. Severity (Şiddet) Haritası (`severity.html` / `severity.png`)
dNBR verisinin USGS standartlarına göre sınıflandırılmış halidir. Raporlama için **en önemli** haritadır.

**Renk Skalası:**
*   🟩 **Koyu Yeşil:** Yanmamış / Çok Düşük
*   🟨 **Sarı:** Düşük Şiddet
*   🟧 **Turuncu:** Orta Şiddet
*   🟥 **Kırmızı:** Yüksek Şiddet
*   🟪 **Bordo/Koyu Kırmızı:** Çok Yüksek Şiddet

## 3. Görsel İyileştirmeler ve Raporlama

### Sınır Çizgileri
Haritalarda gördüğünüz **Magenta (Parlak Mor)** renkli çizgiler:
*   İl sınırlarını veya
*   Analiz edilen odak bölgesinin (10x10 km) sınırlarını gösterir.
*   Bu renk (Magenta), hem yeşil orman hem de kırmızı yanık alanlar üzerinde en yüksek kontrastı sağladığı için seçilmiştir.

### RGB + Severity Kaplaması (`severity_overlay_rgb.png`)
Bu özel PNG çıktısı, raporlarda ve akademik makalelerde kullanılmak üzere tasarlanmıştır.
*   **Alt Katman:** Yangın sonrası (Post-Fire) **Gerçek Renkli (RGB)** uydu görüntüsü. Mevcut araziyi, yolları ve yerleşim yerlerini gösterir.
*   **Üst Katman:** Yarı saydam (%65 opaklık) **Severity (Şiddet)** haritası.
*   **Amaç:** Yangının coğrafi bağlamını (dağın hangi yamacında, hangi yola yakın vb.) anlamayı kolaylaştırır. "Filtre giydirilmiş" görünümü sağlar.

## 4. İstatistiksel Veriler
Her analiz klasöründe `summary_stats.csv` bulunur.
*   `severity_4_yuksek`: Yüksek şiddette yanan alan miktarı (Hektar).
*   `burned_total_ha`: (Varsa) Toplam etkilenen alan.

**Not:** Küçük parazitleri önlemek için analizde **Minimum Yama Büyüklüğü (Minimum Patch Size)** filtresi uygulanmıştır. Bu nedenle çok küçük (örneğin tek bir ağaçlık) yanıklar istatistiklere dahil edilmeyebilir.
