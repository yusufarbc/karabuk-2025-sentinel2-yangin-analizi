"""Uçtan uca analiz hattı (pipeline) - yalnızca `gee.*` modülleri ile.

Kullanım (notebook içinde):
    from gee.pipeline import run_pipeline
    outputs = run_pipeline(
        pre_start="2024-06-01", pre_end="2024-07-01",
        post_start="2024-07-15", post_end="2024-08-15",
        aoi_geojson="aoi.geojson",  # opsiyonel, yoksa Karabük bbox (veya "KARABUK_PROVINCE") kullanılır
        out_dir="results", project=None,
    )
"""

from __future__ import annotations

from typing import Dict, Optional
import os

import ee

from .utils import ee_init
from .aoi import get_aoi
from .preprocess import prepare_composite
from .indices import with_indices
from .change import compute_diffs
from .visualize import (
    vis_params,
    save_folium,
    export_report_pngs,
    export_truecolor_pngs,
)


def run_pipeline(
    pre_start: str,
    pre_end: str,
    post_start: str,
    post_end: str,
    aoi_geojson: str = "aoi.geojson",
    out_dir: str = "results",
    project: Optional[str] = None,
    area_scale: int = 10,
    dnbr_thresholds: Optional[tuple[float, float, float, float]] = None,
    min_patch_ha: Optional[float] = None,
    skip_severity: bool = False,
    overlay_boundary: Optional[ee.Geometry] = None,
) -> Dict[str, str]:
    """Analizi çalıştır ve çıktı dosya yollarını döndür.

    Args:
        pre_start: Ön dönem başlangıç tarihi (YYYY-MM-DD)
        pre_end: Ön dönem bitiş tarihi (YYYY-MM-DD)
        post_start: Sonraki dönem başlangıç tarihi
        post_end: Sonraki dönem bitiş tarihi
        aoi_geojson: AOI GeoJSON yolu (yoksa varsayılan Karabük bbox veya "KARABUK_PROVINCE")
        out_dir: Çıktı klasörü
        project: (opsiyonel) GEE proje ID
        area_scale: Alan hesapları için çözünürlük (metre)
        dnbr_thresholds: Opsiyonel dNBR eşikleri (t0,t1,t2,t3)
        min_patch_ha: Opsiyonel minimum yama alanı (hektar). Bu eşik altındaki yanık yamaları kaldırılır.
        skip_severity: Eğer True ise, bellek yoğun sınıflandırma ve severity harita üretimini atlar (sadece dNBR/dNDVI).
    Returns:
        Üretilen haritalar ve CSV'lerin dosya yolları. Ayrıca "fire_zone_bbox" anahtarı ile ana yangın bölgesinin sınırlarını (list) döndürür.
    """
    ee_init(project)
    aoi = get_aoi(aoi_geojson)

    # Medyan kompozitleri hazırla
    pre_img = prepare_composite(aoi, pre_start, pre_end)
    post_img = prepare_composite(aoi, post_start, post_end)

    # Görüntülerin boş olup olmadığını kontrol et (Bulut filtresi vb. nedeniyle)
    # Not: getInfo() sunucu çağrısı yapar ancak hata ayıklama için kritiktir.
    if pre_img.bandNames().size().getInfo() == 0:
        raise ValueError(f"Ön dönem ({pre_start} - {pre_end}) için belirtilen alanda uygun Sentinel-2 görüntüsü bulunamadı (Tüm görüntüler bulutlu olabilir).")
    
    if post_img.bandNames().size().getInfo() == 0:
        raise ValueError(f"Son dönem ({post_start} - {post_end}) için belirtilen alanda uygun Sentinel-2 görüntüsü bulunamadı.")

    # İndeksleri hesapla
    pre = with_indices(pre_img)
    post = with_indices(post_img)

    diffs = compute_diffs(pre, post)

    wc = ee.ImageCollection("ESA/WorldCover/v200").first()
    mask_forest = wc.eq(10)
    mask_shrub = wc.eq(20)

    landcover_mask = mask_forest.Or(mask_shrub)
    
    vegetation_mask = landcover_mask
    

    severity = None
    fire_zone_bbox_geom = None



    vp = vis_params()
    os.makedirs(out_dir, exist_ok=True)

    outputs: Dict[str, str] = {}
    pre_label = f"{pre_start}-{pre_end}"
    post_label = f"{post_start}-{post_end}"


    # Haritalar - Çıktılar

    outputs["pre_rgb_map"] = os.path.join(out_dir, f"pre_RGB_{pre_start}_{pre_end}.html")
    save_folium(pre, aoi, vp["RGB"], f"Oncesi RGB {pre_label}", outputs["pre_rgb_map"], boundary=overlay_boundary)

    outputs["post_rgb_map"] = os.path.join(out_dir, f"post_RGB_{post_start}_{post_end}.html")
    save_folium(post, aoi, vp["RGB"], f"Sonrasi RGB {post_label}", outputs["post_rgb_map"], boundary=overlay_boundary)

    outputs["dndvi_map"] = os.path.join(out_dir, "dNDVI.html")
    save_folium(diffs["dNDVI"].updateMask(vegetation_mask), aoi, vp["dNDVI"], f"dNDVI {pre_label} vs {post_label}", outputs["dndvi_map"], boundary=overlay_boundary)

    outputs["dnbr_map"] = os.path.join(out_dir, "dNBR.html")
    save_folium(diffs["dNBR"].updateMask(vegetation_mask), aoi, vp["dNBR"], f"dNBR {pre_label} vs {post_label}", outputs["dnbr_map"], boundary=overlay_boundary)

    # PNG Çıktıları

    png_outs = export_report_pngs(pre=pre, post=post, diffs=diffs, severity=severity, aoi=aoi, out_dir=out_dir, boundary=overlay_boundary)
    outputs.update(png_outs)
    
    rgb_outs = export_truecolor_pngs(pre=pre, post=post, aoi=aoi, out_dir=out_dir, boundary=overlay_boundary)

    outputs.update(rgb_outs)

   

    if fire_zone_bbox_geom:
        try:
            outputs["fire_zone_bbox"] = fire_zone_bbox_geom.coordinates().getInfo()
        except Exception:
            outputs["fire_zone_bbox"] = None
        outputs["fire_zone_bbox"] = None

    return outputs
