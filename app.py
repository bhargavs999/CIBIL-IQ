import os
import streamlit as st

st.set_page_config(page_title="CIBIL IQ — Credit Score Simulator", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.stApp,section[data-testid="stMain"]>div{background:#07090F !important;}
header[data-testid="stHeader"],#MainMenu,footer,[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none !important;}
.block-container{padding:0 !important;max-width:100% !important;}

.ciq-header{background:#0D1117;border-bottom:1px solid #1E2535;padding:0 2rem;height:52px;
    display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:999;}
.ciq-logo{font-family:'Space Grotesk',sans-serif;font-size:1.2rem;font-weight:700;color:#fff;letter-spacing:-0.01em;}
.ciq-logo span{color:#4F8EF7;}
.ciq-nav{display:flex;gap:4px;}
.ciq-pill{padding:4px 12px;border-radius:6px;font-size:12px;font-weight:500;color:rgba(255,255,255,0.38);
    border:1px solid transparent;line-height:1.5;white-space:nowrap;}
.ciq-pill.on{background:rgba(79,142,247,0.12);color:#4F8EF7;border-color:rgba(79,142,247,0.28);}

.pw{max-width:880px;margin:0 auto;padding:2rem 1.5rem 4rem;width:100%;}

.hero{text-align:center;padding:2.5rem 1rem 2rem;}
.hero-badge{display:inline-block;background:rgba(79,142,247,0.1);border:1px solid rgba(79,142,247,0.22);
    color:#4F8EF7;font-size:10px;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;
    padding:4px 12px;border-radius:20px;margin-bottom:1.2rem;}
.hero h1{font-family:'Space Grotesk',sans-serif;font-size:clamp(1.8rem,3.5vw,2.6rem);font-weight:700;
    color:#F0F4FF;letter-spacing:-0.03em;line-height:1.15;margin-bottom:0.9rem;}
.hero h1 em{font-style:normal;color:#4F8EF7;}
.hero p{font-size:0.93rem;color:rgba(255,255,255,0.42);max-width:480px;margin:0 auto;line-height:1.8;}

.chips{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-bottom:2rem;}
.chip{background:#0D1117;border:1px solid #1E2535;border-radius:7px;padding:6px 13px;
    font-size:12px;color:rgba(255,255,255,0.48);display:flex;align-items:center;gap:6px;}

.fc{background:#0D1117;border:1px solid #1E2535;border-radius:12px;padding:1.4rem 1.6rem;margin-bottom:0.85rem;}
.fc-label{font-family:'Space Grotesk',sans-serif;font-size:10.5px;font-weight:600;letter-spacing:0.1em;
    text-transform:uppercase;color:rgba(255,255,255,0.28);margin-bottom:1rem;display:flex;align-items:center;gap:8px;}
.fc-label::after{content:'';flex:1;height:1px;background:#1E2535;}

[data-testid="stNumberInput"] input,[data-testid="stTextInput"] input{
    background:#111827 !important;border:1px solid #1E2535 !important;border-radius:8px !important;
    color:#E5EAF5 !important;font-family:'Inter',sans-serif !important;font-size:13px !important;}
[data-testid="stSelectbox"]>div>div{background:#111827 !important;border:1px solid #1E2535 !important;
    border-radius:8px !important;color:#E5EAF5 !important;}
label[data-testid="stWidgetLabel"] p{color:rgba(255,255,255,0.55) !important;font-size:12.5px !important;font-weight:500 !important;}
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"]{background:#4F8EF7 !important;border-color:#4F8EF7 !important;}
[data-testid="stCheckbox"] span,[data-testid="stRadio"] label p{color:rgba(255,255,255,0.6) !important;font-size:13px !important;}

.stButton>button{background:#4F8EF7 !important;color:#fff !important;border:none !important;
    border-radius:9px !important;padding:0.6rem 1.4rem !important;font-family:'Space Grotesk',sans-serif !important;
    font-size:13.5px !important;font-weight:600 !important;width:100% !important;
    transition:background 0.15s !important;box-shadow:0 2px 12px rgba(79,142,247,0.2) !important;}
.stButton>button:hover{background:#3B7BE8 !important;}

[data-testid="stExpander"]{background:#0D1117 !important;border:1px solid #1E2535 !important;border-radius:10px !important;}
[data-testid="stAlert"]{border-radius:9px !important;font-size:13px !important;}

.disc{text-align:center;font-size:11px;color:rgba(255,255,255,0.2);margin-top:1.2rem;line-height:1.65;}
::-webkit-scrollbar{width:5px;}::-webkit-scrollbar-thumb{background:#1E2535;border-radius:3px;}
</style>
""", unsafe_allow_html=True)

if "profile" not in st.session_state: st.session_state.profile = None
if "screen"  not in st.session_state: st.session_state.screen  = "input"

screens = ["input","report","whatif","loans"]
labels  = ["① Profile","② Score Report","③ What-If Lab","④ Loan Matcher"]
cur     = st.session_state.screen

pills = "".join(
    f'<span class="ciq-pill {"on" if screens[i]==cur else ""}">{labels[i]}</span>'
    for i in range(4)
)
st.markdown(f"""
<div class="ciq-header">
    <div class="ciq-logo">CIBIL<span>IQ</span></div>
    <div class="ciq-nav">{pills}</div>
</div>
""", unsafe_allow_html=True)

if   cur=="input":  from pages.profile_input import render; render()
elif cur=="report": from pages.score_report  import render; render()
elif cur=="whatif": from pages.whatif_lab    import render; render()
elif cur=="loans":  from pages.loan_matcher  import render; render()
