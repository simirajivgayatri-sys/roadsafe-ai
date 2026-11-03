import streamlit as st
import streamlit.components.v1 as components
import html
import math
import time
from pathlib import Path
import pickle
import numpy as np
import requests
import Orange

st.set_page_config(
    page_title="ROADSAFE AI | Cyberpunk HUD",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------- SCREEN CONTROL --------------------

if "show_results" not in st.session_state:
    st.session_state.show_results = False

if "journey_data" not in st.session_state:
    st.session_state.journey_data = {}


# -------------------- ORANGE MODEL --------------------

@st.cache_resource
def load_orange_model():
    model_file = Path(__file__).with_name("roadsafe_random_forest.pkcls")

    if not model_file.exists():
        raise FileNotFoundError(
            "roadsafe_random_forest.pkcls is missing. "
            "Place it in the same folder as app.py."
        )

    with model_file.open("rb") as f:
        return pickle.load(f)


def predict_risk(model, weather_value, road_value, traffic_value, visibility_value):
    """Encode four categories for the saved one-hot Orange model."""

    domain = model.domain

    values = {
        "Weather": weather_value,
        "Road Conditions": road_value,
        "Traffic Density": traffic_value,
        "Visibility": visibility_value,
    }

    row = []

    for var in domain.attributes:
        if "=" not in var.name:
            raise ValueError(f"Unexpected model feature: {var.name}")

        feature, category = var.name.split("=", 1)

        if feature not in values:
            raise ValueError(f"Unknown model feature: {var.name}")

        row.append(
            1.0 if values[feature] == category else 0.0
        )

    if len(domain.class_vars) != 1 or not domain.class_var.is_discrete:
        raise ValueError("The model must have one categorical risk target.")

    table = Orange.data.Table.from_numpy(
        domain,
        X=np.asarray([row], dtype=float),
        Y=np.asarray([np.nan], dtype=float),
    )

    prediction = model(table)
    predicted_index = int(prediction[0])

    return str(domain.class_var.values[predicted_index])


# -------------------- LIVE WEATHER --------------------

@st.cache_data(ttl=600, show_spinner=False)
def fetch_current_weather(place_name):

    geo_response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name": place_name,
            "count": 10,
            "language": "en",
            "format": "json",
        },
        timeout=15,
    )

    geo_response.raise_for_status()
    geo_results = geo_response.json().get("results", [])

    if not geo_results:
        raise ValueError(
            f"Could not find '{place_name}'. Try another location."
        )

    place = next(
        (item for item in geo_results
         if item.get("country_code") == "IN"),
        geo_results[0]
    )

    weather_response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": (
                "temperature_2m,relative_humidity_2m,precipitation,rain,"
                "showers,snowfall,weather_code,cloud_cover,"
                "wind_speed_10m,visibility"
            ),
            "timezone": "auto",
        },
        timeout=15,
    )

    weather_response.raise_for_status()
    current = weather_response.json().get("current", {})

    code = int(current.get("weather_code", 0))

    rain_now = (
        float(current.get("precipitation", 0) or 0) > 0
        or float(current.get("rain", 0) or 0) > 0
        or float(current.get("showers", 0) or 0) > 0
        or float(current.get("snowfall", 0) or 0) > 0
    )

    if code in [45, 48]:
        weather_category = "Foggy"

    elif rain_now or code in [
        51, 53, 55, 56, 57, 61, 63, 65,
        66, 67, 71, 73, 75, 77, 80, 81,
        82, 85, 86, 95, 96, 99
    ]:
        weather_category = "Rainy"

    elif code in [1, 2, 3]:
        weather_category = "Cloudy"

    else:
        weather_category = "Clear"

    visibility_m = float(current.get("visibility", 10000) or 0)

    if visibility_m >= 5000:
        visibility_category = "High"
    elif visibility_m >= 2000:
        visibility_category = "Medium"
    else:
        visibility_category = "Low"

    return {
        "place": ", ".join(
            part for part in [
                place.get("name"),
                place.get("admin1"),
                place.get("country")
            ] if part
        ),
        "weather": weather_category,
        "visibility": visibility_category,
        "temperature": current.get("temperature_2m"),
        "humidity": current.get("relative_humidity_2m"),
        "precipitation": current.get("precipitation"),
        "wind_speed": current.get("wind_speed_10m"),
        "visibility_m": visibility_m,
    }


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

.block-container {
  max-width:1450px;
  padding-top:1.2rem;
  padding-bottom:2rem;
}

h1,h2,h3 {
  font-family:Orbitron,sans-serif!important;
}

.eyebrow {
  color:var(--cyan);
  font-size:11px;
  letter-spacing:3px;
  font-weight:700;
}

