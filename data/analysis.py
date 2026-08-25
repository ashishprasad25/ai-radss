"""
AI-RADSS Usability Analysis
BUSI 1783 - Business Analytics Project, University of Greenwich

Computes the usability evaluation results reported in Chapter 5 of the dissertation.

Instrument: nine-item adaptation of the System Usability Scale (Brooke, 1996).
The standard scale comprises ten alternately worded statements; the item concerning
intended frequency of use was inadvertently omitted from the deployed questionnaire.
The remaining nine items retain the standard alternating positive/negative structure.
Scores are computed by the standard procedure and scaled to the 0-100 range.

Data: data/sus_responses_anonymised.csv - ten participants, fully anonymised,
collected under informed consent. No personally identifiable information recorded.

Benchmark: Bangor, Kortum and Miller (2008) identify 68 as the threshold of
above-average usability.

Run with:  python analysis.py
"""

import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- load data
df = pd.read_csv('data/sus_responses_anonymised.csv')
print(f"Participants: {len(df)}\n")

# ------------------------------------------------------- instrument definition
# Positively worded items score as (rating - 1); negatively worded as (5 - rating).
ITEMS = [
    ('Q1_complex',       'N', 'I found the system unnecessarily complex.'),
    ('Q2_easy',          'P', 'I thought the system was easy to use.'),
    ('Q3_need_support',  'N', 'I would need the support of a technical person.'),
    ('Q4_integrated',    'P', 'The various functions were well integrated.'),
    ('Q5_learn_quickly', 'P', 'Most people would learn to use this very quickly.'),
    ('Q6_confident',     'P', 'I felt very confident using the system.'),
    ('Q7_cumbersome',    'N', 'I found the system very cumbersome to use.'),
    ('Q8_inconsistent',  'N', 'There was too much inconsistency in this system.'),
    ('Q9_learn_lot',     'N', 'I needed to learn a lot before I could get going.'),
]
MAX_RAW = len(ITEMS) * 4  # 36

# ------------------------------------------------------- per-participant scores
contrib = pd.DataFrame(index=df.index)
for col, pol, _ in ITEMS:
    contrib[col] = df[col] - 1 if pol == 'P' else 5 - df[col]

df['raw_score'] = contrib.sum(axis=1)
df['sus_scaled'] = (df['raw_score'] / MAX_RAW * 100).round(1)

print("Per-participant scores")
print(df[['participant_id', 'familiarity', 'raw_score', 'sus_scaled']].to_string(index=False))

# ------------------------------------------------------------ summary statistics
s = df['sus_scaled']
print(f"\nMean:               {s.mean():.1f}")
print(f"Median:             {s.median():.1f}")
print(f"Standard deviation: {s.std(ddof=1):.1f}")
print(f"Range:              {s.min()} to {s.max()}")
print(f"At/above 68 (Bangor et al. benchmark): {(s >= 68).sum()}/{len(s)}")
print(f"At/above 70 (project target):          {(s >= 70).sum()}/{len(s)}")
print("\nFamiliarity distribution:")
print(df['familiarity'].value_counts().to_string())

# ----------------------------------------------------------- item-level analysis
rows = [{'item': text, 'polarity': pol,
         'mean_raw': round(df[col].mean(), 2),
         'contribution': round(contrib[col].mean(), 2)}
        for col, pol, text in ITEMS]
items_df = pd.DataFrame(rows).sort_values('contribution', ascending=False)

print("\nItem-level analysis (contribution 0-4, higher = better usability)")
print(items_df.to_string(index=False))

# ------------------------------------------------------------------ visualisation
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].bar(df['participant_id'], df['sus_scaled'], color='#7F77DD')
axes[0].axhline(68, color='#E8875F', linestyle='--', label='Benchmark (68)')
axes[0].axhline(s.mean(), color='#5DCAA5', label=f'Mean ({s.mean():.1f})')
axes[0].set_ylabel('Scaled usability score')
axes[0].set_title('Usability score by participant')
axes[0].set_ylim(0, 100)
axes[0].legend()

ordered = items_df.sort_values('contribution')
axes[1].barh(range(len(ordered)), ordered['contribution'], color='#7F77DD')
axes[1].set_yticks(range(len(ordered)))
axes[1].set_yticklabels([t[:42] for t in ordered['item']], fontsize=8)
axes[1].set_xlabel('Mean contribution (0-4)')
axes[1].set_title('Item-level usability contribution')
axes[1].set_xlim(0, 4)

plt.tight_layout()
plt.savefig('sus_analysis.png', dpi=150, bbox_inches='tight')
print("\nChart saved to sus_analysis.png")
