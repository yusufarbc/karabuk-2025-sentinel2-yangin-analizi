import json

nb_path = "analysis.ipynb"

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# 1. Update Analysis Loop Cell (Restore Marked RGB display)
for cell in nb["cells"]:
    if cell["cell_type"] == "code" and "for zone in FIRE_ZONES:" in "".join(cell["source"]):
        # We want to append the display logic at the end of the try block if it's not there.
        # But we previously removed it carefully. Let's just rewrite the block we know.
        src = "".join(cell["source"])
        if "Anlık Sonuç Gösterimi" not in src:
            # Locate the lines where we want to insert.
            # Look for "zone_results[name] = outputs"
            new_lines = []
            for line in cell["source"]:
                new_lines.append(line)
                if "zone_results[name] = outputs" in line:
                    new_lines.append("\n")
                    new_lines.append("        # Anlık Sonuç Gösterimi (Marked RGB Vurgusu)\n")
                    new_lines.append("        if 'marked_rgb_png' in outputs:\n")
                    new_lines.append("            display(HTML(f\"<b>{name} - Hasar Tespiti (Marked RGB)</b>\"))\n")
                    new_lines.append("            display(Image(filename=outputs['marked_rgb_png'], width=600))\n")
            
            cell["source"] = new_lines
            print("Restored Analysis Loop Cell")

# 2. Update Final Visualization Cell
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
            "        # Masked Overlay (En Önemli)\n",
            "        if 'marked_rgb_png' in res:\n",
            "             display(HTML(f\"<h4>{top_zone} - Maskelenmiş Yangın Katmanı (Marked RGB)</h4>\"))\n",
            "             display(Image(filename=res['marked_rgb_png'], width=800))\n",
            "        \n",
            "        # Diğer Detaylar\n",
            "        if 'rbr_png' in res:\n",
            "             display(HTML(f\"<h4>{top_zone} - RBR Analizi</h4>\"))\n",
            "             display(Image(filename=res['rbr_png'], width=800))\n"
        ]
        print("Restored Visualization Cell")

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=4)
