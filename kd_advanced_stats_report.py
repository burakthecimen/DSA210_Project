import os
import pandas as pd



ICLOUD_DESKTOP = "/Users/burakcimen/Library/Mobile Documents/com~apple~CloudDocs/Desktop"


dsa210_dir = None
for name in os.listdir(ICLOUD_DESKTOP):
    if "DSA 210" in name:
        dsa210_dir = os.path.join(ICLOUD_DESKTOP, name)
        break

if dsa210_dir is None:
    raise SystemExit("DSA 210 klasörü bulunamadı.")


project_dir = None
for name in os.listdir(dsa210_dir):
    if "DSA Proje" in name:
        project_dir = os.path.join(dsa210_dir, name)
        break

if project_dir is None:
    raise SystemExit("DSA Proje klasörü bulunamadı.")


excel_path = None
for fname in os.listdir(project_dir):
    lower = fname.lower()
    if lower.endswith(".xlsx") and "dsa_final_project" in lower:
        excel_path = os.path.join(project_dir, fname)
        break

if excel_path is None:
    raise SystemExit("DSA_Final_Project .xlsx dosyası bulunamadı.")

print("Kullanılan Excel:", excel_path)



sheet_name = "Advanced Statistics"
df = pd.read_excel(excel_path, sheet_name=sheet_name)

df.columns = [str(c).strip() for c in df.columns]
df = df[df["Year"].notna()].copy()
df["Year"] = df["Year"].astype(int)

stats_cols = ["TS%", "USG", "DRtg", "MPG"]
for col in stats_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["Period"] = "Post"
df.loc[df["Year"] <= 2018, "Period"] = "Pre"
df.loc[df["Year"] == 2019, "Period"] = "Transition"

print(df)


summary_rows = []
for col in stats_cols:
    pre_mean = df.loc[df["Period"] == "Pre", col].mean()
    post_mean = df.loc[df["Period"] == "Post", col].mean()
    diff = post_mean - pre_mean
    summary_rows.append({
        "Stat": col,
        "Pre_Injury_Avg": pre_mean,
        "Post_Injury_Avg": post_mean,
        "Post - Pre": diff
    })

summary_df = pd.DataFrame(summary_rows)

print("\nÖzet ortalamalar:")
print(summary_df)


out_path = os.path.join(project_dir, "kd_advanced_with_charts.xlsx")
writer = pd.ExcelWriter(out_path, engine="xlsxwriter")

df.to_excel(writer, sheet_name="AdvancedStats", index=False)
summary_df.to_excel(writer, sheet_name="Summary", index=False)

workbook  = writer.book
ws_data   = writer.sheets["AdvancedStats"]

n_rows = len(df) + 1  
years_col = 0       

start_col_for_charts = 7  

for i, col in enumerate(stats_cols):
    chart = workbook.add_chart({"type": "line"})
    
   
    col_idx = df.columns.get_loc(col) 
    col_letter = chr(ord('A') + col_idx)  

    # X ekseni: Year (A2:A?)
    chart.add_series({
        "name":       col,
        "categories": ["AdvancedStats", 1, years_col, n_rows-1, years_col],
        "values":     ["AdvancedStats", 1, col_idx,   n_rows-1, col_idx],
    })

    chart.set_title({"name": col})
    chart.set_x_axis({"name": "Season (Year)"})
    chart.set_y_axis({"name": col})
    chart.set_legend({"none": True})

    row_pos = 1 + i*15
    col_pos = start_col_for_charts
    cell_addr = chr(ord('A') + col_pos) + str(row_pos+1)
    ws_data.insert_chart(cell_addr, chart)

writer.close()

print("\nYeni Excel oluşturuldu:")
print(" ->", out_path)
