import json

nb_path = "analysis.ipynb"

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

new_cells = []
for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        
        # 1. Fix Province Outputs Visualization Cell
        if "if 'province_outputs' in locals():" in source:
            lines = cell["source"]
            new_lines = []
            for line in lines:
                # Keep Pre/Post RGB
                if "pre_rgb_map" in line or "post_rgb_map" in line:
                    new_lines.append(line)
                # Keep dNDVI / dNBR
                elif "dndvi_map" in line or "dnbr_map" in line:
                    new_lines.append(line)
                # Keep checks/headers
                elif "province_outputs" in line and "get" not in line: # if ... line
                     new_lines.append(line)
                # Remove False Color and Severity
                elif "falsecolor_map" in line or "severity_map" in line or "RBR" in line:
                    continue
                else:
                    new_lines.append(line)
            cell["source"] = new_lines
            print("Fixed Province Outputs Cell")

    new_cells.append(cell)

nb["cells"] = new_cells

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=4)
