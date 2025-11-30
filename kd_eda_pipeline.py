import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from math import pi

#
target_file = "/Users/burakcimen/Desktop/DSA 210/DSA Proje Dosyaları/DSA_Final_Project.xlsx"

OUT_DIR = os.path.join(os.getcwd(), "EDA_Plots")
os.makedirs(OUT_DIR, exist_ok=True)

print("✔ Dosya:", target_file)


xls = pd.ExcelFile(target_file)
sheets = xls.sheet_names
print("Sheets:", sheets)


game_sheets = [s for s in sheets if "Game Log" in s]
print("Game log sheets:", game_sheets)


season_rows = []

for sheet in game_sheets:
    df = pd.read_excel(target_file, sheet_name=sheet)
    df = df.dropna(how="all", axis=1)

  
    season = int(sheet.split()[0].split("-")[0])

    numeric_df = df.select_dtypes(include=[np.number])

    row = numeric_df.mean()
    row["Season"] = season
    season_rows.append(row)

season_df = pd.DataFrame(season_rows).sort_values("Season")
print("\n✔ Season averages hazır")
print(season_df.columns)


adv_df = pd.read_excel(target_file, sheet_name="Advanced Statistics")

adv_df["Year"] = pd.to_numeric(adv_df["Year"], errors="coerce")
adv_df = adv_df.dropna(subset=["Year"])
adv_df["Year"] = adv_df["Year"].astype(int)

print("\n✔ Advanced stats hazır")
print(adv_df.columns)


shoot_df = pd.read_excel(target_file, sheet_name="Shooting")

shoot_df["Year"] = pd.to_numeric(shoot_df["Year"], errors="coerce")
shoot_df = shoot_df.dropna(subset=["Year"])
shoot_df["Year"] = shoot_df["Year"].astype(int)

# Distance & type kategorileri
distance_values = [
    "At Rim",
    "3 to <10 ft",
    "10 to <16 ft",
    "16 ft to <3-pt",
    "3-pt"
]

type_values = [
    "Dunk",
    "Hook Shot",
    "Jump Shot",
    "Lay-Up",
    "Tip Shot"
]

shoot_df = shoot_df[shoot_df["Value"].isin(distance_values + type_values)]


dist_df = shoot_df[shoot_df["Value"].isin(distance_values)]

if not dist_df.empty:
    dist_pivot = (
        dist_df.groupby(["Year", "Value"])["FG"]
        .sum().reset_index()
        .pivot(index="Year", columns="Value", values="FG")
        .fillna(0)
    )
    dist_pivot = dist_pivot.div(dist_pivot.sum(axis=1), axis=0)
else:
    dist_pivot = pd.DataFrame()
    print("\n⚠ Uyarı: Shot Distance için veri bulunamadı.")


stype_df = shoot_df[shoot_df["Value"].isin(type_values)]

if not stype_df.empty:
    stype_pivot = (
        stype_df.groupby(["Year", "Value"])["FG"]
        .sum().reset_index()
        .pivot(index="Year", columns="Value", values="FG")
        .fillna(0)
    )
    stype_pivot = stype_pivot.div(stype_pivot.sum(axis=1), axis=0)
else:
    stype_pivot = pd.DataFrame()
    print("\n⚠ Uyarı: Shot Types için veri bulunamadı.")

print("\n✔ Shooting pivotlar oluşturuldu")


season_df["InjuryPhase"] = season_df["Season"].apply(lambda x: "Pre" if x < 2019 else "Post")
adv_df["InjuryPhase"]    = adv_df["Year"].apply(lambda x: "Pre" if x < 2019 else "Post")


def save_plot(x, y, title, ylabel, filename):
    plt.figure(figsize=(7,4))
    plt.plot(x, y, marker="o")
    plt.title(title)
    plt.xlabel("Season")
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, filename), dpi=300)
    plt.close()


if "PTS" in season_df.columns:
    save_plot(season_df["Season"], season_df["PTS"],
              "PPG Trend", "PTS", "ppg.png")

if "FG%" in season_df.columns:
    save_plot(season_df["Season"], season_df["FG%"],
              "FG% Trend", "FG%", "fg.png")

if "3P%" in season_df.columns:
    save_plot(season_df["Season"], season_df["3P%"],
              "3P% Trend", "3P%", "three.png")

if "eFG%" in season_df.columns:
    save_plot(season_df["Season"], season_df["eFG%"],
              "eFG% Trend", "eFG%", "efg.png")


if not dist_pivot.empty:
    for col in dist_pivot.columns:
        save_plot(dist_pivot.index, dist_pivot[col],
                  f"Shot Distance – {col}", col, f"dist_{col}.png")


if not stype_pivot.empty:
    for col in stype_pivot.columns:
        save_plot(stype_pivot.index, stype_pivot[col],
                  f"Shot Type – {col}", col, f"type_{col}.png")



def safe_mean_adv(col, phase):
    if col not in adv_df.columns:
        return 0
    return adv_df[adv_df["InjuryPhase"]==phase][col].mean()

def safe_mean_season(col, phase):
    if col not in season_df.columns:
        return 0
    return season_df[season_df["InjuryPhase"]==phase][col].mean()

radar_metrics = {
    "TS%": [
        safe_mean_adv("TS%", "Pre"),
        safe_mean_adv("TS%", "Post")
    ],
    "USG": [
        safe_mean_adv("USG", "Pre"),
        safe_mean_adv("USG", "Post")
    ],
    "MPG": [
        safe_mean_adv("MPG", "Pre"),
        safe_mean_adv("MPG", "Post")
    ],
    "InvDRtg": [
        200 - safe_mean_adv("DRtg", "Pre"),
        200 - safe_mean_adv("DRtg", "Post")
    ],
    "PPG": [
        safe_mean_season("PTS", "Pre"),
        safe_mean_season("PTS", "Post")
    ]
}

labels = list(radar_metrics.keys())
pre_vals  = [v[0] for v in radar_metrics.values()]
post_vals = [v[1] for v in radar_metrics.values()]

angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
angles = np.concatenate([angles, [angles[0]]])

pre_vals  = pre_vals  + [pre_vals[0]]
post_vals = post_vals + [post_vals[0]]

plt.figure(figsize=(8,8))
ax = plt.subplot(111, polar=True)
ax.plot(angles, pre_vals, label="Pre-Injury")
ax.fill(angles, pre_vals, alpha=0.1)
ax.plot(angles, post_vals, label="Post-Injury")
ax.fill(angles, post_vals, alpha=0.1)

plt.xticks(angles[:-1], labels)
plt.title("Kevin Durant — Pre vs Post Injury Radar Chart")
plt.legend(loc="upper right")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "radar_pre_post.png"), dpi=300)
plt.close()

print("📁 Grafik klasörü:", OUT_DIR)
