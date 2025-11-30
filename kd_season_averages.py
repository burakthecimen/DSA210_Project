import glob
import os
import numpy as np
import pandas as pd


FILE_DIR = "/Users/burakcimen/Library/Mobile Documents/com~apple~CloudDocs/Desktop/DSA 210/DSA Proje Dosyaları"

FILE_PATTERN = os.path.join(FILE_DIR, "*.xls")

all_files = sorted(glob.glob(FILE_PATTERN))

print("Bulunan .xls dosyaları:")
for f in all_files:
    print(" -", f)

if not all_files:
    raise FileNotFoundError("Klasörde hiç .xls dosyası bulunamadı, path'i kontrol et.")

STAT_COLS = [
    "MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "2P", "2PA", "2P%",
    "eFG%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL",
    "BLK", "TOV", "PF", "PTS", "+/-"
]



def mp_to_minutes(x):
    """ 'MM:SS' formatındaki MP'yi dakika (float)'a çevirir. """
    if pd.isna(x):
        return np.nan
    s = str(x)
    if ":" not in s:
        
        try:
            return float(s)
        except ValueError:
            return np.nan
    m, sec = s.split(":")
    try:
        return int(m) + int(sec) / 60.0
    except ValueError:
        return np.nan


def date_to_season(d: pd.Timestamp):
    """
    Tarihten sezon label'ı üretir: 2013-14, 2014-15 gibi.
    NBA sezonu Ekim'de başlıyor gibi düşünülerek ayarlanıyor.
    """
    if pd.isna(d):
        return np.nan
    y = d.year
    if d.month >= 10:   
        start = y
        end = y + 1
    else:               
        start = y - 1
        end = y
    return f"{start}-{str(end)[-2:]}"



frames = []

for path in all_files:
    print("\nİşleniyor:", os.path.basename(path))
    tables = pd.read_html(path)
    if not tables:
        print("  -> İçinde tablo yok, atlanıyor.")
        continue

    df = tables[0].copy()

    if "Date" not in df.columns:
        print("  -> 'Date' kolonu yok, game log değil, atlanıyor.")
        continue


    for col in ["G", "Rk", "Date"]:
        if col in df.columns:
            df = df[df[col] != col]

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    if "+/-" not in df.columns:
        for alt_name in ["±", "Plus/Minus"]:
            if alt_name in df.columns:
                df.rename(columns={alt_name: "+/-"}, inplace=True)
                break

    if "MP" in df.columns:
        df["MP_min"] = df["MP"].apply(mp_to_minutes)
    else:
        df["MP_min"] = np.nan

    numeric_cols = [
        "FG", "FGA", "FG%", "3P", "3PA", "3P%", "2P", "2PA", "2P%",
        "eFG%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST",
        "STL", "BLK", "TOV", "PF", "PTS", "+/-"
    ]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    df["Season"] = df["Date"].apply(date_to_season)

    df = df[~df["Season"].isna()].copy()

    frames.append(df)

if not frames:
    raise ValueError("Hiç 'Date' kolonlu game log bulunamadı, frames boş.")

full = pd.concat(frames, ignore_index=True)
print("\nToplam satır (tüm sezon maçları):", len(full))



agg_cols = {
    "MP_min": "MP",  
}

for c in STAT_COLS:
    if c == "MP":
        continue  
    if c in full.columns:
        agg_cols[c] = c

grouped = (
    full
    .groupby("Season")
    .agg(
        {
            "MP_min": "mean",
            **{col: "mean" for col in agg_cols if col not in ["MP_min"]}
        }
    )
)

result = grouped.rename(columns={"MP_min": "MP"}).reset_index()

ordered_cols = ["Season"] + STAT_COLS
ordered_cols = [c for c in ordered_cols if c in result.columns]
result = result[ordered_cols]

print("\nSezonluk ortalama istatistikler (ilk birkaç satır):")
print(result.head())


out_path = os.path.join(FILE_DIR, "kd_season_averages.xlsx")
result.to_excel(out_path, index=False)

print("\nExcel dosyası kaydedildi:")
print(" ->", out_path)
