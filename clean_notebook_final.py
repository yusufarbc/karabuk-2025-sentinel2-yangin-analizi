import json

nb_path = "analysis.ipynb"

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# 1. Clean Analysis Loop Cell (Remove Marked RGB display again)
for cell in nb["cells"]:
    if cell["cell_type"] == "code" and "for zone in FIRE_ZONES:" in "".join(cell["source"]):
        new_lines = []
        for line in cell["source"]:
            if "marked_rgb" in line or "Marked RGB" in line:
                continue
            if "Hasar Tespiti" in line:
                continue
            new_lines.append(line)
        cell["source"] = new_lines
        print("Cleaned Analysis Loop")

# 2. Clean Visualization Cell
for cell in nb["cells"]:
    if cell["cell_type"] == "code" and "# En yüksek hasarlı bölgeyi bul ve göster" in "".join(cell["source"]):
         cell["source"] = [
            "# En yüksek hasarlı bölgeyi bul ve göster\n",
            "if summary_list:\n",
            "    top_zone = df_res.iloc[0]['Bölge']\n",
            "    print(f\"🔴 En Çok Etkilenen Bölge: {top_zone}\")\n",
            "    \n",
            "    res = zone_results.get(top_zone)\n",
            "    if res:\n",
            "        # RBR PNG (Daha bilimsel ve net)\n",
            "        if 'rbr_png' in res:\n",
            "             display(HTML(f\"<h4>{top_zone} - RBR Hasar Analizi</h4>\"))\n",
            "             display(Image(filename=res['rbr_png'], width=800))\n"
        ]
         print("Cleaned Visualization Cell")

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=4)
