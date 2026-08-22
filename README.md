# Risk-Adjusted Order Value — deliverables

1. **risk_modelling_analysis.ipynb** — main deliverable. Run cell-by-cell (or Kernel > Restart & Run All).
   Contains Part 1 (EDA), Part 2 (modelling: loss classifier, severity regressor, expected loss,
   expert-review queue), and Part 3 (written answers on sparsity, trust, and decision-making).
   Running it end-to-end regenerates the .joblib model files and .csv artefacts the Streamlit app needs.

2. **streamlit_app.py** — interactive dashboard. Run with:
   ```
   pip install -r requirements.txt
   streamlit run streamlit_app.py
   ```
   Needs to sit in the same folder as the .joblib/.csv artefacts produced by the notebook (already included
   here, but re-run the notebook first if you change the data or modelling code).

3. **orders.csv** — the original dataset, included for convenience/reproducibility.

4. **loss_classifier.joblib, severity_regressor.joblib, orders_scored.csv, expert_review_queue.csv,
   loss_type_medians.csv** — model artefacts produced by the notebook and consumed by the Streamlit app.
