
import streamlit as st
import html

st.set_page_config(
    page_title="ROADSAFE AI | Road Safety Dashboard",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- DESIGN --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #07111f;
    --panel: #101f33;
    --panel2: #142941;
    --blue: #36c5ff;
    --cyan: #6de4ff;
    --text: #edf7ff;
    --muted: #9eb4ca;
}

.stApp {
    background:
        radial-gradient(ellipse at 15% 0%, #103257 0%, transparent 42%),
        radial-gradient(ellipse at 95% 15%, #102849 0%, transparent 35%),
        var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, p, label {
    color: var(--text);
}

.hero {
    background: linear-gradient(115deg, #102b49, #0a1729 65%, #10334d);
    border: 1px solid #244a6b;
    border-radius: 24px;
    padding: 30px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 45px #00000035;
    margin-bottom: 24px;
}

.hero:after {
    content: "〰";
    position: absolute;
    right: 24px;
    top: -50px;
    font-size: 190px;
    color: #36c5ff12;
    transform: rotate(-20deg);
}

.eyebrow {
    color: var(--cyan);
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 3px;
}

.hero h1 {
    font-size: clamp(32px, 5vw, 54px);
    line-height: 1.1;
    font-weight: 800;
    margin: 12px 0;
}

.hero p {
    color: #bed1e4;
    max-width: 620px;
}

.pill {
    display: inline-block;
    border: 1px solid #32648a;
    background: #102e49;
    color: #80dcff;
    padding: 7px 12px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 700;
}

.section-title {
    font-size: 23px;
    font-weight: 800;
    margin: 28px 0 5px;
}

.section-sub {
    color: var(--muted);
    margin-bottom: 18px;
    font-size: 14px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(145deg, #11243a, #0c1b2d);
    border: 1px solid #223e59;
    border-radius: 18px;
}

div[data-testid="stMetric"] {
    background: #10263c;
    border: 1px solid #244761;
    padding: 16px;
    border-radius: 15px;
    transition: transform .25s ease, border-color .25s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: var(--blue);
}

.stButton > button {
    background: linear-gradient(100deg, #1689e8, #24c6f5);
    color: #031324;
    border: none;
    border-radius: 12px;
    min-height: 49px;
    font-weight: 800;
    transition: transform .2s ease, box-shadow .2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 24px #36c5ff55;
    color: #031324;
    border: none;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: #0c1d30;
    border-color: #2a4965;
    border-radius: 10px;
}

div[data-testid="stExpander"] {
    background: #0e2034;
    border: 1px solid #25415d;
    border-radius: 13px;
    margin-bottom: 9px;
}

.risk-card {
    padding: 25px;
    border-radius: 20px;
    border: 1px solid var(--risk);
    background: linear-gradient(120deg, var(--risk-bg), #0d1d30);
    margin: 14px 0;
    animation: rise-in .65s ease both;
}

.risk-name {
    color: var(--risk);
    font-size: clamp(30px, 5vw, 43px);
    font-weight: 800;
    letter-spacing: 1px;
    margin: 6px 0;
}

.risk-track {
    height: 12px;
    border-radius: 30px;
    background: #263a4f;
    overflow: hidden;
    margin-top: 18px;
}

.risk-fill {
    height: 100%;
    border-radius: 30px;
    width: var(--progress);
    background: linear-gradient(90deg, var(--risk), #ffffffaa);
    animation: fill-meter 1.3s ease-out both;
    box-shadow: 0 0 15px var(--risk);
}

.tip-card {
    background: #10253a;
    border: 1px solid #294761;
    border-radius: 14px;
    padding: 15px;
    margin-bottom: 10px;
    transition: transform .2s ease, border-color .2s ease;
}

.tip-card:hover {
    transform: translateX(4px);
    border-color: #36c5ff;
}

.tip-card strong {
    color: #75dcff;
}

.footer {
    text-align: center;
    padding: 25px 10px;
    color: #8da8c0;
    font-size: 12px;
}

@keyframes fill-meter {
    from { width: 0; }
    to { width: var(--progress); }
}

@keyframes rise-in {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

@media (prefers-reduced-motion: reduce) {
    *, *:before, *:after {
        animation: none !important;
        transition: none !important;
    }
}
</style>
""", unsafe_allow_html=True)

# -------------------- HERO --------------------

st.markdown("""
<div class="hero">
    <div class="eyebrow">INTELLIGENT ROAD SAFETY SYSTEM</div>
    <h1>ROADSAFE <span style="color:#36c5ff">AI</span></h1>
    <p>
        Understand your travel conditions, assess potential hazards,
        and get practical safety guidance before you start your journey.
    </p>
    <span class="pill">🚦 ROAD CONDITION ANALYSIS</span>
    &nbsp; <span class="pill">🛡️ SAFETY FIRST</span>
</div>
""", unsafe_allow_html=True)

# Online image: requires internet access in the browser.
st.image(
    "https://images.unsplash.com/photo-1519608487953-e999c86e7455"
    "?auto=format&fit=crop&w=1800&q=85",
    caption="Plan ahead. Stay alert. Make every journey safer.",
    use_container_width=True
)

# -------------------- JOURNEY FORM --------------------

st.markdown(
    '<div class="section-title">📍 Plan your journey</div>'
    '<div class="section-sub">Enter your route and select the conditions you expect.</div>',
    unsafe_allow_html=True
)

with st.container(border=True):
    c1, c2 = st.columns(2)

    with c1:
        start_location = st.text_input(
            "Starting location",
            placeholder="e.g. Kochi"
        )

    with c2:
        destination = st.text_input(
            "Destination",
            placeholder="e.g. Thrissur"
        )

    st.markdown("#### 🌦️ Road & travel conditions")

    c1, c2, c3 = st.columns(3)

    with c1:
        weather = st.selectbox(
            "Weather",
            ["Clear", "Cloudy", "Rainy", "Foggy"]
        )
        road = st.selectbox(
            "Road condition",
            ["Dry", "Damp", "Wet"]
        )

    with c2:
        traffic = st.selectbox(
            "Traffic density",
            ["Low", "Medium", "High"]
        )
        visibility = st.selectbox(
            "Visibility",
            ["High", "Medium", "Low"]
        )

    with c3:
        vehicle = st.selectbox(
            "Vehicle type",
            ["Car", "Motorcycle", "Scooter", "Bus", "Truck"]
        )

    analyse = st.button(
        "🔍  ANALYSE ROAD RISK",
        type="primary",
        use_container_width=True
    )

# -------------------- ANALYSIS --------------------

if analyse:
    if not start_location.strip() or not destination.strip():
        st.warning("Please enter both your starting location and destination.")

    else:
        # Demonstration scoring rules, not a trained ML prediction.
        score = 0

        if weather in ["Rainy", "Foggy"]:
            score += 2
        elif weather == "Cloudy":
            score += 1

        if road == "Wet":
            score += 2
        elif road == "Damp":
            score += 1

        if traffic == "High":
            score += 2
        elif traffic == "Medium":
            score += 1

        if visibility == "Low":
            score += 2
        elif visibility == "Medium":
            score += 1

        if score >= 6:
            risk = "HIGH"
            colour = "#ff5263"
            risk_bg = "#501d2a"
            symbol = "🔴"
            summary = "Extra caution required"
            advice = "Consider delaying non-essential travel if conditions are unsafe."
        elif score >= 3:
            risk = "MODERATE"
            colour = "#ffbd4a"
            risk_bg = "#49371c"
            symbol = "🟠"
            summary = "Drive with increased caution"
            advice = "Allow extra time and adjust your driving to conditions."
        else:
            risk = "LOW"
            colour = "#42e6a4"
            risk_bg = "#123b34"
            symbol = "🟢"
            summary = "Continue to stay alert"
            advice = "Keep following road rules and remain attentive."

        st.markdown(
            '<div class="section-title">📊 Your risk assessment</div>'
            '<div class="section-sub">Review the result and safety guidance for your selected conditions.</div>',
            unsafe_allow_html=True
        )

        progress = int(score / 8 * 100)

        st.markdown(
            f"""
            <div class="risk-card" style="
                --risk:{colour};
                --risk-bg:{risk_bg};
                --progress:{progress}%;
            ">
                <div style="font-size:12px;letter-spacing:2px;color:#c0d4e6">
                    ESTIMATED RISK CATEGORY
                </div>
                <div class="risk-name">{symbol} {risk} RISK</div>
                <div style="font-size:16px;color:#e6f2fc">{summary}</div>
                <div style="margin-top:8px;color:#b7ccdf">{advice}</div>
                <div class="risk-track"><div class="risk-fill"></div></div>
                <div style="display:flex;justify-content:space-between;
                            margin-top:8px;font-size:12px;color:#a8c0d5">
                    <span>Condition score</span>
                    <span>{score}/8 • {progress}% of demonstration scale</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Route and condition overview
        st.markdown("#### 🗺️ Journey overview")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("🚘 Vehicle", vehicle)

        with c2:
            st.metric("🌦️ Weather", weather)

        with c3:
            st.metric("🚦 Traffic", traffic)

        with st.container(border=True):
            st.markdown("**📍 Your route**")
            r1, r2 = st.columns(2)

            with r1:
                st.markdown("**FROM**")
                st.write(start_location)

            with r2:
                st.markdown("**TO**")
                st.write(destination)

        # Recommendations
        st.markdown("#### 🛡️ Priority safety recommendations")

        priorities = []

        if weather in ["Rainy", "Foggy"] or road == "Wet":
            priorities.append((
                "🌧️", "Slow down",
                "Reduce speed gradually and increase your following distance."
            ))

        if visibility == "Low" or weather == "Foggy":
            priorities.append((
                "💡", "Improve visibility",
                "Use low-beam headlights in fog and avoid high beams."
            ))

        if traffic == "High":
            priorities.append((
                "🚗", "Heavy traffic",
                "Avoid sudden lane changes and maintain a safe gap."
            ))

        if road == "Wet":
            priorities.append((
                "🛣️", "Wet road",
                "Brake gently and avoid sudden turns."
            ))

        if not priorities:
            priorities.append((
                "✅", "Stay alert",
                "Follow speed limits, keep a safe distance, and watch for hazards."
            ))

        for icon, heading, detail in priorities:
            st.markdown(
                f"""
                <div class="tip-card">
                    <strong>{icon} &nbsp; {heading}</strong><br>
                    <span style="color:#c4d5e5">{detail}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Vehicle-specific checklist
        st.markdown("#### 🧰 Safety checklist")

        with st.expander("🚦 Speed & safe distance", expanded=True):
            st.markdown("""
            - Follow posted speed limits and adapt to the conditions.
            - Increase your following distance in rain or on wet roads.
            - Avoid sudden braking, sharp turns, and risky overtaking.
            """)

        with st.expander("🪖 Seatbelts & helmets"):
            if vehicle in ["Motorcycle", "Scooter"]:
                st.markdown("""
                - Wear a properly fitted, certified helmet and secure the chin strap.
                - Ensure your passenger wears a helmet too.
                - Wear protective clothing and suitable footwear.
                """)
            else:
                st.markdown("""
                - Fasten your seatbelt before moving.
                - Ensure all passengers wear seatbelts.
                - Use suitable child restraints when needed.
                """)

        with st.expander("💡 Lights & visibility"):
            if weather == "Foggy" or visibility == "Low":
                st.markdown("""
                - Use low-beam headlights and fog lamps if fitted.
                - Avoid high beams in fog.
                - Keep windows clear and use demisters.
                - If visibility becomes dangerously poor, stop somewhere safe away from traffic.
                """)
            elif weather == "Rainy":
                st.markdown("""
                - Use headlights when visibility is reduced.
                - Check wipers, lights, and indicators.
                - Keep windows clear.
                """)
            else:
                st.markdown("""
                - Check headlights, brake lights, and indicators.
                - Signal before turning or changing lanes.
                - Keep mirrors and windscreens clean.
                """)

        with st.expander("✅ Before you start"):
            st.markdown("""
            - Check tyres, brakes, and mirrors.
            - Never use a phone while driving.
            - Never drive under the influence of alcohol or drugs.
            - Rest before travelling if tired.
            - Follow traffic signs and instructions from authorities.
            """)

        st.markdown(
            """
            <div class="tip-card" style="text-align:center;border-color:#247d75">
                <div style="font-size:24px">🛡️</div>
                <strong style="color:#65e9bb">HAVE A SAFE JOURNEY!</strong>
                <p style="color:#bed1e4;margin-bottom:0">
                    Stay alert. Protect every passenger. Make every journey safer.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "Limitations: this version uses predefined demonstration rules. "
            "It does not use live route, weather, or traffic data and is not "
            "a validated prediction of actual accidents. Locations are shown "
            "for reference only. The animated meter represents the rule-based "
            "condition score, not the probability of a crash."
        )

st.markdown("""
<div class="footer">
    ROADSAFE AI · ROAD SAFETY AWARENESS PROJECT<br>
    TECHNOLOGY FOR SAFER JOURNEYS
</div>
""", unsafe_allow_html=True)
