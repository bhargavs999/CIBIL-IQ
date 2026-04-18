import streamlit as st
from pages.score_report import compute_base_score, get_score_band
from utils import ask_gemini_for_analysis

BANKS = [
    {"name":"SBI",  "full":"State Bank of India",  "logo":"🏛","home_loan":{"min_score":650,"rate":"8.50–9.65%"},"personal_loan":{"min_score":700,"rate":"11.05–14.05%"},"car_loan":{"min_score":650,"rate":"8.65–10.15%"}},
    {"name":"HDFC", "full":"HDFC Bank",            "logo":"🔷","home_loan":{"min_score":700,"rate":"8.70–9.40%"},"personal_loan":{"min_score":720,"rate":"10.50–24.00%"},"car_loan":{"min_score":700,"rate":"8.80–10.50%"}},
    {"name":"ICICI","full":"ICICI Bank",           "logo":"🔶","home_loan":{"min_score":700,"rate":"8.75–9.80%"},"personal_loan":{"min_score":710,"rate":"10.65–16.00%"},"car_loan":{"min_score":700,"rate":"8.75–10.00%"}},
    {"name":"Axis", "full":"Axis Bank",            "logo":"🟣","home_loan":{"min_score":700,"rate":"8.75–13.30%"},"personal_loan":{"min_score":700,"rate":"10.49–22.00%"},"car_loan":{"min_score":700,"rate":"8.75–11.00%"}},
    {"name":"Kotak","full":"Kotak Mahindra Bank",  "logo":"🔴","home_loan":{"min_score":720,"rate":"8.75–9.60%"},"personal_loan":{"min_score":720,"rate":"10.99–24.00%"},"car_loan":{"min_score":710,"rate":"9.00–11.50%"}},
    {"name":"PNB",  "full":"Punjab National Bank", "logo":"🟠","home_loan":{"min_score":625,"rate":"8.45–9.80%"},"personal_loan":{"min_score":650,"rate":"11.40–16.95%"},"car_loan":{"min_score":625,"rate":"8.75–9.75%"}},
]

SC = {
    "green":("#22C55E","rgba(34,197,94,0.08)","rgba(34,197,94,0.2)"),
    "amber":("#F59E0B","rgba(245,158,11,0.08)","rgba(245,158,11,0.2)"),
    "red":  ("#EF4444","rgba(239,68,68,0.08)", "rgba(239,68,68,0.2)")
}

def elig(bank, score, lt):
    ld = bank.get(lt)
    if not ld: return {"status":"N/A","code":"amber","rate":"—","min":0}
    m = score - ld["min_score"]
    if m >= 50: return {"status":"✅ Likely Approved","code":"green","rate":ld["rate"],"min":ld["min_score"]}
    if m >= 0:  return {"status":"🟡 Borderline",     "code":"amber","rate":ld["rate"],"min":ld["min_score"]}
    return             {"status":"❌ Likely Rejected","code":"red",  "rate":ld["rate"],"min":ld["min_score"]}

