"""Lightweight GEE helpers used by the notebook-only workflow.

Modules:
- gee.utils: ee_init, ensure_dir, load_aoi_geojson
- gee.aoi: get_aoi from optional GeoJSON path
- gee.preprocess: Sentinel-2 composite preparation
- gee.indices: NDVI, NBR band helpers
- gee.change: dNDVI/dNBR and severity classification
- gee.visualize: vis params, folium save, basic stats/CSV
"""

__all__ = [
    "utils",
    "aoi",
    "preprocess",
    "indices",
    "change",
    "visualize",
]

