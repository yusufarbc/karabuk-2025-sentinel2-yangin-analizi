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
        aoi_geojson: AOI GeoJSON yolu (yoksa varsayılan Karabük bbox veya "KARABUK_PROVINCE")
        out_dir: Çıktı klasörü
        project: (opsiyonel) GEE proje ID
        area_scale: Alan hesapları için çözünürlük (metre)
        dnbr_thresholds: Opsiyonel dNBR eşikleri (t0,t1,t2,t3)
        min_patch_ha: Opsiyonel minimum yama alanı (hektar). Bu eşik altındaki yanık yamaları kaldırılır.
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
    burnable = pre.select("NDVI").gt(0.25)
    mask = burnable

    # Karabük iç bölge olduğu için kıyı tamponu uygulanmaz

    dnbr_masked = diffs["dNBR"].updateMask(mask)
    severity_raw = classify_dnbr(dnbr_masked, thresholds=dnbr_thresholds)  # 0..4

    # Gürültü azaltma: Çıktıyı yumuşatmak için 1.5 piksellik çoğunluk (majority) filtresi uygula
    # Bu işlem 'salt and pepper' (tekil piksel) gürültüsünü temizler.
    severity = severity_raw.focal_mode(radius=1.5, kernelType='circle', iterations=1).updateMask(mask)

    # Yangın Bölgelerini Belirle (Fire Zone Estimation)
    # Şiddeti yüksek (3 ve 4) olan alanları birleştirip bir bounding box çıkaracağız.
    high_severity_mask = severity.gte(3)
    fire_vectors = high_severity_mask.reduceToVectors(
        geometry=aoi,
        scale=30,
        maxPixels=1e9,
        eightConnected=True,
        tileScale=4
    )
    # En büyük yangın alanını bulmak isterseniz feature collection üzerinde işlem yapabilirsiniz.
    # Şimdilik tüm yüksek şiddetli alanları kapsayan bir bounding box alalım.
    fire_zone_bbox_geom = fire_vectors.geometry().bounds()
    # Eğer hiç alan yoksa (boşsa), None dönebilir, kontrol edelim.
    # info = fire_zone_bbox_geom.coordinates().getInfo() # Bunu burada yapmak istemeyiz, lazy kalsın
    # Ancak pipeline çıktısı olarak koordinatları dönmek istiyoruz.


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
    save_folium(pre, aoi, vp["RGB"], f"Oncesi RGB {pre_label}", outputs["pre_rgb_map"])

    outputs["post_rgb_map"] = os.path.join(out_dir, f"post_RGB_{post_start}_{post_end}.html")
    save_folium(post, aoi, vp["RGB"], f"Sonrasi RGB {post_label}", outputs["post_rgb_map"])

    outputs["pre_ndvi_map"] = os.path.join(out_dir, "pre_NDVI.html")
    save_folium(pre.select("NDVI"), aoi, vp["NDVI"], f"Oncesi NDVI {pre_label}", outputs["pre_ndvi_map"])

    outputs["post_ndvi_map"] = os.path.join(out_dir, "post_NDVI.html")
    save_folium(post.select("NDVI"), aoi, vp["NDVI"], f"Sonrasi NDVI {post_label}", outputs["post_ndvi_map"])

    outputs["pre_nbr_map"] = os.path.join(out_dir, "pre_NBR.html")
    save_folium(pre.select("NBR"), aoi, vp["NBR"], f"Oncesi NBR {pre_label}", outputs["pre_nbr_map"])

    outputs["post_nbr_map"] = os.path.join(out_dir, "post_NBR.html")
    save_folium(post.select("NBR"), aoi, vp["NBR"], f"Sonrasi NBR {post_label}", outputs["post_nbr_map"])

    outputs["dndvi_map"] = os.path.join(out_dir, "dNDVI.html")
    save_folium(diffs["dNDVI"].updateMask(mask), aoi, vp["dNDVI"], f"dNDVI {pre_label} vs {post_label}", outputs["dndvi_map"])

    outputs["dnbr_map"] = os.path.join(out_dir, "dNBR.html")
    save_folium(dnbr_masked, aoi, vp["dNBR"], f"dNBR {pre_label} vs {post_label}", outputs["dnbr_map"])

    outputs["severity_map"] = os.path.join(out_dir, "severity.html")
    save_folium(severity, aoi, vp["severity"], f"dNBR Severity {pre_label} vs {post_label}", outputs["severity_map"])

    # PNG Ciktilari (Rapor icin)
    png_outs = export_report_pngs(pre=pre, post=post, diffs=diffs, severity=severity, aoi=aoi, out_dir=out_dir)
    outputs.update(png_outs)
    
    # Dogal Renk PNGleri
    rgb_outs = export_truecolor_pngs(pre=pre, post=post, aoi=aoi, out_dir=out_dir)
    outputs.update(rgb_outs)

    # Özet istatistikler
    summary = {
        "analiz_donemi_oncesi": f"{pre_start} - {pre_end}",
        "analiz_donemi_sonrasi": f"{post_start} - {post_end}",
        "oncesi_ortalama_NDVI": reduce_mean(pre, aoi, "NDVI"),
        "sonrasi_ortalama_NDVI": reduce_mean(post, aoi, "NDVI"),
        "ortalama_dNDVI": reduce_mean(diffs["dNDVI"], aoi, "dNDVI"),
        "ortalama_dNBR": reduce_mean(diffs["dNBR"], aoi, "dNBR"),
    }
    outputs["summary_csv"] = os.path.join(out_dir, "summary_stats.csv")
    write_summary_csv(outputs["summary_csv"], summary)

    # Severity alan istatistikleri ve toplam yanmış alan
    areas = compute_severity_areas(severity, aoi, scale=area_scale)
    outputs["severity_areas_csv"] = os.path.join(out_dir, "severity_areas.csv")
    write_kv_csv(outputs["severity_areas_csv"], areas)

    try:
        # Sunucu tarafında hesaplatıp koordinatları alalım
        fz_info = fire_zone_bbox_geom.coordinates().getInfo()
        # GeoJSON polygon coords: [ [ [x,y], [x,y], ... ] ]
        # Biz bunu basitçe list olarak döndürelim
        outputs["fire_zone_bbox"] = fz_info
    except Exception:
        # Yangin tespit edilemediyse veya sunucu zamani asimi olursa sessizce gec
        outputs["fire_zone_bbox"] = None
        outputs["fire_zone_bbox"] = None

    return outputs
