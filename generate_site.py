import os
import glob

# Configuration
RESULTS_DIR = "results"
OUTPUT_FILE = "index.html"
REPO_URL = "https://github.com/yusufarbc/karabuk-2025-sentinel2-yangin-analizi"

# Descriptions for indices
DESCRIPTIONS = {
    "pre_RGB": "Yangın öncesi doğal renkli (RGB) Sentinel-2 görüntüsü (1-20 Temmuz 2025).",
    "post_RGB": "Yangın sonrası doğal renkli (RGB) Sentinel-2 görüntüsü (5-30 Eylül 2025).",
    "dNDVI": "Delta NDVI (Vejetasyon Fark İndeksi). Kaybolan yeşil alanları ve bitki örtüsü hasarını gösterir.",
    "dNBR": "Delta NBR (Yanmışlık Oranı Farkı). Yangının şiddetini ve topraktaki ısı stresini gösterir."
}

TITLES = {
    "pre_RGB": "Yangın Öncesi (Pre-Fire)",
    "post_RGB": "Yangın Sonrası (Post-Fire)",
    "dNDVI": "Vejetasyon Kaybı (dNDVI)",
    "dNBR": "Yanmışlık Şiddeti (dNBR)"
}

HTML_HEADER = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Karabük 2025 Yangın Analizi</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap" rel="stylesheet">
</head>
<body>
    <header>
        <div class="container">
            <h1>Karabük 2025 Yangın Analizi</h1>
            <p class="subtitle">Sentinel-2 Uydusu ve Google Earth Engine ile Hasar Tespit Raporu</p>
            <div class="stats-grid">
                <div class="stat-item">
                    <span class="stat-value">7</span>
                    <span class="stat-label">Analiz Edilen Bölge</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">1200+ km²</span>
                    <span class="stat-label">Taranan Alan</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">Sentinel-2</span>
                    <span class="stat-label">Uydu Verisi</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">2 Fark İndeksi</span>
                    <span class="stat-label">dNDVI & dNBR</span>
                </div>
            </div>
        </div>
    </header>

    <main class="container">
        
        <section id="ozet">
            <h2 class="section-title">Proje Hakkında</h2>
            <div class="analysis-info">
                <h3>Özet</h3>
                <p>Bu çalışma, 2025 yaz sezonunda Karabük ilinde (Ovacık, Eflani, Safranbolu) meydana gelen orman yangınlarının etkilerini belirlemektedir. 
                ESA WorldCover verisi ile tarım ve yerleşim alanları maskelenerek sadece orman ve çalılık alanlardaki kayıplar analiz edilmiştir.</p>
                <br>
                <h3>Metodoloji</h3>
                <ul>
                    <li><strong>Veri Kaynağı:</strong> Sentinel-2 L2A (10m çözünürlük)</li>
                    <li><strong>Platform:</strong> Google Earth Engine (Python API)</li>
                    <li><strong>Zaman Aralığı:</strong> Temmuz 2025 (Öncesi) vs. Eylül 2025 (Sonrası)</li>
                </ul>
                <div style="margin-top: 1.5rem;">
                    <a href="paper/main.pdf" class="btn btn-primary" target="_blank">📄 Raporu İndir (PDF)</a>
                </div>
            </div>
        </section>

        <section id="il-geneli">
            <h2 class="section-title">İl Geneli Tarama (Overview)</h2>
            <div class="card" style="margin-bottom: 2rem;">
                 <div class="card-img-container" style="aspect-ratio: 21/9;">
                    <img src="paper/figures/overview.png" alt="Genel Bakış">
                 </div>
                 <div class="card-body">
                    <h3 class="card-title">Genel Durum Haritası</h3>
                    <p class="card-desc">Tüm Karabük il sınırları içerisindeki yangın noktalarının kuş bakışı görünümü.</p>
                    <a href="paper/figures/overview.png" class="btn btn-outline" download>Resmi İndir</a>
                 </div>
            </div>

            <div class="grid">
"""

def generate_card(title, desc, relative_img_path, relative_html_path):
    html_btn = ""
    if relative_html_path and os.path.exists(relative_html_path):
        html_btn = f'<a href="{relative_html_path}" class="btn btn-primary" target="_blank">🗺️ İnteraktif Harita</a>'
    
    return f"""
                <div class="card">
                    <div class="card-img-container">
                        <img src="{relative_img_path}" alt="{title}" loading="lazy">
                    </div>
                    <div class="card-body">
                        <h3 class="card-title">{title}</h3>
                        <p class="card-desc">{desc}</p>
                        <div class="btn-group">
                            {html_btn}
                            <a href="{relative_img_path}" class="btn btn-outline" download>⬇️ PNG İndir</a>
                        </div>
                    </div>
                </div>
    """

def process_directory(path_name, section_title):
    global HTML_OUTPUT
    
    # Check if directory exists
    full_path = os.path.join(RESULTS_DIR, path_name)
    if not os.path.exists(full_path):
        return

    HTML_OUTPUT += f"""
        </section>
        <section id="{path_name}">
            <h2 class="section-title">{section_title}</h2>
            <div class="grid">
    """
    
    # We expect these 4 types
    types = ["pre_RGB", "post_RGB", "dNDVI", "dNBR"]
    
    for t in types:
        # Check files
        # Files structure: {t}.png and potentially {t}*.html
        # Note: HTML files sometimes have dates appended e.g. pre_RGB_2025...html
        
        img_path = os.path.join(full_path, f"{t}.png")
        
        # Find corresponding HTML
        html_pattern = os.path.join(full_path, f"{t}*.html")
        html_files = glob.glob(html_pattern)
        html_path = html_files[0] if html_files else None
        
        if os.path.exists(img_path):
            img_rel = img_path.replace("\\", "/")
            html_rel = html_path.replace("\\", "/") if html_path else None
            
            card_html = generate_card(TITLES[t], DESCRIPTIONS[t], img_rel, html_rel)
            HTML_OUTPUT += card_html

    HTML_OUTPUT += """
            </div>
    """

HTML_OUTPUT = HTML_HEADER

# 1. Il Geneli
process_directory("il_geneli", "İl Geneli Detaylı Analiz")

# 2. Yanginlar (Sort them to be sure)
yanginlar_path = os.path.join(RESULTS_DIR, "yanginlar")
if os.path.exists(yanginlar_path):
    subdirs = sorted([d for d in os.listdir(yanginlar_path) if os.path.isdir(os.path.join(yanginlar_path, d))])
    
    for subdir in subdirs:
        # Clean name for title: "1_Cildikisik_Kayi" -> "1. Cildikisik & Kayi"
        clean_name = subdir.replace("_", " ")
        # Add relative path
        rel_path = os.path.join("yanginlar", subdir)
        process_directory(rel_path, clean_name)

HTML_FOOTER = """
        </section>
    </main>
    
    <footer>
        <div class="container">
            <p>2025 &copy; Yusuf Talha ARABACI - Karabük Üniversitesi</p>
            <p style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.7;">Bu çalışma açık kaynaklıdır ve eğitim amaçlı hazırlanmıştır.</p>
        </div>
    </footer>
</body>
</html>
"""

HTML_OUTPUT += HTML_FOOTER

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(HTML_OUTPUT)

print("Index.html successfully generated!")