def render():
    profile = st.session_state.get("profile")
    if not profile:
        st.warning("Please complete your profile first.")
        if st.button("← Back"): st.session_state.screen = "input"; st.rerun()
        return

    sd = compute_base_score(profile)
    score = sd["score"]
    band = get_score_band(score)

    st.markdown('<div class="pw">', unsafe_allow_html=True)
    st.markdown(f"""
<div style="margin-bottom:1.5rem;">
    <div style="font-family:'Space Grotesk',sans-serif;font-size:1.5rem;font-weight:700;color:#F0F4FF;margin-bottom:0.3rem;">
        Your <span style="color:#4F8EF7;">Loan Matches</span>
    </div>
    <p style="font-size:13px;color:rgba(255,255,255,0.4);">
        Based on your score of <strong style="color:{band['color']}">{score}</strong> — eligibility across India's top 6 banks.
    </p>
</div>
""", unsafe_allow_html=True)

    if st.button("← Back to What-If Lab"):
        st.session_state.screen = "whatif"; st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)

    lt = st.radio("Loan type:", ["home_loan","personal_loan","car_loan"],
        format_func=lambda x: {"home_loan":"🏠 Home Loan","personal_loan":"💰 Personal Loan","car_loan":"🚗 Car Loan"}[x],
        horizontal=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Bank cards
    cols = st.columns(3)
    for i, bank in enumerate(BANKS):
        e = elig(bank, score, lt)
        c, bg, bdr = SC[e["code"]]
        with cols[i % 3]:
            st.markdown(f"""
<div style="background:#0D1117;border:1px solid #1E2535;border-radius:11px;padding:1rem;margin-bottom:10px;">
    <div style="display:flex;align-items:center;gap:9px;margin-bottom:9px;">
        <span style="font-size:20px;">{bank['logo']}</span>
        <div>
            <div style="font-family:'Space Grotesk',sans-serif;font-size:13.5px;font-weight:700;color:#F0F4FF;">{bank['name']}</div>
            <div style="font-size:10px;color:rgba(255,255,255,0.3);">{bank['full']}</div>
        </div>
    </div>
    <div style="background:{bg};border:1px solid {bdr};border-radius:6px;
         padding:4px 9px;margin-bottom:8px;font-size:11.5px;color:{c};font-weight:600;">{e['status']}</div>
    <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
        <span style="font-size:11px;color:rgba(255,255,255,0.3);">Interest Rate</span>
        <span style="font-size:12px;font-weight:600;color:rgba(255,255,255,0.75);">{e['rate']}</span>
    </div>
    <div style="display:flex;justify-content:space-between;">
        <span style="font-size:11px;color:rgba(255,255,255,0.3);">Min Score Req.</span>
        <span style="font-size:12px;color:rgba(255,255,255,0.5);">{e['min']}</span>
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Negotiation tips — computed instantly, no button needed
    analysis = st.session_state.get("ai_analysis")
    if not analysis:
        analysis = ask_gemini_for_analysis(profile, sd)
        st.session_state["ai_analysis"] = analysis

    st.markdown("""
<div style="font-family:'Space Grotesk',sans-serif;font-size:10px;font-weight:600;letter-spacing:0.1em;
     text-transform:uppercase;color:rgba(255,255,255,0.25);margin-bottom:0.85rem;">
    💡 Negotiation Tips & Outlook
</div>
""", unsafe_allow_html=True)

    if analysis:
        outlook  = analysis.get("loan_eligibility_outlook", "")
        strength = analysis.get("biggest_strength", "")
        weakness = analysis.get("biggest_weakness", "")
        plan     = analysis.get("action_plan", [])
        lines = []
        if outlook:  lines.append(outlook)
        if strength: lines.append(f"💪 {strength}")
        if weakness: lines.append(f"⚠️ {weakness}")
        for a in plan[:2]:
            lines.append(f"• {a.get('action','')} ({a.get('score_impact','')}) — {a.get('detail','')}")
        st.markdown(f"""
<div style="background:rgba(79,142,247,0.05);border:1px solid rgba(79,142,247,0.15);
     border-radius:10px;padding:1rem 1.2rem;">
    <div style="font-size:13px;color:rgba(255,255,255,0.7);line-height:1.9;">{"<br>".join(lines)}</div>
</div>
""", unsafe_allow_html=True)

    # Next tier
    next_t = next(
        (b.get(lt,{}).get("min_score") for b in sorted(BANKS, key=lambda x: x.get(lt,{}).get("min_score",999))
         if b.get(lt,{}).get("min_score",999) > score), None)
    if next_t:
        st.markdown(f"""
<div style="background:rgba(245,158,11,0.05);border:1px solid rgba(245,158,11,0.15);
     border-radius:10px;padding:0.85rem 1.1rem;text-align:center;margin-top:1rem;">
    <span style="font-size:13px;color:rgba(255,255,255,0.5);">
        Just <strong style="color:#F59E0B;font-size:16px;">+{next_t-score} points</strong> needed to unlock the next tier — use the What-If Lab.
    </span>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎛 Back to What-If Lab", use_container_width=True):
            st.session_state.screen = "whatif"; st.rerun()
    with c2:
        if st.button("🔄 Start Over", use_container_width=True):
            for k in list(st.session_state.keys()):
                if k in ("profile","ai_analysis","screen","sim_analysis") or k.startswith("loan_advice"):
                    del st.session_state[k]
            st.session_state.screen = "input"; st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
