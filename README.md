# Kevin Durant: How Injuries Affected His Performance and Playing Style


## 🏀 Introduction
This project investigates how Kevin Durant’s performance and playing style evolved after his major injuries during his NBA career, especially his 2019 Achilles tendon rupture. The goal is to explore both statistical performance changes and behavioral adjustments such as shot selection and offensive efficiency to understand how an elite player adapts his game after a significant physical setback.

---

## 🎯 1. Motivation
Kevin Durant is widely regarded as one of the most efficient and versatile scorers in NBA history. However, his career has been marked by several serious injuries that challenged his consistency and forced him to adapt his role on the court. This project aims to analyze how Durant’s on-court performance and overall playing style changed before and after his major Achilles injury that happened in 2019. By studying changes in scoring, efficiency, and shot selection, the project seeks to uncover how Kevin Durant recover and evolve their game after his major injury.

---

## ❓ 2. Research Questions
1. How did Kevin Durant’s statistical performance (points, FG%, 3P%, minutes) change before and after his 2019 Achilles injury?  
2. Did his playing style such as shot selection, pace, or reliance on mid-range vs. three-point shots shift in the post-injury seasons?  
3. Is there evidence of a gradual recovery or adaptation trend over the seasons following the injury?

---

## 📊 3. Data Sources

