"""
Akış Modülü
Analiz sürecini yöneten ana pipeline fonksiyonunu içerir.
"""

import os
import ee
from typing import Dict, Optional

from .araclar import ee_init, get_aoi
from .islem import prepare_composite, with_indices, compute_diffs
from .gorsellestirme import vis_params, save_folium, export_maps

def run_pipeline(
    pre_start: str,
    pre_end: str,
    post_start: str,
    post_end: str,
    aoi_geojson: str = "aoi.geojson",
    out_dir: str = "sonuclar",
    project: Optional[str] = None,
    area_scale: int = 10, # Rezerve, kullanılmıyor
    overlay_boundary: Optional[ee.Geometry] = None,
) -> Dict[str, str]:
    """
    Yangın analiz sürecini baştan sona çalıştırır.
    """
    # 1. Başlatma
    ee_init(project)
    aoi = get_aoi(aoi_geojson)
    
    # 2. Veri
    pre_img = prepare_composite(aoi, pre_start, pre_end)
    post_img = prepare_composite(aoi, post_start, post_end)
    
    if pre_img.bandNames().size().getInfo() == 0 or post_img.bandNames().size().getInfo() == 0:
        raise ValueError("Belirtilen tarihlerde uygun görüntü bulunamadı.")
        
    # 3. İndeks ve Analiz
    pre = with_indices(pre_img)
    post = with_indices(post_img)
    diffs = compute_diffs(pre, post)
    
    # Orman Maskesi
    wc = ee.ImageCollection("ESA/WorldCover/v200").first()
    vegetation_mask = wc.eq(10).Or(wc.eq(20)) # Ağaç ve Çalılık
    
    # 4. Çıktı Üretimi
    vp = vis_params()
    outputs = {}
    
    # PNG İndirme
    outputs = export_maps(pre, post, diffs, aoi, out_dir, overlay_boundary)
    
    # HTML Kaydetme
    labels = {"pre": f"{pre_start}_{pre_end}", "post": f"{post_start}_{post_end}"}
    
    save_folium(pre, aoi, vp["RGB"], f"Oncesi {labels['pre']}", os.path.join(out_dir, "pre_rgb.html"), overlay_boundary, outputs.get("pre_rgb_png"))
    save_folium(post, aoi, vp["RGB"], f"Sonrasi {labels['post']}", os.path.join(out_dir, "post_rgb.html"), overlay_boundary, outputs.get("post_rgb_png"))
    
    if "dNDVI" in diffs:
        save_folium(diffs["dNDVI"].updateMask(vegetation_mask), aoi, vp["dNDVI"], "dNDVI Analizi", os.path.join(out_dir, "dNDVI.html"), overlay_boundary, outputs.get("dndvi_png"))
        
    if "dNBR" in diffs:
        save_folium(diffs["dNBR"].updateMask(vegetation_mask), aoi, vp["dNBR"], "dNBR Analizi", os.path.join(out_dir, "dNBR.html"), overlay_boundary, outputs.get("dnbr_png"))
        
    return outputs
