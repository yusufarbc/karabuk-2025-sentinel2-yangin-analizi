from __future__ import annotations

from typing import Optional

import ee

from .utils import load_aoi_geojson


def get_aoi(path: Optional[str] = None) -> ee.Geometry:
    """AOI geometriyi döndür.

    - `path` verilirse ve mevcutsa GeoJSON okunur.
    - Aksi halde Karabük bölgesi için makul bir bbox döndürülür.
    """
    g = load_aoi_geojson(path) if path else None
    if g is not None:
        return g
    # Fallback: approx Karabük bbox
    # Karabük ili yaklaşık sınırlar: 32.3E–33.2E, 41.0N–41.7N
    return ee.Geometry.BBox(32.3, 41.0, 33.2, 41.7)
