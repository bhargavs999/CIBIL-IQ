import streamlit as st
from utils import ask_gemini_for_analysis
import math

WEIGHTS = {"payment_history":0.35,"credit_utilization":0.30,"credit_age":0.15,"credit_mix":0.10,"new_credit":0.10}

def compute_base_score(profile):
    s = {}
    ph = 100
    ph += {"Never missed":0,"1–29 days":-15,"30–59 days":-30,"60–89 days":-50,"90+ days":-70}.get(profile["dpd_worst"],0)
    ph -= min(profile["missed_payments_12m"]*10, 40)
    ph -= min(profile["missed_payments_lifetime"]*3, 20)
    ph -= profile["settled_accounts"] * 25
    s["payment_history"] = max(0, min(100, ph))
    u = profile["utilization_pct"]
    s["credit_utilization"] = 85 if u==0 else 100 if u<=10 else 90 if u<=30 else 65 if u<=50 else 35 if u<=75 else 10
    a = profile["credit_age_years"]
    s["credit_age"] = 0 if a==0 else 25 if a<1 else 55 if a<3 else 75 if a<5 else 88 if a<7 else 100
    mx = 40
    if profile["num_cards"] >= 1: mx += 20
    if len(profile["loan_types"]) >= 1: mx += 20
    if any(x in profile["loan_types"] for x in ["Home Loan","Car Loan"]): mx += 20
    s["credit_mix"] = min(100, mx)
    e = profile["hard_enquiries_6m"]
    s["new_credit"] = 100 if e==0 else 80 if e==1 else 60 if e==2 else 35 if e<=4 else 10
    w = sum(s[k]*WEIGHTS[k] for k in WEIGHTS)
    return {"score": max(300, min(900, int(300+(w/100)*600))), "factors": s}

def get_score_band(score):
    if score>=800: return {"label":"Exceptional","color":"#22C55E","bg":"rgba(34,197,94,0.08)","border":"rgba(34,197,94,0.2)"}
    if score>=750: return {"label":"Very Good",  "color":"#86EFAC","bg":"rgba(134,239,172,0.08)","border":"rgba(134,239,172,0.2)"}
    if score>=700: return {"label":"Good",        "color":"#FCD34D","bg":"rgba(252,211,77,0.08)", "border":"rgba(252,211,77,0.2)"}
    if score>=650: return {"label":"Fair",        "color":"#F97316","bg":"rgba(249,115,22,0.08)", "border":"rgba(249,115,22,0.2)"}
    return                {"label":"Poor",        "color":"#EF4444","bg":"rgba(239,68,68,0.08)",  "border":"rgba(239,68,68,0.2)"}

def build_gauge_html(score, band):
    pct=(score-300)/600; cx,cy,r=150,125,95; sw=240
    def pt(deg,rad): a=math.radians(deg); return cx+rad*math.cos(a), cy+rad*math.sin(a)
    s0x,s0y=pt(210,r); e0x,e0y=pt(210-sw,r); fs=sw*pct; fx,fy=pt(210-fs,r)
    lg="1" if fs>180 else "0"; op=min(1.0,0.35+pct*0.65)
    return (
        f'<svg viewBox="0 0 300 170" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:260px;display:block;margin:0 auto;">'
        f'<defs><linearGradient id="g{score}" x1="0%" y1="0%" x2="100%" y2="0%">'
        f'<stop offset="0%" stop-color="#EF4444"/><stop offset="40%" stop-color="#F59E0B"/>'
        f'<stop offset="75%" stop-color="#86EFAC"/><stop offset="100%" stop-color="#22C55E"/>'
        f'</linearGradient></defs>'
        f'<path d="M{s0x:.1f},{s0y:.1f} A{r},{r} 0 1 1 {e0x:.1f},{e0y:.1f}" fill="none" stroke="#1E2535" stroke-width="13" stroke-linecap="round"/>'
        f'<path d="M{s0x:.1f},{s0y:.1f} A{r},{r} 0 {lg} 1 {fx:.1f},{fy:.1f}" fill="none" stroke="url(#g{score})" stroke-width="13" stroke-linecap="round" opacity="{op:.2f}"/>'
        f'<text x="{cx}" y="{cy}" text-anchor="middle" font-family="Space Grotesk,sans-serif" font-size="36" font-weight="700" fill="{band["color"]}">{score}</text>'
        f'<text x="{cx}" y="{cy+20}" text-anchor="middle" font-family="Inter,sans-serif" font-size="12" fill="rgba(255,255,255,0.4)">{band["label"]}</text>'
        f'<text x="22" y="158" text-anchor="middle" font-family="Inter" font-size="9" fill="#2E3A4E">300</text>'
        f'<text x="278" y="158" text-anchor="middle" font-family="Inter" font-size="9" fill="#2E3A4E">900</text>'
        f'</svg>'
    )

