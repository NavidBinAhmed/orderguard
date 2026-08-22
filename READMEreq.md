# Take-Home Technical Exercise
### Research Scientist, Machine Learning (Risk Modelling and Decision Systems)

**What to submit:** A single Jupyter notebook (or a short report plus code) that we can read top-to-bottom, with your reasoning written inline. Reproducibility matters — we should be able to re-run it. Any language is acceptable; Python is preferred.

**A note on tools:** You may use whatever libraries and, if you wish, AI assistants you would normally use — we care about your judgement, not whether you memorised an API. If you use an AI tool, we would appreciate a sentence on where it helped and where you overrode it, because knowing when not to trust a suggestion is part of the job.

---

## Context

This role is about estimating the **true, risk-adjusted value of a business deal** when the information needed to do so is sparse and unevenly recorded. To let you work on the flavour of that problem without any confidential data, we have created a small **synthetic dataset** of completed export orders. Each row is one order that shipped; some incurred a financial loss after the sale (a dispute, a return, a late or missed payment, extra freight cost), and most did not.

The dataset and its column descriptions are in the accompanying file `orders.csv` and `data_dictionary.md`. It is deliberately small and deliberately imperfect.

---

## Part 1: Understand the data

Explore the dataset and tell us what you find. We are specifically interested in whether you notice:

- how often losses actually occur, and how their sizes are distributed;
- any data-quality problems, missing fields, or fields that look unreliable;
- anything about how the data was generated that would affect how much you can trust it.

Write down what you observe, in plain language, as if briefing a colleague.

## Part 2: Model something useful

Build a model, or models, that would help the business decide which future orders are risky. You have latitude in exactly what you predict — that choice, and your justification for it, is part of what we are assessing. You might, for example, model the *probability* that an order incurs a loss, the *size* of the loss if one occurs, or an *expected loss* that combines both. Tell us why you framed it the way you did.

We are not looking for a high accuracy number. We are looking for:

- a modelling choice that fits the data you actually have, not the data you wish you had;
- sensible handling of the fact that losses are rare and vary a lot in size;
- an evaluation that measures something meaningful, and an honest read of how well it worked;
- clear acknowledgement of what your model cannot do or where it is likely to be unreliable.

If you try something and it does not work, keep it in and tell us why — that is useful signal, not a failure.

## Part 3: Judgement and communication (roughly 1 hour)

Answer these three questions in detail:

1. **Sparsity.** Suppose the single most expensive category of loss (say, a major customer default) has only happened five or six times in the whole dataset, but when it happens it dwarfs everything else. How would you approach estimating the risk of it, given you have almost no examples? What would you *not* do?

2. **Trust.** These orders were historically approved by human sales staff who decided which deals to pursue and at what price. Does that affect what your model can validly learn or claim from this data? If so, how, and what would you do about it?

3. **Decision.** Your model produces a risk estimate. The business wants to use it to decide which orders to prioritise. Would you use it to *drop* risky orders from consideration, or in some other way? Briefly justify your recommendation.

---

## What we are assessing

To be transparent, here is roughly how we read submissions. There are no hidden traps and no single "right" answer to Parts 2 or 3.

| Dimension | What a strong submission shows |
|---|---|
| **Problem framing** | Chooses a sensible target and objective, and explains why, rather than reflexively fitting a classifier. |
| **Reasoning under sparsity** | Recognises rare events and heavy tails as the central difficulty and responds to them thoughtfully. |
| **Statistical judgement** | Understands uncertainty; does not oversell a result; picks evaluation metrics that mean something. |
| **Honesty** | States limitations plainly; distinguishes what the data can and cannot support. |
| **Communication** | We can follow the reasoning end-to-end without reverse-engineering the code. |

---

## Practical details


- If anything is ambiguous, make a reasonable assumption, state it, and continue. Refrain from emailing us for clarification, as handling ambiguity is part of the exercise.
- Return your submission within **7 days** of receiving it.

We know a take-home is a real ask on your time, and we appreciate it. If you reach the interview stage, we will spend most of that conversation discussing the choices you made here, so there is no need to polish, as we want to see how you think.