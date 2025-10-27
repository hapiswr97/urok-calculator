import streamlit as st
import json

st.set_page_config(page_title="ROK Resource Tracker", page_icon="💎", layout="centered")

st.title("💎 Rise of Kingdoms Resource Tracker v2")

# --- Initialize session state ---

if "customers" not in st.session_state:
    st.session_state.customers = {}
if "current_customer" not in st.session_state:
    st.session_state.current_customer = None

# --- Customer selection ---

st.subheader("👥 Customer Session")

col1, col2 = st.columns([2, 1])
with col1:
customer_name = st.text_input("Customer name", placeholder="Enter customer name (e.g. Adit)")

with col2:
if st.button("➕ Add / Switch"):
if not customer_name.strip():
st.warning("Please enter a valid customer name.")
else:
if customer_name not in st.session_state.customers:
st.session_state.customers[customer_name] = {
"saved_states": {},
"before_selected": None,
"after_selected": None,
}
st.session_state.current_customer = customer_name
st.success(f"✅ Active customer: {customer_name}")

if not st.session_state.current_customer:
st.info("Select or create a customer to begin.")
st.stop()

customer = st.session_state.customers[st.session_state.current_customer]

st.markdown(f"### Active Customer: **{st.session_state.current_customer}**")

# --- Input Section ---

st.subheader("📥 Input Current State")

with st.form("input_form"):
gems_10 = st.number_input("10-Gems (from barbarians)", min_value=0, step=1)
gems_100 = st.number_input("100-Gems (from barbarians)", min_value=0, step=1)
inventory = st.number_input("Inventory Gems", min_value=0, step=1)
honor = st.number_input("Honor Points", min_value=0, step=1)
crystal = st.number_input("Crystals", min_value=0, step=1)

```
col1, col2 = st.columns(2)
with col1:
    save_before = st.form_submit_button("💾 Save as Before")
with col2:
    save_after = st.form_submit_button("💾 Save as After")

# Save data
if save_before:
    name = f"Before {len([k for k in customer['saved_states'] if k.startswith('Before')]) + 1}"
    customer["saved_states"][name] = {
        "gems_10": gems_10,
        "gems_100": gems_100,
        "inventory": inventory,
        "honor": honor,
        "crystal": crystal,
    }
    st.success(f"Saved {name} for {st.session_state.current_customer}")
if save_after:
    name = f"After {len([k for k in customer['saved_states'] if k.startswith('After')]) + 1}"
    customer["saved_states"][name] = {
        "gems_10": gems_10,
        "gems_100": gems_100,
        "inventory": inventory,
        "honor": honor,
        "crystal": crystal,
    }
    st.success(f"Saved {name} for {st.session_state.current_customer}")
```

# --- Selection Section ---

st.subheader("📊 Compare States")

before_keys = [k for k in customer["saved_states"] if k.startswith("Before")]
after_keys = [k for k in customer["saved_states"] if k.startswith("After")]

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
before = customer["saved_states"][before_choice]
after = customer["saved_states"][after_choice]

```
    differences = {k: after[k] - before[k] for k in before.keys()}
    monster_gems = (differences["gems_10"] * 10) + (differences["gems_100"] * 100)
    total_gems = differences["inventory"] + monster_gems

    st.markdown("### 📈 Resource Changes:")
    st.write(f"10-Gems: {differences['gems_10']} → **{differences['gems_10'] * 10} gems from barbarians**")
    st.write(f"100-Gems: {differences['gems_100']} → **{differences['gems_100'] * 100} gems from barbarians**")
    st.write(f"Inventory Gems: **{differences['inventory']}**")
    st.write(f"Honor Points: **{differences['honor']}**")
    st.write(f"Crystals: **{differences['crystal']}**")

    st.markdown("---")
    st.markdown(f"### 💰 Total Gems Gained: **{total_gems:,}**")
    st.caption(f"(Includes {monster_gems:,} gems from barbarians)")
```

# --- Export all data ---

st.markdown("---")
if st.download_button(
"📤 Export All Data (JSON)",
data=json.dumps(st.session_state.customers, indent=2),
file_name="rok_service_data.json",
mime="application/json",
):
st.success("Data exported successfully!")
