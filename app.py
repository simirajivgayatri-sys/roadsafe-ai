
import streamlit as st
import streamlit.components.v1 as components
import html
import math

st.set_page_config(
    page_title="ROADSAFE AI | Cyberpunk HUD",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- THEME ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
  --cyan:#00d9ff;
  --blue:#147bff;
  --green:#00f5a0;
  --amber:#ffc247;
  --red:#ff416d;
}
.stApp {
  background:radial-gradient(ellipse at 50% -15%,#10366c 0%,transparent 50%),
  linear-gradient(140deg,#020817,#06152b 55%,#020817);
  color:#eaf7ff;font-family:Inter,sans-serif;
}
header,footer,#MainMenu {visibility:hidden;}
.block-container {max-width:1450px;padding-top:1.2rem;padding-bottom:2rem;}
h1,h2,h3 {font-family:Orbitron,sans-serif!important;}
.eyebrow {color:var(--cyan);font-size:11px;letter-spacing:3px;font-weight:700;}
.hero,.hud {
  background:linear-gradient(145deg,#071b36ee,#030b1bee);
  border:1px solid #087dcc;border-radius:16px;padding:20px;
  box-shadow:inset 0 0 22px #007bff0b,0 0 15px #006bff12;
  transition:transform .25s,border-color .25s,box-shadow .25s;
}
.hero {position:relative;overflow:hidden;padding:28px;}
.hud:hover {transform:translateY(-3px);border-color:var(--cyan);box-shadow:0 0 22px #00bfff25;}
.hero:after {
 content:"";position:absolute;inset:0;pointer-events:none;
 background:linear-gradient(110deg,transparent 35%,#00d9ff09 50%,transparent 65%);
 animation:sweep 5s linear infinite;
}
@keyframes sweep {from{transform:translateX(-100%)}to{transform:translateX(100%)}}
@keyframes pulse {0%,100%{opacity:.5}50%{opacity:1}}
.status-dot {display:inline-block;width:8px;height:8px;border-radius:50%;
 background:var(--green);box-shadow:0 0 12px var(--green);
 animation:pulse 1.4s infinite;margin-right:8px;}
.stTextInput label,.stSelectbox label {color:#a9d8ff!important;font-weight:600!important;}
.stTextInput input,.stSelectbox div[data-baseweb="select"]>div {
 background:#06152b!important;color:white!important;border-color:#1266b8!important;border-radius:9px!important;
}
.stButton>button, .stFormSubmitButton>button {
 width:100%;min-height:52px;color:white;font-family:Orbitron,sans-serif;
 font-weight:700;letter-spacing:1px;border:1px solid #50efff;border-radius:10px;
 background:linear-gradient(90deg,#0755cf,#00bff5,#0755cf);
 background-size:200% 100%;box-shadow:0 0 16px #007bff75;
 transition:transform .2s,box-shadow .2s;
}
.stButton>button:hover,.stFormSubmitButton>button:hover {
 transform:translateY(-3px);box-shadow:0 0 30px #00d9ffb0;
}
div[data-testid="stExpander"] {border:1px solid #1266b8;border-radius:12px;background:#04132b;}
</style>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.markdown("""
<div class="hero">
  <div class="eyebrow"><span class="status-dot"></span> ROAD SAFETY INTELLIGENCE SYSTEM</div>
  <h1 style="font-size:clamp(30px,5vw,54px);margin:12px 0 4px;">
    ROADSAFE <span style="color:#00d9ff;text-shadow:0 0 20px #00bfff;">AI</span>
  </h1>
  <div style="color:#a8d9ff;letter-spacing:2px;font-size:13px;">
    ACCIDENT RISK ASSESSMENT • ROAD SAFETY ADVISORY
  </div>
  <p style="color:#00d9ff;margin-top:15px;font-style:italic;">
    Plan your journey. Assess conditions. Travel safely.
  </p>
  <div class="eyebrow">SYSTEM STATUS: ONLINE / SAFETY MODE ACTIVE</div>
</div>
""", unsafe_allow_html=True)

st.write("")
st.markdown('<div class="eyebrow">01 / JOURNEY CONFIGURATION</div>', unsafe_allow_html=True)
st.header("Your Journey")

# A form prevents results updating while the user is still selecting options.
with st.form("roadsafe_form"):
    c1, c2 = st.columns(2)
    with c1:
        start = st.text_input("📍 Starting Location", placeholder="e.g. Kochi")
    with c2:
        destination = st.text_input("⚑ Destination", placeholder="e.g. Thrissur")

    st.write("")
    st.markdown('<div class="eyebrow">02 / ENVIRONMENTAL TELEMETRY</div>', unsafe_allow_html=True)
    st.subheader("Road & Travel Conditions")

    a, b, c = st.columns(3)
    with a:
        weather = st.selectbox("🌦️ Weather", ["Clear", "Cloudy", "Rainy", "Foggy"])
        road = st.selectbox("🛣️ Road Condition", ["Dry", "Damp", "Wet"])
    with b:
        traffic = st.selectbox("🚘 Traffic Density", ["Low", "Medium", "High"])
        visibility = st.selectbox("👁️ Visibility", ["High", "Medium", "Low"])
    with c:
        vehicle = st.selectbox("🚗 Vehicle Type", ["Car", "Motorcycle", "Scooter", "Bus", "Truck"])
        st.markdown("""
        <div style="padding:12px;border:1px solid #1266b8;border-radius:10px;color:#a9d8ff;">
          <div class="eyebrow">SAFETY PROTOCOL</div>
          <small>Assess conditions before departure. Follow road rules.</small>
        </div>
        """, unsafe_allow_html=True)

    submitted = st.form_submit_button("⌕  ANALYSE ROAD RISK  »")

# ---------- RESULTS ONLY AFTER SUBMISSION ----------
if submitted:
    if not start.strip() or not destination.strip():
        st.warning("Please enter both your starting location and destination.")
        st.stop()

    # Original rule-based risk-scoring logic
    score = 0
    score += 2 if weather in ["Rainy", "Foggy"] else 1 if weather == "Cloudy" else 0
    score += 2 if road == "Wet" else 1 if road == "Damp" else 0
    score += 2 if traffic == "High" else 1 if traffic == "Medium" else 0
    score += 2 if visibility == "Low" else 1 if visibility == "Medium" else 0

    risk = "HIGH" if score >= 6 else "MODERATE" if score >= 3 else "LOW"
    risk_color = "#ff416d" if risk == "HIGH" else "#ffc247" if risk == "MODERATE" else "#00f5a0"
    percentage = round(score / 8 * 100)

    # ---------- ANALYSIS ANIMATION ----------
    progress = st.progress(0, text="INITIALISING ROAD CONDITION SCAN")
    stages = [
        (20, "CHECKING WEATHER & ROAD SURFACE"),
        (45, "ANALYSING TRAFFIC"),
        (70, "CHECKING VISIBILITY"),
        (90, "CALCULATING CONDITION SCORE"),
        (100, "ASSESSMENT COMPLETE"),
    ]
    import time
    for pct, message in stages:
        time.sleep(0.16)
        progress.progress(pct, text=message)
    time.sleep(0.25)
    progress.empty()

    st.write("")
    st.markdown('<div class="eyebrow">03 / ASSESSMENT OUTPUT</div>', unsafe_allow_html=True)
    st.header("Road Risk Analysis")

    left, right = st.columns([1.5, 1])

    # ---------- RELIABLE EMBEDDED JOURNEY MONITOR ----------
    with left:
        st.markdown("""
        <div class="hud" style="padding:16px 18px 0;">
          <div class="eyebrow">ROAD VISUALISATION / 01</div>
          <h3 style="margin-top:8px;">JOURNEY MONITOR</h3>
          <div style="color:#00d9ff;font-size:12px;margin-bottom:8px;">
            <span class="status-dot"></span> VISUAL DISPLAY ACTIVE
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Render the animated SVG in its own HTML frame.
        components.html("""
        <!DOCTYPE html><html><head><style>
        html,body{margin:0;background:#030b1c;overflow:hidden}
        .scene{height:235px;position:relative;overflow:hidden;
          background:radial-gradient(ellipse at 50% 5%,#174d7d,#06162b 65%,#020817);
          border:1px solid #087dcc;border-radius:0 0 14px 14px}
        svg{width:100%;height:100%}
        .beam{animation:flow 1.3s linear infinite}
        .glow{animation:blink 1.4s ease-in-out infinite}
        @keyframes flow{to{stroke-dashoffset:-60}}
        @keyframes blink{50%{opacity:.3}}
        </style></head><body>
        <div class="scene">
        <svg viewBox="0 0 600 235" preserveAspectRatio="xMidYMid slice">
          <defs>
            <linearGradient id="road" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stop-color="#091d37"/><stop offset="1" stop-color="#102b4c"/>
            </linearGradient>
          </defs>
          <g stroke="#0b4470" stroke-width="1" opacity=".65">
            <path d="M0 35H600M0 75H600M0 115H600M0 155H600M0 195H600"/>
            <path d="M80 0V235M160 0V235M240 0V235M320 0V235M400 0V235M480 0V235M560 0V235"/>
          </g>
          <path d="M0 235L240 0H360L600 235Z" fill="url(#road)" stroke="#147bff" stroke-width="2"/>
          <path d="M0 235L240 0M600 235L360 0" stroke="#00d9ff" stroke-width="3" fill="none"/>
          <path d="M300 235L300 0" stroke="#00d9ff" stroke-width="3"
            stroke-dasharray="18 20" class="beam" fill="none"/>
          <path d="M180 235L270 0M420 235L330 0" stroke="#147bff" stroke-width="1" opacity=".8"/>
          <g fill="#00d9ff">
            <circle cx="300" cy="190" r="5" class="glow"/>
            <circle cx="300" cy="140" r="4" class="glow"/>
            <circle cx="300" cy="90" r="3" class="glow"/>
          </g>
          <g fill="#07172d" stroke="#00d9ff" stroke-width="2">
            <path d="M265 184L273 167H327L335 184V198H265Z"/>
            <path d="M276 171H324L329 183H271Z" fill="#0b3a65"/>
            <path d="M268 191H280M320 191H332" stroke="#ff416d" stroke-width="4"/>
          </g>
          <text x="18" y="25" fill="#00d9ff" font-size="11" letter-spacing="2">ROAD SENSOR DISPLAY</text>
          <text x="18" y="218" fill="#7fcaff" font-size="10" letter-spacing="1">VISUAL SIMULATION • NOT LIVE GPS</text>
        </svg></div></body></html>
        """, height=245, scrolling=False)

    # ---------- CIRCULAR GAUGE ----------
    with right:
        circumference = 2 * math.pi * 82
        dash = circumference * percentage / 100
        st.markdown(f"""
        <div class="hud" style="text-align:center;border-color:{risk_color}88;">
          <div class="eyebrow">ESTIMATED CONDITION RISK</div>
          <svg viewBox="0 0 220 220" style="width:100%;max-width:290px;
          filter:drop-shadow(0 0 13px {risk_color}55);">
            <circle cx="110" cy="110" r="82" fill="none" stroke="#102a4c" stroke-width="14"/>
            <circle cx="110" cy="110" r="82" fill="none" stroke="{risk_color}"
              stroke-width="12" stroke-linecap="round"
              stroke-dasharray="{dash} {circumference}"
              transform="rotate(-90 110 110)"
              style="transition:stroke-dasharray 1.2s ease;"/>
            <circle cx="110" cy="110" r="63" fill="#06152b" stroke="{risk_color}55"/>
            <circle cx="110" cy="28" r="4" fill="{risk_color}">
              <animate attributeName="opacity" values="1;.3;1" dur="1.5s" repeatCount="indefinite"/>
            </circle>
            <text x="110" y="89" text-anchor="middle" fill="{risk_color}" font-size="12">RISK LEVEL</text>
            <text x="110" y="121" text-anchor="middle" fill="#f1f8ff"
              font-size="{18 if risk == 'MODERATE' else 23}" font-family="sans-serif" font-weight="700">{risk}</text>
            <text x="110" y="145" text-anchor="middle" fill="#8cb9df" font-size="11">{percentage}% SCORE</text>
          </svg>
          <div style="color:{risk_color};font-weight:700;">{risk} RISK STATUS</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    x, y, z = st.columns(3)
    with x:
        st.markdown(f"""
        <div class="hud">
          <div class="eyebrow">JOURNEY SUMMARY</div>
          <p>📍 <b>FROM</b><br>{html.escape(start)}</p>
          <p>🏁 <b>TO</b><br>{html.escape(destination)}</p>
        </div>""", unsafe_allow_html=True)
    with y:
        st.markdown(f"""
        <div class="hud">
          <div class="eyebrow">VEHICLE</div>
          <h2 style="margin-top:14px;">🚘</h2>
          <div>{html.escape(vehicle)}</div>
        </div>""", unsafe_allow_html=True)
    with z:
        st.markdown(f"""
        <div class="hud">
          <div class="eyebrow">CONDITION SCORE</div>
          <h2 style="margin-top:14px;">{score} / 8</h2>
          <div style="height:6px;background:#142b49;border-radius:8px;">
            <div style="height:6px;width:{percentage}%;background:{risk_color};
              border-radius:8px;box-shadow:0 0 10px {risk_color};"></div>
          </div>
        </div>""", unsafe_allow_html=True)

    # ---------- DYNAMIC RECOMMENDATIONS ----------
    st.write("")
    st.markdown('<div class="eyebrow">04 / SAFETY INTELLIGENCE</div>', unsafe_allow_html=True)
    st.header("Key Recommendations")

    tips = []
    if weather in ["Rainy", "Foggy"]:
        tips.append(("🌧️", "Weather alert", "Rain or fog can reduce visibility and grip. Slow down and increase following distance."))
    elif weather == "Cloudy":
        tips.append(("🌥️", "Weather awareness", "Watch for changing weather and check conditions before departure."))
    else:
        tips.append(("☀️", "Weather conditions", "Continue watching the road and your surroundings."))

    if road == "Wet":
        tips.append(("🛣️", "Wet road caution", "Brake gently, avoid sudden manoeuvres and leave extra stopping distance."))
    elif road == "Damp":
        tips.append(("🚧", "Road surface caution", "Allow extra stopping distance on damp surfaces."))
    else:
        tips.append(("🛣️", "Road surface", "Maintain safe gaps and avoid sudden lane changes."))

    if traffic == "High":
        tips.append(("🚦", "Traffic alert", "Expect congestion. Avoid distractions and follow traffic signals."))
    elif traffic == "Medium":
        tips.append(("🚘", "Traffic awareness", "Keep a safe gap and anticipate other vehicles."))
    else:
        tips.append(("🛣️", "Traffic conditions", "Stay alert even when traffic is light."))

    if visibility == "Low":
        tips.append(("💡", "Visibility warning", "Use appropriate lights, reduce speed and avoid risky overtaking."))
    elif visibility == "Medium":
        tips.append(("👁️", "Visibility caution", "Use lights suitable for conditions and remain attentive."))
    else:
        tips.append(("👁️", "Visibility", "Watch for pedestrians and cyclists."))

    for i in range(0, len(tips), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(tips):
                icon, title, detail = tips[i + j]
                with col:
                    st.markdown(f"""
                    <div class="hud" style="min-height:125px;margin-bottom:10px;">
                      <div style="font-size:23px;">{icon}</div>
                      <div style="color:#00d9ff;font-weight:700;margin:8px 0;">{title}</div>
                      <div style="font-size:13px;color:#b7d4f0;line-height:1.6;">{detail}</div>
                    </div>""", unsafe_allow_html=True)

    p, q, r = st.columns(3)
    with p:
        st.markdown('<div class="hud" style="text-align:center;">🪖<br><b>Seatbelts & Helmets</b><br><small>Wear the right protection.</small></div>', unsafe_allow_html=True)
    with q:
        st.markdown('<div class="hud" style="text-align:center;">💡<br><b>Lights & Visibility</b><br><small>Use lights suitable for conditions.</small></div>', unsafe_allow_html=True)
    with r:
        st.markdown('<div class="hud" style="text-align:center;">🔧<br><b>Vehicle Check</b><br><small>Check tyres, brakes and mirrors.</small></div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("""
    <div class="hud" style="text-align:center;padding:24px;">
      <div class="eyebrow">END OF ASSESSMENT</div>
      <h3 style="color:#00d9ff;">HAVE A SAFE AND HAPPY JOURNEY</h3>
      <div style="color:#b7d4f0;">Stay alert. Protect every passenger. Make every journey safer.</div>
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        "This app applies predefined rules to your selected conditions. "
        "It does not use live route, weather or traffic data and is not a validated "
        "prediction of actual accidents. The road graphic is a visual simulation."
    )
