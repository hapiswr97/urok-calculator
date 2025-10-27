import streamlit as st

st.set_page_config(page_title="ROK Resource Tracker", page_icon="💎", layout="centered")

st.title("💎 Rise of Kingdoms Resource Tracker")

# --- Session State Setup ---
if "saved_states" not in st.session_state:
    st.session_state.saved_states = {}

# --- Input Section ---
st.subheader("📥 Input Current State")

with st.form("input_form"):
    gems_10 = st.number_input("10-Gems (from barbarians)", min_value=0, step=1)
    gems_100 = st.number_input("100-Gems (from barbarians)", min_value=0, step=1)
    inventory = st.number_input("Inventory Gems", min_value=0, step=1)
    honor = st.number_input("Honor Points", min_value=0, step=1)
    crystal = st.number_input("Crystals", min_value=0, step=1)

    col1, col2 = st.columns(2)
    with col1:
        save_before = st.form_submit_button("💾 Save as Before")
    with col2:
        save_after = st.form_submit_button("💾 Save as After")

    # Save data logic
    if save_before:
        name = f"Before {len([k for k in st.session_state.saved_states if k.startswith('Before')]) + 1}"
        st.session_state.saved_states[name] = {
            "gems_10": gems_10,
            "gems_100": gems_100,
            "inventory": inventory,
            "honor": honor,
            "crystal": crystal,
        }
        st.success(f"✅ Saved as {name}")

    if save_after:
        name = f"After {len([k for k in st.session_state.saved_states if k.startswith('After')]) + 1}"
        st.session_state.saved_states[name] = {
            "gems_10": gems_10,
            "gems_100": gems_100,
            "inventory": inventory,
            "honor": honor,
            "crystal": crystal,
        }
        st.success(f"✅ Saved as {name}")

# --- Selection Section ---
st.subheader("📊 Select States to Compare")

before_keys = [k for k in st.session_state.saved_states if k.startswith("Before")]
after_keys = [k for k in st.session_state.saved_states if k.startswith("After")]

col1, col2 = st.columns(2)
with col1:
    before_choice = st.selectbox("Before State", options=before_keys)
with col2:
    after_choice = st.selectbox("After State", options=after_keys)

# --- Calculation ---
if st.button("⚙️ Calculate"):
    if not before_choice or not after_choice:
        st.error("Please select both Before and After states.")
    else:
        before = st.session_state.saved_states[before_choice]
        after = st.session_state.saved_states[after_choice]

        differences = {k: after[k] - before[k] for k in before.keys()}
        monster_gems = (differences["gems_10"] * 10) + (differences["gems_100"] * 100)
        total_gems = differences["inventory"] + monster_gems

        st.markdown("### 📈 Resource Changes:")
        st.write(f"10-Gems: {differences['gems_10']}  →  **{differences['gems_10'] * 10} gems from barbarians**")
        st.write(f"100-Gems: {differences['gems_100']}  →  **{differences['gems_100'] * 100} gems from barbarians**")
        st.write(f"Inventory Gems: **{differences['inventory']}**")
        st.write(f"Honor Points: **{differences['honor']}**")
        st.write(f"Crystals: **{differences['crystal']}**")

        st.markdown("---")
        st.markdown(f"### 💰 Total Gems Gained: **{total_gems:,}**")
        st.caption(f"(Includes {monster_gems:,} gems from barbarians)")
