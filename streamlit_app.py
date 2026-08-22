import pathlib

import numpy as np
import pandas as pd
import joblib
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import sklearn.compose._column_transformer
import types
import sklearn.compose._column_transformer

st.set_page_config(page_title="OrderGuard", layout="wide", page_icon="📦")


# FORCED COMPATIBILITY PATCH: Define and inject the missing legacy class globally
class _RemainderColsList(list): 
    pass

# Bind the class back into the module's attribute list
sklearn.compose._column_transformer._RemainderColsList = _RemainderColsList

# Inject it straight into the global execution registry so pickle can find it anywhere
sys.modules['sklearn.compose._column_transformer._RemainderColsList'] = _RemainderColsList
    
# Direct, high-speed path configuration targeting the results subfolder
RESULTS_DIR = pathlib.Path(__file__).parent.resolve() / "results"
DATA_DIR = RESULTS_DIR

@st.cache_resource
def load_models():
    """Directly loads binary models from the results folder."""
    clf = joblib.load(RESULTS_DIR / "loss_classifier.joblib")
    reg = joblib.load(RESULTS_DIR / "severity_regressor.joblib")
    return clf, reg

@st.cache_data
def load_data():
    """Directly loads data frameworks from the results folder."""
    scored = pd.read_csv(RESULTS_DIR / "orders_scored.csv")
    queue = pd.read_csv(RESULTS_DIR / "expert_review_queue.csv")
    type_medians = pd.read_csv(RESULTS_DIR / "loss_type_medians.csv", index_col=0).squeeze('columns')
    return scored, queue, type_medians




missing_files = [f for f in ["loss_classifier.joblib", "severity_regressor.joblib",
                              "orders_scored.csv", "expert_review_queue.csv", "loss_type_medians.csv"]
                  if not (DATA_DIR / f).exists()]
if missing_files:
    st.error(
        "Missing model artefacts: " + ", ".join(missing_files) +
        ".\n\nRun `TeleShop_Intelligence.ipynb` end-to-end first — its last cells save "
        "these files into the same folder as this app."
    )
    st.stop()

clf, reg = load_models()
scored_df, expert_queue, type_medians = load_data()

RISK_MAP = {"low": 0, "medium": 1, "high": 2}
FEATURE_COLS = ["order_value_usd", "buyer_tenure_yrs", "payment_terms_days",
                 "rep_confidence_score", "route_risk_ordinal", "buyer_region", "product_category"]

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
st.sidebar.title("📦 OrderGuard")
st.sidebar.caption("Your Deal Companion - Analyse Order Risks & Adjusted Values")

page = st.sidebar.radio(
    "View",
    ["Score a new order", "Portfolio dashboard", "Expert review queue", "Model notes & limitations"],
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "See 'Model notes & limitations' before making decisions with this tool."
    "Development and design: Navid Bin Ahmed, 2026"
)

# ---------------------------------------------------------------------------
# Shared scoring function
# ---------------------------------------------------------------------------
def score_order(order_value, buyer_tenure, payment_terms, rep_confidence, route_risk, buyer_region, product_category):
    X = pd.DataFrame([{
        "order_value_usd": order_value,
        "buyer_tenure_yrs": buyer_tenure,
        "payment_terms_days": payment_terms,
        "rep_confidence_score": rep_confidence,
        "route_risk_ordinal": RISK_MAP[route_risk],
        "buyer_region": buyer_region,
        "product_category": product_category,
    }])[FEATURE_COLS]
    proba = clf.predict_proba(X)[0, 1]
    severity = np.expm1(reg.predict(X)[0])
    expected_loss = proba * severity
    risk_adjusted_value = order_value - expected_loss
    return proba, severity, expected_loss, risk_adjusted_value


