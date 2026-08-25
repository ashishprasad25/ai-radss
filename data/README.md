# AI-RADSS — AI Readiness Assessment and Decision Support System

An interactive, open-source decision support system that assesses organisational readiness for AI adoption across five dimensions and delivers a quantified readiness score, tier classification, and prioritised strategic recommendations.

Developed as the Product Development dissertation project for BUSI 1783 — Business Analytics Project, MSc Business Analytics, University of Greenwich.

**Live application:** https://ai-radss-rs7idqqmuls4i4hqw8tucp.streamlit.app/

## What it does

1. **Assessment** — a 25-item questionnaire (5-point Likert scale) across five readiness dimensions: Data readiness, Technology infrastructure, Human capital, Organisational culture, and Strategic alignment.
2. **Scoring** — dimension scores (0–100) are combined into a weighted composite AI Readiness Score (weights: 25/20/20/20/15, justified in Chapter 3 of the dissertation).
3. **Classification** — transparent rule-based thresholds assign one of four readiness tiers: Nascent (0–25), Developing (26–50), Advanced (51–75), AI-Ready (76–100).
4. **Recommendations** — a rule-based engine maps the lowest-scoring dimensions to prioritised, literature-derived strategic actions.
5. **Reporting** — results are visualised (radar chart, dimension bars) and exportable as a text report. No responses are stored, in line with UK GDPR.

## Theoretical grounding

The framework synthesises the Technology–Organisation–Environment framework (Tornatzky and Fleischer, 1990), organisational AI readiness factors (Jöhnk, Weißert and Wyrtki, 2021), AI capability measurement (Mikalef and Gupta, 2021), data readiness as a distinct factor (Pumplun, Tauchert and Heidt, 2019), self-assessment scoring (Holmström, 2022), and maturity model design methodology (Becker, Knackstedt and Pöppelbuß, 2009).

## Repository contents

| File | Description |
|---|---|
| `app.py` | Complete application source code (Streamlit) |
| `requirements.txt` | Dependency specification |
| `analysis.ipynb` | Compiled notebook computing the usability evaluation results reported in Chapter 5 |
| `data/sus_responses_anonymised.csv` | Anonymised usability evaluation dataset (10 participants) |
| `sus_analysis.png` | Output visualisation from the analysis notebook |

## Data source

The dataset in `data/` contains anonymised responses from the usability evaluation described in Chapter 5 of the dissertation. Ten participants completed the live assessment and then a nine-item adaptation of the System Usability Scale (Brooke, 1996) via an anonymous online form. Participation was voluntary and preceded by informed consent. No personally identifiable information was collected or retained; the dataset contains only ordinal ratings and a self-reported familiarity category. No Kaggle datasets were used at any stage of this project.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app opens in your browser at http://localhost:8501

To reproduce the usability analysis:

```bash
jupyter notebook analysis.ipynb
```

## Author

Ashish Chaurasiya — MSc Business Analytics, University of Greenwich
