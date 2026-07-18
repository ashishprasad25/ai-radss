"""
AI-RADSS: AI Readiness Assessment and Decision Support System
BUSI 1783 - Business Analytics Project, University of Greenwich

A multi-dimensional decision support system that assesses organisational
readiness for AI adoption across five dimensions, classifies the
organisation into a readiness tier using rule-based thresholds, and
generates prioritised strategic recommendations.

Framework grounded in: Tornatzky and Fleischer (1990, TOE); Johnk,
Weissert and Wyrtki (2021); Mikalef and Gupta (2021); Pumplun, Tauchert
and Heidt (2019); Holmstrom (2022); Becker, Knackstedt and Poppelbuss (2009).
"""

import streamlit as st
import plotly.graph_objects as go

# --------------------------------------------------------------------------
# Page configuration
# --------------------------------------------------------------------------

st.set_page_config(
    page_title="AI-RADSS | AI readiness assessment",
    page_icon=":bar_chart:",
    layout="centered",
)

# --------------------------------------------------------------------------
# Framework definition: five dimensions, weights, and questionnaire items
# Each dimension and item is grounded in the literature (see dissertation
# Chapter 2 and the theory integration map).
# --------------------------------------------------------------------------

DIMENSIONS = {
    "Data readiness": {
        "weight": 0.25,
        "description": "How prepared is your organisation's data for AI?",
        "questions": [
            "Our organisational data is stored centrally and is accessible when needed.",
            "Data quality checks are performed regularly across departments.",
            "We have clear data governance policies defining ownership and responsibility.",
            "Our data is sufficient in volume and variety to support AI applications.",
            "Data privacy and protection processes comply with regulations such as GDPR.",
        ],
    },
    "Technology infrastructure": {
        "weight": 0.20,
        "description": "Can your current systems support AI deployment?",
        "questions": [
            "Our organisation uses cloud computing or scalable computing infrastructure.",
            "Our core business systems can integrate and exchange data with each other.",
            "We have the technical capacity to deploy and run AI tools.",
            "Our IT infrastructure is regularly updated and maintained.",
            "We have access to the software tools needed for data analysis and AI.",
        ],
    },
    "Human capital": {
        "weight": 0.20,
        "description": "Does your workforce have the skills to work with AI?",
        "questions": [
            "Our organisation employs staff with data analysis or AI-related skills.",
            "Employees across departments have a good level of digital literacy.",
            "We invest in training and upskilling employees in data and AI topics.",
            "We can attract or access AI talent when needed.",
            "Leadership includes people who understand AI capabilities and limitations.",
        ],
    },
    "Organisational culture": {
        "weight": 0.20,
        "description": "Is your organisation culturally ready for AI-driven change?",
        "questions": [
            "Senior leadership actively supports data-driven and AI initiatives.",
            "Our organisation is open to change and experimentation.",
            "Decisions in our organisation are usually informed by data rather than intuition.",
            "Employees trust that AI will support rather than threaten their work.",
            "Cross-departmental collaboration is common in our organisation.",
        ],
    },
    "Strategic alignment": {
        "weight": 0.15,
        "description": "Is AI adoption connected to clear business objectives?",
        "questions": [
            "Our organisation has a documented AI or digital strategy.",
            "We have identified specific use cases where AI could add measurable value.",
            "Budget is allocated or planned for AI initiatives.",
            "AI initiatives are linked to clear business objectives and success metrics.",
            "We have a realistic roadmap or timeline for AI adoption.",
        ],
    },
}

DIM_NAMES = list(DIMENSIONS.keys())

# Rule-based tier thresholds (transparent alternative to clustering,
# per supervisor feedback and Holmstrom 2022 scoring precedent).
TIERS = [
    (0, 25, "Nascent", "Foundational gaps exist across multiple dimensions. "
     "Significant preparation is needed before AI investment."),
    (26, 50, "Developing", "Partial readiness with significant gaps requiring "
     "attention before committing to AI adoption."),
    (51, 75, "Advanced", "Near-ready. Targeted improvements in weaker "
     "dimensions will substantially de-risk AI investment."),
    (76, 100, "AI-Ready", "Prepared to proceed with AI implementation, "
     "starting with a well-scoped pilot project."),
]

TIER_COLOURS = {
    "Nascent": "#E24B4A",
    "Developing": "#EF9F27",
    "Advanced": "#1D9E75",
    "AI-Ready": "#639922",
}

