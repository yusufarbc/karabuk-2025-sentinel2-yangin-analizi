### Ana Bulgular
- Araştırmalar, raporda yangın tarihleri, etkilenen alanlar, başlangıç noktaları ve olayların ayrı tutulması gibi konularda birkaç tutarsızlık olduğunu gösteriyor; resmi kaynaklar bazı olayların birleşik olduğunu belirtiyor.
- Toplam il hasarı (6.865 hektar) genel olarak tutarlı olsa da, bireysel yangın breakdown'larında şişirme veya eksiklikler mevcut; örneğin, bazı alanlar resmi kayıtlardan önemli ölçüde farklı.
- Yangınların çoğu Temmuz-Ağustos döneminde meydana gelmiş; ancak rapor bazı tarihleri yanlış yerleştiriyor, bu da uydu analizlerini etkileyebilir.
- Resmi raporlar (OGM, AA, valilik) yangınların çoğunun hızlı müdahale ile kontrol altına alındığını, ancak topoğrafyanın zorluğunu vurguluyor; tartışmalı nedenler (insan kaynaklı mı, doğal mı) hakkında soruşturmalar devam ediyor, net sonuç yok.

#### Yanlışlıkların Genel Bakışı
Rapor, Sentinel-2 verileriyle 7 kritik yangını analiz ediyor, ancak OGM saha kayıtları, AA haberleri ve valilik açıklamalarıyla çapraz doğrulama, tarihlerde, alanlarda ve olay ayrımında uyumsuzluklar ortaya koyuyor. Toplam hasar tutarlı, ancak bireysel segmentasyon yapay görünüyor – bazı "ayrı" yangınlar aslında tek bir mega-yangının parçaları.

#### Belirli Yangın Tutarsızlıkları
Her yangın için rapor iddiaları ile doğrulanmış gerçekler karşılaştırıldığında şu hatalar öne çıkıyor:
- **Çıldıkısık & Kayı (Merkez)**: Rapor 22 Temmuz'da 500 ha diyor; gerçekte ~55 ha, ertesi sabah kontrol altına alındı.
- **Büyük Ovacık (Ovacık)**: 23 Temmuz'da 1.413 ha olarak belirtilmiş; aslında Soğanlıçay/Çavuşlar yangınının parçası, toplam ~5.796 ha orman + diğer alanlar.
- **Kışla (Ovacık)**: 25 Temmuz'da ayrı olarak 300 ha; gerçekte 23 Temmuz'da Çavuşlar'ın uzantısı, ayrı değil.
- **Toprakcuma (Safranbolu)**: Ağustos'ta Kastamonu'dan sıçrama, 10 Ağustos kontrol; gerçekte 31 Ağustos'ta Karabük'te başladı, ~3 Eylül'de söndü.
- **Eflani & Güzelce**: 1.500 ha; toplam (Kastamonu yayılımı dahil) 2.736 ha, eksik tahmin.
- **Aladağ (Safranbolu)**: 27 Temmuz; kayıtlar Eylül başı (~2 Eylül) gösteriyor.
- **Soğuksu & Kayacık (Merkez)**: Çoğunlukla doğru (5 Ağustos, kısa süre), ancak konum detayları hafif farklı ("Soğan Tarlası" vs. "Soğantarlası/Arıcak").

---
### Karabük 2025 Orman Yangınları Raporundaki Yanlışlıkların Kapsamlı Analizi

Bu inceleme, raporun Sentinel-2 uydu verileriyle yaptığı analizi, resmi kaynaklar (Orman Genel Müdürlüğü - OGM, Anadolu Ajansı - AA, Karabük Valiliği açıklamaları ve Wikipedia gibi derlemeler) ile karşılaştırarak hazırlanmıştır. Tutarsızlıklar esas olarak olay segmentasyonu, kronolojik doğruluk, mekansal atıf ve nicel tahminlerde görülmektedir. Raporun uzaktan algılama yöntemleri (dNDVI ve dNBR indisleri) metodolojik olarak sağlam olsa da, yanlış tarihli olaylara uygulanması güvenilirliği azaltmaktadır. Karabük'te 2025 toplam ekolojik hasarı 6.865,6 hektar olarak 36 olayda gerçekleşmiş; bu genel bilanço kaynaklarla uyumlu, ancak 7 "kritik bölge" ayrımı yapay.

