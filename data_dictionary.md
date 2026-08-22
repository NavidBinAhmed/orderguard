# Data Dictionary — `orders.csv`

This is a **synthetic** dataset created for this exercise. It does not contain any real Teleshop data. It is designed to resemble the *shape* of the problem this role works on: completed export orders, a minority of which incurred a financial loss after the sale, recorded imperfectly.

Each row is one order that shipped.

| Column | Type | Description |
|---|---|---|
| `order_id` | integer | Unique identifier for the order. |
| `ship_date` | date | Date the order shipped. |
| `buyer_region` | category | Buyer's region. Occasionally missing. |
| `product_category` | category | One of `home_appliance`, `beauty`, `cleaning`, `pet_care`. |
| `order_value_usd` | float | Gross value of the order in USD. |
| `buyer_tenure_yrs` | float | How long this buyer has traded with the company, in years. |
| `new_buyer` | 0/1 | Flag: 1 if this is effectively a new buyer (short tenure). |
| `payment_terms_days` | integer | Credit terms granted: 0 (prepaid), 30, 60, or 90 days. |
| `route_risk_flag` | category | Internal shipping-route risk label: `low`, `medium`, `high`. |
| `rep_confidence_score` | float | A score (0–1) recorded by the sales representative at the time of the deal, reflecting their own confidence in the order. Its exact meaning is not formally documented. |
| `loss_recorded` | 0/1 | 1 if a financial loss has been recorded against this order. |
| `loss_type` | category | Type of loss if recorded: `freight_overrun`, `return`, `dispute`, `late_payment`, `default`, or `none`. |
| `loss_amount_usd` | float | Recorded size of the loss in USD. May be missing even when a loss is recorded (the figure was not always logged). |
| `days_to_loss_recorded` | float | Days between shipment and the loss being recorded. Blank if no loss recorded. |
| `notes` | text | Free-text note from the accounts or shipping team, where one exists. Frequently blank. Occasionally present on orders with no recorded loss. |

## Things worth knowing

- The data was assembled from internal records that were **not designed for analysis**. Some fields are more reliable than others.
- A recorded loss reflects what had been logged **as of the time the data was extracted**. Orders ship on different dates, so different orders have been "observed" for different lengths of time.
- Losses vary enormously in size depending on type.
- You are not expected to use every column. Part of the exercise is deciding what to rely on.

If something about the data seems off or inconvenient, that is not a mistake in the file — it is part of what we are asking you to navigate. Note it and proceed.