# Rule-based recommendation engine: strategic actions per dimension,
# derived from the literature review (Johnk et al. 2021 actionable
# indicators; IBM 2024 barrier evidence; Vial 2019 transformation levers).
RECOMMENDATIONS = {
    "Data readiness": [
        "Establish a data governance framework and assign clear data ownership.",
        "Audit existing data sources for quality, completeness and consistency.",
        "Consolidate departmental data into a central, accessible repository.",
        "Implement data protection processes aligned with GDPR before AI deployment.",
    ],
    "Technology infrastructure": [
        "Assess cloud readiness and plan migration of core workloads where appropriate.",
        "Enable integration between key business systems through APIs.",
        "Pilot AI tooling on existing infrastructure before large-scale investment.",
        "Create a technology upgrade roadmap covering the next 12 to 24 months.",
    ],
    "Human capital": [
        "Run a skills audit to identify data and AI capability gaps.",
        "Launch a data literacy training programme across departments.",
        "Recruit or contract at least one data analyst to anchor analytics capability.",
        "Brief senior leadership on AI capabilities, limitations and governance.",
    ],
    "Organisational culture": [
        "Secure visible senior-leadership sponsorship for AI initiatives.",
        "Establish a cross-functional AI working group to build shared ownership.",
        "Communicate openly with employees about how AI will support their roles.",
        "Introduce data-informed decision-making practices in management meetings.",
    ],
    "Strategic alignment": [
        "Develop a documented AI strategy linked to specific business objectives.",
        "Identify two or three high-value AI use cases and prioritise them.",
        "Allocate a defined budget and owner for AI initiatives.",
        "Set measurable success criteria and a 12-month adoption roadmap.",
    ],
}

# --------------------------------------------------------------------------
# Scoring engine
# --------------------------------------------------------------------------


def dimension_score(values):
    """Convert a list of 1-5 Likert responses into a 0-100 dimension score."""
    mean = sum(values) / len(values)
    return round(((mean - 1) / 4) * 100, 1)


def composite_score(dim_scores):
    """Weighted aggregation of dimension scores into the overall AIRS."""
    total = 0.0
    for name, score in dim_scores.items():
        total += score * DIMENSIONS[name]["weight"]
    return round(total, 1)


def classify(score):
    """Map the composite score to a readiness tier using rule-based thresholds.

    Uses continuous upper bounds so decimal scores (e.g. 25.5) always
    fall into exactly one tier.
    """
    for _, high, name, description in TIERS:
        if score <= high:
            return name, description
    return TIERS[-1][2], TIERS[-1][3]


