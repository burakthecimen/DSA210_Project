import os
import pandas as pd

BASE_DIR = "/Users/burakcimen/Library/Mobile Documents/com~apple~CloudDocs/Desktop/DSA 210/DSA Proje Dosyaları"

IN_FILE  = os.path.join(BASE_DIR, "shooting_kd_averages.xlsx")
OUT_FILE = os.path.join(BASE_DIR, "kd_shot_trends_single.xlsx")

print("Giriş dosyası:", IN_FILE)
print("Çıkış dosyası:", OUT_FILE)

df = pd.read_excel(IN_FILE, sheet_name="ShootingSplits")
df.columns = [str(c).strip() for c in df.columns]
df["Year"] = df["Year"].astype(str)


shot_dist = df[df["Split"] == "Shot Distance"].copy()

shot_dist["FGA_share"] = (
    shot_dist.groupby("Year")["FGA"]
             .transform(lambda x: x / x.sum())
)

dist_pivot = shot_dist.pivot(index="Year", columns="Value", values="FGA_share")
dist_pivot = dist_pivot.add_prefix("Dist_")  


shot_type = df[df["Split"] == "Shot Type"].copy()

shot_type["FGA_share"] = (
    shot_type.groupby("Year")["FGA"]
             .transform(lambda x: x / x.sum())
)

type_pivot = shot_type.pivot(index="Year", columns="Value", values="FGA_share")
type_pivot = type_pivot.add_prefix("Type_")   


combined = dist_pivot.join(type_pivot, how="outer").reset_index()

print("İlk satırlar:")
print(combined.head())


combined.to_excel(OUT_FILE, sheet_name="ShotTrends", index=False)

print("Shot trend dosyası oluşturuldu:")
print(" ->", OUT_FILE)
