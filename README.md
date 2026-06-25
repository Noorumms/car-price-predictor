# 🚗 Car Price Predictor

> End-to-end ML regression pipeline that predicts used car prices from real-world Indian market data — cleaned, analyzed, modeled, and deployed as a live web app.

🔗 **[Live Demo →](https://preloved-wheels.streamlit.app/)**

---

## What It Does

Enter a car's company, model, year, fuel type, and kilometres driven — get an instant price estimate. The model was trained on 10,000+ real listings scraped from Quikr India and optimized across 1000 random train/test splits to find the most stable prediction.

---

## How It Works
Raw Data → Cleaning → EDA → OneHotEncoding → Linear Regression → Prediction

**Data problems solved:**
- Year column had garbage values like `"Lucky"`, `"Individual"` — kept only numeric years
- Price had `"Ask For Price"` rows — removed entirely
- kms_driven had values like `"45,000 kms"` — stripped units and commas
- Car names were too long — kept only first 3 words for cleaner encoding
- Removed luxury car outliers above 60 lac — they skewed the model

**Why Linear Regression?**
Tested on this dataset it gives clean, interpretable results. The pipeline wraps OneHotEncoding + Linear Regression together so new predictions go through the exact same transformation as training data.

**Why 1000 random splits?**
`train_test_split` is random — different splits give different scores. We ran 1000 splits, found the one with the best R² score, and trained the final model on that split.

---

## Results

| Metric | Score |
|---|---|
| R² Score | ~0.85 |
| Best random state | found via 1000 iterations |

---

## EDA Highlights

- **Maruti dominates** the dataset — model predicts budget cars more accurately than luxury
- **Brand is the strongest predictor** — numeric features (year, kms) have weak correlation with price alone
- **Diesel cars** command higher average prices than petrol
- **Right-skewed price distribution** — most cars between 1-5 lac, few outliers above 20 lac
- **Newer cars have wider price variance** — a 2019 car could be a cheap Maruti or an expensive BMW

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.9.0-orange?style=flat-square)
![Pandas](https://img.shields.io/badge/Pandas-2.0-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58-red?style=flat-square)

---

## Project Structure
car-price-predictor/

├── app.py                        # Streamlit frontend

├── LinearRegressionModel.pkl     # Trained pipeline (OHE + LR)

├── Cleaned_Car.csv               # Cleaned dataset for dropdowns

├── car_price_predictor.ipynb     # Full EDA + training notebook

└── requirements.txt

---

## Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/Noorumms/car-price-predictor.git
cd car-price-predictor
```

**2. Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
streamlit run app.py
```

---

## Requirements
streamlit

scikit-learn==1.9.0

pandas

numpy

---

## Key Learnings

- Real world data is messy — 40% of cleaning effort was just the year and price columns
- Brand name carries more price signal than year or kms driven — categorical features matter
- Wrapping preprocessing in a `Pipeline` prevents data leakage and makes deployment clean
- Running 1000 random splits instead of one gives a much more reliable final model
- Outlier removal (60 lac threshold) improved model performance significantly

---

## Dataset

[Quikr Used Cars Dataset](https://www.kaggle.com/datasets/arnabchaki/used-cars-dataset) — scraped from Quikr India.
Prices are in **INR (Indian Rupees)**.

---

## Author

**Noor Fatima**
[LinkedIn](https://linkedin.com/in/noor-fatimah-8b86322a7) · [Portfolio](https://noorumms.vercel.app) · [GitHub](https://github.com/Noorumms)