def emi_calc(principal, rate_annual, months):
    r = rate_annual / (12 * 100)
    if r == 0: return principal / months
    return principal * r * (1+r)**months / ((1+r)**months - 1)

def render():
    profile = st.session_state.get("profile")
    if not profile:
        st.warning("Please complete your profile first.")
        if st.button("← Back to Profile"): st.session_state.screen="input"; st.rerun()
        return

    sd = compute_base_score(profile)
    score = sd["score"]; band = get_score_band(score)

    if "ai_analysis" not in st.session_state or st.session_state.ai_analysis is None:
        st.session_state.ai_analysis = ask_gemini_for_analysis(profile, sd)
    ai = st.session_state.ai_analysis

    st.markdown('<div class="pw">', unsafe_allow_html=True)

    if st.button("← Edit Profile"):
        st.session_state.pop("ai_analysis", None); st.session_state.screen="input"; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
<div style="background:rgba(245,158,11,0.06);border:1px solid rgba(245,158,11,0.15);
     border-radius:8px;padding:8px 14px;margin-bottom:1.5rem;text-align:center;
     font-size:11.5px;color:rgba(255,255,255,0.38);">
    ⚠️ Simulation only — not actual CIBIL bureau data. Visit <strong style="color:rgba(255,255,255,0.5);">cibil.com</strong> for your official score.
</div>""", unsafe_allow_html=True)

    # ── Score + Summary ──────────────────────────────────────────────────────
    cg, cs = st.columns([1,2])
    with cg:
        st.markdown(f"""
<div style="background:#0D1117;border:1px solid #1E2535;border-radius:12px;padding:1.25rem;text-align:center;">
    <div style="font-family:'Space Grotesk',sans-serif;font-size:10px;font-weight:600;letter-spacing:0.1em;
         text-transform:uppercase;color:rgba(255,255,255,0.25);margin-bottom:0.75rem;">Estimated Score</div>
    {build_gauge_html(score,band)}
</div>""", unsafe_allow_html=True)

    with cs:
        summ = ai.get("score_summary","") if ai else ""
        strn = ai.get("biggest_strength","") if ai else ""
        weak = ai.get("biggest_weakness","") if ai else ""
        st.markdown(f"""
