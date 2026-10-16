
import streamlit as st

st.set_page_config(
    page_title="ROADSAFE AI",
    page_icon="🚦",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1100px;
}
div[data-testid="stMetric"] {
    background: rgba(128,128,128,0.08);
    border: 1px solid rgba(128,128,128,0.25);
    padding: 18px;
    border-radius: 14px;
}
div[data-testid="stExpander"] {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("🚦 ROADSAFE AI")
st.caption("ACCIDENT RISK ASSESSMENT • ROAD SAFETY ADVISORY")
st.write("Plan your journey. Assess conditions. Travel safely.")

st.divider()

# JOURNEY DETAILS
st.subheader("📍 Your Journey")

c1, c2 = st.columns(2)

with c1:
    start_location = st.text_input(
        "Starting Location",
        placeholder="e.g. Kochi"
    )

with c2:
    destination = st.text_input(
        "Destination",
        placeholder="e.g. Thrissur"
    )

# ROAD CONDITIONS
st.subheader("🌦️ Road & Travel Conditions")

c1, c2, c3 = st.columns(3)

with c1:
    weather = st.selectbox(
        "Weather",
        ["Clear", "Cloudy", "Rainy", "Foggy"]
    )

    road = st.selectbox(
        "Road Condition",
        ["Dry", "Damp", "Wet"]
    )

with c2:
    traffic = st.selectbox(
        "Traffic Density",
        ["Low", "Medium", "High"]
    )

    visibility = st.selectbox(
        "Visibility",
        ["High", "Medium", "Low"]
    )

with c3:
    vehicle = st.selectbox(
        "Vehicle Type",
        ["Car", "Motorcycle", "Scooter", "Bus", "Truck"]
    )

analyse = st.button(
    "🔍 ANALYSE ROAD RISK",
    type="primary",
    use_container_width=True
)

if analyse:
    if not start_location.strip() or not destination.strip():
        st.warning("Please enter both your starting location and destination.")

    else:
        # DEMONSTRATION SCORING RULES
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
            colour = "#dc2626"
            symbol = "🔴"
            summary = "Extra caution required"
        elif score >= 3:
            risk = "MODERATE"
            colour = "#d97706"
            symbol = "🟠"
            summary = "Drive with increased caution"
        else:
            risk = "LOW"
            colour = "#16a34a"
            symbol = "🟢"
            summary = "Continue to stay alert"

        st.divider()
        st.header("📊 Your Risk Assessment")

        # PROMINENT RISK RESULT
        st.markdown(
            f"""
            <div style="
                background:{colour}14;
                border:2px solid {colour};
                border-radius:18px;
                padding:24px;
                text-align:center;
                margin-bottom:16px;
            ">
                <div style="font-size:18px;">ESTIMATED RISK CATEGORY</div>
                <div style="font-size:38px;font-weight:800;color:{colour};">
                    {symbol} {risk}
                </div>
                <div style="font-size:17px;">{summary}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ROUTE SUMMARY
        st.markdown("### 🗺️ Journey Summary")

        c1, c2 = st.columns([2, 1])

        with c1:
            st.info(
                f"**FROM**\n\n{start_location}\n\n"
                f"**TO**\n\n{destination}"
            )

        with c2:
            st.metric("Vehicle", vehicle)
            st.metric("Condition Score", f"{score}/8")

        st.caption(
            "The condition score is an internal demonstration score, "
            "not a measured probability of an accident."
        )

        # PRIORITY ADVICE
        st.markdown("### ⚠️ Key Recommendations")

        priorities = []

        if weather in ["Rainy", "Foggy"] or road == "Wet":
            priorities.append(
                "🌧️ **Slow down:** reduce speed gradually and "
                "increase your following distance."
            )

        if visibility == "Low" or weather == "Foggy":
            priorities.append(
                "💡 **Improve visibility:** use low-beam headlights "
                "and avoid high beams in fog."
            )

        if traffic == "High":
            priorities.append(
                "🚗 **Heavy traffic:** avoid sudden lane changes "
                "and maintain a safe gap."
            )

        if road == "Wet":
            priorities.append(
                "🛣️ **Wet road:** brake gently and avoid sudden turns."
            )

        if not priorities:
            priorities.append(
                "✅ Follow speed limits, keep a safe distance, "
                "and remain alert."
            )

        for item in priorities:
            st.markdown(f"- {item}")

        # EXPANDABLE ADVICE SECTIONS
        st.markdown("### 🛡️ Safety Checklist")

        with st.expander("🚦 Speed & Safe Distance", expanded=True):
            st.write(
                "- Follow posted speed limits; drive slower when "
                "weather, visibility or traffic requires it.\n"
                "- Increase the following distance in rain or on wet roads.\n"
                "- Avoid sudden braking, sharp turns and risky overtaking."
            )

        with st.expander("🪖 Seatbelts & Helmets"):
            if vehicle in ["Motorcycle", "Scooter"]:
                st.write(
                    "- Wear a properly fitted, certified helmet.\n"
                    "- Fasten the chin strap securely.\n"
                    "- Ensure your passenger wears a helmet too.\n"
                    "- Wear protective clothing and suitable footwear."
                )
            else:
                st.write(
                    "- Fasten your seatbelt before moving.\n"
                    "- Ensure all passengers wear seatbelts.\n"
                    "- Use appropriate child restraints when needed."
                )

        with st.expander("💡 Lights & Visibility"):
            if weather == "Foggy" or visibility == "Low":
                st.write(
                    "- Use low-beam headlights and fog lamps if fitted.\n"
                    "- Avoid high beams in fog.\n"
                    "- Use demisters and keep windows clear.\n"
                    "- If visibility becomes dangerously poor, stop "
                    "somewhere safe away from moving traffic."
                )
            elif weather == "Rainy":
                st.write(
                    "- Use headlights when visibility is reduced.\n"
                    "- Check wipers, headlights, brake lights and indicators.\n"
                    "- Keep windows clear."
                )
            else:
                st.write(
                    "- Check headlights, brake lights and indicators.\n"
                    "- Signal before turning or changing lanes.\n"
                    "- Keep mirrors and windscreens clean."
                )

        with st.expander("✅ Before You Start"):
            st.write(
                "- Check tyres, brakes and mirrors.\n"
                "- Never use a phone while driving.\n"
                "- Never drive under the influence of alcohol or drugs.\n"
                "- Rest before travelling if tired.\n"
                "- Follow traffic signs and instructions from authorities."
            )

        st.success(
            "🌟 HAVE A SAFE AND HAPPY JOURNEY! 🌟\n\n"
            "Stay alert. Protect every passenger. Make every journey safer."
        )

        st.caption(
            "This assessment uses predefined rules applied to your selected "
            "conditions. It does not use live route, weather or traffic data, "
            "and is not a validated prediction of actual accidents. "
            "The entered locations are displayed for journey reference only."
        )
