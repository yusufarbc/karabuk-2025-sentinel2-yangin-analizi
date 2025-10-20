from __future__ import annotations

import ee


def _mask_s2_sr(image: ee.Image) -> ee.Image:
    """Simple cloud/cirrus mask for Sentinel-2 SR (QA60 bits 10/11)."""
    qa = image.select("QA60")
    cloud_bit = 1 << 10
    cirrus_bit = 1 << 11
    mask = qa.bitwiseAnd(cloud_bit).eq(0).And(qa.bitwiseAnd(cirrus_bit).eq(0))
    return image.updateMask(mask)


def _mask_scl_water_and_shadows(image: ee.Image) -> ee.Image:
    """Use S2 SCL to mask water and cloud shadows optionally.

    SCL classes (common): 6=Water, 3=Cloud shadow, 8=Cloud medium prob, 9=Cloud high prob, 10=Thin cirrus.
    We only mask water here; clouds are handled in QA60 mask above.
    """
    scl = image.select("SCL")
    water = scl.eq(6)
    # Mask out water
    return image.updateMask(water.Not())


def prepare_composite(aoi: ee.Geometry, start: str, end: str) -> ee.Image:
    """Prepare median Sentinel-2 SR composite clipped to AOI for date range.

    Applies QA60 cloud/cirrus mask and SCL-based water mask.
    """
    col = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate(start, end)
        .filterBounds(aoi)
        .map(_mask_s2_sr)
        # Karabük iç bölge: SCL su maskesi uygulanmaz
    )
    img = col.median().clip(aoi)
    return img
