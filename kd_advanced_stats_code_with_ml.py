import os
import pandas as pd
import matplotlib.pyplot as plt


ICLOUD_DESKTOP = "/Users/burakcimen/Library/Mobile Documents/com~apple~CloudDocs/Desktop"
DESKTOP = ICLOUD_DESKTOP


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


df = pd.read_excel(excel_path, sheet_name="Advanced Statistics")
df.columns = [str(c).strip() for c in df.columns]
df = df[df["Year"].notna()].copy()
df["Year"] = df["Year"].astype(int)

stats_cols = ["TS%", "USG", "DRtg", "MPG"]
for col in stats_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")


df["Period"] = "Post"
df.loc[df["Year"] <= 2018, "Period"] = "Pre"
df.loc[df["Year"] == 2019, "Period"] = "Transition"


summary_rows = []
for col in stats_cols:
    pre_mean = df.loc[df["Period"] == "Pre", col].mean()
    post_mean = df.loc[df["Period"] == "Post", col].mean()
    summary_rows.append({
        "Stat": col,
        "Pre_Injury_Avg": pre_mean,
        "Post_Injury_Avg": post_mean,
        "Post - Pre": post_mean - pre_mean
    })

summary_df = pd.DataFrame(summary_rows)


out_path = os.path.join(DESKTOP, "kd_advanced_with_charts.xlsx")
writer = pd.ExcelWriter(out_path, engine="xlsxwriter")

df.to_excel(writer, sheet_name="AdvancedStats", index=False)
summary_df.to_excel(writer, sheet_name="Summary", index=False)

workbook = writer.book
ws_data = writer.sheets["AdvancedStats"]

n_rows = len(df) + 1
years_col = df.columns.get_loc("Year")
start_col_for_charts = 7

for i, col in enumerate(stats_cols):
    chart = workbook.add_chart({"type": "line"})
    col_idx = df.columns.get_loc(col)

    chart.add_series({
        "name": col,
        "categories": ["AdvancedStats", 1, years_col, n_rows - 1, years_col],
        "values":     ["AdvancedStats", 1, col_idx,   n_rows - 1, col_idx],
    })

    chart.set_title({"name": col})
    chart.set_x_axis({"name": "Season (Year)"})
    chart.set_y_axis({"name": col})
    chart.set_legend({"none": True})

    ws_data.insert_chart(f"H{1 + i*15}", chart)

writer.close()

print("📄 Excel Desktop'a kaydedildi:")
print(" ->", out_path)


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

ml_df = df[df["Period"].isin(["Pre", "Post"])].copy()
ml_df["Label"] = ml_df["Period"].map({"Pre": 0, "Post": 1})

features = ["TS%", "USG", "DRtg", "MPG"]
X = ml_df[features].fillna(0)
y = ml_df["Label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

rf = RandomForestClassifier(n_estimators=300, random_state=42)
rf.fit(X_train, y_train)

plt.figure(figsize=(7,4))
plt.barh(features, rf.feature_importances_)
plt.title("Feature Importance – Injury Phase")
plt.tight_layout()

fi_path = os.path.join(DESKTOP, "ml_feature_importance_advanced.png")
plt.savefig(fi_path, dpi=300)
plt.close()

print("📈 Feature importance Desktop'a kaydedildi:")
print(" ->", fi_path)

print("\n✅ TÜM ÇIKTILAR DESKTOP'TA")
