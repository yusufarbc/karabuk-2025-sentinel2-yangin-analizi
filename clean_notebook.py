import json

nb_path = "analysis.ipynb"

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# 1. Update Analysis Loop Cell (Remove Marked RGB display)
for cell in nb["cells"]:
    if cell["cell_type"] == "code" and "for zone in FIRE_ZONES:" in "".join(cell["source"]):
        src = "".join(cell["source"])
        if "marked_rgb" in src:
            # Replace the specific block
            new_src_lines = []
            skip = False
            for line in cell["source"]:
                if "Anlık Sonuç Gösterimi (Marked RGB Vurgusu)" in line:
                    skip = True
                if skip and "if 'marked_rgb_png' in outputs:" in line:
                    continue
                if skip and "marked_rgb_png" in line and "display(" in line:
                    continue
                if skip and line.strip() == "":
                    skip = False # End of block assumption? or indentation check.
                    # Simple heuristic: Just filter out the lines we know.
                
                # Safer: reconstruct the cell content without that block.
                if "marked_rgb_png" not in line and "Anlık Sonuç Gösterimi (Marked RGB Vurgusu)" not in line:
                    new_src_lines.append(line)
            
            cell["source"] = new_src_lines
            print("Cleaned Analysis Loop Cell")

# 2. Update Final Visualization Cell
for cell in nb["cells"]:
    if cell["cell_type"] == "code" and "# En yüksek hasarlı bölgeyi bul ve göster" in "".join(cell["source"]):
        # Rewrite this cell simply to show RBR or FalseColor which are standard.
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
