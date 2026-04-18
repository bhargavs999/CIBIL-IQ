def ask_gemini_for_analysis(profile: dict, score_data: dict) -> dict:
    """
    Rule-based credit analysis — no API, instant, always works.
    Returns the same structure the rest of the app expects.
    """
    score   = score_data.get("score", 0)
    factors = score_data.get("factors", {})

    u    = profile.get("utilization_pct", 0)
    miss = profile.get("missed_payments_12m", 0)
    age  = profile.get("credit_age_years", 0)
    enq  = profile.get("hard_enquiries_6m", 0)
    sett = profile.get("settled_accounts", 0)
    dpd  = profile.get("dpd_worst", "Never missed")
    emp  = profile.get("employment_type", "Salaried")
    eyrs = profile.get("employment_years", 0)

    # ── Score summary ────────────────────────────────────────────────────────
    if score >= 800:
        summary = (f"Your credit profile is exceptional at {score}/900 — you are in the top tier of borrowers in India. "
                   "Most lenders will offer you their best rates with minimal documentation.")
    elif score >= 750:
        summary = (f"Your score of {score}/900 is very good and well above the average Indian borrower. "
                   "You qualify for most loan products; a few targeted improvements could unlock premium rates.")
    elif score >= 700:
        summary = (f"Your score of {score}/900 is good and you are eligible with most major banks. "
                   "Reducing utilization and avoiding new enquiries over the next 6 months will push you into the 'Very Good' band.")
    elif score >= 650:
        summary = (f"Your score of {score}/900 is fair — you may face higher interest rates or stricter conditions. "
                   "Focus on clearing overdue balances and avoiding fresh applications for at least 6 months.")
    else:
        summary = (f"Your score of {score}/900 needs significant attention. "
                   "Prioritise clearing any overdue accounts and maintaining zero missed payments for 12 consecutive months.")

    # ── Biggest strength ─────────────────────────────────────────────────────
    best_factor = max(factors, key=factors.get) if factors else "payment_history"
    strength_map = {
        "payment_history":    "Your payment history is excellent — consistent on-time payments are the single most valued trait by lenders.",
        "credit_utilization": f"Your credit utilization of {u:.0f}% is well-managed, signalling responsible credit usage to bureaus.",
        "credit_age":         f"Your credit history spans {age} years, giving lenders confidence in your long-term borrowing behaviour.",
        "credit_mix":         "You have a healthy mix of credit types (cards + loans), which demonstrates versatile credit management.",
        "new_credit":         "You have made very few recent credit applications, keeping your profile clean and enquiry-free.",
    }
    strength = strength_map.get(best_factor, "Your overall credit discipline is your strongest asset.")

    # ── Biggest weakness ─────────────────────────────────────────────────────
    worst_factor = min(factors, key=factors.get) if factors else "credit_age"
    weakness_map = {
        "payment_history":    f"You have {miss} missed payment(s) in the last 12 months — this is the highest-weighted negative factor at 35%.",
        "credit_utilization": f"Your credit utilization is {u:.0f}% — anything above 30% actively reduces your score every month.",
        "credit_age":         f"Your oldest account is only {age} year(s) old — a thin credit history limits your score ceiling.",
        "credit_mix":         "You have limited diversity in credit types; adding a secured loan or a credit card could improve this.",
        "new_credit":         f"You made {enq} credit application(s) in the last 6 months — each hard enquiry temporarily lowers your score.",
    }
    if sett > 0:
        weakness = f"You have {sett} settled/written-off account(s) — this is a serious red flag that can stay on your report for 7 years."
    elif dpd not in ("Never missed", "1–29 days"):
        weakness = f"Your worst DPD is '{dpd}' — severe delinquency history significantly reduces lender confidence."
    else:
        weakness = weakness_map.get(worst_factor, "Your credit mix could be improved by diversifying your borrowing.")

    # ── Factor insights ──────────────────────────────────────────────────────
    ph_score = factors.get("payment_history", 100)
    cu_score = factors.get("credit_utilization", 100)

    fi = {
        "payment_history": (
            "Perfect payment record — keep it up." if miss == 0 and dpd == "Never missed"
            else f"{miss} missed payment(s) recently. Set auto-pay to prevent future misses."
        ),
        "credit_utilization": (
            f"{u:.0f}% utilization — excellent, keep below 30%." if u <= 30
            else f"{u:.0f}% utilization — pay down ₹{max(0,int((u-25)*profile.get('total_credit_limit',0)/100)):,} to reach 25%."
        ),
        "credit_age": (
            f"{age} year(s) history. Do not close your oldest card — age improves naturally over time." if age >= 3
            else f"Only {age} year(s) of history. Keep existing accounts open and avoid closing any."
        ),
        "credit_mix": (
            "Good mix of secured and unsecured credit." if len(profile.get("loan_types", [])) >= 2
            else "Consider a small secured loan (e.g. FD-backed) to diversify your credit mix."
        ),
        "new_credit": (
            "No recent enquiries — great discipline." if enq == 0
            else f"{enq} enquiry/enquiries in 6 months. Avoid all new applications for the next 6 months."
        ),
    }

    # ── Action plan ──────────────────────────────────────────────────────────
    actions = []

    if u > 30:
        reduce_by = int((u - 25) * profile.get("total_credit_limit", 0) / 100)
        actions.append({
            "action": "Reduce Credit Card Utilization",
            "detail": f"Pay down ₹{reduce_by:,} to bring utilization from {u:.0f}% to ~25%. Pay more than the minimum due each month.",
            "score_impact": "+20 to +40 points",
            "time_to_impact": "1–2 months",
            "priority": "high"
        })

    if miss > 0 or dpd not in ("Never missed", "1–29 days"):
        actions.append({
            "action": "Fix Payment History",
            "detail": "Set up auto-pay for all EMIs and credit card minimum dues. 12 months of clean payments can significantly recover your score.",
            "score_impact": "+30 to +50 points",
            "time_to_impact": "6–12 months",
            "priority": "high"
        })

    if enq >= 2:
        actions.append({
            "action": "Stop New Credit Applications",
            "detail": f"You have {enq} hard enquiries in 6 months. Every new application lowers your score. Apply for nothing new for at least 6 months.",
            "score_impact": "+10 to +20 points",
            "time_to_impact": "6 months",
            "priority": "high"
        })

    if sett > 0:
        actions.append({
            "action": "Address Settled / Written-Off Accounts",
            "detail": "Contact the lender to convert 'Settled' status to 'Closed' by paying the remaining amount. This removes the worst flag from your report.",
            "score_impact": "+40 to +80 points",
            "time_to_impact": "3–6 months after closure",
            "priority": "high"
        })

    if age < 3:
        actions.append({
            "action": "Do Not Close Old Accounts",
            "detail": f"Your oldest account is {age} year(s) old. Never close your oldest credit card — even if unused. Credit age grows passively.",
            "score_impact": "+10 to +25 points",
            "time_to_impact": "12–24 months",
            "priority": "medium"
        })

    if len(profile.get("loan_types", [])) < 2:
        actions.append({
            "action": "Diversify Credit Mix",
            "detail": "If you only have cards, consider an FD-backed loan or small personal loan. If you only have loans, add a credit card with low utilization.",
            "score_impact": "+10 to +20 points",
            "time_to_impact": "3–6 months",
            "priority": "medium"
        })

    if u <= 30 and miss == 0 and enq <= 1 and sett == 0:
        actions.append({
            "action": "Request Credit Limit Increase",
            "detail": "With your clean profile, ask your bank for a credit limit increase (without using it). This reduces utilization ratio automatically.",
            "score_impact": "+10 to +15 points",
            "time_to_impact": "1 month",
            "priority": "medium"
        })

    # Ensure at least 2 actions
    if not actions:
        actions.append({
            "action": "Monitor Your Credit Report",
            "detail": "Get your free annual CIBIL report at cibil.com. Check for errors, duplicate accounts, or fraudulent enquiries and raise disputes immediately.",
            "score_impact": "+5 to +30 points (if errors found)",
            "time_to_impact": "30–45 days",
            "priority": "medium"
        })

    # ── Loan outlook ─────────────────────────────────────────────────────────
    if score >= 750:
        outlook = "You are well-positioned to negotiate preferential interest rates with most major banks — approach 2–3 lenders and compare offers."
    elif score >= 700:
        outlook = "You qualify for home and car loans with most banks; personal loan approval is likely though rates may be 1–2% higher than premium borrowers."
    elif score >= 650:
        outlook = "You may face conditional approval — expect requests for a co-applicant or higher down payment; PSU banks like SBI and PNB are more accessible."
    else:
        outlook = "Loan approval will be difficult at most banks; focus on score improvement for 6–12 months before applying, or consider an NBFC as a starting point."

    return {
        "score_summary":          summary,
        "biggest_strength":       strength,
        "biggest_weakness":       weakness,
        "factor_insights":        fi,
        "action_plan":            actions[:4],
        "loan_eligibility_outlook": outlook,
    }
