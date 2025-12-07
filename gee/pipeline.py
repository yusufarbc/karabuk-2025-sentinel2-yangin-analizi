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
from .change import compute_diffs, classify_dnbr
from .visualize import (
    vis_params,
    save_folium,
    reduce_mean,
    write_summary_csv,
    compute_severity_areas,

    write_kv_csv,
    export_report_pngs,
    export_truecolor_pngs,
    export_severity_rgb_overlay,
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

    # Yanabilir bitki örtüsü (burnable vegetation): kıyı/su kontrolleri olmadan maske (Karabük iç bölge)
    # Yanabilir bitki örtüsü (burnable vegetation): kıyı/su kontrolleri olmadan maske (Karabük iç bölge)
    burnable = pre.select("NDVI").gt(0.25)
    mask = burnable

    # Gürültü Azaltma (Noise Reduction)
    # 1. dNBR verisini yumuşat (median filtre) - Tekil piksel hatalarını giderir. Radius artırıldı (2.0)
    dnbr_smooth = diffs["dNBR"].focal_median(radius=2.0, kernelType='circle', iterations=1)

    # 2. dNBR Görselleştirmesi için Maskeleme
    # Normalde mask değişkeni sadece Yanabilir Bitki Örtüsünü (NDVI > 0.25) içerir.
    # Ancak görsel harita (dnbr_masked) için gürültüleri atmak istiyoruz.
    
    # Eşik: 0.1 (Düşük Şiddet Başlangıcı). Bunun altı "Yanmamış" kabul edilir ve haritada gösterilmez.
    significant_change = dnbr_smooth.gt(0.1)
    
    # Speckle Filtering: En az 3 bağlantılı piksel kuralı
    cpc = significant_change.connectedPixelCount(maxSize=100, eightConnected=True)
    is_large_enough = cpc.gte(3)
    
    # Temiz Maske: (Bitki Örtüsü VAR) VE (Değişim > 0.1) VE (Yeterince Büyük Yama)
    dnbr_vis_mask = mask.And(significant_change).And(is_large_enough)

    dnbr_masked = dnbr_smooth.updateMask(dnbr_vis_mask)
    severity = None
    fire_zone_bbox_geom = None

    if not skip_severity:
        # Severity hesapla (0..4)
        severity_raw = classify_dnbr(dnbr_masked, thresholds=dnbr_thresholds) 

        # Gürültü azaltma: Çıktıyı yumuşatmak için MOD filtresi uygula. Radius artırıldı (2.5) daha homojen alanlar için.
        severity = severity_raw.focal_mode(radius=2.5, kernelType='circle', iterations=1)
        
        # Kritik Adım: dNBR Haritası için uyguladığımız katı temizlik maskesini (dnbr_vis_mask) Severity haritasına da uygula.
        # Böylece (değişim < 0.1) veya (çok küçük, <3 piksel) olan gürültüler Severity haritasından da silinir.
        severity = severity.updateMask(dnbr_vis_mask)

        # Yangın Bölgelerini Belirle (Fire Zone Estimation)
        # Şiddeti yüksek (3 ve 4) olan alanları birleştirip bir bounding box çıkaracağız.
        high_severity_mask = severity.gte(3)
        fire_vectors = high_severity_mask.reduceToVectors(
            geometry=aoi,
            scale=30,
            maxPixels=1e9,
            eightConnected=True,
            tileScale=8
        )
        # Bounding box hesapla (Analiz için odak bölgesi)
        fire_zone_bbox_geom = fire_vectors.geometry().bounds()


        # Opsiyonel minimum yama alanı filtresi (yanmış sınıflar > 0)
        if min_patch_ha and min_patch_ha > 0:
            burn_mask = severity.gt(0)
            # Bağlantılı piksel sayısı (8-komşuluk)
            cpc = burn_mask.connectedPixelCount(maxSize=1024, eightConnected=True)
            px_area = ee.Image.pixelArea()
            comp_area_m2 = cpc.multiply(px_area)
            keep = comp_area_m2.gte(min_patch_ha * 10000.0)
            # Yanmamış veya büyük yanmış alanları tut
            keep_mask = burn_mask.And(keep).Or(severity.eq(0))
            severity = severity.updateMask(keep_mask)

    vp = vis_params()
    os.makedirs(out_dir, exist_ok=True)

    outputs: Dict[str, str] = {}
    pre_label = f"{pre_start}-{pre_end}"
    post_label = f"{post_start}-{post_end}"

    # Haritalar (Maps)
    outputs["pre_rgb_map"] = os.path.join(out_dir, f"pre_RGB_{pre_start}_{pre_end}.html")
    save_folium(pre, aoi, vp["RGB"], f"Oncesi RGB {pre_label}", outputs["pre_rgb_map"], boundary=overlay_boundary)

    outputs["post_rgb_map"] = os.path.join(out_dir, f"post_RGB_{post_start}_{post_end}.html")
    save_folium(post, aoi, vp["RGB"], f"Sonrasi RGB {post_label}", outputs["post_rgb_map"], boundary=overlay_boundary)

    outputs["pre_ndvi_map"] = os.path.join(out_dir, "pre_NDVI.html")
    save_folium(pre.select("NDVI"), aoi, vp["NDVI"], f"Oncesi NDVI {pre_label}", outputs["pre_ndvi_map"], boundary=overlay_boundary)

    outputs["post_ndvi_map"] = os.path.join(out_dir, "post_NDVI.html")
    save_folium(post.select("NDVI"), aoi, vp["NDVI"], f"Sonrasi NDVI {post_label}", outputs["post_ndvi_map"], boundary=overlay_boundary)

    outputs["pre_nbr_map"] = os.path.join(out_dir, "pre_NBR.html")
    save_folium(pre.select("NBR"), aoi, vp["NBR"], f"Oncesi NBR {pre_label}", outputs["pre_nbr_map"], boundary=overlay_boundary)

    outputs["post_nbr_map"] = os.path.join(out_dir, "post_NBR.html")
    save_folium(post.select("NBR"), aoi, vp["NBR"], f"Sonrasi NBR {post_label}", outputs["post_nbr_map"], boundary=overlay_boundary)

    outputs["dndvi_map"] = os.path.join(out_dir, "dNDVI.html")
    save_folium(diffs["dNDVI"].updateMask(mask), aoi, vp["dNDVI"], f"dNDVI {pre_label} vs {post_label}", outputs["dndvi_map"], boundary=overlay_boundary)

    outputs["dnbr_map"] = os.path.join(out_dir, "dNBR.html")
    save_folium(dnbr_masked, aoi, vp["dNBR"], f"dNBR {pre_label} vs {post_label}", outputs["dnbr_map"], boundary=overlay_boundary)

    if severity:
        outputs["severity_map"] = os.path.join(out_dir, "severity.html")
        save_folium(severity, aoi, vp["severity"], f"dNBR Severity {pre_label} vs {post_label}", outputs["severity_map"], boundary=overlay_boundary)

    # PNG Ciktilari (Rapor icin)
    png_outs = export_report_pngs(pre=pre, post=post, diffs=diffs, severity=severity, aoi=aoi, out_dir=out_dir, boundary=overlay_boundary)
    outputs.update(png_outs)
    
    # Dogal Renk PNGleri
    rgb_outs = export_truecolor_pngs(pre=pre, post=post, aoi=aoi, out_dir=out_dir, boundary=overlay_boundary)
    outputs.update(rgb_outs)

    # Severity + RGB Overlay (Yeni)
    if severity:
        overlay_out = export_severity_rgb_overlay(post=post, severity=severity, aoi=aoi, out_dir=out_dir, boundary=overlay_boundary)
        outputs.update(overlay_out)

    # Özet istatistikler
    summary_rows = {
        "analiz_donemi_oncesi": f"{pre_start} - {pre_end}",
        "analiz_donemi_sonrasi": f"{post_start} - {post_end}",
        "oncesi_ortalama_NDVI": reduce_mean(pre, aoi, "NDVI", scale=area_scale),
        "sonrasi_ortalama_NDVI": reduce_mean(post, aoi, "NDVI", scale=area_scale),
        "ortalama_dNDVI": reduce_mean(diffs["dNDVI"], aoi, "dNDVI", scale=area_scale),
        "ortalama_dNBR": reduce_mean(diffs["dNBR"], aoi, "dNBR", scale=area_scale),
    }

    if severity:
        sev_areas = compute_severity_areas(severity, aoi, scale=area_scale)
        summary_rows.update(sev_areas)

    outputs["summary_csv"] = os.path.join(out_dir, "summary_stats.csv")
    write_summary_csv(outputs["summary_csv"], summary_rows)

    if fire_zone_bbox_geom:
        try:
            outputs["fire_zone_bbox"] = fire_zone_bbox_geom.coordinates().getInfo()
        except Exception:
            outputs["fire_zone_bbox"] = None
        outputs["fire_zone_bbox"] = None

    return outputs