.hero,.hud {
  background:linear-gradient(145deg,#071b36ee,#030b1bee);
  border:1px solid #087dcc;
  border-radius:16px;
  padding:20px;
  box-shadow:inset 0 0 22px #007bff0b,0 0 15px #006bff12;
  transition:transform .25s,border-color .25s,box-shadow .25s;
}

.hero {
  position:relative;
  overflow:hidden;
  padding:28px;
}

.hud:hover {
  transform:translateY(-3px);
  border-color:var(--cyan);
  box-shadow:0 0 22px #00bfff25;
}

.hero:after {
 content:"";
 position:absolute;
 inset:0;
 pointer-events:none;
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
  display:inline-block;
  width:8px;
  height:8px;
  border-radius:50%;
  background:var(--green);
  box-shadow:0 0 12px var(--green);
  animation:pulse 1.4s infinite;
  margin-right:8px;
}

.stTextInput label,.stSelectbox label {
  color:#a9d8ff!important;
  font-weight:600!important;
}

.stTextInput input,.stSelectbox div[data-baseweb="select"]>div {
  background:#06152b!important;
  color:white!important;
  border-color:#1266b8!important;
  border-radius:9px!important;
}

.stButton>button,.stFormSubmitButton>button {
  width:100%;
  min-height:52px;
  color:white;
  font-family:Orbitron,sans-serif;
  font-weight:700;
  letter-spacing:1px;
  border:1px solid #50efff;
  border-radius:10px;
  background:linear-gradient(90deg,#0755cf,#00bff5,#0755cf);
  background-size:200% 100%;
  box-shadow:0 0 16px #007bff75;
  transition:transform .2s,box-shadow .2s;
}

.stButton>button:hover,.stFormSubmitButton>button:hover {
  transform:translateY(-3px);
  box-shadow:0 0 30px #00d9ffb0;
}

div[data-testid="stExpander"] {
  border:1px solid #1266b8;
  border-radius:12px;
  background:#04132b;
}
</style>
""", unsafe_allow_html=True)


# -------------------- HERO --------------------

st.markdown("""
<div class="hero">
  <div class="eyebrow">
    <span class="status-dot"></span>
    ROAD SAFETY INTELLIGENCE SYSTEM
  </div>

  <h1 style="font-size:clamp(30px,5vw,54px);margin:12px 0 4px;">
    ROADSAFE
    <span style="color:#00d9ff;text-shadow:0 0 20px #00bfff;">AI</span>
  </h1>

  <div style="color:#a8d9ff;letter-spacing:2px;font-size:13px;">
    ACCIDENT RISK ASSESSMENT • ROAD SAFETY ADVISORY
  </div>

  <p style="color:#00d9ff;margin-top:15px;font-style:italic;">
    Plan your journey. Assess conditions. Travel safely.
  </p>

  <div class="eyebrow">
    SYSTEM STATUS: ONLINE / SAFETY MODE ACTIVE
  </div>
</div>
""", unsafe_allow_html=True)


# -------------------- HOME SCREEN --------------------

submitted = False

if not st.session_state.show_results:

    st.write("")

    st.markdown(
        '<div class="eyebrow">01 / JOURNEY CONFIGURATION</div>',
        unsafe_allow_html=True
    )

    st.header("Your Journey")

    with st.form("roadsafe_form"):

        use_live_weather = st.checkbox(
            "🌦️ Automatically fetch current weather for the starting location",
            value=True,
            help="Uses Open-Meteo current weather and visibility. Uncheck to enter these manually."
        )

        st.caption(
            "📍 IMPORTANT: Enter locations in City, State, Country format. "
            "Example: Kochi, Kerala, India."
        )

        c1, c2 = st.columns(2)

        with c1:
            start = st.text_input(
                "📍 Starting Location",
                placeholder="Kochi, Kerala, India",
                help="Enter the complete location: city, state, country."
            )

        with c2:
            destination = st.text_input(
                "⚑ Destination",
                placeholder="Thrissur, Kerala, India",
                help="Enter the complete location: city, state, country."
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
                ["Clear", "Cloudy", "Rainy", "Foggy"],
                disabled=use_live_weather
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
                ["High", "Medium", "Low"],
                disabled=use_live_weather
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


# -------------------- SAVE SUBMITTED JOURNEY --------------------

if submitted:

    if not start.strip() or not destination.strip():
        st.warning("Please enter both your starting location and destination.")

    else:
        st.session_state.journey_data = {
            "start": start,
            "destination": destination,
            "weather": weather,
            "road": road,
            "traffic": traffic,
            "visibility": visibility,
            "vehicle": vehicle,
            "use_live_weather": use_live_weather,
        }

        st.session_state.show_results = True
        st.rerun()


# -------------------- PREDICTION SCREEN --------------------

if st.session_state.show_results:

    data = st.session_state.journey_data

    start = data["start"]
    destination = data["destination"]
    weather = data["weather"]
    road = data["road"]
    traffic = data["traffic"]
    visibility = data["visibility"]
    vehicle = data["vehicle"]
    use_live_weather = data["use_live_weather"]

    if st.button("← BACK TO JOURNEY CONFIGURATION"):
        st.session_state.show_results = False
        st.session_state.journey_data = {}
        st.rerun()

    weather_details = None

    if use_live_weather:
        try:
            with st.spinner("Fetching current weather..."):
                weather_details = fetch_current_weather(start.strip())

            weather = weather_details["weather"]
            visibility = weather_details["visibility"]

        except Exception as exc:
            st.error(f"Could not retrieve live weather: {exc}")
            st.info(
                "Return to the journey form, uncheck automatic weather "
                "and enter Weather and Visibility manually."
            )
            st.stop()

    # -------------------- ORANGE MODEL PREDICTION --------------------

    try:
        orange_model = load_orange_model()

        model_risk = predict_risk(
            orange_model,
            weather,
            road,
            traffic,
            visibility
        ).strip().title()

    except Exception as exc:
        st.error(f"Could not load or run the Orange model: {exc}")
        st.stop()

    if model_risk not in ["Low", "Medium", "High"]:
        st.error(f"Unexpected model output: {model_risk}")
        st.stop()

    risk = (
        "HIGH" if model_risk == "High"
        else "MODERATE" if model_risk == "Medium"
        else "LOW"
    )

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
        (90, "CALCULATING CONDITION SCORE"),
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

    # -------------------- WEATHER DETAILS --------------------

    if weather_details:

        st.markdown(
            f"""
            <div class="hud" style="margin:12px 0;">
              <div class="eyebrow">LIVE WEATHER / START LOCATION</div>

              <h3 style="margin:8px 0;">
                {html.escape(weather_details["place"])}
              </h3>

              <div style="color:#a9d8ff;">
                Current condition: <b>{weather}</b> |
                Visibility: <b>{visibility}</b>
              </div>

              <div style="color:#a9d8ff;margin-top:8px;">
                Temperature: <b>{weather_details["temperature"]} °C</b>
                &nbsp; · &nbsp;
                Humidity: <b>{weather_details["humidity"]}%</b>
                &nbsp; · &nbsp;
                Wind: <b>{weather_details["wind_speed"]} km/h</b>
                &nbsp; · &nbsp;
                Visibility: <b>{weather_details["visibility_m"] / 1000:.1f} km</b>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        st.info(
            f"Manual weather inputs: {weather} and {visibility} visibility."
        )

    # -------------------- ROUTE VISUALISATION --------------------

    left, right = st.columns([1.5, 1])

    with left:

        st.markdown("""
        <div class="hud" style="padding:16px 18px;">
          <div class="eyebrow">ROUTE VISUALISATION / 01</div>
          <h3 style="margin-top:8px;">JOURNEY MONITOR</h3>
          <div style="color:#00d9ff;font-size:12px;">
            <span class="status-dot"></span>
            ROUTE DISPLAY ACTIVE
          </div>
        </div>
        """, unsafe_allow_html=True)

        safe_start = html.escape(start.strip())[:55]
        safe_destination = html.escape(destination.strip())[:55]

        map_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
          html,body {{
            margin:0;
            padding:0;
            background:#030b1c;
            font-family:Arial,sans-serif;
            overflow:hidden;
          }}

          .map {{
            position:relative;
            height:330px;
            overflow:hidden;
            border:1px solid #087dcc;
            border-radius:12px;
            background:
              radial-gradient(ellipse at 75% 20%,#10345b 0%,transparent 48%),
              linear-gradient(135deg,#07182c,#030b1c);
          }}

          .grid {{
            position:absolute;
            inset:0;
            background-image:
              linear-gradient(#00aaff13 1px,transparent 1px),
              linear-gradient(90deg,#00aaff13 1px,transparent 1px);
            background-size:26px 26px;
          }}

          .road {{
            fill:none;
            stroke:#102e4c;
            stroke-width:23;
            stroke-linecap:round;
            stroke-linejoin:round;
          }}

          .road-edge {{
            fill:none;
            stroke:#147bff;
            stroke-width:2;
          }}

          .route {{
            fill:none;
            stroke:#00d9ff;
            stroke-width:4;
            stroke-dasharray:10 10;
            animation:travel 1.2s linear infinite;
            filter:drop-shadow(0 0 5px #00d9ff);
          }}

          .pin {{
            animation:pinpulse 1.5s ease-in-out infinite;
          }}

          .label {{
            fill:#eaf7ff;
            font-size:12px;
            font-weight:bold;
          }}

          .small {{
            fill:#71cfff;
            font-size:9px;
            letter-spacing:1.4px;
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

            <path class="road"
                  d="M-20 65 L110 115 L175 82 L280 120 L390 55 L520 100"/>

            <path class="road-edge"
                  d="M-20 65 L110 115 L175 82 L280 120 L390 55 L520 100"/>

            <path class="road"
                  d="M10 290 L100 230 L165 250 L255 190 L340 220 L510 150"/>

            <path class="road-edge"
                  d="M10 290 L100 230 L165 250 L255 190 L340 220 L510 150"/>

            <path class="route"
                  d="M95 70 C130 95 140 145 205 158
                     S300 200 340 220 S390 245 420 270"/>

            <g class="pin">
              <circle cx="95" cy="70" r="17"
                      fill="#00d9ff" opacity=".18"/>
              <circle cx="95" cy="70" r="8"
                      fill="#00d9ff" stroke="#eafaff" stroke-width="2"/>
            </g>

            <text x="115" y="59" class="small">START</text>
            <text x="115" y="75" class="label">{safe_start}</text>

            <g class="pin">
              <circle cx="420" cy="270" r="18"
                      fill="#00f5a0" opacity=".18"/>
              <circle cx="420" cy="270" r="9"
                      fill="#00f5a0" stroke="#eafff6" stroke-width="2"/>
            </g>

            <text x="405" y="296"
                  text-anchor="end" class="small">DESTINATION</text>

            <text x="405" y="312"
                  text-anchor="end" class="label">{safe_destination}</text>

            <text x="16" y="22" class="small">
              ROADSAFE / ROUTE DISPLAY
            </text>

            <text x="16" y="310" class="small">
              ILLUSTRATIVE MAP • NOT LIVE GPS
            </text>
          </svg>
        </div>
        </body>
        </html>
        """

        components.html(map_html, height=340, scrolling=False)

    # -------------------- RISK GAUGE --------------------

    with right:

        circumference = 2 * math.pi * 82
        gauge_font = 18 if risk == "MODERATE" else 23

        gauge_html = f"""
        <!DOCTYPE html>
        <html>
        <body style="margin:0;background:transparent;
                     font-family:Arial,sans-serif;">

            <div style="background:linear-gradient(145deg,#071b36,#030b1b);
                        border:1px solid {risk_color}88;
                        border-radius:16px;
                        padding:20px;
                        text-align:center;
                        color:white;">

                <div style="color:#00d9ff;font-size:11px;
                            font-weight:bold;letter-spacing:3px;">
                    TRAINED MODEL CLASSIFICATION
                </div>

                <svg viewBox="0 0 220 220"
                     style="width:100%;max-width:290px;">

                    <circle cx="110" cy="110" r="82"
                            fill="none" stroke="#102a4c"
                            stroke-width="14"/>

                    <circle cx="110" cy="110" r="82"
                            fill="none" stroke="{risk_color}"
                            stroke-width="12"
                            stroke-linecap="round"
                            stroke-dasharray="{circumference} {circumference}"
                            transform="rotate(-90 110 110)"/>

                    <circle cx="110" cy="110" r="63"
                            fill="#06152b"
                            stroke="{risk_color}"/>

                    <text x="110" y="89" text-anchor="middle"
                          fill="{risk_color}" font-size="12">
                        RISK LEVEL
                    </text>

                    <text x="110" y="121" text-anchor="middle"
                          fill="#f1f8ff"
                          font-size="{gauge_font}"
                          font-weight="700">
                        {risk}
                    </text>

                    <text x="110" y="145" text-anchor="middle"
                          fill="#8cb9df" font-size="11">
                        MODEL CLASS
                    </text>
                </svg>

                <div style="color:{risk_color};font-weight:bold;">
                    {risk} RISK STATUS
                </div>
            </div>
        </body>
        </html>
        """

        components.html(gauge_html, height=310, scrolling=False)

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
          <div style="color:#b7d4f0;font-size:13px;">
            Classified by the trained Orange Random Forest.
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
            "Rain or fog can reduce visibility and grip. "
            "Slow down and increase following distance."
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

    # -------------------- SAFETY FOOTER --------------------

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
      <h3 style="color:#00d9ff;">
        HAVE A SAFE AND HAPPY JOURNEY
      </h3>
      <div style="color:#b7d4f0;">
        Stay alert. Protect every passenger. Make every journey safer.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        "Risk category is predicted by the trained Orange Random Forest "
        "using weather and visibility fetched from Open-Meteo when automatic "
        "weather is enabled, plus road and traffic conditions entered by the "
        "user. This is a school-project demonstration, not a validated "
        "estimate of real-world accident probability. Traffic is not fetched "
        "live, and the route diagram is illustrative rather than a verified "
        "GPS route."
    )