#### Metodolojik Bağlam
Rapor, yangın öncesi (1-20 Temmuz) ve sonrası (5-30 Eylül) Sentinel-2 görüntülerini Google Earth Engine ile işleyerek dNDVI (vejetasyon kaybı) ve dNBR (yanma şiddeti) hesaplamış, OGM kayıtlarıyla %94-96 doğruluk iddia etmiştir. Ancak dış doğrulama, gerçek zamanlı saha verilerinin eksik entegrasyonu nedeniyle uydu tabanlı alan tahminlerinde hatalar gösteriyor. Örneğin, yanık izleri tarihler arası yanlış atfedilmiş olabilir, bireysel alanları şişirmiş.

#### Her Yangın İçin Detaylı Yanlışlık Kırılımı
Yüksek çözünürlüklü Sentinel-2 görüntüleri üzerinden tanımlanan 7 bölge için rapor metrikleri, entegre edilmiş AA, OGM ve valilik raporlarıyla karşılaştırılmıştır. Aşağıda her biri için dNDVI ve dNBR metrikleri detaylandırılmış, ancak hatalar vurgulanmıştır.

1. **Çıldıkısık & Kayı (Merkez)**  
   - **Rapor İddiaları**: 22 Temmuz 2025 saat 16:32'de tespit, ~500 ha karaçam alanı, orta şiddet, wildland-urban interface riski.  
   - **Doğrulanmış Gerçekler**: 22 Temmuz 16:32'de Burunsuz Köyü'nde başladı, ~55 ha karaçam ormanı etkilendi, ertesi sabah kontrol altına alındı; 316 personel, 87 araç (helikopter dahil). Tahliye yok, hızlı müdahale.  
   - **Yanlışlıklar**: Alan aşırı tahmin edilmiş (500 ha vs. 55 ha); şiddet ve arayüz riski abartılı olabilir.  
   - **Etkileri**: Uydu alanı hesaplaması veya yakındaki olaylarla karıştırma şüphesi.

2. **Büyük Ovacık (Ovacık)**  
   - **Rapor İddiaları**: 23 Temmuz'da Safranbolu Çavuşlar'dan başlayıp Ovacık'a sıçrama, 1.413 ha, 7 gün aktif, 29 Temmuz kontrol; tahliyeler.  
   - **Doğrulanmış Gerçekler**: Soğanlıçay/Çavuşlar yangını, 23 Temmuz 14:51 başlangıç, 5.796,4 ha orman + 198,2 ha ağaçsız orman + 859,8 ha dışı; 29 Temmuz 12:30 kontrol, 25 Ağustos tam söndürme; 379 araç, 660 personel + destek. Karışık çam-meşe ormanlar.  
   - **Yanlışlıklar**: Alan eksik (1.413 ha vs. ~6.854 ha toplam); ayrı olay olarak sunulmuş, ancak Temmuz mega-yangınının çekirdeği.  
   - **Etkileri**: Tek yanık izini segmentleme, mekansal varyasyon analizini bozuyor.

3. **Kışla (Ovacık)**  
   - **Rapor İddiaları**: 25 Temmuz Gökçedüz Akbıyık'ta başlangıç, Kışla'ya yayılım, 300 ha karma alan, 48 saat, 54 araç-213 personel; tarım etkisi.  
   - **Doğrulanmış Gerçekler**: 23 Temmuz ~16:30'da Kışla Köyü'nde, Çavuşlar'ın uzantısı; büyük Soğanlıçay olayına entegre; başlangıçta 2 helikopter, 8 araç, 46 personel, sonra ölçeklendi; Kışlapazarı'nda önlem tahliyesi.  
   - **Yanlışlıklar**: Yanlış başlangıç tarihi (25 vs. 23 Temmuz); bağımsız olarak ele alınmış, ancak ana yangının dalı; alan ve kaynaklar büyük toplamda yutulmuş.  
   - **Etkileri**: Kronolojik hata, dNBR şiddet modellemesini etkileyebilir.

