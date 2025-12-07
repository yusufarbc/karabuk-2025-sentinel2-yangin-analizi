from __future__ import annotations

from typing import Dict, Optional
import os
import csv

import ee
import folium
from branca.colormap import LinearColormap
import requests
import json

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


def _add_continuous_legend(m: folium.Map, title: str, palette, vmin: float, vmax: float) -> None:
    cmap = LinearColormap(colors=list(palette), vmin=vmin, vmax=vmax)
    cmap.caption = title
    m.add_child(cmap)


def _add_severity_legend(m: folium.Map) -> None:
    labels = ["Yanmamış/Düşük", "Düşük", "Orta-Düşük", "Orta-Yüksek", "Yüksek"]
    colors = ["#1a9850", "#a6d96a", "#fee08b", "#f46d43", "#a50026"]
    html = [
        '<div style="position: fixed; bottom: 25px; left: 10px; z-index: 9999; '
        'background: white; padding: 10px; border: 2px solid #bbb; '
        'font-size: 12px; line-height: 14px;">',
        '<b>dNBR Şiddeti</b><br/>'
    ]
    for c, lab in zip(colors, labels):
        html.append(f'<i style="background:{c};width:12px;height:12px;display:inline-block;margin-right:6px;"></i>{lab}<br/>')
    html.append('</div>')
    folium.map.Marker(location=[0, 0], icon=folium.DivIcon(html=''.join(html))).add_to(m)


def save_folium(image: ee.Image, aoi: ee.Geometry, vis: dict, name: str, out_html: str):
    ensure_dir(os.path.dirname(out_html))
    m = folium.Map(location=_center_of(aoi), zoom_start=9, control_scale=True)
    _add_ee_tile(m, image, vis, name)
    folium.LayerControl().add_to(m)
    try:
        if "Severity" in name:
            _add_severity_legend(m)
        elif all(k in vis for k in ("palette", "min", "max")):
            _add_continuous_legend(m, name, vis["palette"], float(vis["min"]), float(vis["max"]))
    except Exception:
        pass
    m.save(out_html)


def reduce_mean(image: ee.Image, aoi: ee.Geometry, band: str, scale: int = 20) -> float:
    stats = image.select(band).reduceRegion(
        reducer=ee.Reducer.mean(), geometry=aoi, scale=scale, maxPixels=1e13, tileScale=4
    )
    val = stats.get(band).getInfo()
    return float(val) if val is not None else float("nan")


def write_summary_csv(path: str, rows: Dict[str, float]):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        for k, v in rows.items():
            w.writerow([k, v])


def compute_severity_areas(severity: ee.Image, aoi: ee.Geometry, *, scale: int = 10) -> Dict[str, float]:
    """Şiddet sınıfı başına alan hesapla (hektar)."""
    labels = [
        "severity_0_yanmamis",
        "severity_1_dusuk",
        "severity_2_orta_dusuk",
        "severity_3_orta_yuksek",
        "severity_4_yuksek",
    ]
    areas = {}
    for idx, label in enumerate(labels):
        mask = severity.eq(idx)
        area_img = ee.Image.pixelArea().updateMask(mask)
        area_m2 = area_img.reduceRegion(
            reducer=ee.Reducer.sum(), geometry=aoi, scale=scale, maxPixels=1e13, tileScale=4
        ).get("area")
        val = ee.Number(area_m2).divide(10000).getInfo()  # hectares
        areas[label] = float(val) if val is not None else 0.0
    # Toplam yanmış alan (sınıf 1..4)
    burned = sum(areas[k] for k in labels[1:])
    areas["burned_total_ha"] = burned
    return areas


def write_kv_csv(path: str, rows: Dict[str, float]):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["key", "value"])
        for k, v in rows.items():
            w.writerow([k, v])