# ---------------------------------------------------------------------------
# PAGE 1 — Score a new order
# ---------------------------------------------------------------------------
if page == "Score a new order":
    st.title("Score a new order")
    st.caption("Enter order details to get a loss probability, an expected severity, and a risk-adjusted value.")

    col1, col2 = st.columns(2)
    with col1:
        order_value = st.number_input("Order value (USD)", min_value=100.0, max_value=200000.0, value=10000.0, step=100.0)
        buyer_tenure = st.slider("Buyer tenure (years)", 0.0, 21.0, 3.0, 0.1)
        payment_terms = st.selectbox("Payment terms (days)", [0, 30, 60, 90], index=1)
        product_category = st.selectbox("Product category", sorted(scored_df["product_category"].unique()))
    with col2:
        route_risk = st.selectbox("Route risk flag", ["low", "medium", "high"], index=0)
        buyer_region = st.selectbox("Buyer region", sorted([r for r in scored_df["buyer_region"].unique() if r != "Unknown"]) + ["Unknown"])
        rep_confidence = st.slider(
            "Rep confidence score (0-1)", 0.0, 1.0, 0.5, 0.01,
            help="Recorded by the sales rep at deal time. Its exact meaning is undocumented "
                 "in the source data — treat as a weak signal, not a certainty (see Model notes).",
        )

    if st.button("Score this order", type="primary"):
        proba, severity, expected_loss, rav = score_order(
            order_value, buyer_tenure, payment_terms, rep_confidence, route_risk, buyer_region, product_category
        )

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("P(loss)", f"{proba:.1%}")
        m2.metric("Expected severity if loss occurs", f"${severity:,.0f}")
        m3.metric("Expected loss", f"${expected_loss:,.0f}")
        m4.metric("Risk-adjusted value", f"${rav:,.0f}", delta=f"-${expected_loss:,.0f} vs face value")

        # simple traffic-light framing, deliberately NOT an auto-decline recommendation
        if proba < 0.10:
            st.success("Low flagged risk. Standard handling.")
        elif proba < 0.25:
            st.warning("Moderate flagged risk. Consider tighter payment terms or route review rather than declining.")
        else:
            st.error("️️️⚠️ WARNING: Elevated flagged risk. Recommend human underwriting review before proceeding — "
                     "not an automatic decline.")

        st.caption(
            "This score reflects patterns in historically **approved** deals only (see Model notes: Trust). "
            "It is a triage aid, not a ground-truth risk certificate — especially for deals unlike anything "
            "reps have historically written."
        )

    st.markdown("---")
    st.subheader("Where does this order sit versus history?")
    fig = px.scatter(
        scored_df, x="order_value_usd", y="expected_loss", color=scored_df["loss_recorded"].map({0: "No loss", 1: "Loss"}),
        color_discrete_map={"No loss": "#4C72B0", "Loss": "#C44E52"}, opacity=0.55,
        labels={"order_value_usd": "Order value (USD)", "expected_loss": "Model expected loss (USD)", "color": "Actual outcome"},
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
# PAGE 2 — Portfolio dashboard
# ---------------------------------------------------------------------------
elif page == "Portfolio dashboard":
    st.title("Portfolio dashboard")
    st.caption("All 1,400 historical orders, scored by the model. Use filters to slice by segment.")

    c1, c2, c3 = st.columns(3)
    cat_filter = c1.multiselect("Product category", sorted(scored_df["product_category"].unique()),
                                 default=sorted(scored_df["product_category"].unique()))
    region_filter = c2.multiselect("Buyer region", sorted(scored_df["buyer_region"].unique()),
                                    default=sorted(scored_df["buyer_region"].unique()))
    risk_filter = c3.multiselect("Route risk", ["low", "medium", "high"], default=["low", "medium", "high"])

    f = scored_df[
        scored_df["product_category"].isin(cat_filter)
        & scored_df["buyer_region"].isin(region_filter)
        & scored_df["route_risk_flag"].isin(risk_filter)
    ]

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Orders", f"{len(f):,}")
    k2.metric("Actual loss rate", f"{f['loss_recorded'].mean():.1%}")
    k3.metric("Total order value", f"${f['order_value_usd'].sum():,.0f}")
    k4.metric("Total model expected loss", f"${f['expected_loss'].sum():,.0f}")

    st.markdown("#### Expected loss by segment")
    seg_col = st.selectbox("Segment by", ["product_category", "buyer_region", "route_risk_flag", "payment_terms_days"])
    seg = f.groupby(seg_col).agg(
        n=("order_id", "count"),
        actual_loss_rate=("loss_recorded", "mean"),
        avg_pred_proba=("pred_loss_proba", "mean"),
        total_expected_loss=("expected_loss", "sum"),
        total_order_value=("order_value_usd", "sum"),
    ).reset_index()
    seg["expected_loss_pct_of_value"] = seg["total_expected_loss"] / seg["total_order_value"]

    fig1 = px.bar(seg, x=seg_col, y=["actual_loss_rate", "avg_pred_proba"], barmode="group",
                   labels={"value": "Rate", "variable": ""}, height=380,
                   title="Actual loss rate vs model's average predicted probability")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(seg, x=seg_col, y="expected_loss_pct_of_value", height=380,
                   labels={"expected_loss_pct_of_value": "Expected loss as % of order value"},
                   title="Where is risk-adjusted value being eroded?")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### Loss type breakdown (severity)")
    lt = scored_df[scored_df.loss_recorded == 1]
    fig3 = px.box(lt, x="loss_type", y="loss_amount_usd", points="all", height=420,
                   title="Loss amount by type — note the 'default' tail")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("#### Full scored table")
    st.dataframe(
        f[["order_id", "ship_date", "product_category", "buyer_region", "order_value_usd",
           "route_risk_flag", "pred_loss_proba", "pred_severity_if_loss", "expected_loss", "risk_adjusted_value"]]
        .sort_values("expected_loss", ascending=False)
        .style.format({
            "order_value_usd": "${:,.0f}", "pred_loss_proba": "{:.1%}",
            "pred_severity_if_loss": "${:,.0f}", "expected_loss": "${:,.0f}", "risk_adjusted_value": "${:,.0f}",
        }),
        use_container_width=True, height=400,
    )


# ---------------------------------------------------------------------------
# PAGE 3 — Expert review queue
# ---------------------------------------------------------------------------
elif page == "Expert review queue":
    st.title("Expert review queue")
    st.caption(
        "Orders where the loss label is confirmed-but-estimated, or where informal notes hint at a "
        "near-miss that was never formally logged as a loss. Built for a human reviewer, not for silent "
        "model consumption — see Notebook §2.6."
    )

    tiers = expert_queue["confidence_tier"].unique().tolist()
    tier_filter = st.multiselect("Confidence tier", tiers, default=tiers)
    q = expert_queue[expert_queue["confidence_tier"].isin(tier_filter)]

    st.metric("Records awaiting review", f"{len(q):,}", help="Out of 1,400 total orders")

    tier_counts = expert_queue["confidence_tier"].value_counts().reset_index()
    tier_counts.columns = ["confidence_tier", "count"]
    fig = px.bar(tier_counts, x="count", y="confidence_tier", orientation="h", height=280)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(q, use_container_width=True, height=420)

    st.download_button(
        "Download review queue (CSV)",
        data=q.to_csv(index=False).encode("utf-8"),
        file_name="expert_review_queue.csv",
        mime="text/csv",
    )


# ---------------------------------------------------------------------------
# PAGE 4 — Model notes & limitations
# ---------------------------------------------------------------------------
else:
    st.title("Model notes & limitations")
    st.markdown("""
### What this tool does
Two models, trained on 1,400 historical shipped orders:
- **Classifier** → P(order incurs a loss)
- **Severity regressor** (trained only on the ~210 loss events) → expected loss size *if* a loss occurs

Combined into **expected loss = P(loss) × severity**, and **risk-adjusted value = order value − expected loss**.

### What it can't do
- **Sparse tail events.** Only 12 `default`-type losses exist in the training data (5 with a logged dollar
  amount). No model — this one included — can reliably estimate default risk for an individual order from
  that few examples. Treat any default-adjacent flag as a prompt for human underwriting, not a probability
  to trust at face value.
- **Selection bias.** Every training order was already approved by a sales rep at a price and term the rep
  chose. The model has only ever seen the "approved" region of the deal space — it cannot validly speak to
  deals very different from historical norms (new regions, unusually large orders, unfamiliar buyer profiles).
- **Modest discrimination.** Cross-validated PR-AUC for the loss classifier is well above the no-skill
  baseline but far from perfect separation — expect real false positives and false negatives at any
  threshold.
- **Rough severity estimates**, dragged around by a handful of very large historical losses. Good for sizing
  typical small-to-medium losses; not for pricing a specific worst-case default.

### How we recommend using it
- As an **input to prioritisation and pricing/terms decisions** (shorter payment terms, route scrutiny,
  human underwriting for high-value + high-risk orders) — **not** as an automatic decline rule.
- Alongside buyer-relevance scores, so the business can test — with a genuine held-out comparison — whether
  ranking by risk-adjusted value actually improves outcomes over ranking by relevance alone.
- With the expert review queue kept in the loop for the subset of records with low-confidence labels..
""")
