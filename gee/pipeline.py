"""Uçtan uca analiz hattı (pipeline) - yalnızca `gee.*` modülleri ile.

Kullanım (notebook içinde):
    from gee.pipeline import run_pipeline
    outputs = run_pipeline(
        pre_start="2024-06-01", pre_end="2024-07-01",
        post_start="2024-07-15", post_end="2024-08-15",
        aoi_geojson="aoi.geojson",  # opsiyonel, yoksa Karabük bbox kullanılır
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
from .change import compute_diffs, classify_dnbr
from .visualize import (
    vis_params,
    save_folium,
    reduce_mean,
    write_summary_csv,
    compute_severity_areas,
    write_kv_csv,
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
) -> Dict[str, str]:
    """Analizi çalıştır ve çıktı dosya yollarını döndür.

    Args:
        pre_start: Ön dönem başlangıç tarihi (YYYY-MM-DD)
        pre_end: Ön dönem bitiş tarihi (YYYY-MM-DD)
        post_start: Sonraki dönem başlangıç tarihi
        post_end: Sonraki dönem bitiş tarihi
        aoi_geojson: AOI GeoJSON yolu (yoksa varsayılan Karabük bbox)
        out_dir: Çıktı klasörü
        project: (opsiyonel) GEE proje ID
        area_scale: Alan hesapları için çözünürlük (metre)
        dnbr_thresholds: Opsiyonel dNBR eşikleri (t0,t1,t2,t3)
        min_patch_ha: Opsiyonel minimum yama alanı (hektar). Bu eşik altındaki yanık yamaları kaldırılır.
    Returns:
        Üretilen haritalar ve CSV'lerin dosya yolları.
    """
    ee_init(project)
    aoi = get_aoi(aoi_geojson)

    # Prepare median composites and indices
    pre = with_indices(prepare_composite(aoi, pre_start, pre_end))
    post = with_indices(prepare_composite(aoi, post_start, post_end))

    diffs = compute_diffs(pre, post)

    # Burnable vegetation: kıyı/su kontrolleri olmadan maske (Karabük iç bölge)
    burnable = pre.select("NDVI").gt(0.25)
    mask = burnable

    # Karabük iç bölge olduğu için kıyı tamponu uygulanmaz

    dnbr_masked = diffs["dNBR"].updateMask(mask)
    severity = classify_dnbr(dnbr_masked, thresholds=dnbr_thresholds)  # 0..4

    # Optional minimum patch area filter on burned classes (>0)
    if min_patch_ha and min_patch_ha > 0:
        burn_mask = severity.gt(0)
        # Connected pixel count (8-connected)
        cpc = burn_mask.connectedPixelCount(maxSize=4096, eightConnected=True)
        px_area = ee.Image.pixelArea()
        comp_area_m2 = cpc.multiply(px_area)
        keep = comp_area_m2.gte(min_patch_ha * 10000.0)
        # Keep unburned or burned-and-large
        keep_mask = burn_mask.And(keep).Or(severity.eq(0))
        severity = severity.updateMask(keep_mask)

    vp = vis_params()
    os.makedirs(out_dir, exist_ok=True)

    outputs: Dict[str, str] = {}
    pre_label = f"{pre_start}-{pre_end}"
    post_label = f"{post_start}-{post_end}"

    # Maps
    outputs["pre_rgb_map"] = os.path.join(out_dir, f"pre_RGB_{pre_start}_{pre_end}.html")
    save_folium(pre, aoi, vp["RGB"], f"Pre RGB {pre_label}", outputs["pre_rgb_map"])

    outputs["post_rgb_map"] = os.path.join(out_dir, f"post_RGB_{post_start}_{post_end}.html")
    save_folium(post, aoi, vp["RGB"], f"Post RGB {post_label}", outputs["post_rgb_map"])

    outputs["pre_ndvi_map"] = os.path.join(out_dir, "pre_NDVI.html")
    save_folium(pre.select("NDVI"), aoi, vp["NDVI"], f"Pre NDVI {pre_label}", outputs["pre_ndvi_map"])

    outputs["post_ndvi_map"] = os.path.join(out_dir, "post_NDVI.html")
    save_folium(post.select("NDVI"), aoi, vp["NDVI"], f"Post NDVI {post_label}", outputs["post_ndvi_map"])

    outputs["pre_nbr_map"] = os.path.join(out_dir, "pre_NBR.html")
    save_folium(pre.select("NBR"), aoi, vp["NBR"], f"Pre NBR {pre_label}", outputs["pre_nbr_map"])

    outputs["post_nbr_map"] = os.path.join(out_dir, "post_NBR.html")
    save_folium(post.select("NBR"), aoi, vp["NBR"], f"Post NBR {post_label}", outputs["post_nbr_map"])

    outputs["dndvi_map"] = os.path.join(out_dir, "dNDVI.html")
    save_folium(diffs["dNDVI"].updateMask(mask), aoi, vp["dNDVI"], f"dNDVI {pre_label} vs {post_label}", outputs["dndvi_map"])

    outputs["dnbr_map"] = os.path.join(out_dir, "dNBR.html")
    save_folium(dnbr_masked, aoi, vp["dNBR"], f"dNBR {pre_label} vs {post_label}", outputs["dnbr_map"])

    outputs["severity_map"] = os.path.join(out_dir, "severity.html")
    save_folium(severity, aoi, vp["severity"], f"dNBR Severity {pre_label} vs {post_label}", outputs["severity_map"])

    # Summary stats
    summary = {
        "pre_mean_NDVI": reduce_mean(pre, aoi, "NDVI"),
        "post_mean_NDVI": reduce_mean(post, aoi, "NDVI"),
        "mean_dNDVI": reduce_mean(diffs["dNDVI"], aoi, "dNDVI"),
        "mean_dNBR": reduce_mean(diffs["dNBR"], aoi, "dNBR"),
    }
    outputs["summary_csv"] = os.path.join(out_dir, "summary_stats.csv")
    write_summary_csv(outputs["summary_csv"], summary)

    # Severity alan istatistikleri ve toplam yanmış alan
    areas = compute_severity_areas(severity, aoi, scale=area_scale)
    outputs["severity_areas_csv"] = os.path.join(out_dir, "severity_areas.csv")
    write_kv_csv(outputs["severity_areas_csv"], areas)

    return outputs