def download_png(image: ee.Image, aoi: ee.Geometry, vis: dict, out_path: str, *, scale: Optional[int] = 20, dimensions: Optional[int] = None) -> str:
    """Görselleştirilmiş ee.Image için rapor dostu PNG indir. Hata durumunda (bellek limiti) daha düşük çözünürlükle tekrar dener."""
    ensure_dir(os.path.dirname(out_path))
    vis_img = image.visualize(**vis)
    
    # Geometriyi basitleştir: Bounding Box kullan
    try:
        region_geom = aoi.bounds() 
        region = region_geom.getInfo()
    except Exception as e:
        print(f"Uyarı: Server-side bounds hesabı başarısız ({e}). Orijinal AOI kullanılıyor.")
        region = aoi.getInfo()

    def _attempt_download(dims, sc, retry_count=0):
        params: Dict[str, object] = {
            "region": json.dumps(region), 
            "format": "png",
            "crs": "EPSG:4326"
        }
        
        if dims is not None:
            params["dimensions"] = dims
        elif sc is not None:
            params["scale"] = sc

        url = vis_img.getThumbURL(params)
        
        try:
            with requests.get(url, stream=True) as r:
                if r.status_code != 200:
                    try:
                        err_msg = r.json()
                    except:
                        err_msg = r.text
                        
                    # Eğer bellek hatası ise (400) ve henüz retry yapmadıysak
                    if r.status_code == 400 and retry_count < 2:
                        print(f"⚠️ GEE Bellek Hatası (400) algılandı. Çözünürlük düşürülerek tekrar deneniyor... ({os.path.basename(out_path)})")
                        
                        new_dims = dims // 2 if dims else None
                        new_scale = sc * 2 if sc else None
                        
                        # Eğer dims verilmediyse ama scale verilmediyse hesaplanamaz, o yüzden scale 2 katına çıkar
                        # (dims öncelikli olduğu için dims varsa ona bakıyoruz)
                        
                        return _attempt_download(new_dims, new_scale, retry_count + 1)
                    
                    print(f"GEE download error for {os.path.basename(out_path)}: {r.status_code} - {err_msg}")
                    r.raise_for_status()
                    
                with open(out_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
        except Exception as e:
            # Recursive çağrıdan başarılı döndüyse burası çalışmamalı, üstteki return çıkış yapar.
            # Ancak request hatası fırlatırsa buraya düşeriz.
            if retry_count < 2 and "400" in str(e):
                 # Yukarıdaki yakalama bloğu status code kontrolü yapıyordu, burası exception içindeki mesajı kollar
                 # Ancak requests.get hata fırlatmaz (raise_for_status çağrılmadıkça), o yüzden üstteki blok daha güvenli.
                 # Burası network hataları için.
                 pass
            raise e

    _attempt_download(dimensions, scale)
    return out_path


def export_report_pngs(*, pre: ee.Image, post: ee.Image, diffs: Dict[str, ee.Image], severity: ee.Image, aoi: ee.Geometry, out_dir: str = "results") -> Dict[str, str]:
    """Raporlar için ana analiz katmanlarını PNG olarak dışa aktar."""
    ensure_dir(out_dir)
    vp = vis_params()
    outs: Dict[str, str] = {}
    outs["pre_ndvi_png"] = os.path.join(out_dir, "pre_NDVI.png")
    download_png(pre.select("NDVI"), aoi, vp["NDVI"], outs["pre_ndvi_png"], dimensions=2560)

    outs["post_ndvi_png"] = os.path.join(out_dir, "post_NDVI.png")
    download_png(post.select("NDVI"), aoi, vp["NDVI"], outs["post_ndvi_png"], dimensions=2560)

    outs["pre_nbr_png"] = os.path.join(out_dir, "pre_NBR.png")
    download_png(pre.select("NBR"), aoi, vp["NBR"], outs["pre_nbr_png"], dimensions=2560)

    outs["post_nbr_png"] = os.path.join(out_dir, "post_NBR.png")
    download_png(post.select("NBR"), aoi, vp["NBR"], outs["post_nbr_png"], dimensions=2560)

    outs["dndvi_png"] = os.path.join(out_dir, "dNDVI.png")
    download_png(diffs["dNDVI"], aoi, vp["dNDVI"], outs["dndvi_png"], dimensions=2560)

    outs["dnbr_png"] = os.path.join(out_dir, "dNBR.png")
    download_png(diffs["dNBR"], aoi, vp["dNBR"], outs["dnbr_png"], dimensions=2560)

    outs["severity_png"] = os.path.join(out_dir, "severity.png")
    download_png(severity, aoi, vp["severity"], outs["severity_png"], dimensions=2560)
    return outs


def export_truecolor_pngs(*, pre: ee.Image, post: ee.Image, aoi: ee.Geometry, out_dir: str = "results", min_val: int = 0, max_val: int = 3000, gamma: float = 1.2) -> Dict[str, str]:
    """Raporlar için öncesi/sonrası gerçek renkli (B4,B3,B2) PNG'leri dışa aktar."""
    ensure_dir(out_dir)
    vis_rgb = {"bands": ["B4", "B3", "B2"], "min": min_val, "max": max_val, "gamma": [gamma, gamma, gamma]}
    outs: Dict[str, str] = {}
    outs["pre_rgb_png"] = os.path.join(out_dir, "pre_RGB.png")
    download_png(pre, aoi, vis_rgb, outs["pre_rgb_png"], dimensions=1600)
    outs["post_rgb_png"] = os.path.join(out_dir, "post_RGB.png")
    download_png(post, aoi, vis_rgb, outs["post_rgb_png"], dimensions=1600)
    return outs
