"""
Araçlar Modülü
Genel yardımcı fonksiyonlar, dosya/dizin yönetimi ve GEE başlatma işlemlerini içerir.
"""

import os
import json
import requests
import ee
from typing import Optional

def ee_init(project: Optional[str] = None) -> None:
    """Earth Engine oturumunu başlatır."""
    try:
        if project:
            ee.Initialize(project=project)
        else:
            ee.Initialize()
    except Exception:
        ee.Authenticate()
        if project:
            ee.Initialize(project=project)
        else:
            ee.Initialize()


def ensure_dir(path: str) -> None:
    """Klasör yoksa oluşturur."""
    if path:
        os.makedirs(path, exist_ok=True)


def download_url(url: str, path: str) -> bool:
    """URL'den dosya indirir."""
    ensure_dir(os.path.dirname(path))
    try:
        r = requests.get(url, timeout=300)
        if r.status_code == 200:
            with open(path, "wb") as f:
                f.write(r.content)
            return True
    except Exception as e:
        print(f"İndirme hatası: {e}")
    return False


def get_karabuk_province() -> ee.Geometry:
    """Karabük il sınırlarını FAO/GAUL verisetinden getirir."""
    dataset = ee.FeatureCollection("FAO/GAUL/2015/level1")
    karabuk = dataset.filter(ee.Filter.eq("ADM1_NAME", "Karabuk"))
    return karabuk.geometry()


def get_aoi(path: Optional[str] = None) -> ee.Geometry:
    """GeoJSON dosyasından veya varsayılan il sınırlarından analiz alanını (AOI) yükler."""
    if path == "KARABUK_PROVINCE":
        return get_karabuk_province()

    if path and os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                gj = json.load(f)
            # GeoJSON parsing logic (simplified)
            if isinstance(gj, dict):
                if "geometry" in gj: return ee.Geometry(gj["geometry"]) # Feature
                if "features" in gj: return ee.FeatureCollection(gj).geometry() # FeatureCol
                if "bbox" in gj: return ee.Geometry.Rectangle(gj["bbox"]) # BBox only
                return ee.Geometry(gj) # Direct geometry
        except Exception:
            pass # Fallback to default
    
    # Fallback: Karabük yaklaşık bbox
    return ee.Geometry.BBox(32.3, 41.0, 33.2, 41.7)
