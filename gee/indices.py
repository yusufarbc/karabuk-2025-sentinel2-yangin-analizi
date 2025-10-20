from __future__ import annotations

import ee


def with_indices(img: ee.Image) -> ee.Image:
    """Girdi Sentinel-2 görüntüsüne NDVI, NBR, NDWI, MNDWI bantlarını ekler.

    Bant eşlemleri (Sentinel-2 SR):
      - Kırmızı (Red): B4
      - Yeşil (Green): B3
      - NIR: B8
      - SWIR1: B11
      - SWIR2: B12
    """
    red = img.select("B4").toFloat()
    green = img.select("B3").toFloat()
    nir = img.select("B8").toFloat()
    swir1 = img.select("B11").toFloat()
    swir2 = img.select("B12").toFloat()

    # Küçük sayı ile payda stabilizasyonu
    eps = ee.Image.constant(1e-6)

    ndvi = nir.subtract(red).divide(nir.add(red).add(eps)).rename("NDVI")
    nbr = nir.subtract(swir2).divide(nir.add(swir2).add(eps)).rename("NBR")
    ndwi = green.subtract(nir).divide(green.add(nir).add(eps)).rename("NDWI")
    mndwi = green.subtract(swir1).divide(green.add(swir1).add(eps)).rename("MNDWI")

    return img.addBands([ndvi, nbr, ndwi, mndwi])

