"""
Görselleştirme Modülü
Harita üretimi (Folium) ve statiik görsel (PNG) dışa aktarım işlevlerini içerir.
"""

from __future__ import annotations

import os
import math
from typing import Dict, Optional
from PIL import Image, ImageDraw, ImageFont
import folium
import ee

from .araclar import ensure_dir, download_url

def vis_params() -> Dict[str, dict]:
    """Görselleştirme ayarlarını döndürür (Sadece RGB, dNDVI, dNBR)."""
    return {
        "RGB": {"bands": ["B4", "B3", "B2"], "min": 0, "max": 3000, "gamma": 1.2},
        # dNDVI: Kahverengi(kayıp) -> Yeşil(kazanç)
        "dNDVI": {"min": -0.6, "max": 0.6, "palette": ["#8b0000", "#ff8c00", "#ffffbf", "#a6d96a", "#1a9850"]},
        # dNBR: Mavi(iyileşme) -> Kırmızı(yanma)
        "dNBR": {"min": -0.2, "max": 1.0, "palette": ["#2b83ba", "#abdda4", "#ffffbf", "#fdae61", "#d7191c"]},
    }


def _center_of(aoi: ee.Geometry):
    """Alanın merkez koordinatlarını (lat, lon) döndürür."""
    c = aoi.centroid(10).coordinates().getInfo()
    return [c[1], c[0]]


def _add_scale_bar(image_path: str, aoi: ee.Geometry) -> None:
    """PNG görselinin sağ altına ölçek çubuğu ekler."""
    try:
        coords = aoi.bounds().coordinates().getInfo()[0]
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        
        # Genişlik (metre): Derece farkı * 111320 * cos(lat)
        width_m = (max(lons) - min(lons)) * 111320 * math.cos(math.radians(sum(lats) / len(lats)))
        
        with Image.open(image_path) as img:
            w_px, _ = img.size
            px_per_m = w_px / width_m
            
            # Hedef ölçek (Resmin 1/5'i)
            targets = [100, 200, 500, 1000, 2000, 5000, 10000] # Maks 10km
            scale_m = min(targets, key=lambda x: abs(x - (w_px/5)/px_per_m))
            scale_px = scale_m * px_per_m
            
            draw = ImageDraw.Draw(img)
            x = w_px - scale_px - 20
            y = img.size[1] - 40
            
            # Çizim
            draw.line([(x, y), (w_px - 20, y)], fill="black", width=5)
            draw.line([(x, y), (w_px - 20, y)], fill="white", width=3)
            
            label = f"{scale_m/1000:.1f} km" if scale_m >= 1000 else f"{int(scale_m)} m"
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
            
            draw.text((x, y - 25), label, fill="black", font=font, stroke_width=2, stroke_fill="white")
            img.save(image_path)
    except Exception as e:
        print(f"Ölçek eklenemedi: {e}")


def _get_thumb_url(image: ee.Image, aoi: ee.Geometry, vis: dict, boundary: Optional[ee.Geometry] = None) -> str:
    """GEE Thumbnail URL oluşturur."""
    img_vis = image.visualize(**vis)
    if boundary:
         line = ee.FeatureCollection([ee.Feature(boundary, {})]).style(color="FF00FF", width=2, fillColor="00000000")
         img_vis = img_vis.blend(line)
    
    return img_vis.getThumbURL({'dimensions': 1024, 'region': aoi.bounds(), 'format': 'png'})


def save_folium(image: ee.Image, aoi: ee.Geometry, vis: dict, name: str, out_html: str, boundary: Optional[ee.Geometry] = None, static_image_path: Optional[str] = None):
    """Folium haritası olarak kaydeder (Static Image Overlay destekli)."""
    ensure_dir(os.path.dirname(out_html))
    m = folium.Map(location=_center_of(aoi), zoom_start=11, control_scale=True)
    
    if static_image_path and os.path.exists(static_image_path):
        # Statik görseli göm (GitHub Pages uyumlu)
        coords = aoi.bounds().coordinates().getInfo()[0]
        lats = [c[1] for c in coords]; lons = [c[0] for c in coords]
        bounds = [[min(lats), min(lons)], [max(lats), max(lons)]]
        
        folium.raster_layers.ImageOverlay(
            image=static_image_path, bounds=bounds, name=name, opacity=1.0, interactive=True
        ).add_to(m)
    else:
        # Dinamik GEE layer
        map_id = image.getMapId(vis)
        tile_url = map_id["tile_fetcher"].url_format
        folium.raster_layers.TileLayer(tiles=tile_url, attr="Google Earth Engine", name=name, overlay=True).add_to(m)
    
    if boundary:
        # Sınır çizgisi
        line_fc = ee.FeatureCollection([ee.Feature(boundary, {})]).style(color="FF00FF", width=2, fillColor="00000000")
        mid = line_fc.getMapId()
        folium.raster_layers.TileLayer(tiles=mid["tile_fetcher"].url_format, attr="Boundary", name="Sinir", overlay=True).add_to(m)

    m.save(out_html)


def export_maps(pre_image: ee.Image, post_image: ee.Image, diff_images: dict, aoi: ee.Geometry, out_dir: str, boundary: Optional[ee.Geometry] = None) -> dict:
    """Tüm haritaları (RGB, dNBV, dNDVI) PNG olarak indirir."""
    ensure_dir(out_dir)
    outs = {}
    vp = vis_params()
    
    # 1. RGB
    for tag, img in [("pre_rgb_png", pre_image), ("post_rgb_png", post_image)]:
        try:
            url = _get_thumb_url(img, aoi, vp["RGB"], boundary)
            path = os.path.join(out_dir, f"{tag.replace('_png','')}.png") # pre_rgb.png
            if download_url(url, path):
                _add_scale_bar(path, aoi)
                outs[tag] = path
        except Exception as e:
            print(f"Hata {tag}: {e}")

    # 2. Analizler
    if "dNBR" in diff_images:
        try:
            url = _get_thumb_url(diff_images["dNBR"], aoi, vp["dNBR"], boundary)
            path = os.path.join(out_dir, "dNBR.png")
            if download_url(url, path):
                _add_scale_bar(path, aoi)
                outs["dnbr_png"] = path
        except Exception: pass

    if "dNDVI" in diff_images:
        try:
            url = _get_thumb_url(diff_images["dNDVI"], aoi, vp["dNDVI"], boundary)
            path = os.path.join(out_dir, "dNDVI.png")
            if download_url(url, path):
                _add_scale_bar(path, aoi)
                outs["dndvi_png"] = path
        except Exception: pass
            
    return outs
