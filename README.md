# CIBIL IQ — Credit Intelligence Platform

> A production-grade credit score simulator and financial intelligence tool built entirely in Python and Streamlit. CIBIL IQ replicates the TransUnion CIBIL scoring model to estimate your credit score, diagnose every factor affecting it, calculate loan affordability, match you to real Indian bank products, and generate a step-by-step financial recovery or optimisation plan — all running instantly in the browser with zero external dependencies.

---

## Live Demo

**👉 [Click here to open the app](<https://cibil-iq.streamlit.app/>)**

---

## Why This Project Exists

Most Indians discover their credit score only at the loan counter — when it's already too late to improve it. CIBIL IQ solves that by putting a comprehensive credit intelligence engine in the hands of anyone with a browser. It doesn't just show you a number; it explains the mechanics behind it, quantifies exactly what each action is worth in points, identifies the specific flags that an underwriter would see in your file, and tells you which banks to walk into first and what to say when you get there.

The analysis engine mirrors the exact five-factor weighting model that TransUnion CIBIL uses — not an approximation. Every output is personalised to the user's actual numbers: specific rupee amounts to pay down, real bank names and rates, precise timelines, and the lender psychology behind each recommendation.

---

## Feature Walkthrough

### Step 1 — Profile Input

The onboarding form collects 16 data points across five structured sections, each designed to mirror exactly what a bank's underwriting system evaluates.

**Income & Employment**
- Monthly take-home income (used for FOIR calculation on every subsequent page)
- Employment type: Salaried / Self-Employed / Business Owner / Freelancer / Student
- Years at current job or business (lenders weight income stability separately from income level)

**Credit Cards**
- Number of active credit cards across all banks
- Combined credit limit across all cards
- Current total outstanding balance
- Live credit utilization percentage with a colour-coded progress bar that updates as you type — green below 30%, amber 30–50%, red above 50% — with a plain-language verdict ("Excellent — ideal for score" / "High — hurting your score monthly" / "Very high — major score drag, act immediately")

**Active Loans**
- Number of active loan accounts
- Total principal outstanding across all loans
- Loan type checkboxes: Home Loan/LAP, Car/Vehicle Loan, Personal Loan, Education Loan (used for credit mix scoring and FOIR estimation)

**Payment History** *(the highest-weighted section at 35%)*
- Missed payments in the last 12 months
- Total missed payments across the entire credit lifetime
- Worst Days Past Due (DPD) ever recorded: Never missed / 1–29 days / 30–59 days / 60–89 days / 90+ days

**Credit History & Enquiries**
- Age of oldest account in years (the primary credit age input)
- Number of loan or card applications in the last 6 months (each creates a hard enquiry)
- Number of settled or written-off accounts (the most serious derogatory flag)

Every input field carries a tooltip explaining what the field measures, why lenders care about it, and what value to enter if you're unsure.

---

### Step 2 — Score Report

The score report is the analytical core of the application. It translates 16 raw inputs into a structured multi-section intelligence brief.

**Estimated Score Gauge**
- SVG arc gauge spanning 300 to 900, built from scratch with hand-calculated arc coordinates
- Live gradient fill from red (300) through amber to green (900) with opacity proportional to score level
- Score rendered in the centre alongside the band label
- Colour-coded band badge: Poor (red) / Fair (orange) / Good (yellow) / Very Good (green-tinted) / Exceptional (green)

**Score Summary**
- A 2–3 sentence personalised interpretation of what the score means in today's Indian lending market
- Specific references to which banks will compete for your business, what documentation they'll ask for, and whether you are effectively pre-approved anywhere

**What This Band Means for Loans**
- Concrete rate ranges available at this band (e.g. "home loans at 8.50–8.80%, personal loans up to ₹25L")
- Which specific private and PSU banks are accessible vs borderline at this band
- The precise monthly savings from improving to the next band on a ₹50L home loan

**Biggest Strength**
- Identifies the highest-scoring CIBIL factor with specific numbers
- Explains *why* that factor is valuable to lenders in plain language
- Not generic — references the user's exact percentage, years, or count

**Biggest Weakness**
- Identifies the primary drag on the score with exact figures
- If settled accounts exist, they are always surfaced here with the 7-year retention explanation
- If DPD is severe, the delinquency aging curve is explained
- If utilization is the issue, the exact rupee amount to pay down is calculated and stated

**Income & Debt Analysis**
- Calculates the user's estimated FOIR (Fixed Obligation to Income Ratio) from their income and outstanding loan balance
- States their current FOIR as a percentage
- Tells them their remaining monthly EMI capacity in rupees before hitting bank ceilings
- Flags if FOIR is above 50–55% and explains that new loan approvals will be difficult until it comes down

**12-Month Trajectory**
- Scores the profile across 5 binary dimensions: utilization ≤30%, zero missed payments, ≤1 enquiry, zero settled accounts, clean DPD
- Renders a narrative — improving / mixed / under pressure — based on how many dimensions are positive
- Projects what happens to the score over 12 months if no action is taken vs if the action plan is followed

**Red Flags Lenders Will See**
- Only surfaces flags that actually exist in the user's data — no generic warnings
- Covers: settled/written-off accounts, severe DPD, recent missed payments, high enquiry count, extreme utilization, and high FOIR
- Each flag is described exactly as an underwriter would phrase it internally

**Positive Signals**
- Lists the specific positive traits a lender will see when reviewing the file
- Covers: clean payment record, low utilization, long credit history, zero enquiries, diverse credit mix, stable employment tenure, and high income
- Directly actionable: tells the user which of these to lead with in a loan application conversation

**Score Factor Breakdown**
Five individual factor cards displayed in a responsive 5-column grid, each showing:
- The factor score out of 100
- The CIBIL weight (35% / 30% / 15% / 10% / 10%)
- A progress bar coloured green / amber / red based on the score
- A specific insight referencing the user's actual numbers — not placeholder text

| Factor | Weight | Insight Type |
|--------|--------|-------------|
| Payment History | 35% | Exact missed count, DPD reference, auto-pay instruction |
| Credit Utilization | 30% | Current %, target %, exact rupee amount to pay |
| Credit Age | 15% | Age in years, account closure warning, passive growth explanation |
| Credit Mix | 10% | Product types held, specific FD-backed loan suggestion if needed |
| New Credit | 10% | Enquiry count, cooling period advice, soft-check guidance |

**Personalised Action Plan**
Up to 5 prioritised actions, each containing:
- Action title
- Step-by-step instruction with specific rupee amounts, bank names, portal URLs, and regulatory timelines (e.g. "bureaus must resolve disputes within 30 working days under RBI guidelines")
- Priority badge: HIGH (red) or MEDIUM (amber)
- Estimated score impact range (e.g. "+30 to +50 points")
- Realistic timeline to see that impact in the Indian banking cycle
- "Why it matters" — the lender psychology or RBI regulation behind the action

Actions are generated conditionally based on the actual profile — only actions relevant to the user's specific issues appear. The order follows a strict priority logic: settled accounts first, then payment history, then utilization, then enquiries, then age, then mix.

**Quick Wins — Do These This Week**
- 3–4 immediate actions the user can take within days with no financial outlay
- Covers: auto-pay setup, extra card payment before statement date, free CIBIL report audit, credit limit increase request, FD-backed overdraft enquiry
- Each is specific — includes exact amounts, exact portals, exact steps

**Loan Eligibility Outlook**
- 3–4 sentences interpreting what the score means for loan applications right now
- Names specific banks to approach first and why
- States realistic interest rates for the current band
- Calculates the monthly saving from reaching the next score band on a typical loan amount

---

### Step 3 — What-If Score Lab

An interactive simulator that lets users test hypothetical improvements in real time without committing to anything.

**Adjustment Sliders**
Five sliders correspond to the five most actionable CIBIL variables:
- Credit utilization (0–100%)
- Missed payments in last 12 months (0–12)
- Hard enquiries in last 6 months (0–10)
- Age of oldest account in years (0–20)
- Number of settled/written-off accounts (0–5)

**Live Score Gauge**
- Score updates instantly as sliders move — no button press required
- Shows the simulated score on the same SVG gauge used in the report
- Displays the point delta vs the user's actual baseline score (e.g. "+47 pts") in green or red
- Renders the new score band badge

**Factor Changes Grid**
A 5-column grid showing, for every factor:
- The before and after score (e.g. "45→78")
- The delta as a signed number in green or red

**Simulation Analysis** *(auto-updates with every slider change)*
The full analysis engine reruns instantly on the simulated profile and renders:
- A new personalised score summary for the simulated scenario
- Strongest factor vs still-needs-work factor for the simulated profile
- Income & debt analysis recalculated against the simulation
- 12-month trajectory for the simulated scenario
- Loan eligibility outlook for the simulated score
- A full action plan (up to 3 items) specific to what still needs fixing in the simulation

This means a user can drag the utilization slider from 65% to 20%, watch the score jump 38 points, and immediately read a full analysis of what that 38-point improvement unlocks — which banks open up, what rates become available, and what the remaining weaknesses are.

---

### Step 4 — Loan Matcher

Matches the user's profile against 6 major Indian banks across 3 loan types, with full product-level detail and a personalised application strategy.

**Loan Type Selector**
Horizontal radio toggle between:
- 🏠 Home Loan
- 💰 Personal Loan
- 🚗 Car Loan

**Approval Summary Bar**
Four summary chips at the top showing:
- Number of banks likely to approve
- Number of borderline banks
- Number of banks likely to reject
- Best available interest rate from approving banks

**Bank Cards (6 banks × 3 loan types)**
Each bank card shows:
- Bank name, full name, logo emoji, and PSU/Private badge
- Approval status badge: ✅ Likely Approved / 🟡 Borderline / ❌ Likely Rejected — with colour-coded background
- Interest rate range (e.g. "8.70–9.40%")
- Minimum credit score required
- Maximum tenure
- Processing fee
- A one-line positioning note explaining when this bank is the right choice

Banks covered: SBI, HDFC Bank, ICICI Bank, Axis Bank, Kotak Mahindra Bank, Punjab National Bank

Approval logic: 50+ points above minimum = Likely Approved; 0–49 above = Borderline; below minimum = Likely Rejected.

**Next Tier Nudge**
If any bank's minimum score is above the user's current score, a callout appears showing exactly how many points they need to unlock the next tier, with a link back to the What-If Lab.

**Personalised Loan Strategy**
The full analysis engine runs against the user's profile and renders a complete loan application brief:

- *Loan strategy for this loan type* — which banks to approach, in what order, what to say, whether to negotiate, and what rate to expect
- *Affordability & FOIR analysis* — whether the user can actually service the new EMI given their existing obligations
- *Highlight in your application* — the specific positive signals from the profile that the user should lead with when talking to a loan officer
- *Be ready to explain* — any red flags that will definitely come up in the application, with suggested responses
- *Actions before applying* — up to 3 high-priority improvements with exact instructions and score impact
- *Do before applying* — quick wins the user can action in the week before submitting a formal application

---

## Analysis Engine

The analysis engine (`utils.py`) is the intellectual core of the project. It is a deterministic rule-based system that processes 16 profile inputs through a multi-stage pipeline and produces 12 structured output fields.

**Inputs processed:**
Monthly income, employment type, employment years, number of cards, total credit limit, current card balance, utilization percentage, number of active loans, total loan outstanding, loan types held, missed payments (12-month), missed payments (lifetime), worst DPD, credit age, hard enquiries (6-month), settled accounts.

**Outputs produced:**

| Field | Description |
|-------|-------------|
| `score_summary` | Personalised interpretation of the score in the Indian lending context |
| `score_band_context` | Specific rates, banks, and approval experience for this score band |
| `biggest_strength` | The highest-scoring factor with data-referenced explanation |
| `biggest_weakness` | The primary drag with exact figures and remediation path |
| `factor_insights` | Individual insight for each of the 5 CIBIL factors |
| `action_plan` | Up to 5 conditional, prioritised actions with full instructions |
| `loan_eligibility_outlook` | Which loans are accessible now, which banks to approach, rate expectations |
| `income_debt_analysis` | FOIR calculation with EMI headroom in rupees |
| `credit_health_trajectory` | 12-month projection based on current profile momentum |
| `quick_wins` | 3–4 immediate actions requiring no financial outlay |
| `red_flags_for_lenders` | Derogatory marks visible to underwriters, only if present |
| `positive_signals` | Strengths to surface in a loan application conversation |

**CIBIL Scoring Formula implemented:**

```
Score = 300 + (weighted_average / 100) × 600

Payment History Score:
  Base: 100
  DPD adjustment: 0 / -15 / -30 / -50 / -70 (Never / 1-29 / 30-59 / 60-89 / 90+)
  Missed payments (12m): -10 per miss, capped at -40
  Missed payments (lifetime): -3 per miss, capped at -20
  Settled accounts: -25 per account

Credit Utilization Score:
  0%: 85 | ≤10%: 100 | ≤30%: 90 | ≤50%: 65 | ≤75%: 35 | >75%: 10

Credit Age Score:
  0 yrs: 0 | <1 yr: 25 | <3 yrs: 55 | <5 yrs: 75 | <7 yrs: 88 | ≥7 yrs: 100

Credit Mix Score:
  Base: 40 | Has cards: +20 | Has loans: +20 | Has secured loan: +20 (capped at 100)

New Credit Score:
  0 enquiries: 100 | 1: 80 | 2: 60 | 3–4: 35 | 5+: 10
```

Every action plan item, insight, red flag, and positive signal is conditionally generated. Nothing is hardcoded to always appear — the engine evaluates each condition against the actual profile data and only produces output that is relevant.

---

## CIBIL Scoring Model Reference

| Factor | Weight | What It Measures |
|--------|--------|-----------------|
| Payment History | 35% | Missed payments, DPD severity, settled/written-off accounts |
| Credit Utilization | 30% | Balance-to-limit ratio across all revolving credit |
| Credit Age | 15% | Age of the oldest open credit account |
| Credit Mix | 10% | Diversity: secured + unsecured, revolving + installment |
| New Credit | 10% | Hard enquiries from loan/card applications in last 6 months |

Score range: **300 (Poor) → 900 (Exceptional)**

Indian average: ~720 | Home loan minimum: ~650 | Best rates: 750+

---

## Banks and Products Covered

| Bank | Type | Home Loan Min | Personal Loan Min | Car Loan Min |
|------|------|--------------|------------------|-------------|
| SBI | PSU | 650 | 700 | 650 |
| HDFC Bank | Private | 700 | 720 | 700 |
| ICICI Bank | Private | 700 | 710 | 700 |
| Axis Bank | Private | 700 | 700 | 700 |
| Kotak Mahindra | Private | 720 | 720 | 710 |
| PNB | PSU | 625 | 650 | 625 |

Each bank entry includes rate range, maximum tenure, and processing fee across all three loan types.

---

## Project Structure

```
CIBIL_IQ/
├── app.py                   # Entry point: page config, global CSS, navigation header, routing
├── utils.py                 # Analysis engine: 16-input → 12-output rule-based pipeline
├── requirements.txt         # Single dependency: streamlit>=1.32.0
└── pages/
    ├── __init__.py
    ├── profile_input.py     # 16-field form with live utilization calculator
    ├── score_report.py      # Score gauge, factor breakdown, action plan, FOIR, outlook
    ├── whatif_lab.py        # Interactive simulation with live score delta and analysis
    └── loan_matcher.py      # 6-bank eligibility matrix with personalised strategy
```

---

## Setup & Local Development

**Requirements:** Python 3.9+

```bash
git clone https://github.com/your-username/cibil-iq.git
cd cibil-iq
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`

---

## Deploy on Streamlit Cloud

1. Push the project to a public GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repo → set main file to `app.py`
4. Click **Deploy**

No environment variables. No secrets file. No external service configuration. The app is self-contained.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend & Backend | Python 3.9+ + Streamlit |
| Typography | Space Grotesk (headings) + Inter (body) via Google Fonts |
| Score Gauge | Custom hand-built SVG with arc path calculations |
| Analysis Engine | Deterministic rule-based Python — no ML, no external API |
| Styling | ~300 lines of custom CSS injected via `st.markdown` |
| Deployment | Streamlit Community Cloud |
| Dependencies | `streamlit>=1.32.0` only |

---

## Design Principles

**Every output references the user's actual numbers.** The analysis engine never produces generic advice. Every action plan item includes the exact rupee amount to pay, the exact number of months to wait, the specific bank to call, and the specific portal to visit. This is the difference between "reduce your utilization" and "pay ₹32,500 before your next HDFC statement date to bring utilization from 67% to 25%."

**The scoring model is transparent.** The formula is documented in the README and in the code comments. Users can see exactly why their score is what it is and verify the calculation themselves.

**Conditional output only.** Nothing appears unless it's relevant. If a user has no red flags, the red flags section shows a "No red flags detected" confirmation. If a user has a perfect profile, the action plan reflects that rather than manufacturing problems.

**No data leaves the session.** The application processes everything in Streamlit's session state. Nothing is transmitted to any server, stored in any database, or logged anywhere. The privacy model is zero-data by architecture, not by policy.

---

## Disclaimer

CIBIL IQ is an educational simulation tool. It does not connect to TransUnion CIBIL, any credit bureau, or any financial institution. Scores are estimated from user-provided inputs using the publicly documented CIBIL weighting methodology and do not constitute an official credit assessment. For your actual CIBIL score, visit [cibil.com](https://www.cibil.com).

*CIBIL IQ is not affiliated with or endorsed by TransUnion CIBIL Limited.*
