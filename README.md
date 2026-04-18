# CIBIL IQ — Credit Score Simulator

> A free, offline-capable financial intelligence tool that estimates your CIBIL credit score, explains every factor, and shows you exactly how to improve it — built with Python and Streamlit.

---

## 🚀 Live Demo

**👉 [Click here to open the app](<https://cibil-iq.streamlit.app/>)**

---

## 📌 What It Does

CIBIL IQ simulates your CIBIL credit score using the same five weighted factors that TransUnion CIBIL uses. It gives you a personalised breakdown, an action plan to improve your score, bank-wise loan eligibility, and a built-in EMI calculator — all running instantly with no external API.

---

## ✨ Features

### ① Profile Input
- Collects income, employment, credit cards, active loans, payment history, and credit enquiries
- Live credit utilization calculator with colour-coded feedback
- Clean, section-based form layout

### ② Score Report
- Animated gauge displaying your estimated CIBIL score (300–900)
- Score band: Poor / Fair / Good / Very Good / Exceptional
- Full breakdown of all 5 CIBIL factors with individual scores and progress bars
- Personalised action plan with score impact and time estimates for each step
- **Benchmark comparison** — how your score compares to the Indian average, top 10% borrowers, and the minimum required for a home loan
- Loan eligibility outlook
- **EMI Calculator** — enter loan amount, rate, and tenure to instantly see:
  - Monthly EMI
  - Total interest payable
  - Total amount payable
  - FOIR (Fixed Obligation to Income Ratio) with affordability verdict

### ③ What-If Score Lab
- Interactive sliders to simulate changes to utilization, missed payments, enquiries, credit age, and settled accounts
- Real-time score update and delta display
- Factor-by-factor change table
- One-click action plan for your simulated scenario

### ④ Loan Matcher
- Eligibility check across 6 major Indian banks: SBI, HDFC, ICICI, Axis, Kotak, PNB
- Covers Home Loan, Personal Loan, and Car Loan
- Shows interest rate range and minimum score requirement per bank
- Negotiation tips and loan outlook personalised to your profile
- "Points needed to unlock next tier" nudge

---

## 🏦 CIBIL Scoring Model Used

| Factor | Weight | What It Measures |
|--------|--------|-----------------|
| Payment History | 35% | Missed payments, DPD, settled accounts |
| Credit Utilization | 30% | Balance-to-limit ratio across all cards |
| Credit Age | 15% | Age of oldest credit account |
| Credit Mix | 10% | Diversity of credit types (cards + loans) |
| New Credit | 10% | Hard enquiries in last 6 months |

Score range: **300 (Poor) → 900 (Exceptional)**

---

## 🗂 Project Structure

```
CIBIL IQ/
├── app.py                  # Main entry point, global CSS, routing
├── utils.py                # Rule-based credit analysis engine
├── requirements.txt
├── .streamlit/
│   └── secrets.toml        # No API keys required
└── pages/
    ├── __init__.py
    ├── profile_input.py    # Step 1: User profile form
    ├── score_report.py     # Step 2: Score, factors, EMI calculator
    ├── whatif_lab.py       # Step 3: Interactive score simulator
    └── loan_matcher.py     # Step 4: Bank eligibility matcher
```

---

## ⚙️ Setup & Run Locally

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
git clone https://github.com/your-username/cibil-iq.git
cd cibil-iq
pip install -r requirements.txt
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## ☁️ Deploy on Streamlit Cloud

1. Push the project to a public GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repo → set main file to `app.py`
4. Click **Deploy** — no environment variables or secrets needed

---

## 💡 Key Design Decisions

**No external API** — The analysis engine (`utils.py`) is entirely rule-based, using the actual CIBIL weighting formula. This means zero latency, zero rate limits, zero cost, and the app works even offline. The insights are personalised to each user's exact numbers — specific rupee amounts to pay down, precise months to recovery, etc.

**FOIR Calculator** — Banks use Fixed Obligation to Income Ratio to assess repayment capacity. Including it makes this a genuinely useful pre-application tool, not just a score estimator.

**What-If Lab** — Users can test "what if I reduce utilization to 20%?" or "what if I clear my missed payments?" and see the exact score delta, making the tool educational and actionable.

---

## 📊 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend & Backend | Python + Streamlit |
| Styling | Custom CSS (Space Grotesk + Inter fonts) |
| Charting | SVG (hand-built gauge) |
| Analysis Engine | Rule-based Python (no API) |
| Deployment | Streamlit Community Cloud |

---

## ⚠️ Disclaimer

This tool is an **educational simulation** — it does not access your actual CIBIL bureau data. Scores are estimated based on the information you provide using publicly documented CIBIL weightings. For your official credit score, visit [cibil.com](https://www.cibil.com).

---

## 👤 Author - BHARGAV SINGH 

Built a project demonstrating applied financial data modelling, UI/UX design, and deployment on Streamlit Cloud.

---

*CIBIL IQ is not affiliated with TransUnion CIBIL Limited.*
