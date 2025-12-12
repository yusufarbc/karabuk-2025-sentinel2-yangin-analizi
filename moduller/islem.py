"""
GEE İşlemleri Modülü
Sentinel-2 veri hazırlığı, indeks hesaplama (NDVI, NBR) ve değişim analizi (dNDVI, dNBR) işlevlerini içerir.
"""

from __future__ import annotations
import ee

def prepare_composite(aoi: ee.Geometry, start: str, end: str) -> ee.Image:
    """
    Belirtilen tarih ve alan için maskelenmiş Sentinel-2 medyan görüntüsü oluşturur.
    Sadece bulut ve su maskesi uygulanır.
    """
    def _mask(img):
        # QA60 Bulut Maskesi
        qa = img.select("QA60")
        cloud = (1 << 10)
        cirrus = (1 << 11)
        mask_cloud = qa.bitwiseAnd(cloud).eq(0).And(qa.bitwiseAnd(cirrus).eq(0))
        
        # SCL Su Maskesi (SCL=6 sudur)
        scl = img.select("SCL")
        mask_water = scl.eq(6).Not()
        
        return img.updateMask(mask_cloud).updateMask(mask_water)

    col = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate(start, end)
        .filterBounds(aoi)
        .map(_mask)
    )
    
    return col.median().clip(aoi)


def with_indices(img: ee.Image) -> ee.Image:
    """
    Görüntüye NDVI ve NBR indekslerini ekler.
    
    NDVI = (NIR - RED) / (NIR + RED)
    NBR = (NIR - SWIR2) / (NIR + SWIR2)
    """
    red = img.select("B4").toFloat()
    nir = img.select("B8").toFloat()
    swir2 = img.select("B12").toFloat()
    eps = 1e-6
    
    ndvi = nir.subtract(red).divide(nir.add(red).add(eps)).rename("NDVI")
    nbr = nir.subtract(swir2).divide(nir.add(swir2).add(eps)).rename("NBR")
    
    return img.addBands([ndvi, nbr])


def compute_diffs(pre: ee.Image, post: ee.Image) -> dict:
    """
    Değişim analizini hesaplar (dNDVI, dNBR).
    
    dNDVI = Post - Pre (Vejetasyon kaybı negatif)
    dNBR = Pre - Post (Yanıklık şiddeti pozitif)
    """
    dndvi = post.select("NDVI").subtract(pre.select("NDVI")).rename("dNDVI")
    dnbr = pre.select("NBR").subtract(post.select("NBR")).rename("dNBR")
    return {"dNDVI": dndvi, "dNBR": dnbr}