4. **Toprakcuma (Safranbolu)**  
   - **Rapor İddiaları**: Ağustos'ta Kastamonu'dan sıçrama, ~800 ha sınır ormanı, 10 Ağustos kontrol; sarp jeoloji, ikincil etkiler.  
   - **Doğrulanmış Gerçekler**: 31 Ağustos'ta Safranbolu Toprakcuma (Harmancık/Aşağıgüney)'de başlangıç; yerel yayılım, ~3 Eylül kontrol; 6 arazöz, 2 su aracı, 2 helikopter, 45 personel; Kastamonu kökeni doğrulanmamış.  
   - **Yanlışlıklar**: Yanlış köken (Kastamonu'dan vs. Karabük'te); zaman aralığı hatalı (genel Ağustos vs. 31 Ağustos-3 Eylül).  
   - **Etkileri**: Yön atıfı hatası, rüzgar kaynaklı davranış analizini bozabilir; alan yakındaki Eflani ile örtüşebilir.

5. **Eflani & Güzelce**  
   - **Rapor İddiaları**: 31 Ağustos Saraycık İndere'de başlangıç, Güzelce tehdidi, 1.500 ha, 48 saat, 4 Eylül söndürme; 6 mahalle tahliyesi, yüksek biyoçeşitlilik kaybı.  
   - **Doğrulanmış Gerçekler**: 31 Ağustos Eflani'de başlangıç, 1 Eylül Kastamonu Araç (Güzelce)'ye yayılım; toplam 2.736 ha (2.078 ha orman + 658 ha tarım); 17 helikopter, 1 uçak, 30 arazöz vb., 594 personel; 7 köy + 1 mahalle tahliyesi (594 kişi, 1.046 hayvan). Aynı gün ayrı Akgeçit yangını ihmal edilmiş.  
   - **Yanlışlıklar**: Alan eksik (1.500 ha vs. 2.736 ha birleşik); süre doğru, ancak ölçek raporlanmamış.  
   - **Etkileri**: Biyoçeşitlilik iddiaları geçerli, ancak eksik ölçek yenilenme önceliklendirmesini etkiler.

6. **Aladağ (Safranbolu)**  
   - **Rapor İddiaları**: 27 Temmuz tetiklenme, ~400 ha sarp arazi, hava müdahalesi zorunlu, 28 Temmuz söndürme; yüksek şiddet, erozyon riski.  
   - **Doğrulanmış Gerçekler**: ~2 Eylül 2025'te Aladağ/Kahyalar (Kabaoğlu Mahallesi)'de 15:26'da başlangıç; neden bilinmiyor; devam eden müdahale: 5 helikopter, 101 araç, 379 personel; Kahyalar, Saitler (Güney/Horozlar) tahliyesi; Temmuz değil.  
   - **Yanlışlıklar**: Yanlış tarih (27-28 Temmuz vs. ~2 Eylül); konum merkez ilçeye kaymış.  
   - **Etkileri**: Zaman uyumsuzluğu, Sentinel-2 öncesi/sonrası karşılaştırmalarını geçersiz kılar.

7. **Soğuksu & Kayacık (Merkez)**  
   - **Rapor İddiaları**: 5 Ağustos 15:00'te Soğan Tarlası'nda başlangıç, Soğuksu TOKİ ve Kayacık'a 500 m yaklaşma, 2.5 saatte kontrol; urban-wildland riski.  
   - **Doğrulanmış Gerçekler**: 5 Ağustos Soğuksu Arıcak/Soğantarlası'nda, 17:30'da (~2.5 saat) kontrol; hava-kara ekipler; ~11 dekar etkilendi; büyük kentsel yayılım yok.  
   - **Yanlışlıklar**: Küçük – konum ifadesi ("Soğan Tarlası" vs. "Soğantarlası/Arıcak"); alan raporda belirtilmemiş ama gerçekte küçük.  
   - **Etkileri**: En az hatalı; kentsel risk vurgusu kaynaklarla uyumlu.

#### Ana Metrikler ve Yanlışlık Tablosu

