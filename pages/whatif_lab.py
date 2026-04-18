import streamlit as st
from pages.score_report import compute_base_score, get_score_band, build_gauge_html
from utils import ask_gemini_for_analysis

def render():
    profile = st.session_state.get("profile")
    if not profile:
        st.warning("Please complete your profile first.")
        if st.button("← Back"): st.session_state.screen="input"; st.rerun()
        return

    base = compute_base_score(profile)
    base_score = base["score"]
    if "sim_analysis" not in st.session_state: st.session_state.sim_analysis = None

    st.markdown('<div class="pw">', unsafe_allow_html=True)
    st.markdown("""
<div style="margin-bottom:1.5rem;">
    <div style="font-family:'Space Grotesk',sans-serif;font-size:1.5rem;font-weight:700;color:#F0F4FF;margin-bottom:0.3rem;">
        What-If <span style="color:#4F8EF7;">Score Lab</span>
    </div>
    <p style="font-size:13px;color:rgba(255,255,255,0.4);line-height:1.7;">
        Adjust the sliders to simulate changes. See how each action impacts your score in real time.
    </p>
</div>""", unsafe_allow_html=True)

    if st.button("← Back to Report"):
        st.session_state.screen="report"; st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)

    c_sl, c_res = st.columns([3,2])
    sim = profile.copy()

    with c_sl:
        st.markdown("""<div style="font-family:'Space Grotesk',sans-serif;font-size:10px;font-weight:600;
             letter-spacing:0.1em;text-transform:uppercase;color:rgba(255,255,255,0.25);margin-bottom:0.85rem;">
             Adjust Variables</div>""", unsafe_allow_html=True)
        st.markdown("**💳 Credit Utilization (%)**")
        sim["utilization_pct"] = st.slider("util",0,100,int(profile["utilization_pct"]),label_visibility="collapsed")
        st.markdown("**📅 Missed Payments (last 12m)**")
        sim["missed_payments_12m"] = st.slider("miss",0,12,profile["missed_payments_12m"],label_visibility="collapsed")
        st.markdown("**🔍 Hard Enquiries (last 6m)**")
        sim["hard_enquiries_6m"] = st.slider("enq",0,10,profile["hard_enquiries_6m"],label_visibility="collapsed")
        st.markdown("**📆 Age of Oldest Account (yrs)**")
        sim["credit_age_years"] = st.slider("age",0,20,profile["credit_age_years"],label_visibility="collapsed")
        st.markdown("**🏦 Settled / Written-off Accounts**")
        sim["settled_accounts"] = st.slider("set",0,5,profile["settled_accounts"],label_visibility="collapsed")

    with c_res:
        sd = compute_base_score(sim); ss = sd["score"]
        delta = ss - base_score; band = get_score_band(ss)
        dc = "#22C55E" if delta>0 else "#EF4444" if delta<0 else "#64748B"
        dsym = "+" if delta>=0 else ""
        st.markdown(f"""
<div style="background:#0D1117;border:1px solid #1E2535;border-radius:12px;
     padding:1.25rem;text-align:center;position:sticky;top:60px;">
    <div style="font-family:'Space Grotesk',sans-serif;font-size:10px;font-weight:600;letter-spacing:0.1em;
         text-transform:uppercase;color:rgba(255,255,255,0.25);margin-bottom:0.6rem;">Simulated Score</div>
    {build_gauge_html(ss,band)}
    <div style="font-family:'Space Grotesk',sans-serif;font-size:26px;font-weight:700;color:{dc};margin-top:0.5rem;">
        {dsym}{delta} pts
    </div>
    <div style="font-size:11.5px;color:rgba(255,255,255,0.35);">vs your baseline of {base_score}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Factor delta table
    st.markdown("""<div style="font-family:'Space Grotesk',sans-serif;font-size:10px;font-weight:600;letter-spacing:0.1em;
         text-transform:uppercase;color:rgba(255,255,255,0.25);margin-bottom:0.85rem;">Factor Changes</div>""",
         unsafe_allow_html=True)
    fm = {"payment_history":("Payment","📅"),"credit_utilization":("Utilization","💳"),
          "credit_age":("Age","📆"),"credit_mix":("Mix","🏦"),"new_credit":("New Credit","🔍")}
    cols = st.columns(5)
    for i,(k,(lbl,ico)) in enumerate(fm.items()):
        o=base["factors"][k]; n=sd["factors"][k]; d=n-o
        dc2="#22C55E" if d>0 else "#EF4444" if d<0 else "#64748B"
        ds=f"+{d:.0f}" if d>=0 else f"{d:.0f}"
        with cols[i]:
            st.markdown(f"""
<div style="background:#0D1117;border:1px solid #1E2535;border-radius:10px;padding:0.7rem 0.5rem;text-align:center;">
    <div style="font-size:16px;">{ico}</div>
    <div style="font-size:10px;color:rgba(255,255,255,0.35);margin:3px 0;">{lbl}</div>
    <div style="font-family:'Space Grotesk',sans-serif;font-size:17px;font-weight:700;color:{dc2};">{ds}</div>
    <div style="font-size:10px;color:rgba(255,255,255,0.28);">{o:.0f}→{n:.0f}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Instant sim analysis on button click
    if st.button("📋 Get Action Plan for This Simulation", use_container_width=True):
        st.session_state.sim_analysis = ask_gemini_for_analysis(sim, {"score":ss,"factors":sd["factors"]})

    if st.session_state.sim_analysis:
        a = st.session_state.sim_analysis
        st.markdown(f"""
<div style="background:rgba(79,142,247,0.05);border:1px solid rgba(79,142,247,0.15);border-radius:10px;padding:1rem 1.2rem;margin-bottom:0.75rem;">
    <div style="font-size:13.5px;color:rgba(255,255,255,0.8);line-height:1.75;">{a.get('score_summary','')}</div>
</div>""", unsafe_allow_html=True)
        cc1,cc2 = st.columns(2)
        with cc1:
            st.markdown(f"""<div style="background:rgba(34,197,94,0.07);border:1px solid rgba(34,197,94,0.18);
                 border-radius:8px;padding:10px 12px;">
                <div style="font-size:9.5px;font-weight:600;color:#22C55E;margin-bottom:3px;">💪 STRENGTH</div>
                <div style="font-size:12px;color:rgba(255,255,255,0.65);">{a.get('biggest_strength','')}</div>
            </div>""", unsafe_allow_html=True)
        with cc2:
            st.markdown(f"""<div style="background:rgba(239,68,68,0.07);border:1px solid rgba(239,68,68,0.18);
                 border-radius:8px;padding:10px 12px;">
                <div style="font-size:9.5px;font-weight:600;color:#EF4444;margin-bottom:3px;">⚠️ KEY ISSUE</div>
                <div style="font-size:12px;color:rgba(255,255,255,0.65);">{a.get('biggest_weakness','')}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        for item in a.get("action_plan",[]):
            pc="#EF4444" if item.get("priority")=="high" else "#F59E0B"
            st.markdown(f"""
<div style="background:#0D1117;border:1px solid #1E2535;border-radius:10px;padding:0.85rem 1rem;margin-bottom:7px;">
    <div style="display:flex;align-items:center;gap:7px;margin-bottom:3px;flex-wrap:wrap;">
        <span style="font-size:13px;font-weight:600;color:#E5EAF5;">{item.get('action','')}</span>
        <span style="font-size:9.5px;color:{pc};background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.15);padding:1px 6px;border-radius:4px;">{item.get('priority','').upper()}</span>
    </div>
    <div style="font-size:12px;color:rgba(255,255,255,0.45);margin-bottom:5px;">{item.get('detail','')}</div>
    <span style="font-size:11px;color:#22C55E;font-weight:600;">📈 {item.get('score_impact','')}</span>
    <span style="font-size:11px;color:rgba(255,255,255,0.3);margin-left:10px;">⏱ {item.get('time_to_impact','')}</span>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        if st.button("← Back to Report",use_container_width=True): st.session_state.screen="report"; st.rerun()
    with c2:
        if st.button("🏦 Find Loan Matches →",use_container_width=True): st.session_state.screen="loans"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