- **Basketball Reference – Game Logs:** Game-by-game statistics such as points, minutes, FG%, and 3P%.  
  🔗 [https://www.basketball-reference.com/players/d/duranke01/gamelog/](https://www.basketball-reference.com/players/d/duranke01/gamelog/)

- **NBA.com Player Page:** Official advanced analytics including true shooting percentage (TS%), usage rate, shot zones, and efficiency ratings.  
  🔗 [https://www.nba.com/stats/player/201142/](https://www.nba.com/stats/player/201142/)

- **ESPN Stats:** Advanced box score data and player splits, providing contextual performance measures by season and team.  
  🔗 [https://www.espn.com/nba/player/advancedstats/_/id/3202/kevin-durant](https://www.espn.com/nba/player/advancedstats/_/id/3202/kevin-durant)

- **StatMuse – Kevin Durant Insights:** Interactive player database showing team-by-team performance and game outcomes.  
  Useful for analyzing how Durant’s presence affects team success and how different team systems influence his efficiency and style of play.  
  🔗 [https://www.statmuse.com/nba/player/kevin-durant-985](https://www.statmuse.com/nba/player/kevin-durant-985)

- **GitHub – NBA Shots 2004–2025 Dataset:**  
  A comprehensive open-source dataset containing every NBA shot attempt from 2004 to 2025. The dataset includes shot location coordinates (x/y), distance from the basket, shot result (make/miss), player name, and team information. This will be used to analyze **how Kevin Durant’s shot selection and spatial tendencies changed** before and after his 2019 Achilles injury for instance, whether he began taking more perimeter jumpers and fewer drives to the rim.  
  🔗 [https://github.com/DomSamangy/NBA_Shots_04_25](https://github.com/DomSamangy/NBA_Shots_04_25)

📅 **Time Range:** The dataset will include games between 2013 and 2025, covering both pre-injury and post-injury periods.  
The June 2019 Achilles injury serves as the dividing point for labeling games as `pre_injury` or `post_injury`.

---

## 🧠 4. Data Collection and Preparation Plan
1. **Data Download:** Export Kevin Durant’s game logs (CSV) and gather injury dates from ESPN.  
2. **Integration:** Combine game logs with advanced metrics from the NBA Stats (e.g., TS%, usage rate).  
3. **Labeling:** Mark each game as *pre-injury* or *post-injury* based on the June 2019 Achilles injury.  
4. **Feature Engineering:** Add new columns such as:
   - 3PA/FGA ratio → reflects perimeter vs. inside shot tendency  
   - Minutes/game → workload intensity  
   - Efficiency differential (TS% change per season)
  
---

# Data Preparation & Processing Pipeline

All data preparation steps were automated using a unified Python pipeline.

### ✔ Game Log Processing (2013–2025)
- Imported 13 separate game log sheets  
- Cleaned column names and formats  
- Computed season-level averages:  
  - PPG  
  - FG% / 3P% / eFG%  
  - Rebounds, assists, steals, blocks  
  - Turnovers, fouls  
  - Minutes per game  
- **Export:** `kd_season_averages.xlsx`

### ✔ Advanced Statistics Processing
- Loaded TS%, USG%, DRtg, MPG  
- Converted season strings to numeric  
- Merged with game log outputs  
- Generated trend charts  
- **Export:** `kd_advanced_with_charts.xlsx`

### ✔ Shooting Data Processing
- Extracted: Shot Distance, Shot Type, Shot Points  
- Pivoted into one-row-per-season  
- Normalized all values into % distributions  
- **Exports:**  
  - `kd_shot_trends_single.xlsx`  
  - `EDA_Results.xlsx`

### ✔ Injury Labeling

| Label | Seasons |
|-------|---------|
| Pre-Injury | 2013–2018 |
| Post-Injury | 2020–2025 |
| 2019 excluded | Injury year |

---

# Exploratory Data Analysis (EDA)

### ✔ Season Performance Trends
- PPG ↓ after injury  
- FG% and eFG% slight decline  
- 3PT% stable or ↑  
- MPG ↓ significantly  

### ✔ Shooting Style Evolution
**Shot Distances**
- Rim attempts ↓↓  
- Midrange ↑  
- 3PT slightly ↑  

**Shot Types**
- Jump shots ↑↑  
- Dunks ↓  
- Layups ↓  

### ✔ Advanced Stats Trends
- TS% stayed elite  
- USG% ↓  
- DRtg worsened  
- MPG ↓ due to load management  

---

# Hypothesis Testing

### 1️⃣ T-Test: PPG (Pre vs Post)
- p < 0.05 → Significant difference

### 2️⃣ T-Test: TS% (Pre vs Post)
- p > 0.05 → No significant change

### 3️⃣ Chi-Square Tests
- Shot Distance Distribution → p << 0.05  
- Shot Type Distribution → p << 0.05  

---

# Outputs Generated

| File | Description |
|------|-------------|
| kd_season_averages.xlsx | Game log season aggregates |
| kd_advanced_with_charts.xlsx | Advanced metrics + charts |
| kd_shot_trends_single.xlsx | Shot distance/type trends |
| EDA_Results.xlsx | Unified EDA results |

Included charts:
- PPG / FG% / 3P% / eFG% time series  
- Shot distance trends  
- Shot type distributions  
- Pre vs Post radar chart  

---

# Conclusions

- Durant shifted toward skill-based scoring after the Achilles injury  
- Fewer rim attacks, more jump shots  
- MPG and defensive impact drop  
- TS% remains elite  
- Strong evidence of major style adaptation post-injury
---

## 📈 5. Analysis Plan
- **Statistical Analysis:**  
  Compare pre and post-injury averages for scoring, shooting accuracy, and minutes using t-tests or non-parametric alternatives.  
- **Playing Style Analysis:**  
  Examine shot selection patterns and offensive tendencies to detect shifts in playing style (e.g., increased reliance on jump shots).  
- **Visualization:**  
  Use time-series plots to show recovery trends and bar/heatmap visualizations to illustrate play-style evolution.

---

## 🧩 6. Expected Outcomes

This project aims to find data-driven answers to the following research questions:  
- How did Kevin Durant’s statistical performance (points, FG%, 3P%, minutes) change before and after his 2019 Achilles injury?  
- Did his playing style — such as shot selection, pace, or reliance on mid-range vs. three-point shots — shift in the post-injury seasons?  
- Is there evidence of a gradual recovery or adaptation trend across the following seasons?

Expected findings include:  
- Quantified differences in performance metrics before and after the injury.  
- Visual evidence of how Durant’s play style shifted (for example, more perimeter-oriented or efficient shot distribution).  
- Insights into recovery and adaptation strategies among elite athletes.  
- Clear, data-driven conclusions about the trade-off between scoring volume and long-term efficiency.

---