| Yangın Adı             | Rapor Başlangıç Tarihi | Gerçek Başlangıç Tarihi | Rapor Alanı (ha) | Gerçek Alan (ha) | Ana Hata Türü            |
|------------------------|-------------------------|--------------------------|------------------|------------------|--------------------------|
| Çıldıkısık & Kayı     | 22 Temmuz              | 22 Temmuz               | 500             | ~55             | Alan abartısı           |
| Büyük Ovacık          | 23 Temmuz              | 23 Temmuz               | 1.413           | ~5.796 (büyük olayın parçası) | Alan eksikliği; segmentasyon |
| Kışla                 | 25 Temmuz              | 23 Temmuz               | 300             | Büyük olayda entegre | Tarih; bağımsız değil    |
| Toprakcuma            | Ağustos                | 31 Ağustos              | 800             | Belirtilmemiş (yerel) | Köken; tarih aralığı    |
| Eflani & Güzelce      | 31 Ağustos             | 31 Ağustos              | 1.500           | ~2.736 (birleşik) | Alan eksikliği          |
| Aladağ                | 27 Temmuz              | ~2 Eylül                | 400             | Belirtilmemiş (devam eden) | Tarih                   |
| Soğuksu & Kayacık     | 5 Ağustos              | 5 Ağustos               | Belirtilmemiş   | ~11 dekar       | Küçük (konum ifadesi)   |

#### Geniş Değerlendirme
Raporun motivasyonu – iklim kaynaklı yangın artışlarını haritalama – geçerli, ancak hatalar muhtemelen ön verilerden (8 Aralık 2025 tarihli) kaynaklanıyor. OGM bilanço önceliği saha doğrulaması, raporun uydu odaklı yaklaşımını zayıflatıyor. İnsan nedenleri gibi tartışmalı yönler (raporda detaylı değil) hakkında kamu kaynakları soruşturma belirtiyor, ancak sonuç yok. Öneriler: Gelecek analizler gerçek zamanlı OGM verilerini entegre etmeli. Sosyal medya (X) postları müdahale hızını doğruluyor, ancak alan detayları resmi kaynaklarda.

