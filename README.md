# Kevin Durant: How Injuries Affected His Performance and Playing Style


## 🏀 Introduction
This project investigates how Kevin Durant’s performance and playing style evolved after major injuries during his NBA career, especially his 2019 Achilles tendon rupture.  
The goal is to explore both **statistical performance changes** and **behavioral adjustments** — such as shot selection and offensive efficiency — to understand how an elite player adapts his game after a significant physical setback.

---

## 🎯 1. Motivation
Kevin Durant is widely regarded as one of the most efficient and versatile scorers in NBA history.  
However, his career has been marked by several serious injuries that challenged his consistency and forced him to adapt his role on the court.  
This project aims to analyze how Durant’s on-court performance and overall playing style changed before and after his major injuries.  
By studying changes in scoring, efficiency, and shot selection, the project seeks to uncover how elite players recover and evolve their game after major injuries.

---

## ❓ 2. Research Questions
1. How did Kevin Durant’s statistical performance (points, FG%, 3P%, minutes) change before and after his 2019 Achilles injury?  
2. Did his **playing style** — such as shot selection, pace, or reliance on mid-range vs. three-point shots — shift in the post-injury seasons?  
3. Is there evidence of a gradual recovery or adaptation trend over the seasons following the injury?

---

## 📊 3. Data Sources
- **Basketball Reference – Game Logs:** Game-by-game statistics such as points, minutes, FG%, and 3P%.  
  🔗 [https://www.basketball-reference.com/players/d/duranke01/gamelog/](https://www.basketball-reference.com/players/d/duranke01/gamelog/)
- **NBA Stats API:** Advanced analytics such as true shooting percentage (TS%), usage rate, and shot type distributions.  
  🔗 [https://documenter.getpostman.com/view/24232555/2s93shzpR3](https://documenter.getpostman.com/view/24232555/2s93shzpR3)
- **Wikipedia & ESPN Injury Reports:** Dates and descriptions of Durant’s injuries for labeling pre/post periods.  
  🔗 [https://en.wikipedia.org/wiki/Kevin_Durant](https://en.wikipedia.org/wiki/Kevin_Durant)

The dataset will include games between **2017 and 2025**, covering both pre-injury and post-injury periods.

---

## 🧠 4. Data Collection and Preparation Plan
1. **Data Download:** Export Kevin Durant’s game logs (CSV) and gather injury dates from Wikipedia/ESPN.  
2. **Integration:** Combine game logs with advanced metrics from the NBA Stats API (e.g., TS%, usage rate).  
3. **Labeling:** Mark each game as *pre-injury* or *post-injury* based on the June 2019 Achilles injury.  
4. **Feature Engineering:** Add new columns such as:
   - 3PA/FGA ratio → reflects perimeter vs. inside shot tendency  
   - Minutes/game → workload intensity  
   - Efficiency differential (TS% change per season)  
5. **Cleaning:** Remove “Did Not Play” entries and standardize numeric formats.  
6. **Storage:** Save the cleaned dataset in the `/data/` folder as `durant_games_clean.csv`.

---

## 📈 5. Analysis Plan
- **Statistical Analysis:**  
  Compare pre- and post-injury averages for scoring, shooting accuracy, and minutes using t-tests or non-parametric alternatives.  
- **Playing Style Analysis:**  
  Examine shot selection patterns and offensive tendencies to detect shifts in playing style (e.g., increased reliance on jump shots).  
- **Visualization:**  
  Use time-series plots to show recovery trends and bar/heatmap visualizations to illustrate play-style evolution.

---

## 🧩 6. Expected Outcomes
- Quantified differences in performance metrics before and after the injury.  
- Visual evidence of how Durant’s play style shifted (for example, more perimeter-oriented or efficient shot distribution).  
- Insights on recovery and adaptation strategies among elite athletes.  
- Clear, data-driven conclusions about the trade-off between scoring volume and long-term efficiency.

---


