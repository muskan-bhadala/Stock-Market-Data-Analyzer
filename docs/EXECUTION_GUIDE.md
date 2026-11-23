# Execution Guide — do these in order (about 1–2 hours total)

## STEP 1 — Install tools (10 min)
1. Install Python 3.10+ from python.org (tick **Add Python to PATH** on Windows).
2. Install Git from git-scm.com. Install VS Code (optional).
3. Check: `python --version` and `git --version`.

## STEP 2 — Put the project on your computer (2 min)
1. Unzip `Stock-Market-Data-Analyzer.zip` to e.g. `C:\Users\<you>\Documents\` (Mac: `~/Documents/`).
2. Open a terminal inside the folder `Stock-Market-Data-Analyzer`.

## STEP 3 — Virtual environment + install libraries (5 min)
Windows:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Mac/Linux:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## STEP 4 — Run the project (2 min)
```
python main.py --ticker AAPL --start 2024-01-01 --end 2025-12-31
```
Creates:
- `images/01_closing_price.png`, `02_moving_averages.png`, `03_daily_returns.png`, `04_volatility_drawdown.png`
- `reports/AAPL_report.txt`
- `outputs/AAPL_processed.csv`
- `data/AAPL.csv` (raw data)

If internet/Yahoo fails, it automatically uses demo data and labels the report "DEMO". Re-run when online for real data.
Run a second stock too: `python main.py --ticker TCS.NS` (more proof).

## STEP 5 — Dashboard (optional, 3 min)
```
streamlit run app.py
```
Opens at http://localhost:8501 → type ticker → click **Analyze**.

## STEP 6 — Capture screenshots into `docs/` (10 min)
Save these as PNG in the `docs/` folder:
1. `docs/01_folder_structure.png` — VS Code explorer showing the folders
2. `docs/02_dataset_preview.png` — `data/AAPL.csv` opened
3. `docs/03_terminal_output.png` — terminal after `python main.py`
4. `docs/04_dashboard.png` — Streamlit page
5. Charts and report are already in `images/` and `reports/`

## STEP 7 — GitHub upload (10 min)
1. github.com → **New repository** → name: `Stock-Market-Data-Analyzer`
   - Description: `Python tool for stock price analysis: moving averages, returns, volatility, charts & reports (Pandas, yfinance, Streamlit)`
   - Public, **do not** add README/.gitignore (you already have them).
   - Topics: `python` `pandas` `stock-market` `data-analysis` `yfinance` `streamlit` `finance` `data-visualization` `fintech` `matplotlib`
2. In the project folder terminal:
```
git init
git add .
git commit -m "Initial commit: project structure and requirements"
git branch -M main
git remote add origin https://github.com/<your-username>/Stock-Market-Data-Analyzer.git
git push -u origin main
```
3. Later updates: `git add .` → `git commit -m "..."` → `git push`.

## Fast commit plan (if you have 1 day)
| Commit | When | Message |
|---|---|---|
| 1 | after Step 7 | `Initial commit: project structure and requirements` |
| 2 | after first run | `Add data loading, cleaning and analysis modules` |
| 3 | after charts | `Add visualizations: price, moving averages, returns, volatility` |
| 4 | after report | `Add insights report and processed CSV outputs` |
| 5 | after screenshots | `Add Streamlit dashboard and screenshots to docs` |
| 6 | final | `Update README with results and learning outcomes` |
(Make these as separate commits by running the project, committing the new output each time — GitHub shows your activity timeline.)

## Day-wise plan (if you have 6 days)
- Day 1 setup & folders · Day 2 `data_loader.py`, `cleaner.py` · Day 3 EDA in a notebook (`notebooks/eda.ipynb`) · Day 4 `analysis.py` · Day 5 `visualize.py` + `app.py` · Day 6 `report.py`, README, GitHub.

## Where things happen (file map)
| Task | File |
|---|---|
| Fetch data (yfinance → CSV → demo) | `src/data_loader.py` |
| Clean data | `src/cleaner.py` |
| Returns, SMAs, volatility, drawdown, trend | `src/analysis.py` |
| Charts | `src/visualize.py` |
| Report + CSV | `src/report.py` |
| Run everything | `main.py` |
| Dashboard | `app.py` |

## Common errors
- `'python' not recognized` → reinstall Python with PATH ticked, or use `py`.
- `ModuleNotFoundError` → venv not activated or `pip install -r requirements.txt` not run.
- Empty data → check ticker (Indian stocks need `.NS`), dates, internet.
- Run commands from inside the project folder (so `src` imports work).

---

# Interview Preparation

**1. Explain your project.**
"I built a Stock Market Data Analyzer in Python. It fetches historical prices using yfinance, cleans them with Pandas, calculates daily returns, 20/50/200-day moving averages, volatility, drawdown and Sharpe ratio, detects the trend, saves charts, and generates a text report. I also built a Streamlit dashboard. The code is modular — separate files for loading, cleaning, analysis, visualization and reporting — and it has CSV and demo-data fallbacks so it never fails."

**2. Why did you choose this project?** Finance data is a real-world use of time-series analysis, and the same workflow is used in investment research and FinTech.

**3. What is a moving average?** The average of the last N closing prices, recalculated each day. It smooths noise; price above a rising SMA suggests an uptrend.

**4. What is volatility and how did you compute it?** The standard deviation of daily returns, multiplied by √252 to annualize. Higher = riskier.

**5. How do you calculate daily return?** `(today − yesterday) / yesterday`, done with `pct_change()`.

**6. What is max drawdown?** The largest fall from a previous peak: `Close / running max − 1`, minimum value.

**7. What is the Sharpe ratio?** Return per unit of risk: annualized return ÷ annualized volatility. I assumed a 0% risk-free rate for simplicity.

**8. How did you handle missing or bad data?** Converted types, dropped duplicate dates and missing closes, sorted by date, forward-filled small gaps.

**9. What challenges did you face / what would you improve?** API failures → added CSV and demo fallbacks. Next: strategy backtesting, multi-stock comparison, alerts, a FastAPI backend.

**10. How is it useful to a company?** Analysts get fast trend and risk summaries instead of manual spreadsheet work; the pipeline is reusable for any ticker.

**HR-style answer:** "It shows I can take a real-world problem, break it into steps, write clean code, and present results clearly — and I finished and documented it on GitHub."

**Technical one-liner:** "Pipeline: ingestion → cleaning → feature engineering with rolling windows → risk metrics → visualization → automated report."

*Disclaimer: educational project, not financial advice.*
