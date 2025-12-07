from __future__ import annotations

import ee


def _mask_s2_sr(image: ee.Image) -> ee.Image:
    """Sentinel-2 SR için basit bulut/cirrus maskesi (QA60 bit 10/11)."""
    qa = image.select("QA60")
    cloud_bit = 1 << 10
    cirrus_bit = 1 << 11
    mask = qa.bitwiseAnd(cloud_bit).eq(0).And(qa.bitwiseAnd(cirrus_bit).eq(0))
    return image.updateMask(mask)


def _mask_scl_water_and_shadows(image: ee.Image) -> ee.Image:
    """S2 SCL kullanarak su ve bulut gölgelerini maskele (opsiyonel).

    SCL sınıfları (yaygın): 6=Su, 3=Bulut gölgesi, 8=Orta olasılıklı bulut, 9=Yüksek olasılıklı bulut, 10=İnce cirrus.
    Burada sadece suyu maskeliyoruz; bulutlar yukarıda QA60 ile halledildi.
    """
    scl = image.select("SCL")
    water = scl.eq(6)
    # Mask out water
    return image.updateMask(water.Not())


def prepare_composite(aoi: ee.Geometry, start: str, end: str) -> ee.Image:
    """Tarih aralığı için AOI'ye göre kesilmiş medyan Sentinel-2 SR kompoziti hazırlar.

    QA60 bulut/cirrus maskesi ve SCL tabanlı su maskesi uygular.
    """
    col = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate(start, end)
        .filterBounds(aoi)
        .map(_mask_s2_sr)
        .map(_mask_scl_water_and_shadows)
    )
    # Median almadan önce koleksiyon boyutunu kontrol et
    # (Boşsa hata verebilir, ama pipeline içinde try-catch var)
    
    # Kompozit oluştur
    img = col.median().clip(aoi)

    # Görüntülerin tarih aralığını metadata olarak ekle
    # Gerçek piksel tarihi piksel bazında değişir (mosaic), 
    # bu yüzden genel analiz aralığını not düşüyoruz.
    img = img.set({
        "system:time_start": ee.Date(start).millis(),
        "date_range": f"{start}_{end}"
    })
    return img
