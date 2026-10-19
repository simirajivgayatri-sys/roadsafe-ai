
import streamlit as st
import streamlit.components.v1 as components
import html
import math
import time
from pathlib import Path
import pandas as pd

st.set_page_config(
    page_title="ROADSAFE AI | Cyberpunk HUD",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------- STYLING --------------------
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
  color:#eaf7ff;
  font-family:Inter,sans-serif;
}
header,footer,#MainMenu {visibility:hidden;}
.block-container {max-width:1450px;padding-top:1.2rem;padding-bottom:2rem;}
h1,h2,h3 {font-family:Orbitron,sans-serif!important;}
.eyebrow {color:var(--cyan);font-size:11px;letter-spacing:3px;font-weight:700;}
.hero,.hud {
  background:linear-gradient(145deg,#071b36ee,#030b1bee);
  border:1px solid #087dcc;
  border-radius:16px;
  padding:20px;
  box-shadow:inset 0 0 22px #007bff0b,0 0 15px #006bff12;
  transition:transform .25s,border-color .25s,box-shadow .25s;
}
.hero {position:relative;overflow:hidden;padding:28px;}
.hud:hover {
  transform:translateY(-3px);
  border-color:var(--cyan);
  box-shadow:0 0 22px #00bfff25;
}
.hero:after {
 content:"";position:absolute;inset:0;pointer-events:none;
 background:linear-gradient(110deg,transparent 35%,#00d9ff09 50%,transparent 65%);
 animation:sweep 5s linear infinite;
}
@keyframes sweep {
  from {transform:translateX(-100%)}
  to {transform:translateX(100%)}
}
@keyframes pulse {
  0%,100% {opacity:.5}
  50% {opacity:1}
}
.status-dot {
  display:inline-block;width:8px;height:8px;border-radius:50%;
  background:var(--green);box-shadow:0 0 12px var(--green);
  animation:pulse 1.4s infinite;margin-right:8px;
}
.stTextInput label,.stSelectbox label {
  color:#a9d8ff!important;font-weight:600!important;
}
.stTextInput input,.stSelectbox div[data-baseweb="select"]>div {
  background:#06152b!important;color:white!important;
  border-color:#1266b8!important;border-radius:9px!important;
}
.stButton>button,.stFormSubmitButton>button {
  width:100%;min-height:52px;color:white;
  font-family:Orbitron,sans-serif;font-weight:700;letter-spacing:1px;
  border:1px solid #50efff;border-radius:10px;
  background:linear-gradient(90deg,#0755cf,#00bff5,#0755cf);
  background-size:200% 100%;box-shadow:0 0 16px #007bff75;
  transition:transform .2s,box-shadow .2s;
}
.stButton>button:hover,.stFormSubmitButton>button:hover {
  transform:translateY(-3px);box-shadow:0 0 30px #00d9ffb0;
}
div[data-testid="stExpander"] {
  border:1px solid #1266b8;border-radius:12px;background:#04132b;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HERO --------------------
st.markdown("""
<div class="hero">
  <div class="eyebrow">
    <span class="status-dot"></span> ROAD SAFETY INTELLIGENCE SYSTEM
  </div>
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
st.markdown(
    '<div class="eyebrow">01 / JOURNEY CONFIGURATION</div>',
    unsafe_allow_html=True
)
st.header("Your Journey")

# -------------------- INPUT FORM --------------------
with st.form("roadsafe_form"):
    c1, c2 = st.columns(2)

    with c1:
        start = st.text_input(
            "📍 Starting Location",
            placeholder="e.g. Kochi"
        )

    with c2:
        destination = st.text_input(
            "⚑ Destination",
            placeholder="e.g. Thrissur"
        )

    st.write("")
    st.markdown(
        '<div class="eyebrow">02 / ENVIRONMENTAL TELEMETRY</div>',
        unsafe_allow_html=True
    )
    st.subheader("Road & Travel Conditions")

    a, b, c = st.columns(3)

    with a:
        weather = st.selectbox(
            "🌦️ Weather",
            ["Clear", "Cloudy", "Rainy", "Foggy"]
        )
        road = st.selectbox(
            "🛣️ Road Condition",
            ["Dry", "Damp", "Wet"]
        )

    with b:
        traffic = st.selectbox(
            "🚘 Traffic Density",
            ["Low", "Medium", "High"]
        )
        visibility = st.selectbox(
            "👁️ Visibility",
            ["High", "Medium", "Low"]
        )

    with c:
        vehicle = st.selectbox(
            "🚗 Vehicle Type",
            ["Car", "Motorcycle", "Scooter", "Bus", "Truck"]
        )
        st.markdown("""
        <div style="padding:12px;border:1px solid #1266b8;
                    border-radius:10px;color:#a9d8ff;">
          <div class="eyebrow">SAFETY PROTOCOL</div>
          <small>Assess conditions before departure. Follow road rules.</small>
        </div>
        """, unsafe_allow_html=True)

    submitted = st.form_submit_button("⌕  ANALYSE ROAD RISK  »")

# -------------------- RESULTS --------------------
if submitted:

    if not start.strip() or not destination.strip():
        st.warning("Please enter both your starting location and destination.")

    else:
        # Use predictions exported from the trained Orange decision tree.
        predictions_path = Path(__file__).with_name(
            "roadsafe_predictions.csv"
        )

        if not predictions_path.exists():
            st.error(
                "The trained-model prediction file is missing. "
                "Please make sure roadsafe_predictions.csv is uploaded "
                "to the same GitHub repository folder as app.py."
            )
            st.stop()

        try:
            predictions_table = pd.read_csv(
                predictions_path,
                dtype=str
            ).fillna("")
        except Exception as error:
            st.error(f"Could not read the prediction file: {error}")
            st.stop()

        required_columns = [
            "Weather",
            "Road Conditions",
            "Traffic Density",
            "Visibility",
            "Risk Level",
        ]

        if not all(
            column in predictions_table.columns
            for column in required_columns
        ):
            st.error(
                "The CSV columns do not match the expected format. "
                "Please check roadsafe_predictions.csv."
            )
            st.stop()

        # Match the selected conditions to the exported model prediction.
        match = predictions_table[
            (predictions_table["Weather"].str.strip() == weather)
            & (
                predictions_table["Road Conditions"].str.strip()
                == road
            )
            & (
                predictions_table["Traffic Density"].str.strip()
                == traffic
            )
            & (
                predictions_table["Visibility"].str.strip()
                == visibility
            )
        ]

        if match.empty:
            st.error(
                "These conditions were not found in the model prediction "
                "table. Please check roadsafe_predictions.csv."
            )
            st.stop()

        model_risk = str(
            match.iloc[0]["Risk Level"]
        ).strip().title()

        risk_mapping = {
            "High": "HIGH",
            "Medium": "MODERATE",
            "Low": "LOW",
        }

        if model_risk not in risk_mapping:
            st.error(
                f"Unexpected risk category in CSV: {model_risk}"
            )
            st.stop()

        risk = risk_mapping[model_risk]

        risk_color = (
            "#ff416d" if risk == "HIGH"
            else "#ffc247" if risk == "MODERATE"
            else "#00f5a0"
        )

        # -------------------- SCANNING ANIMATION --------------------
        st.write("")
        progress = st.progress(
            0,
            text="INITIALISING ROAD CONDITION SCAN"
        )

        stages = [
            (20, "CHECKING WEATHER & ROAD SURFACE"),
            (45, "ANALYSING TRAFFIC"),
            (70, "CHECKING VISIBILITY"),
            (90, "READING TRAINED MODEL OUTPUT"),
            (100, "ASSESSMENT COMPLETE"),
        ]

        for pct, message in stages:
            time.sleep(0.15)
            progress.progress(pct, text=message)

        time.sleep(0.2)
        progress.empty()

        st.write("")
        st.markdown(
            '<div class="eyebrow">03 / ASSESSMENT OUTPUT</div>',
            unsafe_allow_html=True
        )
        st.header("Road Risk Analysis")

        # -------------------- MAP-STYLE JOURNEY MONITOR --------------------
        left, right = st.columns([1.5, 1])

        with left:
            st.markdown("""
            <div class="hud" style="padding:16px 18px;">
              <div class="eyebrow">ROUTE VISUALISATION / 01</div>
              <h3 style="margin-top:8px;">JOURNEY MONITOR</h3>
              <div style="color:#00d9ff;font-size:12px;">
                <span class="status-dot"></span> ROUTE DISPLAY ACTIVE
              </div>
            </div>
            """, unsafe_allow_html=True)

            safe_start = html.escape(start.strip())[:55]
            safe_destination = html.escape(destination.strip())[:55]

            # Illustrative route diagram, not a real GPS map.
            map_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <style>
              html,body {{
                margin:0;padding:0;background:#030b1c;
                font-family:Arial,sans-serif;overflow:hidden;
              }}
              .map {{
                position:relative;height:330px;overflow:hidden;
                border:1px solid #087dcc;border-radius:12px;
                background:
                  radial-gradient(ellipse at 75% 20%,#10345b 0%,transparent 48%),
                  linear-gradient(135deg,#07182c,#030b1c);
              }}
              .grid {{
                position:absolute;inset:0;
                background-image:
                  linear-gradient(#00aaff13 1px,transparent 1px),
                  linear-gradient(90deg,#00aaff13 1px,transparent 1px);
                background-size:26px 26px;
              }}
              .road {{
                fill:none;stroke:#102e4c;stroke-width:23;
                stroke-linecap:round;stroke-linejoin:round;
              }}
              .road-edge {{
                fill:none;stroke:#147bff;stroke-width:2;
                stroke-linecap:round;stroke-linejoin:round;
              }}
              .route {{
                fill:none;stroke:#00d9ff;stroke-width:4;
                stroke-linecap:round;stroke-linejoin:round;
                stroke-dasharray:10 10;
                animation:travel 1.2s linear infinite;
                filter:drop-shadow(0 0 5px #00d9ff);
              }}
              .pin {{
                animation:pinpulse 1.5s ease-in-out infinite;
                transform-box:fill-box;transform-origin:center;
              }}
              .label {{
                fill:#eaf7ff;font-size:12px;font-weight:bold;
              }}
              .small {{
                fill:#71cfff;font-size:9px;letter-spacing:1.4px;
              }}
              @keyframes travel {{
                to {{stroke-dashoffset:-40;}}
              }}
              @keyframes pinpulse {{
                0%,100% {{opacity:1;}}
                50% {{opacity:.55;}}
              }}
            </style>
            </head>
            <body>
            <div class="map">
              <div class="grid"></div>
              <svg viewBox="0 0 500 330"
                   style="position:absolute;width:100%;height:100%;"
                   preserveAspectRatio="xMidYMid meet">
                <path class="road" d="M-20 65 L110 115 L175 82 L280 120 L390 55 L520 100"/>
                <path class="road-edge" d="M-20 65 L110 115 L175 82 L280 120 L390 55 L520 100"/>
                <path class="road" d="M10 290 L100 230 L165 250 L255 190 L340 220 L510 150"/>
                <path class="road-edge" d="M10 290 L100 230 L165 250 L255 190 L340 220 L510 150"/>
                <path class="road" d="M55 -20 L95 70 L70 150 L125 210 L100 350"/>
                <path class="road-edge" d="M55 -20 L95 70 L70 150 L125 210 L100 350"/>
                <path class="road" d="M420 -20 L390 55 L420 130 L385 205 L450 350"/>
                <path class="road-edge" d="M420 -20 L390 55 L420 130 L385 205 L450 350"/>

                <path class="route"
                      d="M95 70 C130 95 140 145 205 158
                         S300 200 340 220 S390 245 420 270"/>

                <g class="pin">
                  <circle cx="95" cy="70" r="17" fill="#00d9ff" opacity=".18"/>
                  <circle cx="95" cy="70" r="8" fill="#00d9ff"
                          stroke="#eaffff" stroke-width="2"/>
                </g>
                <text x="115" y="59" class="small">START</text>
                <text x="115" y="75" class="label">{safe_start}</text>

                <g class="pin">
                  <circle cx="420" cy="270" r="18" fill="#00f5a0" opacity=".18"/>
                  <circle cx="420" cy="270" r="9" fill="#00f5a0"
                          stroke="#eafff6" stroke-width="2"/>
                </g>
                <text x="405" y="296" text-anchor="end" class="small">DESTINATION</text>
                <text x="405" y="312" text-anchor="end" class="label">{safe_destination}</text>

                <g fill="#147bff">
                  <circle cx="175" cy="82" r="3"/>
                  <circle cx="280" cy="120" r="3"/>
                  <circle cx="255" cy="190" r="3"/>
                  <circle cx="390" cy="55" r="3"/>
                </g>
                <text x="16" y="22" class="small">ROADSAFE / ROUTE DISPLAY</text>
                <text x="16" y="310" class="small">ILLUSTRATIVE MAP • NOT LIVE GPS</text>
              </svg>
            </div>
            </body>
            </html>
            """

            components.html(map_html, height=340, scrolling=False)

        # -------------------- CIRCULAR RISK GAUGE --------------------
        with right:
            circumference = 2 * math.pi * 82
            gauge_font = 18 if risk == "MODERATE" else 23

            st.markdown(f"""
            <div class="hud" style="text-align:center;border-color:{risk_color}88;">
              <div class="eyebrow">TRAINED MODEL CLASSIFICATION</div>
              <svg viewBox="0 0 220 220"
                   style="width:100%;max-width:290px;filter:drop-shadow(0 0 13px {risk_color}55);">
                <circle cx="110" cy="110" r="82" fill="none"
                        stroke="#102a4c" stroke-width="14"/>
                <circle cx="110" cy="110" r="82" fill="none"
                        stroke="{risk_color}" stroke-width="12"
                        stroke-linecap="round"
                        stroke-dasharray="{circumference} {circumference}"
                        transform="rotate(-90 110 110)"/>
                <circle cx="110" cy="110" r="63" fill="#06152b"
                        stroke="{risk_color}55"/>
                <circle cx="110" cy="28" r="4" fill="{risk_color}">
                  <animate attributeName="opacity" values="1;.3;1"
                           dur="1.5s" repeatCount="indefinite"/>
                </circle>
                <text x="110" y="89" text-anchor="middle"
                      fill="{risk_color}" font-size="12">RISK LEVEL</text>
                <text x="110" y="121" text-anchor="middle"
                      fill="#f1f8ff" font-size="{gauge_font}"
                      font-family="sans-serif" font-weight="700">{risk}</text>
                <text x="110" y="145" text-anchor="middle"
                      fill="#8cb9df" font-size="11">MODEL OUTPUT</text>
              </svg>
              <div style="color:{risk_color};font-weight:700;">
                {risk} RISK STATUS
              </div>
            </div>
            """, unsafe_allow_html=True)

        # -------------------- VEHICLE SUMMARY --------------------
        vehicle_icons = {
            "Car": "🚗",
            "Motorcycle": "🏍️",
            "Scooter": "🛵",
            "Bus": "🚌",
            "Truck": "🚚",
        }
        vehicle_icon = vehicle_icons.get(vehicle, "🚗")

        st.write("")
        x, y, z = st.columns(3)

        with x:
            st.markdown(f"""
            <div class="hud">
              <div class="eyebrow">JOURNEY SUMMARY</div>
              <p>📍 <b>FROM</b><br>{html.escape(start)}</p>
              <p style="color:#00d9ff;">······ ROUTE ······</p>
              <p>🏁 <b>TO</b><br>{html.escape(destination)}</p>
            </div>
            """, unsafe_allow_html=True)

        with y:
            st.markdown(f"""
            <div class="hud">
              <div class="eyebrow">VEHICLE</div>
              <div style="font-size:34px;margin-top:14px;">{vehicle_icon}</div>
              <div style="font-size:18px;">{html.escape(vehicle)}</div>
            </div>
            """, unsafe_allow_html=True)

        with z:
            st.markdown(f"""
            <div class="hud">
              <div class="eyebrow">TRAINED MODEL OUTPUT</div>
              <h2 style="margin-top:14px;color:{risk_color};">{risk}</h2>
              <div style="color:#b7d4f0;font-size:13px;line-height:1.6;">
                Classified by the exported Orange decision tree.
              </div>
            </div>
            """, unsafe_allow_html=True)

        # -------------------- SAFETY RECOMMENDATIONS --------------------
        st.write("")
        st.markdown(
            '<div class="eyebrow">04 / SAFETY INTELLIGENCE</div>',
            unsafe_allow_html=True
        )
        st.header("Key Recommendations")

        tips = []

        if weather in ["Rainy", "Foggy"]:
            tips.append((
                "🌧️", "Weather alert",
                "Rain or fog can reduce visibility and grip. Slow down and increase following distance."
            ))
        elif weather == "Cloudy":
            tips.append((
                "🌥️", "Weather awareness",
                "Watch for changing weather and check conditions before departure."
            ))
        else:
            tips.append((
                "☀️", "Weather conditions",
                "Continue watching the road and your surroundings."
            ))

        if road == "Wet":
            tips.append((
                "🛣️", "Wet road caution",
                "Brake gently, avoid sudden manoeuvres and leave extra stopping distance."
            ))
        elif road == "Damp":
            tips.append((
                "🚧", "Road surface caution",
                "Allow extra stopping distance on damp surfaces."
            ))
        else:
            tips.append((
                "🛣️", "Road surface",
                "Maintain safe gaps and avoid sudden lane changes."
            ))

        if traffic == "High":
            tips.append((
                "🚦", "Traffic alert",
                "Expect congestion. Avoid distractions and follow traffic signals."
            ))
        elif traffic == "Medium":
            tips.append((
                "🚘", "Traffic awareness",
                "Keep a safe gap and anticipate other vehicles."
            ))
        else:
            tips.append((
                "🛣️", "Traffic conditions",
                "Stay alert even when traffic is light."
            ))

        if visibility == "Low":
            tips.append((
                "💡", "Visibility warning",
                "Use appropriate lights, reduce speed and avoid risky overtaking."
            ))
        elif visibility == "Medium":
            tips.append((
                "👁️", "Visibility caution",
                "Use lights suitable for conditions and remain attentive."
            ))
        else:
            tips.append((
                "👁️", "Visibility",
                "Watch for pedestrians and cyclists."
            ))

        for i in range(0, len(tips), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(tips):
                    icon, title, detail = tips[i + j]
                    with col:
                        st.markdown(f"""
                        <div class="hud" style="min-height:125px;margin-bottom:10px;">
                          <div style="font-size:23px;">{icon}</div>
                          <div style="color:#00d9ff;font-weight:700;margin:8px 0;">
                            {title}
                          </div>
                          <div style="font-size:13px;color:#b7d4f0;line-height:1.6;">
                            {detail}
                          </div>
                        </div>
                        """, unsafe_allow_html=True)

        p, q, r = st.columns(3)

        with p:
            st.markdown("""
            <div class="hud" style="text-align:center;">
              🪖<br><b>Seatbelts & Helmets</b><br>
              <small>Wear the right protection.</small>
            </div>
            """, unsafe_allow_html=True)

        with q:
            st.markdown("""
            <div class="hud" style="text-align:center;">
              💡<br><b>Lights & Visibility</b><br>
              <small>Use lights suitable for conditions.</small>
            </div>
            """, unsafe_allow_html=True)

        with r:
            st.markdown("""
            <div class="hud" style="text-align:center;">
              🔧<br><b>Vehicle Check</b><br>
              <small>Check tyres, brakes and mirrors.</small>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.markdown("""
        <div class="hud" style="text-align:center;padding:24px;">
          <div class="eyebrow">END OF ASSESSMENT</div>
          <h3 style="color:#00d9ff;">HAVE A SAFE AND HAPPY JOURNEY</h3>
          <div style="color:#b7d4f0;">
            Stay alert. Protect every passenger. Make every journey safer.
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.caption(
            "Risk category is generated from predictions exported from a "
            "trained Orange decision tree using the selected weather, road, "
            "traffic and visibility inputs. This is not a validated estimate "
            "of real-world accident probability and does not use live route, "
            "weather or traffic data. The route diagram is illustrative, "
            "not a verified GPS route."
        )
