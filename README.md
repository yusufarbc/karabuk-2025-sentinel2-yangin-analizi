# karabuk-2025-sentinel2-yangin-analizi

2025 Karabük orman yangınının Sentinel-2 uydu görüntüleriyle yanma şiddeti (dNBR) ve bitki örtüsü kaybı analizi.

## Canlı Demo ve Sonuçlar

Interaktif haritalar ve çıktı listesi:

➡️ [GitHub Pages — Proje Sonuçları](https://yusufarbc.github.io/KarabukWildfire2025/)

Yerelde görüntüleme: Depo kökündeki `index.html` dosyasını tarayıcıda açın (tüm haritalar ve CSV/PNG bağlantıları `results/` altına işaret eder).

---

## Proje Yapısı

| Klasör/Dosya | Açıklama |
| :--- | :--- |
| `gee/` | Analiz kodları: `pipeline.py` (uçtan uca akış), `preprocess.py`, `indices.py`, `change.py` (dNBR sınıfları), `visualize.py`, `utils.py`, `aoi.py` ve `aoi.geojson`. |
| `results/` | Üretilen haritalar (HTML/PNG) ve özet istatistikler (`summary_stats.csv`, `severity_areas.csv`). |
| `paper/` | LaTeX raporu (`paper/main.tex`). |
| `analysis.ipynb` | Jupyter defteri; adım adım analiz ve görselleştirme. |
| `index.html` | Web sonuç sayfası (kart tabanlı, responsive). |
| `requirements.txt` | Gerekli Python kütüphaneleri (yoksa aşağıdaki listeyi kullanın). |

## Kurulum

Önkoşul: Google Earth Engine (GEE) API erişimi.

1) Sanal ortam ve bağımlılıklar

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
.\.venv\Scripts\activate

# Eğer `requirements.txt` yoksa aşağıdakileri kurun:
pip install earthengine-api folium branca requests pandas
# (opsiyonel ama tavsiye: jupyter)
pip install jupyter
```

2) Earth Engine kimlik doğrulama

```bash
earthengine authenticate
```

## Çalıştırma

İki tip kullanım desteklenir: Jupyter defteri veya doğrudan Python çağrısı.

1) Jupyter Notebook (önerilen)

```bash
jupyter notebook analysis.ipynb
```

2) Python ile doğrudan çalıştırma (örnek)

```python
from gee.utils import ee_init
from gee.pipeline import run_pipeline

ee_init(project="karabukwildfire2025")  # Proje ID'nizi kullanın

outputs = run_pipeline(
    pre_start="2025-07-10", pre_end="2025-07-25",
    post_start="2025-07-26", post_end="2025-08-10",
    aoi_geojson="gee/aoi.geojson",
    out_dir="results",
    # Opsiyonel: AOI'ye göre dNBR eşiklerini özelleştir
    dnbr_thresholds=(0.10, 0.27, 0.44, 0.66),
    # Opsiyonel: minimum yama alanı (hektar)
    min_patch_ha=0.5,
)

print(outputs)
```

Başarılı çalıştırma sonrası `results/` klasöründe interaktif haritalar (HTML) ve statik görseller (PNG) oluşur. Hızlı göz atmak için depo kökündeki `index.html` sayfasını açın.

Not: Bu çalışmada öncesi (pre) 10–25 Temmuz, sonrası (post) 26 Temmuz–10 Ağustos aralığı baz alınmıştır.

## Rapor (LaTeX)

`paper/main.tex` derlemek için:

```bash
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Notlar:
- pdfLaTeX (LaTeX motoru) kullanılmalıdır; `pdftex`/`tex` (plain) ile derlemeyin.
- Yardımcı dosyalar `.gitignore` ile hariç tutulur; raporu yerelde derleyin.
## Dokümantasyon

Detaylı teknik bilgi ve kullanım kılavuzları `docs/` klasöründedir:
*   [📄 Metodoloji ve Teknik Yaklaşım](docs/metodoloji.md): Kullanılan indeksler, USGS standartları ve gürültü temizleme algoritmaları.
*   [📊 Sonuçların Yorumlanması](docs/sonuclar.md): Harita türleri, renk kodları ve özel rapor görselleri hakkında rehber.

## Lisans

Bu proje MIT lisansı altındadır. Ayrıntılar için `LICENSE` dosyasına bakınız.
