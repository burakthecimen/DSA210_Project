import os
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score



DESKTOP = "/Users/burakcimen/Desktop"

OUT_DIR = os.path.join(DESKTOP, "DSA210_SHOT_ML_OUTPUTS")
os.makedirs(OUT_DIR, exist_ok=True)

BASE_DIR = "/Users/burakcimen/Library/Mobile Documents/com~apple~CloudDocs/Desktop/DSA 210/DSA Proje Dosyaları"
IN_FILE = os.path.join(BASE_DIR, "shooting_kd_averages.xlsx")

OUT_EXCEL = os.path.join(OUT_DIR, "kd_shot_trends_ml.xlsx")
OUT_FI    = os.path.join(OUT_DIR, "ml_feature_importance_shots.png")

print("📥 Input:", IN_FILE)
print("📤 Output dir:", OUT_DIR)


df = pd.read_excel(IN_FILE, sheet_name="ShootingSplits")
df.columns = [str(c).strip() for c in df.columns]


df["Year"] = df["Year"].astype(str).str[:4].astype(int)



shot_dist = df[df["Split"] == "Shot Distance"].copy()

shot_dist["FGA_share"] = (
    shot_dist.groupby("Year")["FGA"]
             .transform(lambda x: x / x.sum())
)

dist_pivot = (
    shot_dist
    .pivot(index="Year", columns="Value", values="FGA_share")
    .add_prefix("Dist_")
)



shot_type = df[df["Split"] == "Shot Type"].copy()

shot_type["FGA_share"] = (
    shot_type.groupby("Year")["FGA"]
             .transform(lambda x: x / x.sum())
)

type_pivot = (
    shot_type
    .pivot(index="Year", columns="Value", values="FGA_share")
    .add_prefix("Type_")
)


features = (
    dist_pivot
    .join(type_pivot, how="outer")
    .fillna(0)
    .reset_index()
)



features["Period"] = "Post"
features.loc[features["Year"] <= 2018, "Period"] = "Pre"
features.loc[features["Year"] == 2019, "Period"] = "Transition"

ml_df = features[features["Period"].isin(["Pre", "Post"])].copy()
ml_df["Label"] = ml_df["Period"].map({"Pre": 0, "Post": 1})



feature_cols = [
    c for c in ml_df.columns
    if c.startswith("Dist_") or c.startswith("Type_")
]

X = ml_df[feature_cols]
y = ml_df["Label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

rf = RandomForestClassifier(
    n_estimators=400,
    random_state=42
)

rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

print("\n🌲 Random Forest – Pre vs Post Injury")
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))



importances = pd.Series(
    rf.feature_importances_,
    index=feature_cols
).sort_values()

plt.figure(figsize=(10, 6))
importances.plot(kind="barh")
plt.title("Feature Importance – Shot Selection (Pre vs Post Injury)")
plt.tight_layout()
plt.savefig(OUT_FI, dpi=300)
plt.close()

print("\n📈 Feature importance saved:")
print(" ->", OUT_FI)



ml_df.to_excel(OUT_EXCEL, sheet_name="Shot_Trends_ML", index=False)

print("\n📄 Excel saved:")
print(" ->", OUT_EXCEL)

print("\n✅ SCRIPT FINISHED SUCCESSFULLY")
