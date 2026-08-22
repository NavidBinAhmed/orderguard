import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Risk-Adjusted Deal Valuation Engine", layout="wide")

# App Header
st.title("🛡️ Risk-Adjusted Valuation & Heavy-Tail Loss Dashboard")
st.markdown("""
This interface implements an enterprise **Two-Stage Hurdle Architecture** to mitigate high-severity tail exposures. 
It analyzes order risks dynamically and factors informal accounting adjustments via expert calibration layers.
""")

# Persistent State Initialization for Expert Adjustments
if 'expert_mod' not in st.session_state:
    st.session_state.expert_mod = 1.0

# Sidebar Context: Parameter Entry Layout
st.sidebar.header("📥 Live Deal Parametric Inputs")
order_val = st.sidebar.number_input("Order Value ($ USD)", min_value=1000, max_value=500000, value=45000, step=500)
buyer_tenure = st.sidebar.slider("Buyer Tenure (Years)", 0, 15, 3)
new_buyer_flag = st.sidebar.selectbox("New Buyer Profile?", ["No", "Yes"])
payment_terms = st.sidebar.selectbox("Payment Net Terms (Days)", [15, 30, 45, 60])
route_risk = st.sidebar.checkbox("Flagged Supply Route Transport Risk?")
# In your Streamlit app sidebar:
route_risk_selection = st.sidebar.selectbox("Route Risk Level", ["None", "Low", "Medium", "High"])

# Convert text selection to the exact numerical format the model expects:
app_route_mapping = {"None": 0, "Low": 1, "Medium": 2, "High": 3}
route_risk_input_encoded = app_route_mapping[route_risk_selection]

rep_score = st.sidebar.slider("Account Representative Confidence Score", 50.0, 100.0, 82.5)
has_informal_notes = st.sidebar.checkbox("Presence of informal warning records/notes?")

# Dummy Fitted Coefficients representing our Robust Training Runs
prob_base = 0.05 + (0.15 if route_risk else 0.0) + (0.10 if new_buyer_flag == "Yes" else 0.0) - (0.005 * buyer_tenure) + (0.08 if has_informal_notes else 0.0)
predicted_prob = max(0.01, min(0.99, prob_base))

base_loss_calc = order_val * (0.35 + (0.20 if route_risk else 0.0) - (0.01 * buyer_tenure))
predicted_severity = max(0.0, base_loss_calc)

# Expert Validation Panel
st.subheader("⚙️ Real-time Expert Adjustment & Verification Framework")
col_exp1, col_exp2 = st.columns(2)
with col_exp1:
    st.markdown("**Informal Record Audit Metrics:**")
    st.caption(f"Route Condition Status: {'⚠️ HIGH EXPOSURE' if route_risk else '✅ STABLE'}")
    st.caption(f"Correspondence Flagging Status: {'⚠️ RISK NOTE DETECTED' if has_informal_notes else '✅ CLEAR'}")
with col_exp2:
    multiplier = st.slider("Expert Scaling Override (Tail Shock Factor)", 0.5, 3.0, 1.0, step=0.1)
    st.session_state.expert_mod = multiplier

# Compute final metric risk positions
adjusted_severity = predicted_severity * st.session_state.expert_mod
expected_loss = predicted_prob * adjusted_severity
risk_adjusted_deal_value = order_val - expected_loss

# Metrics Banner Layout
st.markdown("---")
st.subheader("📊 Quantitative Deal Risk Telemetry")
m1, m2, m3, m4 = st.columns(4)
m1.metric(label="Loss Probability (Stage 1)", value=f"{predicted_prob:.1%}")
m2.metric(label="Estimated Severity (Stage 2)", value=f"${adjusted_severity:,.2f}")
m3.metric(label="Expected Economic Loss", value=f"${expected_loss:,.2f}", delta=f"${expected_loss - predicted_severity:,.2f} via override", delta_color="inverse")
m4.metric(label="Risk-Adjusted Contract Net Value", value=f"${risk_adjusted_deal_value:,.2f}")

# Business Action Scenarios Card Matrix
st.markdown("### 🚦 Operational Underwriting Recommendation")
if predicted_prob > 0.25 or adjusted_severity > (0.60 * order_val):
    st.error(f"❌ **REJECT OR RE-STRUCTURE DEAL:** The deal expected tail loss profile (${expected_loss:,.2f}) breaks normal operational tolerance standards. Require escrow deposits or collateralization.")
elif predicted_prob > 0.12:
    st.warning("⚠️ **CONDITIONAL APPROVAL:** Deal exposure is manageable but volatile. Shorten payment terms to Net 30 days and execute mandatory transaction auditing.")
else:
    st.success("✅ **STANDARD CLEARANCE:** Deal parameters sit within optimized historic operating profit boundaries.")

# Heavy-Tail Scenario Simulation Charting
st.markdown("---")
st.subheader("📈 Stress-Testing Value at Risk (VaR) Distribution Curve")
simulated_shocks = np.random.pareto(a=1.3, size=1000) * (adjusted_severity * 0.4)
sim_df = pd.DataFrame({"Simulated Tail Loss Scenario ($)": simulated_shocks})

fig = px.histogram(sim_df, x="Simulated Tail Loss Scenario ($)", nbins=50, title="Heavy-Tail Severity Extrapolation Simulation", color_discrete_sequence=['#EF553B'])
fig.add_vline(x=expected_loss, line_dash="dash", line_color="yellow", annotation_text="Expected Hurdle Loss Value")
fig.add_vline(x=adjusted_severity, line_dash="solid", line_color="red", annotation_text="Target Maximum Loss Limit")
st.plotly_chart(fig, use_container_width=None)