def build_report(dim_scores, overall, tier, tier_text, priority_dims):
    """Create a plain-text report the user can download."""
    lines = [
        "AI-RADSS readiness report",
        "=" * 40,
        f"Overall AI readiness score: {overall} / 100",
        f"Readiness tier: {tier}",
        f"Interpretation: {tier_text}",
        "",
        "Dimension scores",
        "-" * 40,
    ]
    for name, score in dim_scores.items():
        lines.append(f"{name}: {score} / 100")
    lines += ["", "Priority recommendations", "-" * 40]
    for dim in priority_dims:
        lines.append(f"\n{dim} (score {dim_scores[dim]}):")
        for i, rec in enumerate(RECOMMENDATIONS[dim], 1):
            lines.append(f"  {i}. {rec}")
    lines += [
        "",
        "Generated by AI-RADSS - AI Readiness Assessment and Decision",
        "Support System. BUSI 1783, University of Greenwich.",
        "Responses are processed in-session only and are not stored.",
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------

if "section" not in st.session_state:
    st.session_state.section = 0          # 0-4 questionnaire, 5 = results
if "answers" not in st.session_state:
    st.session_state.answers = {}         # (dim_index, q_index) -> 1..5


def radio_key(d_idx, q_idx):
    return f"w_{d_idx}_{q_idx}"


# --------------------------------------------------------------------------
# Questionnaire pages
# --------------------------------------------------------------------------

def show_questionnaire(d_idx):
    dim_name = DIM_NAMES[d_idx]
    dim = DIMENSIONS[dim_name]
    n_questions = len(dim["questions"])

    st.title("AI-RADSS")
    st.caption("AI readiness assessment and decision support system")
    st.progress((d_idx) / len(DIM_NAMES),
                text=f"Section {d_idx + 1} of {len(DIM_NAMES)}")

    st.subheader(dim_name)
    st.write(dim["description"] + f" Rate each statement from 1 "
             f"(strongly disagree) to 5 (strongly agree).")

    for q_idx, question in enumerate(dim["questions"]):
        saved = st.session_state.answers.get((d_idx, q_idx))
        st.radio(
            f"Q{q_idx + 1}. {question}",
            options=[1, 2, 3, 4, 5],
            index=None if saved is None else saved - 1,
            horizontal=True,
            key=radio_key(d_idx, q_idx),
        )

    st.divider()
    col_back, col_next = st.columns([1, 1])

    with col_back:
        if d_idx > 0 and st.button("Back"):
            _save_current(d_idx, n_questions)
            st.session_state.section -= 1
            st.rerun()

    with col_next:
        label = "See my results" if d_idx == len(DIM_NAMES) - 1 else "Next section"
        if st.button(label, type="primary"):
            values = _save_current(d_idx, n_questions)
            if None in values:
                st.warning("Answer every statement before continuing.")
            else:
                st.session_state.section += 1
                st.rerun()

    st.caption("Responses are processed in-session only and are not stored, "
               "in line with UK GDPR.")


def _save_current(d_idx, n_questions):
    values = []
    for q_idx in range(n_questions):
        value = st.session_state.get(radio_key(d_idx, q_idx))
        if value is not None:
            st.session_state.answers[(d_idx, q_idx)] = value
        values.append(st.session_state.answers.get((d_idx, q_idx)))
    return values


# --------------------------------------------------------------------------
# Results dashboard
# --------------------------------------------------------------------------

def show_results():
    # Compute scores
    dim_scores = {}
    for d_idx, name in enumerate(DIM_NAMES):
        vals = [st.session_state.answers[(d_idx, q)]
                for q in range(len(DIMENSIONS[name]["questions"]))]
        dim_scores[name] = dimension_score(vals)

    overall = composite_score(dim_scores)
    tier, tier_text = classify(overall)

    lowest_dim = min(dim_scores, key=dim_scores.get)
    priority_dims = [lowest_dim] + [d for d, s in dim_scores.items()
                                    if s < 50 and d != lowest_dim]

    st.title("Your AI readiness results")

    # Metric cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Overall readiness score", f"{overall} / 100")
    col2.markdown(
        f"<p style='font-size:0.85rem;color:grey;margin-bottom:4px'>"
        f"Readiness tier</p>"
        f"<span style='background:{TIER_COLOURS[tier]}22;"
        f"color:{TIER_COLOURS[tier]};padding:6px 16px;border-radius:14px;"
        f"font-weight:600'>{tier}</span>",
        unsafe_allow_html=True,
    )
    col3.metric("Priority gap", lowest_dim)

    st.info(tier_text)

    # Radar chart and dimension bars
    left, right = st.columns(2)

    with left:
        st.markdown("**Dimension profile**")
        categories = DIM_NAMES + [DIM_NAMES[0]]
        values = [dim_scores[d] for d in DIM_NAMES] + [dim_scores[DIM_NAMES[0]]]
        radar = go.Figure(go.Scatterpolar(
            r=values, theta=categories, fill="toself",
            line=dict(color="#7F77DD"), fillcolor="rgba(127,119,221,0.30)",
        ))
        radar.update_layout(
            polar=dict(radialaxis=dict(range=[0, 100], showticklabels=True)),
            showlegend=False, height=330, margin=dict(l=40, r=40, t=20, b=20),
        )
        st.plotly_chart(radar, use_container_width=True)

    with right:
        st.markdown("**Dimension scores**")
        bar_colours = ["#F0997B" if dim_scores[d] < 50 else "#7F77DD"
                       for d in DIM_NAMES]
        bars = go.Figure(go.Bar(
            x=[dim_scores[d] for d in DIM_NAMES],
            y=DIM_NAMES, orientation="h",
            marker_color=bar_colours,
            text=[f"{dim_scores[d]}" for d in DIM_NAMES],
            textposition="outside",
        ))
        bars.update_layout(
            xaxis=dict(range=[0, 105]), height=330,
            margin=dict(l=10, r=10, t=20, b=20),
            yaxis=dict(autorange="reversed"),
        )
        st.plotly_chart(bars, use_container_width=True)

    # Recommendations panel
    st.subheader("Priority recommendations")
    for dim in priority_dims:
        with st.expander(f"{dim} — score {dim_scores[dim]} / 100",
                         expanded=(dim == lowest_dim)):
            for i, rec in enumerate(RECOMMENDATIONS[dim], 1):
                st.write(f"{i}. {rec}")

    # Export and restart
    st.divider()
    report = build_report(dim_scores, overall, tier, tier_text, priority_dims)
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.download_button("Export report", report,
                           file_name="ai_radss_report.txt")
    with col_b:
        if st.button("Start a new assessment"):
            st.session_state.section = 0
            st.session_state.answers = {}
            st.rerun()


# --------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------

if st.session_state.section < len(DIM_NAMES):
    show_questionnaire(st.session_state.section)
else:
    show_results()
