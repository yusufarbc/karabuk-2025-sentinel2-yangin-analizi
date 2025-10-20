"""Genel yardımcılar ve GEE başlatma (initialize) işlevleri.

- ee_init: Google Earth Engine oturumu açar (kullanıcı OAuth)
- ensure_dir: Klasör yoksa oluşturur
- load_aoi_geojson: GeoJSON dosyasını ee.Geometry olarak yükler
"""

from __future__ import annotations

import os
import json
from typing import Optional

import ee


def ee_init(project: Optional[str] = None) -> None:
    """Earth Engine'i kullanıcı OAuth ile başlat.

    Parametre olarak yalnızca Project ID kabul edilir (örn: "your-gcp-project").
    Servis hesabı ve ortam değişkenleri bu basit yordamda kullanılmaz.
    """
    project_id = project
    if project_id is not None:
        if not isinstance(project_id, str):
            raise ValueError("ee_init: 'project' must be a string Project ID, not a number.")
        if project_id.isdigit():
            raise ValueError("ee_init: received a numeric-looking value. Pass Project ID, not project number.")

    def _init() -> None:
        if project_id:
            ee.Initialize(project=project_id)
        else:
            ee.Initialize()

    try:
        try:
            _init()
        except Exception:
            ee.Authenticate()
            _init()
    except Exception as e:  # pragma: no cover - environment dependent
        if not project_id:
            raise RuntimeError(
                "Earth Engine init failed: Proje ID yok. 'project' parametresi geçin. Orijinal hata: "
                + str(e)
            )
        raise RuntimeError(f"Earth Engine init failed for project '{project_id}': {e}")


def ensure_dir(path: str) -> None:
    """Verilen yolu (varsa üstleriyle birlikte) oluşturur."""
    if path:
        os.makedirs(path, exist_ok=True)


def load_aoi_geojson(path: str) -> Optional[ee.Geometry]:
    """GeoJSON dosyasından AOI'yi `ee.Geometry` olarak yükler.

    Esnek destek:
    - Feature: `geometry` alanı kullanılır
    - FeatureCollection: union geometry
    - Polygon/MultiPolygon (doğrudan geometri)
    - Sadece `bbox`: dikdörtgen oluşturulur
    Hata durumunda None döner (çağıran taraf varsayılan bbox kullanır).
    """
    if not path or not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        gj = json.load(f)

    try:
        if isinstance(gj, dict):
            t = gj.get("type")
            # Feature
            if t == "Feature":
                geom = gj.get("geometry")
                if not geom and "bbox" in gj:
                    bbox = gj["bbox"]
                    return ee.Geometry.Rectangle(bbox)
                return ee.Geometry(geom)
            # FeatureCollection
            if t == "FeatureCollection" or ("features" in gj and isinstance(gj["features"], list)):
                fc = ee.FeatureCollection(gj)
                return fc.geometry()
            # Bare geometry
            if t in {"Polygon", "MultiPolygon", "LineString", "MultiLineString", "Point", "MultiPoint"}:
                return ee.Geometry(gj)
            # Only bbox provided
            if "bbox" in gj:
                return ee.Geometry.Rectangle(gj["bbox"])
        # Fallbacks: try as Geometry first, then as FeatureCollection geometry
        try:
            return ee.Geometry(gj)
        except Exception:
            try:
                fc = ee.FeatureCollection(gj)
                return fc.geometry()
            except Exception:
                return None
    except Exception:
        return None