<div style="background:{band['bg']};border:1px solid {band['border']};border-radius:12px;padding:1.25rem;">
    <div style="font-family:'Space Grotesk',sans-serif;font-size:10px;font-weight:600;letter-spacing:0.1em;
         text-transform:uppercase;color:{band['color']};margin-bottom:0.6rem;opacity:0.8;">Score Analysis</div>
    <p style="font-size:13.5px;color:rgba(255,255,255,0.8);line-height:1.75;margin-bottom:0.9rem;">{summ}</p>
    <div style="display:flex;gap:8px;flex-wrap:wrap;">
        <div style="flex:1;min-width:150px;background:rgba(34,197,94,0.07);border:1px solid rgba(34,197,94,0.18);border-radius:8px;padding:9px 12px;">
            <div style="font-size:9.5px;font-weight:600;letter-spacing:0.08em;color:#22C55E;margin-bottom:3px;">💪 STRENGTH</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.65);">{strn}</div>
        </div>
        <div style="flex:1;min-width:150px;background:rgba(239,68,68,0.07);border:1px solid rgba(239,68,68,0.18);border-radius:8px;padding:9px 12px;">
            <div style="font-size:9.5px;font-weight:600;letter-spacing:0.08em;color:#EF4444;margin-bottom:3px;">⚠️ KEY ISSUE</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.65);">{weak}</div>
        </div>
    </div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Score Benchmarks ─────────────────────────────────────────────────────
    st.markdown("""
<div style="font-family:'Space Grotesk',sans-serif;font-size:10px;font-weight:600;letter-spacing:0.1em;
     text-transform:uppercase;color:rgba(255,255,255,0.25);margin-bottom:0.85rem;">How You Compare</div>
""", unsafe_allow_html=True)
    benchmarks = [("Indian Average","~750","rgba(255,255,255,0.15)"),("Your Score",str(score),band['color']),
                  ("Top 10% Borrowers","800+","#22C55E"),("Minimum for Home Loan","700","#F59E0B")]
    bcols = st.columns(4)
    for i,(lbl,val,col) in enumerate(benchmarks):
        with bcols[i]:
            st.markdown(f"""
<div style="background:#0D1117;border:1px solid #1E2535;border-radius:10px;padding:0.85rem;text-align:center;">
    <div style="font-family:'Space Grotesk',sans-serif;font-size:22px;font-weight:700;color:{col};">{val}</div>
    <div style="font-size:11px;color:rgba(255,255,255,0.38);margin-top:4px;">{lbl}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Factor Breakdown ─────────────────────────────────────────────────────
    st.markdown("""
<div style="font-family:'Space Grotesk',sans-serif;font-size:10px;font-weight:600;letter-spacing:0.1em;
     text-transform:uppercase;color:rgba(255,255,255,0.25);margin-bottom:0.85rem;">Score Factors</div>
""", unsafe_allow_html=True)
    fmeta = {
        "payment_history":    ("Payment History",   "35%","📅"),
        "credit_utilization": ("Credit Utilization","30%","💳"),
        "credit_age":         ("Credit Age",        "15%","📆"),
        "credit_mix":         ("Credit Mix",        "10%","🏦"),
        "new_credit":         ("New Credit",        "10%","🔍"),
    }
    fi = ai.get("factor_insights",{}) if ai else {}
    cols = st.columns(5)
    for i,(k,(lbl,wt,ico)) in enumerate(fmeta.items()):
        v = sd["factors"][k]
        col = "#22C55E" if v>=75 else "#F59E0B" if v>=50 else "#EF4444"
        ins = fi.get(k,"")
        with cols[i]:
            st.markdown(f"""
<div style="background:#0D1117;border:1px solid #1E2535;border-radius:10px;padding:0.85rem 0.7rem;text-align:center;">
    <div style="font-size:18px;margin-bottom:5px;">{ico}</div>
    <div style="font-family:'Space Grotesk',sans-serif;font-size:21px;font-weight:700;color:{col};">{v:.0f}</div>
    <div style="font-size:9.5px;color:rgba(255,255,255,0.28);margin-bottom:4px;">/100 · {wt}</div>
    <div style="font-size:11px;font-weight:600;color:rgba(255,255,255,0.6);margin-bottom:6px;">{lbl}</div>
    <div style="height:3px;background:#1E2535;border-radius:2px;margin-bottom:6px;">
        <div style="width:{v}%;height:3px;background:{col};border-radius:2px;"></div>
    </div>
    <div style="font-size:10px;color:rgba(255,255,255,0.38);line-height:1.5;text-align:left;">{ins}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Action Plan ──────────────────────────────────────────────────────────
    if ai and ai.get("action_plan"):
        st.markdown("""
<div style="font-family:'Space Grotesk',sans-serif;font-size:10px;font-weight:600;letter-spacing:0.1em;
     text-transform:uppercase;color:rgba(255,255,255,0.25);margin-bottom:0.85rem;">Your Action Plan</div>
""", unsafe_allow_html=True)
        for i,a in enumerate(ai.get("action_plan",[])):
            pc = "#EF4444" if a.get("priority")=="high" else "#F59E0B"
            st.markdown(f"""
<div style="background:#0D1117;border:1px solid #1E2535;border-radius:10px;
     padding:0.9rem 1.1rem;margin-bottom:8px;display:flex;gap:0.9rem;align-items:flex-start;">
    <div style="background:rgba(79,142,247,0.1);border:1px solid rgba(79,142,247,0.2);border-radius:6px;
         min-width:28px;height:28px;display:flex;align-items:center;justify-content:center;
         font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:13px;color:#4F8EF7;">{i+1}</div>
    <div style="flex:1;">
        <div style="display:flex;align-items:center;gap:7px;margin-bottom:3px;flex-wrap:wrap;">
            <span style="font-size:13.5px;font-weight:600;color:#E5EAF5;">{a.get('action','')}</span>
            <span style="font-size:9.5px;background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.18);
                 color:{pc};padding:2px 7px;border-radius:4px;font-weight:600;">{a.get('priority','med').upper()}</span>
        </div>
        <div style="font-size:12px;color:rgba(255,255,255,0.48);margin-bottom:6px;">{a.get('detail','')}</div>
        <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <span style="font-size:11px;color:#22C55E;font-weight:600;">📈 {a.get('score_impact','')}</span>
            <span style="font-size:11px;color:rgba(255,255,255,0.35);">⏱ {a.get('time_to_impact','')}</span>
        </div>
    </div>
</div>""", unsafe_allow_html=True)

        outlook = ai.get("loan_eligibility_outlook","")
        if outlook:
            st.markdown(f"""
<div style="background:rgba(79,142,247,0.05);border:1px solid rgba(79,142,247,0.15);
     border-radius:10px;padding:0.9rem 1.1rem;margin-top:0.5rem;">
    <div style="font-size:10px;font-weight:600;letter-spacing:0.08em;color:#4F8EF7;margin-bottom:5px;">🏦 LOAN OUTLOOK</div>
    <div style="font-size:13px;color:rgba(255,255,255,0.62);line-height:1.7;">{outlook}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── EMI Calculator ───────────────────────────────────────────────────────
    st.markdown("""
<div style="font-family:'Space Grotesk',sans-serif;font-size:10px;font-weight:600;letter-spacing:0.1em;
     text-transform:uppercase;color:rgba(255,255,255,0.25);margin-bottom:0.85rem;">🧮 EMI Calculator</div>
""", unsafe_allow_html=True)
    with st.expander("Calculate your loan EMI based on your score", expanded=False):
        ec1,ec2,ec3 = st.columns(3)
        with ec1: loan_amt   = st.number_input("Loan Amount (₹)", 100_000, 100_000_000, 2_000_000, 100_000, key="emi_amt")
        with ec2: rate_input = st.number_input("Interest Rate (% p.a.)", 5.0, 30.0, 8.5, 0.1, key="emi_rate")
        with ec3: tenure     = st.number_input("Tenure (months)", 12, 360, 240, 12, key="emi_tenure")
        monthly_emi = emi_calc(loan_amt, rate_input, tenure)
        total_pay   = monthly_emi * tenure
        total_int   = total_pay - loan_amt
        fobr_ratio  = (monthly_emi / profile["monthly_income"] * 100) if profile["monthly_income"] > 0 else 0
        fobr_color  = "#22C55E" if fobr_ratio < 40 else "#F59E0B" if fobr_ratio < 55 else "#EF4444"
        fobr_label  = "Healthy (<40%)" if fobr_ratio < 40 else "Stretched (40–55%)" if fobr_ratio < 55 else "Unaffordable (>55%)"
        rc1,rc2,rc3,rc4 = st.columns(4)
        for col_w, label, value in [
            (rc1,"Monthly EMI",f"₹{monthly_emi:,.0f}"),
            (rc2,"Total Interest",f"₹{total_int:,.0f}"),
            (rc3,"Total Payable",f"₹{total_pay:,.0f}"),
            (rc4,"FOIR Ratio",f"{fobr_ratio:.1f}%"),
        ]:
            v_color = fobr_color if label=="FOIR Ratio" else "#4F8EF7"
            with col_w:
                st.markdown(f"""
<div style="background:#0D1117;border:1px solid #1E2535;border-radius:10px;padding:0.85rem;text-align:center;">
    <div style="font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:700;color:{v_color};">{value}</div>
    <div style="font-size:11px;color:rgba(255,255,255,0.35);margin-top:4px;">{label}</div>
    {"<div style='font-size:10px;color:"+fobr_color+";margin-top:2px;'>"+fobr_label+"</div>" if label=="FOIR Ratio" else ""}
</div>""", unsafe_allow_html=True)
        st.markdown("""
<div style="font-size:11px;color:rgba(255,255,255,0.3);margin-top:0.75rem;">
    FOIR (Fixed Obligation to Income Ratio) — banks typically approve loans where FOIR stays below 40–50%.
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        if st.button("🎛 What-If Simulator →", use_container_width=True):
            st.session_state.screen="whatif"; st.rerun()
    with c2:
        if st.button("🏦 See Loan Matches →", use_container_width=True):
            st.session_state.screen="loans"; st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
