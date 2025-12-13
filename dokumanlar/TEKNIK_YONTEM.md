# TEKNİK YÖNTEM VE ALGORİTMALAR

Bu proje, 2025 Karabük orman yangınlarının etkilerini uzaktan algılama teknikleri kullanarak nicel olarak analiz eder. Analizler Google Earth Engine (GEE) platformu üzerinde, Sentinel-2 (MultiSpectral Instrument) uydu verileri kullanılarak gerçekleştirilmiştir.

## 1. Veri Kaynağı: Sentinel-2
Analizde **Sentinel-2 L2A** (Level-2A, Atmosferik Olarak Düzeltilmiş) veri seti kullanılmıştır.
*   **Mekansal Çözünürlük:** RGB ve NIR bantları için 10 metre.
*   **Spektral Çözünürlük:** Görünür ışıktan (VIS) kısa dalga kızılötesine (SWIR) kadar 13 bant.
*   **Analiz Dönemleri:**
    *   **Referans (Yangın Öncesi):** 1 Haziran 2025 - 30 Haziran 2025 (Sağlıklı vejetasyon).
    *   **Değerlendirme (Yangın Sonrası):** 5 Eylül 2025 - 30 Eylül 2025 (Yangın sonrası durum).

Geçiş mevsiminin etkilerini minimize etmek için geniş tarih aralıkları seçilmiş ve bulutsuz piksel kompozitleri (Cloud-Free Median Composite) oluşturulmuştur.

## 2. Spektral İndeksler
Yangın etkisini tespit etmek için iki temel indeks hesaplanmıştır:

### NBR (Normalized Burn Ratio)
Yanmış alanları tespit etmek için geliştirilmiş standart indekstir. Sağlıklı bitki örtüsü NIR bandında yüksek yansıtma yaparken, yanmış alanlar SWIR bandında yüksek yansıtma yapar.
$$ \text{NBR} = \frac{\text{NIR} - \text{SWIR}}{\text{NIR} + \text{SWIR}} $$

### NDVI (Normalized Difference Vegetation Index)
Genel bitki sağlığını ölçmek için kullanılır.
$$ \text{NDVI} = \frac{\text{NIR} - \text{RED}}{\text{NIR} + \text{RED}} $$

## 3. Değişim Analizi ve Sınıflandırma

Hasar tespiti için yangın öncesi ve sonrası indekslerin farkı (Delta) alınır:
$$ \text{dNBR} = \text{NBR}_{\text{önce}} - \text{NBR}_{\text{sonra}} $$

### USGS Yanma Şiddeti Sınıflandırması
Hesaplanan dNBR değerleri, Amerika Birleşik Devletleri Jeolojik Araştırmalar Kurumu (USGS) standartlarına göre 5 sınıfa ayrılır:

| Şiddet Sınıfı | dNBR Değer Aralığı | Açıklama |
| :--- | :--- | :--- |
| **Yanmamış** | < 0.10 | Değişim yok veya çok az (fenolojik değişim). |
| **Düşük Şiddet** | 0.10 – 0.27 | Üst örtüde hafif yanma, ağaçlar canlı kalabilir. |
| **Orta-Düşük** | 0.27 – 0.44 | Yer örtüsü yanmış, ağaç gövdelerinde hafif hasar. |
| **Orta-Yüksek** | 0.44 – 0.66 | Ağaç taçlarında (tepe) önemli yanma. |
| **Yüksek Şiddet** | > 0.66 | Tamamen yanmış, biyokütle kaybı yüksek. |

## 4. Gürültü Azaltma ve İyileştirme (Noise Reduction)
Uydu görüntülerindeki atmosferik etkiler veya tekil piksel hatalarını (salt-and-pepper noise) gidermek için analiz hattına (pipeline) gelişmiş filtreler eklenmiştir:

1.  **Medyan Yumuşatma (Smoothing):**
    *   Ham dNBR ve Severity haritaları üzerinde **2.5 piksel** yarıçaplı medyan/mod filtresi uygulanır.
    *   Bu işlem, izole pikselleri komşularına benzeterek daha homojen ve yorumlanabilir "yanık lekeleri" oluşturur.

2.  **Minimum Yama Büyüklüğü (Minimum Patch Size):**
    *   Gerçek bir orman yangını belirli bir alana yayılır. Tek bir pikselin değişimi genellikle hatadır.
    *   Analizde, **2.0 Hektar**'dan küçük olan izole yanmış alanlar **filtrelenerek haritadan atılır**.
    *   Bölgesel (Zoom) analizlerde bu eşik daha hassas (0.1 hektar) tutulur.

3.  **İl Geneli Tarama Stratejisi:**
    *   Tüm Karabük ilini içeren büyük analizde bellek yönetimi kritik öneme sahiptir.
    *   Bu nedenle 1. Aşama taraması **100 metre** ölçeğinde (scale) yapılır.
    *   Daha sonra tespit edilen odak bölgelerde analiz **10 metre** (tam çözünürlük) ölçeğine indirilir.
