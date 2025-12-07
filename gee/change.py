from __future__ import annotations

import ee


def compute_diffs(pre: ee.Image, post: ee.Image) -> dict:
    """Fark görüntülerini hesapla (Compute difference images).

    dNDVI = post - pre (vejetasyon düşüşleri negatif)
    dNBR  = pre - post (yanıklık artışı pozitif)
    """
    dndvi = post.select("NDVI").subtract(pre.select("NDVI")).rename("dNDVI")
    dnbr = pre.select("NBR").subtract(post.select("NBR")).rename("dNBR")
    return {"dNDVI": dndvi, "dNBR": dnbr}


def classify_dnbr(
    dnbr: ee.Image,
    thresholds: tuple[float, float, float, float] | None = None,
) -> ee.Image:
    """dNBR'yi şiddet sınıflarına (0..4) ayırır.

    thresholds: opsiyonel (t0, t1, t2, t3). Varsayılan USGS-benzeri:
      < 0.10: 0 (Yanmamış/Düşük)
      0.10–0.27: 1 (Düşük)
      0.27–0.44: 2 (Orta-Düşük)
      0.44–0.66: 3 (Orta-Yüksek)
      > 0.66: 4 (Yüksek)
    """
    if thresholds is None:
        t0, t1, t2, t3 = 0.10, 0.27, 0.44, 0.66
    else:
        t0, t1, t2, t3 = thresholds

    c0 = dnbr.lt(t0)
    c1 = dnbr.gte(t0).And(dnbr.lt(t1))
    c2 = dnbr.gte(t1).And(dnbr.lt(t2))
    c3 = dnbr.gte(t2).And(dnbr.lt(t3))
    c4 = dnbr.gte(t3)

    classified = (
        c0.multiply(0)
        .add(c1.multiply(1))
        .add(c2.multiply(2))
        .add(c3.multiply(3))
        .add(c4.multiply(4))
        .rename("severity")
        .toUint8()
    )
    return classified