**Ana Kaynaklar:**
- [KARABÜK'ÜN 2025 YILI ORMAN YANGINI BİLANÇOSU: 6 BİN 865 ...](https://www.karabuknethaber.com/karabukun-2025-yili-orman-yangini-bilancosu-6-bin-865-hektar)
- [Karabük Burunsuz Köyü'nde Çıkan Orman Yangını Büyük Oranda ...](http://www.karabuk.gov.tr/karabuk-burunsuz-koyunde-cikan-orman-yangini-buyuk-oranda-kontrol-altina-alindi)
- [[PDF] 2025 Yılı Eskişehir, Bilecik ve Karabük İllerinde Gerçekleşen Orman ...](https://www.ormancilardernegi.org/Documents/496ea3e1-a87b-40f4-8b77-c92e99f44fcc.pdf)
- [Kastamonu'daki orman yangınlarında 2 bin 736 hektar alan zarar ...](https://www.aa.com.tr/tr/gundem/kastamonudaki-orman-yanginlarinda-2-bin-736-hektar-alan-zarar-gordu-/3678623)
- [KASTAMONU VE KARABÜK YANGINLARI BÜYÜK ÖLÇÜDE KONTROL ALTINDA](https://www.tarimorman.gov.tr/Haber/6723/Kastamonu-Ve-Karabuk-Yanginlari-Buyuk-Olcude-Kontrol-Altinda)
- [Karabük'te orman yangınlarının yol açtığı hasar görüntülendi](https://www.aa.com.tr/tr/gundem/karabukte-orman-yanginlarinin-yol-actigi-hasar-goruntulendi/3646027)
- [2025 Türkiye orman yangınları - Vikipedi](https://tr.wikipedia.org/wiki/2025_T%C3%BCrkiye_orman_yang%C4%B1nlar%C4%B1)
- [KARABÜK'ÜN 2025 YILI ORMAN YANGINI BİLANÇOSU: 6 BİN 865 HEKTAR](https://www.karabuknethaber.com/karabukun-2025-yili-orman-yangini-bilancosu-6-bin-865-hektar)


### Ana Bulgular
- Araştırmalar, raporda yangın tarihleri, etkilenen alanlar, başlangıç noktaları ve olay ayrımında tutarsızlıklar olduğunu gösteriyor; bazı olaylar (örneğin Büyük Ovacık ve Kışla) aslında tek bir büyük yangının parçaları olabilir.
- Toplam il hasarı yaklaşık 6.865 hektar olarak tutarlı görünse de, bireysel yangın alanları resmi kayıtlara göre ya abartılı ya da eksik; örneğin Çıldıkısık & Kayı'da 500 ha yerine ~55 ha.
- Yangınların çoğu Temmuz-Ağustos döneminde meydana geldi; rapor bazı tarihleri yanlış yerleştiriyor, bu da uydu analizlerini etkileyebilir.
- Resmi kaynaklar (OGM, AA, valilik) hızlı müdahaleleri vurguluyor, ancak topoğrafya zorluklarını belirtiyor; yangın nedenleri konusunda soruşturmalar devam ediyor, net sonuçlar sınırlı.

#### Yanlışlıkların Genel Bakışı
Rapor, Sentinel-2 verileriyle 7 kritik yangını analiz ediyor, ancak OGM saha kayıtları, AA haberleri ve valilik açıklamalarıyla karşılaştırma, tarih, alan ve ayrımda uyumsuzluklar ortaya koyuyor. Toplam hasar tutarlı, ancak segmentasyon yapay – bazı "ayrı" yangınlar tek olay.

#### Belirli Yanlışlıklar
Her yangın için rapor iddiaları ile doğrulanmış gerçekler karşılaştırıldığında şu hatalar öne çıkıyor:
- **Çıldıkısık & Kayı**: Rapor 500 ha diyor; gerçek ~55 ha.
- **Büyük Ovacık**: 1.413 ha; aslında ~5.796 ha orman + diğer.
- **Kışla**: Ayrı olay olarak 300 ha; aslında Büyük Ovacık'ın uzantısı.
- **Toprakcuma**: Kastamonu kökenli; aslında Karabük'te başladı.
- **Eflani & Güzelce**: 1.500 ha; birleşik ~2.736 ha.
- **Aladağ**: Temmuz; aslında Eylül başı.
- **Soğuksu & Kayacık**: Çoğunlukla doğru, ancak alan küçük (~11 dekar).

---

### Karabük 2025 Orman Yangınları Raporundaki Yanlışlıkların Kapsamlı Analizi

Bu inceleme, raporun Sentinel-2 uydu verileriyle yaptığı analizi, resmi kaynaklar (Orman Genel Müdürlüğü - OGM, Anadolu Ajansı - AA, Karabük Valiliği açıklamaları ve uluslararası raporlar gibi) ile karşılaştırarak hazırlanmıştır. Tutarsızlıklar esas olarak olay segmentasyonu, kronolojik doğruluk, mekansal atıf ve nicel tahminlerde görülmektedir. Raporun uzaktan algılama yöntemleri (dNDVI ve dNBR indisleri) metodolojik olarak sağlam olsa da, yanlış tarihli olaylara uygulanması güvenilirliği azaltmaktadır. Karabük'te 2025 toplam ekolojik hasarı 6.865,6 hektar olarak 36 olayda gerçekleşmiş; bu genel bilanço kaynaklarla uyumlu, ancak 7 "kritik bölge" ayrımı yapay.

#### Metodolojik Bağlam
Rapor, yangın öncesi (1-20 Temmuz) ve sonrası (5-30 Eylül) Sentinel-2 görüntülerini Google Earth Engine ile işleyerek dNDVI (vejetasyon kaybı) ve dNBR (yanma şiddeti) hesaplamış, OGM kayıtlarıyla %94-96 doğruluk iddia etmiştir. Ancak dış doğrulama, gerçek zamanlı saha verilerinin eksik entegrasyonu nedeniyle uydu tabanlı alan tahminlerinde hatalar gösteriyor. Örneğin, yanık izleri tarihler arası yanlış atfedilmiş olabilir, bireysel alanları şişirmiş. X (eski Twitter) postları müdahale hızını doğruluyor, ancak alan detayları resmi kaynaklarda daha net.

#### Her Yangın İçin Detaylı Yanlışlık Kırılımı
Yüksek çözünürlüklü Sentinel-2 görüntüleri üzerinden tanımlanan 7 bölge için rapor metrikleri, entegre edilmiş AA, OGM ve valilik raporlarıyla karşılaştırılmıştır. Aşağıda her biri için dNDVI ve dNBR metrikleri detaylandırılmış, ancak hatalar vurgulanmıştır.

1. **Çıldıkısık & Kayı (Merkez İlçe)**  
   - **Rapor İddiaları**: 22 Temmuz 2025 saat 16:32'de tespit, ~500 ha karaçam alanı, orta şiddet, wildland-urban interface riski.  
   - **Doğrulanmış Gerçekler**: 22 Temmuz 16:32'de Burunsuz Köyü'nde başladı, ~55 ha karaçam ormanı etkilendi, ertesi sabah kontrol altına alındı; 316 personel, 87 araç (helikopter dahil). Tahliye yok, hızlı müdahale.  
   - **Yanlışlıklar**: Alan aşırı tahmin edilmiş (500 ha vs. 55 ha); şiddet ve arayüz riski abartılı olabilir.  
   - **Etkileri**: Uydu alanı hesaplaması veya yakındaki olaylarla karıştırma şüphesi.

2. **Büyük Ovacık (Ovacık İlçe)**  
   - **Rapor İddiaları**: 23 Temmuz'da Safranbolu Çavuşlar'dan başlayıp Ovacık'a sıçrama, 1.413 ha, 7 gün aktif, 29 Temmuz kontrol; tahliyeler.  
   - **Doğrulanmış Gerçekler**: Soğanlıçay/Çavuşlar yangını, 23 Temmuz 14:51 başlangıç, 5.796,4 ha orman + 198,2 ha ağaçsız orman + 859,8 ha dışı; 29 Temmuz 12:30 kontrol, 25 Ağustos tam söndürme; 379 araç, 660 personel + destek. Karışık çam-meşe ormanlar, 19 köy tahliyesi, 1.839 kişi.  
   - **Yanlışlıklar**: Alan eksik (1.413 ha vs. ~6.854 ha toplam); ayrı olay olarak sunulmuş, ancak Temmuz mega-yangınının çekirdeği.  
   - **Etkileri**: Tek yanık izini segmentleme, mekansal varyasyon analizini bozuyor.

3. **Kışla (Ovacık İlçe)**  
   - **Rapor İddiaları**: 25 Temmuz Gökçedüz Akbıyık'ta başlangıç, Kışla'ya yayılım, 300 ha karma alan, 48 saat, 54 araç-213 personel; tarım etkisi.  
   - **Doğrulanmış Gerçekler**: 23 Temmuz ~16:00'da Kışla Pazaryeri'nde, Çavuşlar'ın uzantısı; büyük Soğanlıçay olayına entegre; başlangıçta helikopterler ve personel, sonra ölçeklendi; tahliyeler.  
   - **Yanlışlıklar**: Yanlış başlangıç tarihi (25 vs. 23 Temmuz); bağımsız olarak ele alınmış, ancak ana yangının dalı; alan ve kaynaklar büyük toplamda yutulmuş.  
   - **Etkileri**: Kronolojik hata, dNBR şiddet modellemesini etkileyebilir.

4. **Toprakcuma (Safranbolu İlçe)**  
   - **Rapor İddiaları**: Ağustos'ta Kastamonu'dan sıçrama, ~800 ha sınır ormanı, 10 Ağustos kontrol; sarp jeoloji, ikincil etkiler.  
   - **Doğrulanmış Gerçekler**: 31 Ağustos'ta Safranbolu Toprakcuma Harmancık/Aşağıgüney'de başlangıç; yerel yayılım, ~3 Eylül kontrol; helikopterler, arazözler, 45 personel; Kastamonu kökeni doğrulanmamış. Alan belirtilmemiş, muhtemelen küçük.  
   - **Yanlışlıklar**: Yanlış köken (Kastamonu'dan vs. Karabük'te); zaman aralığı hatalı (genel Ağustos vs. 31 Ağustos-3 Eylül).  
   - **Etkileri**: Yön atıfı hatası, rüzgar kaynaklı davranış analizini bozabilir; alan yakındaki Eflani ile örtüşebilir.

5. **Eflani & Güzelce**  
   - **Rapor İddiaları**: 31 Ağustos Saraycık İndere'de başlangıç, Güzelce tehdidi, 1.500 ha, 48 saat, 4 Eylül söndürme; 6 mahalle tahliyesi, yüksek biyoçeşitlilik kaybı.  
   - **Doğrulanmış Gerçekler**: 31 Ağustos Eflani'de başlangıç, 1 Eylül Kastamonu Araç (Güzelce)'ye yayılım; toplam 2.736 ha (2.078 ha orman + 658 ha tarım); 17 helikopter, 1 uçak, 30 arazöz vb., 594 personel; 7 köy + 1 mahalle tahliyesi (594 kişi, 1.046 hayvan). Aynı gün ayrı Akgeçit yangını ihmal edilmiş.  
   - **Yanlışlıklar**: Alan eksik (1.500 ha vs. 2.736 ha birleşik); süre doğru, ancak ölçek raporlanmamış.  
   - **Etkileri**: Biyoçeşitlilik iddiaları geçerli, ancak eksik ölçek yenilenme önceliklendirmesini etkiler.

6. **Aladağ (Safranbolu İlçe)**  
   - **Rapor İddiaları**: 27 Temmuz tetiklenme, ~400 ha sarp arazi, hava müdahalesi zorunlu, 28 Temmuz söndürme; yüksek şiddet, erozyon riski.  
   - **Doğrulanmış Gerçekler**: 2 Eylül 2025'te Aladağ/Kahyalar (Kabaoğlu Mahallesi)'de 15:26'da başlangıç; neden bilinmiyor; 5 helikopter, 101 araç, 379 personel; Kahyalar, Saitler (Güney/Horozlar) tahliyesi; Temmuz değil, ikinci yangın (bir ay arayla).  
   - **Yanlışlıklar**: Yanlış tarih (27-28 Temmuz vs. 2 Eylül); konum merkez ilçeye kaymış.  
   - **Etkileri**: Zaman uyumsuzluğu, Sentinel-2 öncesi/sonrası karşılaştırmalarını geçersiz kılar.

7. **Soğuksu & Kayacık (Merkez İlçe)**  
   - **Rapor İddiaları**: 5 Ağustos 15:00'te Soğan Tarlası'nda başlangıç, Soğuksu TOKİ ve Kayacık'a 500 m yaklaşma, 2.5 saatte kontrol; urban-wildland riski.  
   - **Doğrulanmış Gerçekler**: 5 Ağustos Soğuksu Soğan Tarlası/Melise Köyü'nde, ~2.5 saatte kontrol; 1 helikopter, 45 araç, 129 personel; ~11 dekar etkilendi; büyük kentsel yayılım yok.  
   - **Yanlışlıklar**: Küçük – konum ifadesi ("Soğan Tarlası" vs. "Soğan Tarlası/Melise"); alan raporda belirtilmemiş ama gerçekte küçük.  
   - **Etkileri**: En az hatalı; kentsel risk vurgusu kaynaklarla uyumlu.

#### Ana Metrikler ve Yanlışlık Tablosu

| Yangın Adı             | Rapor Başlangıç Tarihi | Gerçek Başlangıç Tarihi | Rapor Alanı (ha) | Gerçek Alan (ha) | Ana Hata Türü            |
|------------------------|-------------------------|--------------------------|------------------|------------------|--------------------------|
| Çıldıkısık & Kayı     | 22 Temmuz              | 22 Temmuz               | 500             | ~55             | Alan abartısı           |
| Büyük Ovacık          | 23 Temmuz              | 23 Temmuz               | 1.413           | ~5.796 (orman) + diğer | Alan eksikliği; segmentasyon |
| Kışla                 | 25 Temmuz              | 23 Temmuz               | 300             | Büyük olayda entegre | Tarih; bağımsız değil    |
| Toprakcuma            | Ağustos                | 31 Ağustos              | 800             | Belirtilmemiş (yerel) | Köken; tarih aralığı    |
| Eflani & Güzelce      | 31 Ağustos             | 31 Ağustos              | 1.500           | ~2.736 (birleşik) | Alan eksikliği          |
| Aladağ                | 27 Temmuz              | 2 Eylül                 | 400             | Belirtilmemiş (devam eden) | Tarih                   |
| Soğuksu & Kayacık     | 5 Ağustos              | 5 Ağustos               | Belirtilmemiş   | ~11 dekar       | Küçük (konum/alan)      |

#### Geniş Değerlendirme
Raporun motivasyonu – iklim kaynaklı yangın artışlarını haritalama – geçerli, ancak hatalar muhtemelen ön verilerden (8 Aralık 2025 tarihli) kaynaklanıyor. OGM bilanço önceliği saha doğrulaması, raporun uydu odaklı yaklaşımını zayıflatıyor. İnsan nedenleri gibi tartışmalı yönler (raporda detaylı değil) hakkında kamu kaynakları soruşturma belirtiyor, ancak sonuç yok. Öneriler: Gelecek analizler gerçek zamanlı OGM verilerini entegre etmeli. X postları müdahale hızını doğruluyor, ancak alan detayları resmi kaynaklarda.

**Ana Kaynaklar:**
- [KARABÜK'ÜN 2025 YILI ORMAN YANGINI BİLANÇOSU: 6 BİN 865 HEKTAR](https://www.karabuknethaber.com/karabukun-2025-yili-orman-yangini-bilancosu-6-bin-865-hektar)
- [Karabük Burunsuz Köyü'nde Çıkan Orman Yangını Büyük Oranda Kontrol Altına Alındı](http://www.karabuk.gov.tr/karabuk-burunsuz-koyunde-cikan-orman-yangini-buyuk-oranda-kontrol-altina-alindi)
- [[PDF] 2025 Yılı Eskişehir, Bilecik ve Karabük İllerinde Gerçekleşen Orman Yangınları](https://www.ormancilardernegi.org/Documents/496ea3e1-a87b-40f4-8b77-c92e99f44fcc.pdf)
- [Üç ildeki yangınlar kontrol altında, Karabük ve Kastamonu'da müdahale devam ediyor](https://www.aa.com.tr/tr/gundem/uc-ildeki-yanginlar-kontrol-altinda-karabuk-ve-kastamonuda-mudahale-devam-ediyor/3675827)
- [Karabük'te orman yangınlarının yol açtığı hasar görüntülendi](https://www.aa.com.tr/tr/gundem/karabukte-orman-yanginlarinin-yol-actigi-hasar-goruntulendi/3646027)
- [Yangın Bölgesinde Hayat Normale Dönüyor](http://www.karabuk.gov.tr/yangin-bolgesinde-hayat-normale-donuyor)
- [Ovacık ilçesi Kışla köyünde orman yangını devam ediyor](https://www.facebook.com/halktvcomtr/videos/ovac%C4%B1k-il%C3%A7esi-k%C4%B1%C5%9Fla-k%C3%B6y%C3%BCnde-orman-yang%C4%B1n%C4%B1-devam-ediyor/1050623343903611/)
- [Karabük / Safranbolu Toprakcuma tarafında Harmancık Köyü yakınlarında orman yangını başladı](https://www.facebook.com/tillakaraarslan/posts/karab%C3%BCk-safranbolu-toprakcuma-taraf%C4%B1nda-harmanc%C4%B1k-k%C3%B6y%C3%BC-yak%C4%B1nlar%C4%B1nda-orman-yang%C4%B1n/10162160959203195/)
- [Toprakcuma'da Orman Yangını Çıktı](https://www.kastamonugundemgazetesi.com/toprakcuma-da-orman-yangini-cikti/95698/)
- [Kahyalar Köyü iki yangın arasında kaldı: Dron ile böyle görüntülendi](https://www.ajanskarabuk.com/kahyalar-koyu-iki-yangin-arasinda-kaldi-dron-ile-boyle-goruntulendi/9371/)
- [Karabük'te orman yangınlarında zarar gören alanlar havadan görüntülendi](https://www.aa.com.tr/tr/yesilhat/dogal-yasam/karabukte-orman-yanginlarinda-zarar-goren-alanlar-havadan-goruntulendi/1827105)
- [Geçmiş olsun #Karabük Soğuksu Soğan Tarlası ve Melise Köyü mevkiindeki ormanlık alanda çıkan yangın](https://www.facebook.com/karabukbelediyesi/videos/ge%C3%A7mi%C5%9F-olsun-karab%C3%BCkso%C4%9Fuksu-so%C4%9Fan-tarlas%C4%B1-ve-melise-k%C3%B6y%C3%BC-mevkiindeki-ormanl%C4%B1k-al/1105020634341497/)
- [Geçmiş Olsun Karabük](https://www.karabuk.bel.tr/haber.asp?id=100668186)