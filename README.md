## Order Guard - Your Trusted Deal Companion
This tool encompasses the research, training and development of a `dual-ML algorithm based model`, that enables businesses to predict and compute the tentative loss for taking predictive measures, following a sparse-rarely orccuring target events, i.e., loss.


### Authors:
- `Stakeholder`: TeleShop HK Ltd.
- `Dev`: Navid Bin Ahmed
- 23-Aug 2026

#### Link:
App : [Link](orderguard.streamlit.app)


#### Tools Used:
- Python 3
- Jupyter Notebook
- GitHub
- Stremlit


### How to Use the Dashboard
- Predicts loss amount and adjusted-value for the given inputs, along with the expert review queue kept in the loop for the subset of records with low-confidence labels..
- As an input to prioritisation and pricing/terms decisions (shorter payment terms, route scrutiny, human underwriting for high-value + high-risk orders) — not as an automatic decline rule.
- Alongside buyer-relevance scores, so the business can test — with a genuine held-out comparison — whether ranking by risk-adjusted value actually improves outcomes over ranking by relevance alone.


### What this Tool does
Two models, trained on historical shipped orders:

- `Classifier` → P(order incurs a loss)
- `Severity regressor` → expected loss size if a loss occurs

- `Combined into expected loss` = P(loss) × severity, and risk-adjusted value = order value − expected loss.


#### Confidentiality