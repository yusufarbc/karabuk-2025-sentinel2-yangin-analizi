from __future__ import annotations

from typing import Dict, Optional
import os
import csv
import requests
import json

import ee
import folium
from branca.colormap import LinearColormap

from .utils import ensure_dir


def _center_of(aoi: ee.Geometry):
    c = aoi.centroid(10).coordinates().getInfo()
    return [c[1], c[0]]  # lat, lon


def vis_params() -> Dict[str, dict]:
    return {
        "RGB": {"bands": ["B4", "B3", "B2"], "min": 0, "max": 3000, "gamma": [1.2, 1.2, 1.2]},
        "NDVI": {"min": -0.2, "max": 0.9, "palette": ["#440154", "#3b528b", "#21908d", "#5dc963", "#fde725"]},
        "NBR": {"min": -0.5, "max": 1.0, "palette": ["#8b0000", "#ff8c00", "#ffff00", "#00ff00", "#006400"]},
        "dNDVI": {"min": -0.6, "max": 0.6, "palette": ["#8b0000", "#ff8c00", "#ffffbf", "#a6d96a", "#1a9850"]},
        "dNBR": {"min": -0.2, "max": 1.0, "palette": ["#2b83ba", "#abdda4", "#ffffbf", "#fdae61", "#d7191c"]},
        "severity": {"min": 0, "max": 4, "palette": ["#1a9850", "#a6d96a", "#fee08b", "#f46d43", "#a50026"]},
    }


def _ee_tile_url(image: ee.Image, vis: dict) -> str:
    info = image.getMapId(vis)
    if isinstance(info, dict):
        tf = info.get("tile_fetcher")
        if tf is not None and hasattr(tf, "url_format"):
            return tf.url_format
        if "tile_url_template" in info:
            return info["tile_url_template"]
        if "mapid" in info and "token" in info:
            return f"https://earthengine.googleapis.com/map/{info['mapid']}/{{z}}/{{x}}/{{y}}?token={info['token']}"
    raise RuntimeError("Unable to retrieve EE tiles URL.")


def _add_ee_tile(m: folium.Map, image: ee.Image, vis: dict, name: str, opacity: float = 1.0):
    tiles_url = _ee_tile_url(image, vis)
    folium.raster_layers.TileLayer(
        tiles=tiles_url,
        attr="Google Earth Engine",
        name=name,
        overlay=True,
        control=True,
        show=True,
        opacity=opacity,
    ).add_to(m)


def save_folium(image: ee.Image, aoi: ee.Geometry, vis: dict, name: str, out_html: str, boundary: Optional[ee.Geometry] = None):
    ensure_dir(os.path.dirname(out_html))
    m = folium.Map(location=_center_of(aoi), zoom_start=9, control_scale=True)
    _add_ee_tile(m, image, vis, name)
    
    if boundary:
        # Sınırları ekle (Magenta kenarlık, içi boş)
        line_fc = ee.FeatureCollection([ee.Feature(boundary, {})])
        line_img = line_fc.style(color="FF00FF", width=2, fillColor="00000000")
        _add_ee_tile(m, line_img, {}, "Sinirlar")
    
    m.save(out_html)


def reduce_mean(image: ee.Image, region: ee.Geometry, band_name: str, scale: int = 10) -> float:
    try:
        val = image.select(band_name).reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=scale,
            maxPixels=1e9,
            tileScale=32,
            bestEffort=True
        ).get(band_name).getInfo()
        return float(val) if val is not None else 0.0
    except Exception as e:
        print(f"Error in reduce_mean: {e}")
        return 0.0


def compute_severity_areas(severity: ee.Image, region: ee.Geometry, scale: int = 10) -> dict:
    try:
        # severity band is named 'severity'
        hist = severity.reduceRegion(
            reducer=ee.Reducer.frequencyHistogram(),
            geometry=region,
            scale=scale,
            maxPixels=1e9,
            tileScale=32,
            bestEffort=True
        ).get("severity").getInfo()
        
        out = {}
        if not hist:
            return out
        
        # Pixel area in hectares.
        pixel_ha = (scale * scale) / 10000.0
        
        for k, count in hist.items():
            try:
                cls_id = int(float(k))
                out[f"alan_ha_sinif_{cls_id}"] = count * pixel_ha
            except:
                pass
        return out
    except Exception as e:
        print(f"Error in compute_severity_areas: {e}")
        return {}


