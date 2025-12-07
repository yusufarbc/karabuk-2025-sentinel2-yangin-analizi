from __future__ import annotations

import ee


def compute_diffs(pre: ee.Image, post: ee.Image) -> dict:
    """Fark görüntülerini hesapla (Compute difference images) including RBR.

    dNDVI = post - pre (vejetasyon düşüşleri negatif)
    dNBR  = pre - post (yanıklık artışı pozitif)
    RBR   = dNBR / (pre_nbr + 1.001)
    """
    dndvi = post.select("NDVI").subtract(pre.select("NDVI")).rename("dNDVI")
    
    pre_nbr = pre.select("NBR")
    post_nbr = post.select("NBR")
    
    dnbr = pre_nbr.subtract(post_nbr).rename("dNBR")
    
    # RBR calculation: dNBR / (PreNBR + 1.001)
    rbr = dnbr.divide(pre_nbr.add(1.001)).rename("RBR")
    
    return {"dNDVI": dndvi, "dNBR": dnbr, "RBR": rbr}


def classify_metric(
    image: ee.Image,
    thresholds: tuple[float, float, float, float] | None = None,
) -> ee.Image:
    """Verilen metriği (dNBR veya RBR) şiddet sınıflarına (0..4) ayırır.

    thresholds: opsiyonel (t0, t1, t2, t3). 
    Varsayılan (RBR için önerilen): <0.1, 0.1-0.35, 0.35-0.75, >0.75
    """
    if thresholds is None:
        # User defined RBR thresholds
        # < 0.1 : Unburned
        # 0.1 - 0.35 : Low
        # 0.35 - 0.75 : Moderate
        # > 0.75 : High
        t0, t1, t2, t3 = 0.10, 0.35, 0.75, 999.0 # t3 is upper bound for class 3
        # Logic adaptation:
        # Class 0: < t0
        # Class 1: t0 <= x < t1
        # Class 2: t1 <= x < t2
        # Class 3: t2 <= x (< t3/inf)
        # Class 4?? User only defined 4 distinct ranges (Unburned, Low, Mod, High) -> 0, 1, 2, 3?
        # Let's map to standard severity codes if possible or follow user exactly.
        # User list:
        # < 0.1 (Green - Unburned) -> Code 0
        # 0.1 - 0.35 (Yellow - Low) -> Code 1
        # 0.35 - 0.75 (Orange - Moderate) -> Code 2
        # > 0.75 (Red - High) -> Code 4 (Skip 3 to match intense colors?) or Code 3?
        # Standard typically has 4 or 5 classes. Let's use 0, 1, 2, 3.
        # But vis_params['severity'] expects 0..4 range palette usually.
        # Let's map > 0.75 to Code 4 (High) for consistent coloring with previous logic if palette is 5 colors.
        # Previous palette: ["#1a9850", "#a6d96a", "#fee08b", "#f46d43", "#a50026"] (5 colors)
        # We need to map user's 4 classes to these.
        # 0: Green -> Unburned
        # 1: Yellow-ish -> Low
        # 2: Orange -> Moderate
        # 3 or 4: Red -> High
        pass

    # Let's stick to the 5-class logic structure but adapt t values.
    # If user provided 3 boundaries (0.1, 0.35, 0.75), we have 4 zones.
    # We can map > 0.75 to class 4, and skip class 3, or merge.
    
    # REVISED STRATEGY: GENERIC
    if thresholds is None:
        t0, t1, t2, t3 = 0.10, 0.35, 0.75, 100.0 # Just default placeholders if called without settings
    else:
        t0, t1, t2, t3 = thresholds

    c0 = image.lt(t0)
    c1 = image.gte(t0).And(image.lt(t1))
    c2 = image.gte(t1).And(image.lt(t2))
    # For RBR specific map:
    # 0.1 - 0.35 -> Low
    # 0.35 - 0.75 -> Moderate
    # > 0.75 -> High
    # Let's assign:
    # 0: Unburned (< 0.10)
    # 1: Low (0.10 - 0.35)
    # 2: Moderate (0.35 - 0.75)
    # 3: High (> 0.75)
    # 4: Extreme? (Not defined, so maybe merge into 3 or keep empty)
    
    c3 = image.gte(t2) # All above 0.75
    # Remove c4 split if we only have 3 thresholds defining 4 classes
    
    classified = (
        c0.multiply(0)
        .add(c1.multiply(1))
        .add(c2.multiply(2))
        .add(c3.multiply(4)) # Jump to 4 for "High" red color? Or 3?
        # Let's use 3 and ensure palette handles it.
        # Old palette: 0,1,2,3,4.
        # If we use 0, 1, 2, 4 -> It matches Green, Yellow, Orange, Dark Red. 
        # (Assuming palette[1] is yellow-green, palette[2] yellow, palette[3] orange, palette[4] red)
        # Wait, let's look at palette in visualize.py: 
        # ["#1a9850", "#a6d96a", "#fee08b", "#f46d43", "#a50026"]
        # 0: Dark Green
        # 1: Light Green
        # 2: Yellow
        # 3: Orange
        # 4: Red
        
        # User wants:
        # < 0.1: Green (0/1)
        # 0.1-0.35: Yellow (2)
        # 0.35-0.75: Orange (3)
        # > 0.75: Red (4)
        
        # So we should map:
        # c0 -> 1 (Light Green) or 0? 0 is fine.
        # c1 -> 2 (Yellow)
        # c2 -> 3 (Orange)
        # c3 -> 4 (Red)
    )
    # Actually, let's rewrite the logic slightly to be cleaner
    
    # 0: < t0
    # 1: t0 <= x < t1
    # 2: t1 <= x < t2
    # 3: >= t2
    
    # To match palette indices:
    # 0 -> 0 (Green)
    # 1 -> 2 (Yellow)
    # 2 -> 3 (Orange)
    # 3 -> 4 (Red)
    
    classified = (
        c0.multiply(0)
        .add(c1.multiply(2))
        .add(c2.multiply(3))
        .add(c3.multiply(4))
        .rename("severity")
        .toUint8()
    )
    return classified

