"""
2025 Karabük Yangınları - 7 Kritik Bölge Analizi
Bu script, belirlenen 7 yangın bölgesi için GEE pipeline'ını çalıştırır.
"""
import os
import json
import ee
from gee.pipeline import run_pipeline

# 7 Bölge Tanımı (Koordinatlar Onaylandı)
FIRE_ZONES = [
    {
        "name": "1_Aladaglar",
        "center": [32.55, 41.13], # Safranbolu güneyi, Aladağ-Kahyalar
        "buffer": 3000
    },
    {
        "name": "2_Cumayani",
        "center": [32.70, 41.20], # Safranbolu kuzeyi
        "buffer": 3000
    },
    {
        "name": "3_Buyuk_Ovacik",
        "center": [32.80, 41.25], # Ovacık/Safranbolu - En büyük alan
        "buffer": 5000 # Büyük olduğu için buffer geniş
    },
    {
        "name": "4_Kisla",
        "center": [32.85, 41.28], # Büyük Ovacık doğusu
        "buffer": 3000
    },
    {
        "name": "5_Soguksu_Aricak",
        "center": [32.589, 41.198], # DÜZELTİLDİ: 37.00E -> 32.589E
        "buffer": 3000
    },
    {
        "name": "6_Toprakcuma",
        "center": [33.10, 41.30], # Safranbolu Toprakcuma
        "buffer": 3000
    },
    {
        "name": "7_Eflani_Guzelce",
        "center": [33.20, 41.35], # Eflani Saraycık
        "buffer": 4000
    }
]

# Ortak Tarihler (Tüm sezonu kapsar)
# Pre: Temmuz başı (Yangınlar 23 Temmuz'da başladı)
# Post: Eylül sonu (Son yangın 3 Eylül'de bitti)
PRE_START = '2025-07-01'
PRE_END = '2025-07-20'
POST_START = '2025-09-05'
POST_END = '2025-09-30'

BASE_OUT_DIR = r"c:\Users\WORKSTATION\Documents\GitHub\karabuk-2025-sentinel2-yangin-analizi\results\yanginlar"

def main():
    print("🚀 7 Bölge Analizi Başlatılıyor...")
    
    # GEE Init (Eğer pipeline içinde init yoksa buraya ekleyebilirdik ama pipeline.py yapıyor)
    # Ancak proje ID'si burada verilebilir.
    # ee.Initialize(project='karabuk-orman-yangini-2025') # pipeline.py hallediyor.

    for zone in FIRE_ZONES:
        zm = zone['name']
        print(f"\n📍 İşleniyor: {zm}")
        
        # Bounding Box Oluştur
        pt = ee.Geometry.Point(zone['center'])
        bbox = pt.buffer(zone['buffer']).bounds()
        
        # Geçici GeoJSON yaz
        temp_geo = f"temp_{zm}.geojson"
        with open(temp_geo, "w") as f:
            json.dump({"type": "Feature", "geometry": bbox.getInfo()}, f)
            
        out_dir = os.path.join(BASE_OUT_DIR, zm)
        
        try:
            # Pipeline Çalıştır
            # area_scale=20 (Hız İçin)
            outputs = run_pipeline(
                pre_start=PRE_START, pre_end=PRE_END,
                post_start=POST_START, post_end=POST_END,
                aoi_geojson=temp_geo,
                out_dir=out_dir,
                area_scale=20, # OPTİMİZASYON: 10m yerine 20m
                skip_severity=False # Severity haritası isteniyor
            )
            print(f"✅ Tamamlandı: {zm}")
            # print(outputs.keys()) # Debug
            
        except Exception as e:
            print(f"❌ HATA ({zm}): {e}")
            
        finally:
            if os.path.exists(temp_geo):
                os.remove(temp_geo)
                
    print("\n🏁 Tüm analizler bitti.")

if __name__ == "__main__":
    main()