def write_summary_csv(path: str, data: dict):
    ensure_dir(os.path.dirname(path))
    keys = list(data.keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerow(data)


def write_kv_csv(path: str, data: dict):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Key", "Value"])
        for k, v in data.items():
            writer.writerow([k, v])


def _download_url(url: str, path: str):
    ensure_dir(os.path.dirname(path))
    try:
        r = requests.get(url, timeout=300)
        if r.status_code == 200:
            with open(path, "wb") as f:
                f.write(r.content)
    except Exception as e:
        print(f"Failed to download {url}: {e}")


def _get_thumb_url(image: ee.Image, aoi: ee.Geometry, vis: dict, boundary: Optional[ee.Geometry] = None) -> str:
    img_vis = image.visualize(**vis)
    if boundary:
         line_fc = ee.FeatureCollection([ee.Feature(boundary, {})])
         line_img = line_fc.style(color="FF00FF", width=2, fillColor="00000000")
         img_vis = img_vis.blend(line_img)
    
    return img_vis.getThumbURL({
        'dimensions': 1024,
        'region': aoi.bounds(), 
        'format': 'png'
    })


def export_truecolor_pngs(pre: ee.Image, post: ee.Image, aoi: ee.Geometry, out_dir: str, boundary: Optional[ee.Geometry] = None) -> dict:
    vp = vis_params()["RGB"]
    outs = {}
    
    u1 = _get_thumb_url(pre, aoi, vp, boundary)
    p1 = os.path.join(out_dir, "pre_RGB.png")
    _download_url(u1, p1)
    outs["pre_rgb_png"] = p1
    
    u2 = _get_thumb_url(post, aoi, vp, boundary)
    p2 = os.path.join(out_dir, "post_RGB.png")
    _download_url(u2, p2)
    outs["post_rgb_png"] = p2
    
    return outs


def export_report_pngs(pre, post, diffs, severity, aoi, out_dir, boundary=None) -> dict:
    outs = {}
    vp = vis_params()
    
    if "dNBR" in diffs:
        u = _get_thumb_url(diffs["dNBR"], aoi, vp["dNBR"], boundary)
        p = os.path.join(out_dir, "dNBR.png")
        _download_url(u, p)
        outs["dnbr_png"] = p
        
    if "dNDVI" in diffs:
        u = _get_thumb_url(diffs["dNDVI"], aoi, vp["dNDVI"], boundary)
        p = os.path.join(out_dir, "dNDVI.png")
        _download_url(u, p)
        outs["dndvi_png"] = p
        
    if severity:
        u = _get_thumb_url(severity, aoi, vp["severity"], boundary)
        p = os.path.join(out_dir, "severity.png")
        _download_url(u, p)
        outs["severity_png"] = p
        
    return outs


def export_severity_rgb_overlay(post: ee.Image, severity: ee.Image, aoi: ee.Geometry, out_dir: str, boundary: Optional[ee.Geometry] = None) -> dict:
    vp_rgb = vis_params()["RGB"]
    vp_sev = vis_params()["severity"]
    
    rgb_vis = post.visualize(**vp_rgb)
    sev_vis = severity.visualize(**vp_sev)
    
    # Basit blend (opak overlay, veya GEE'nin default blend mantığı şeffaflık yoksa üstüne çizer)
    # Severity genellikle discrete class'tır, maskeli yerler alttakini gösterir.
    combined = rgb_vis.blend(sev_vis)
    
    if boundary:
         line_fc = ee.FeatureCollection([ee.Feature(boundary, {})])
         line_img = line_fc.style(color="FF00FF", width=2, fillColor="00000000")
         combined = combined.blend(line_img)
    
    url = combined.getThumbURL({
        'dimensions': 1024,
        'region': aoi.bounds(),
        'format': 'png'
    })
    
    p = os.path.join(out_dir, "severity_overlay.png")
    _download_url(url, p)
    return {"severity_overlay_png": p}
