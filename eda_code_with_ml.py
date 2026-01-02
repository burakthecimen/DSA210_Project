import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

target_file = "/Users/burakcimen/Desktop/DSA 210/DSA Proje Dosyaları/DSA_Final_Project.xlsx"
OUT_DIR = "/Users/burakcimen/Desktop/DSA_210_OUTPUTS"
os.makedirs(OUT_DIR, exist_ok=True)

print("✔ Outputs will be saved to:", OUT_DIR)


xls = pd.ExcelFile(target_file)
sheets = xls.sheet_names
game_sheets = [s for s in sheets if "Game Log" in s]


season_rows = []
MIN_GAMES = 30

for sheet in game_sheets:
    df = pd.read_excel(target_file, sheet_name=sheet)
    df.columns = df.columns.str.strip()

    season = int(sheet.split()[0].split("-")[0])
    games = len(df)

    if games < MIN_GAMES:
        continue

    FG  = df["FG"].sum()
    FGA = df["FGA"].sum()
    P3  = df["3P"].sum()
    P3A = df["3PA"].sum()

    row = {
        "Season": season,
        "Games": games,
        "FG%": FG / FGA if FGA > 0 else np.nan,
        "3P%": P3 / P3A if P3A > 0 else np.nan,
        "eFG%": (FG + 0.5 * P3) / FGA if FGA > 0 else np.nan
    }

    season_rows.append(row)

season_df = pd.DataFrame(season_rows).sort_values("Season")
print("✔ Season efficiency metrics computed")


adv_df = pd.read_excel(target_file, sheet_name="Advanced Statistics")
adv_df.columns = adv_df.columns.str.strip()

adv_df["Year"] = pd.to_numeric(adv_df["Year"], errors="coerce")
adv_df = adv_df.dropna(subset=["Year"])
adv_df["Year"] = adv_df["Year"].astype(int)


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

save_plot(season_df["Season"], season_df["FG%"],  "FG% Trend",  "FG%",  "fg.png")
save_plot(season_df["Season"], season_df["3P%"],  "3P% Trend",  "3P%",  "three.png")
save_plot(season_df["Season"], season_df["eFG%"], "eFG% Trend", "eFG%", "efg.png")


ml_df = season_df.copy()

adv_cols = ["TS%", "USG", "MPG", "DRtg"]
adv_small = adv_df[["Year"] + adv_cols].rename(columns={"Year": "Season"})
ml_df = ml_df.merge(adv_small, on="Season", how="left")

# Injury label
ml_df["injury_label"] = ml_df["Season"].apply(lambda x: 0 if x < 2019 else 1)
ml_df = ml_df[ml_df["Season"] != 2019]

print("✔ ML dataset shape:", ml_df.shape)


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

features = ["FG%", "3P%", "eFG%", "TS%", "USG", "MPG"]
features = [f for f in features if f in ml_df.columns]

X = ml_df[features].fillna(0)
y = ml_df["injury_label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

# Logistic Regression
lr = LogisticRegression()
lr.fit(X_train, y_train)
print("\n📊 Logistic Regression")
print(classification_report(y_test, lr.predict(X_test)))

# Random Forest
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)
print("\n🌲 Random Forest")
print(classification_report(y_test, rf.predict(X_test)))

# Feature importance
plt.figure(figsize=(8,4))
plt.barh(features, rf.feature_importances_)
plt.title("Feature Importance – Injury Phase")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "ml_feature_importance.png"), dpi=300)
plt.close()

print("\n✅ PIPELINE COMPLETED (PPG REMOVED – DATA VALID)")
print("📁 Outputs saved to:", OUT_DIR)
