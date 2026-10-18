
import streamlit as st
import streamlit.components.v1 as components
import html
import math
import time

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
  --cyan: #00d9ff;
  --blue: #147bff;
  --navy: #030b1c;
  --panel: rgba(5, 23, 48, .92);
  --green: #00f5a0;
  --amber: #ffc247;
  --red: #ff416d;
}
.stApp {
  background:
    radial-gradient(ellipse at 50% -15%, #10366c 0%, transparent 50%),
    linear-gradient(140deg, #020817, #06152b 55%, #020817);
  color: #eaf7ff;
  font-family: Inter, sans-serif;
}
header, footer, #MainMenu {visibility: hidden;}
.block-container {max-width: 1450px; padding-top: 1.2rem; padding-bottom: 2rem;}
h1, h2, h3 {font-family: Orbitron, sans-serif !important;}
h1 {letter-spacing: 2px;}
section[data-testid="stVerticalBlock"] {gap: 1rem;}
.stTextInput label, .stSelectbox label {
  color: #a9d8ff !important;
  font-weight: 600 !important;
}
.stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
  background: #06152b !important;
  color: white !important;
  border-color: #1266b8 !important;
  border-radius: 9px !important;
}
.stButton > button {
  width: 100%;
  min-height: 52px;
  color: white;
  font-family: Orbitron, sans-serif;
  font-weight: 700;
  letter-spacing: 1px;
  border: 1px solid #50efff;
  border-radius: 10px;
  background: linear-gradient(90deg, #0755cf, #00bff5, #0755cf);
  background-size: 200% 100%;
  box-shadow: 0 0 16px #007bff75, inset 0 0 12px #64eaff45;
  transition: transform .2s, box-shadow .2s, background-position .4s;
}
.stButton > button:hover {
  transform: translateY(-3px) scale(1.005);
  background-position: 100% 0;
  box-shadow: 0 0 30px #00d9ffb0;
}
.hud {
  background: linear-gradient(145deg, #071b36ee, #030b1bee);
  border: 1px solid #087dcc;
  border-radius: 16px;
  padding: 20px;
  position: relative;
  overflow: hidden;
  box-shadow: inset 0 0 22px #007bff0b, 0 0 15px #006bff12;
  transition: transform .25s, border-color .25s, box-shadow .25s;
}
.hud:hover {
  transform: translateY(-3px);
  border-color: var(--cyan);
  box-shadow: 0 0 22px #00bfff25, inset 0 0 20px #00bfff0b;
}
.eyebrow {color: var(--cyan); font-size: 11px; letter-spacing: 3px; font-weight: 700;}
.hero {
  padding: 28px;
  border: 1px solid #087dcc;
  border-radius: 18px;
  background: linear-gradient(100deg, #04132cfa 20%, #06172dcc 70%, #051128ee);
  position: relative;
  overflow: hidden;
  box-shadow: 0 0 30px #007bff18;
}
.hero:after {
  content:"";
  position:absolute; inset:0; pointer-events:none;
  background:linear-gradient(110deg, transparent 35%, #00d9ff09 50%, transparent 65%);
  animation: sweep 5s linear infinite;
}
@keyframes sweep {from {transform:translateX(-100%)} to {transform:translateX(100%)}}
@keyframes pulse {0%,100%{opacity:.5}50%{opacity:1}}
@keyframes scan {0%{transform:translateY(-100%)}100%{transform:translateY(800%)}}
@keyframes rotate {to{transform:rotate(360deg)}}
@keyframes flicker {0%,100%{opacity:1}50%{opacity:.75}}
.status-dot {
  display:inline-block; width:8px; height:8px; border-radius:50%;
  background:var(--green); box-shadow:0 0 12px var(--green);
  animation:pulse 1.4s infinite; margin-right:8px;
}
.stCaption {color:#8bb7df !important;}
div[data-testid="stExpander"] {
  border:1px solid #1266b8; border-radius:12px; background:#04132b;
}
div[data-testid="stAlert"] {border-radius:12px;}
</style>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.markdown("""
<div class="hero">
  <div class="eyebrow"><span class="status-dot"></span> ROAD SAFETY INTELLIGENCE SYSTEM</div>
  <h1 style="font-size:clamp(30px,5vw,54px); margin:12px 0 4px;">
    ROADSAFE <span style="color:#00d9ff;text-shadow:0 0 20px #00bfff;">AI</span>
  </h1>
  <div style="color:#a8d9ff;letter-spacing:2px;font-size:13px;">
    ACCIDENT RISK ASSESSMENT • ROAD SAFETY ADVISORY
  </div>
  <p style="color:#00d9ff;margin-top:15px;font-style:italic;">
    Plan your journey. Assess conditions. Travel safely.
  </p>
  <div class="eyebrow">SYSTEM STATUS: ONLINE &nbsp; / &nbsp; SAFETY MODE ACTIVE</div>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- JOURNEY INPUTS ----------
st.markdown('<div class="eyebrow">01 / JOURNEY CONFIGURATION</div>', unsafe_allow_html=True)
st.markdown("## Your Journey")

c1, c2 = st.columns(2)
with c1:
    start = st.text_input("📍 Starting Location", placeholder="e.g. Kochi")
with c2:
    destination = st.text_input("⚑ Destination", placeholder="e.g. Thrissur")

st.write("")
st.markdown('<div class="eyebrow">02 / ENVIRONMENTAL TELEMETRY</div>', unsafe_allow_html=True)
st.markdown("## Road & Travel Conditions")

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
    <div class="hud" style="padding:13px;margin-top:3px;">
      <div class="eyebrow">SAFETY PROTOCOL</div>
      <div style="font-size:13px;color:#b4d9f7;margin-top:8px;">
      Assess conditions before departure. Always follow local road rules.
      </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
analyse = st.button("⌕  ANALYSE ROAD RISK  »", use_container_width=True)

# ---------- RULE-BASED RISK CALCULATION ----------
# This preserves the previous app's scoring rules.
score = 0
score += 2 if weather in ["Rainy", "Foggy"] else 1 if weather == "Cloudy" else 0
score += 2 if road == "Wet" else 1 if road == "Damp" else 0
score += 2 if traffic == "High" else 1 if traffic == "Medium" else 0
score += 2 if visibility == "Low" else 1 if visibility == "Medium" else 0

risk = "HIGH" if score >= 6 else "MODERATE" if score >= 3 else "LOW"
risk_color = "#ff416d" if risk == "HIGH" else "#ffc247" if risk == "MODERATE" else "#00f5a0"
risk_icon = "▲" if risk == "HIGH" else "◆" if risk == "MODERATE" else "✓"
percentage = round(score / 8 * 100)

# ---------- ANALYSIS ANIMATION ----------
if analyse:
    placeholder = st.empty()
    for pct, message in [
        (18, "INITIALISING ROAD CONDITION SCAN"),
        (42, "CHECKING WEATHER & ROAD SURFACE"),
        (68, "ANALYSING TRAFFIC & VISIBILITY"),
        (88, "CALCULATING CONDITION SCORE"),
        (100, "ASSESSMENT COMPLETE"),
    ]:
        placeholder.markdown(f"""
        <div class="hud">
          <div class="eyebrow"><span class="status-dot"></span> {message}</div>
          <div style="height:7px;background:#10294a;border-radius:10px;margin-top:15px;overflow:hidden;">
            <div style="height:100%;width:{pct}%;background:linear-gradient(90deg,#126dff,#00e5ff);
            box-shadow:0 0 14px #00d9ff;border-radius:10px;transition:width .3s;"></div>
          </div>
          <div style="text-align:right;color:#00d9ff;font-size:12px;margin-top:6px;">{pct}%</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.18)
    st.session_state["roadsafe_analysed"] = True

# ---------- RISK GAUGE ----------
def gauge_html(value, label, color):
    circumference = 2 * math.pi * 82
    dash = circumference * value / 100
    return f"""
    <div style="display:flex;justify-content:center;align-items:center;padding:10px 0 0;">
      <svg viewBox="0 0 220 220" style="width:min(100%,290px);filter:drop-shadow(0 0 13px {color}55);">
        <defs>
          <linearGradient id="ring" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{color}"/>
            <stop offset="100%" stop-color="#087bff"/>
          </linearGradient>
        </defs>
        <circle cx="110" cy="110" r="82" fill="none" stroke="#102a4c" stroke-width="14"/>
        <circle cx="110" cy="110" r="82" fill="none" stroke="#164e86" stroke-width="2"
          stroke-dasharray="3 8"/>
        <circle cx="110" cy="110" r="82" fill="none" stroke="url(#ring)" stroke-width="12"
          stroke-linecap="round" stroke-dasharray="{dash} {circumference}"
          transform="rotate(-90 110 110)"
          style="transition:stroke-dasharray 1.4s ease;"/>
        <circle cx="110" cy="110" r="63" fill="#06152b" stroke="{color}55" stroke-width="1.5"/>
        <circle cx="110" cy="45" r="4" fill="{color}" style="animation:pulse 1s infinite;"/>
        <text x="110" y="91" text-anchor="middle" fill="{color}" font-size="13">RISK LEVEL</text>
        <text x="110" y="123" text-anchor="middle" fill="#f1f8ff"
          font-size="{19 if label == 'MODERATE' else 24}" font-family="Orbitron, sans-serif"
          font-weight="700">{label}</text>
        <text x="110" y="146" text-anchor="middle" fill="#8cb9df" font-size="11">{value}% SCORE</text>
      </svg>
    </div>
    """

st.write("")
st.markdown('<div class="eyebrow">03 / ASSESSMENT OUTPUT</div>', unsafe_allow_html=True)
left, right = st.columns([1.65, 1])

with left:
    st.markdown("""
    <div class="hud" style="padding:0;min-height:250px;">
      <div style="padding:15px 18px;position:relative;z-index:2;">
        <div class="eyebrow">ROAD VISUALISATION / 01</div>
        <div style="font-family:Orbitron,sans-serif;font-size:18px;margin-top:8px;">JOURNEY MONITOR</div>
      </div>
      <div style="height:190px;position:relative;overflow:hidden;
        background:radial-gradient(ellipse at 50% 20%,#174d7d,#06162b 65%,#020817);">
        <div style="position:absolute;inset:0;
          background:repeating-linear-gradient(0deg,transparent 0 28px,#00d9ff0b 29px 30px),
          repeating-linear-gradient(90deg,transparent 0 28px,#00d9ff0b 29px 30px);"></div>
        <svg viewBox="0 0 600 190" preserveAspectRatio="xMidYMid slice"
          style="position:absolute;width:100%;height:100%;">
          <path d="M175 190 L255 15 L345 15 L425 190 Z" fill="#071225" stroke="#087dcc" stroke-width="2"/>
          <path d="M295 190 L298 145 L300 120 L300 95 L300 65 L300 35"
            stroke="#00d9ff" stroke-width="3" stroke-dasharray="12 13" fill="none"/>
          <path d="M175 190 L255 15 M425 190 L345 15" stroke="#00bfff" stroke-width="2" fill="none"/>
          <g fill="#00d9ff">
            <circle cx="300" cy="157" r="4"><animate attributeName="opacity" values="1;.2;1" dur="1.3s" repeatCount="indefinite"/></circle>
            <circle cx="300" cy="110" r="3"><animate attributeName="opacity" values=".2;1;.2" dur="1.3s" repeatCount="indefinite"/></circle>
            <circle cx="300" cy="66" r="2"><animate attributeName="opacity" values="1;.2;1" dur="1.3s" repeatCount="indefinite"/></circle>
          </g>
          <path d="M0 180 L150 180 M450 180 L600 180" stroke="#147bff" stroke-width="2"/>
        </svg>
        <div style="position:absolute;bottom:12px;left:15px;font-size:11px;color:#00d9ff;letter-spacing:2px;">
          <span class="status-dot"></span> TELEMETRY DISPLAY
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div class="hud" style="text-align:center;min-height:250px;border-color:{risk_color}88;">
      <div class="eyebrow">ESTIMATED CONDITION RISK</div>
      {gauge_html(percentage, risk, risk_color)}
      <div style="font-family:Orbitron,sans-serif;color:{risk_color};font-size:13px;
        animation:pulse 1.8s infinite;">{risk_icon} {risk} RISK STATUS</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
x, y, z = st.columns(3)
with x:
    st.markdown(f"""
    <div class="hud">
      <div class="eyebrow">ROUTE SUMMARY</div>
      <div style="font-size:14px;margin-top:10px;">📍 {html.escape(start or 'Starting point not entered')}</div>
      <div style="color:#00d9ff;padding:4px 0;">↓ JOURNEY ↓</div>
      <div style="font-size:14px;">🏁 {html.escape(destination or 'Destination not entered')}</div>
    </div>
    """, unsafe_allow_html=True)
with y:
    st.markdown(f"""
    <div class="hud">
      <div class="eyebrow">VEHICLE PROFILE</div>
      <div style="font-size:26px;margin-top:14px;">🚘</div>
      <div style="font-size:18px;">{vehicle}</div>
    </div>
    """, unsafe_allow_html=True)
with z:
    st.markdown(f"""
    <div class="hud">
      <div class="eyebrow">CONDITION SCORE</div>
      <div style="font-size:28px;font-family:Orbitron,sans-serif;margin-top:12px;">{score} <span style="color:#7598bb;">/ 8</span></div>
      <div style="height:6px;background:#142b49;border-radius:8px;margin-top:12px;">
        <div style="height:6px;width:{percentage}%;background:{risk_color};
        border-radius:8px;box-shadow:0 0 10px {risk_color};"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ---------- DYNAMIC ADVISORY ----------
st.write("")
st.markdown('<div class="eyebrow">04 / SAFETY INTELLIGENCE</div>', unsafe_allow_html=True)
st.markdown("## Key Recommendations")

tips = []
if weather in ["Rainy", "Foggy"]:
    tips.append(("🌧️", "Weather alert", "Rain or fog can reduce visibility and grip. Slow down and increase following distance."))
elif weather == "Cloudy":
    tips.append(("🌥️", "Weather awareness", "Stay alert to changing weather and check conditions before departure."))
else:
    tips.append(("☀️", "Weather conditions", "Conditions selected as clear. Continue to watch the road and surroundings."))

if road == "Wet":
    tips.append(("🛣️", "Wet road caution", "Brake gently, avoid sudden manoeuvres and leave extra stopping distance."))
elif road == "Damp":
    tips.append(("🚧", "Road surface caution", "Allow extra stopping distance on damp surfaces."))
else:
    tips.append(("🛣️", "Road surface", "Maintain safe gaps and avoid sudden lane changes."))

if traffic == "High":
    tips.append(("🚦", "Traffic alert", "Expect congestion. Avoid distractions and follow traffic signals."))
elif traffic == "Medium":
    tips.append(("🚘", "Traffic awareness", "Keep a safe gap and anticipate the movement of nearby vehicles."))
else:
    tips.append(("🛣️", "Traffic conditions", "Low selected traffic does not remove the need for caution."))

if visibility == "Low":
    tips.append(("💡", "Visibility warning", "Use appropriate lights, reduce speed and avoid risky overtaking."))
elif visibility == "Medium":
    tips.append(("👁️", "Visibility caution", "Keep lights appropriate to conditions and remain attentive."))
else:
    tips.append(("👁️", "Visibility", "Continue checking mirrors and watch for pedestrians and cyclists."))

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
                </div>
                """, unsafe_allow_html=True)

s1, s2, s3 = st.columns(3)
with s1:
    st.markdown('<div class="hud" style="text-align:center;">🪖<br><b>Seatbelts & Helmets</b><br><small>Wear the right protection for your vehicle.</small></div>', unsafe_allow_html=True)
with s2:
    st.markdown('<div class="hud" style="text-align:center;">💡<br><b>Lights & Visibility</b><br><small>Use lights suitable for road conditions.</small></div>', unsafe_allow_html=True)
with s3:
    st.markdown('<div class="hud" style="text-align:center;">🔧<br><b>Vehicle Check</b><br><small>Check tyres, brakes and mirrors before leaving.</small></div>', unsafe_allow_html=True)

st.write("")
st.markdown("""
<div class="hud" style="text-align:center;padding:24px;">
  <div class="eyebrow">END OF ASSESSMENT</div>
  <div style="font-family:Orbitron,sans-serif;color:#00d9ff;font-size:18px;margin-top:8px;">
    HAVE A SAFE AND HAPPY JOURNEY
  </div>
  <div style="color:#b7d4f0;margin-top:8px;">Stay alert. Protect every passenger. Make every journey safer.</div>
</div>
""", unsafe_allow_html=True)

st.caption(
    "Important: This app applies predefined rules to the selected conditions. "
    "It does not use live route, weather or traffic data and is not a validated prediction "
    "of actual accidents. The entered locations are displayed for journey reference only."
)
