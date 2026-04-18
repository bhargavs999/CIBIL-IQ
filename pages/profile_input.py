import streamlit as st

def render():
    st.markdown("""
<div class="hero">
    <div class="hero-badge">Free Credit Intelligence Tool</div>
    <h1>Know Your <em>CIBIL Score</em><br>Before the Bank Does</h1>
    <p>Enter your financial profile. We analyse it using real CIBIL weightings and show you exactly how to improve it.</p>
</div>
<div class="chips">
    <div class="chip">🔒 No data stored</div>
    <div class="chip">🏦 6 Indian banks matched</div>
    <div class="chip">📊 Real CIBIL weightings</div>
    <div class="chip">⚡ Instant results</div>
    <div class="chip">🧮 EMI calculator included</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="pw">', unsafe_allow_html=True)

    st.markdown('<div class="fc"><div class="fc-label">💼 Income & Employment</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1: monthly_income = st.number_input("Monthly Income (₹)", 0, 10_000_000, 75_000, 5_000)
    with c2: employment_type = st.selectbox("Employment Type", ["Salaried","Self-Employed","Business Owner","Freelancer","Student/No Income"])
    with c3: employment_years = st.number_input("Years Employed", 0, 50, 3, 1)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="fc"><div class="fc-label">💳 Credit Cards</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1: num_cards = st.number_input("No. of Credit Cards", 0, 20, 2, 1)
    with c2: total_credit_limit = st.number_input("Total Credit Limit (₹)", 0, 50_000_000, 200_000, 10_000)
    with c3: current_card_balance = st.number_input("Current Balance Owed (₹)", 0, 50_000_000, 40_000, 5_000)
    utilization = 0.0
    if total_credit_limit > 0:
        utilization = (current_card_balance / total_credit_limit) * 100
        col = "#22C55E" if utilization < 30 else "#F59E0B" if utilization < 50 else "#EF4444"
        tag = "✅ Excellent — keep below 30%" if utilization < 30 else "⚠️ High — actively hurts your score" if utilization < 50 else "🔴 Very high — major negative impact"
        st.markdown(f"""
<div style="margin-top:0.5rem;padding:9px 13px;background:#111827;border:1px solid #1E2535;
     border-radius:8px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
    <span style="font-size:12px;color:rgba(255,255,255,0.35);">Utilization</span>
    <span style="font-size:15px;font-weight:700;color:{col};">{utilization:.1f}%</span>
    <span style="font-size:11px;color:rgba(255,255,255,0.28);">{tag}</span>
</div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="fc"><div class="fc-label">🏠 Active Loans</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        num_active_loans = st.number_input("Number of Active Loans", 0, 20, 1, 1)
        home_loan      = st.checkbox("Home Loan / LAP")
        car_loan       = st.checkbox("Car / Vehicle Loan")
    with c2:
        total_loan_outstanding = st.number_input("Total Outstanding (₹)", 0, 100_000_000, 500_000, 10_000)
        personal_loan  = st.checkbox("Personal Loan", value=True)
        education_loan = st.checkbox("Education Loan")
    loan_types = [x for x,y in [("Home Loan",home_loan),("Car Loan",car_loan),("Personal Loan",personal_loan),("Education Loan",education_loan)] if y]
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="fc"><div class="fc-label">📅 Payment History — Highest Weight (35%)</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1: missed_payments_12m      = st.number_input("Missed Payments (last 12m)", 0, 50, 0, 1)
    with c2: missed_payments_lifetime = st.number_input("Total Missed Payments (ever)", 0, 100, 1, 1)
    with c3: dpd_worst = st.selectbox("Worst Days Past Due", ["Never missed","1–29 days","30–59 days","60–89 days","90+ days"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="fc"><div class="fc-label">📈 Credit History & Enquiries</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1: credit_age_years  = st.number_input("Age of Oldest Account (yrs)", 0, 40, 4, 1)
    with c2: hard_enquiries_6m = st.number_input("Loan/Card Applications (last 6m)", 0, 20, 1, 1)
    with c3: settled_accounts  = st.number_input("Settled / Written-off Accounts", 0, 20, 0, 1)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1,2,1])
    with mid:
        if st.button("📊 Analyse My CIBIL Score →", use_container_width=True):
            st.session_state.profile = {
                "monthly_income": monthly_income, "employment_type": employment_type,
                "employment_years": employment_years, "num_cards": num_cards,
                "total_credit_limit": total_credit_limit, "current_card_balance": current_card_balance,
                "utilization_pct": round(utilization,1), "num_active_loans": num_active_loans,
                "total_loan_outstanding": total_loan_outstanding, "loan_types": loan_types,
                "missed_payments_12m": missed_payments_12m, "missed_payments_lifetime": missed_payments_lifetime,
                "dpd_worst": dpd_worst, "credit_age_years": credit_age_years,
                "hard_enquiries_6m": hard_enquiries_6m, "settled_accounts": settled_accounts,
            }
            st.session_state.pop("ai_analysis", None)
            st.session_state.pop("sim_analysis", None)
            st.session_state.screen = "report"
            st.rerun()

    st.markdown("""
<div class="disc">Simulation only — not actual CIBIL bureau data. For your official score visit <strong>cibil.com</strong>.</div>
</div>""", unsafe_allow_html=True)
