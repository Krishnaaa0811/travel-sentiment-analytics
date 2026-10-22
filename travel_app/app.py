import calendar
import re

import altair as alt
import joblib
import pandas as pd
import streamlit as st

from pathlib import Path
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(page_title="Travel Sentiment Analytics", page_icon="🧳", layout="wide")

# ============ EDIT THESE ============
GITHUB_URL = "https://github.com/Krishnaaa0811/travel-sentiment-analytics"
LINKEDIN_URL = ""        # paste your LinkedIn post link here later
ML_ACCURACY = "73.5%"      
PBIX_URL = "https://drive.google.com/file/d/1sLpDbXpanIikK5XZpEz9b9R4nVCDZgzp/view?usp=sharing"           

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

MODEL_CANDIDATES = [
    PROJECT_DIR / "models" / "sentiment_model.joblib",
    BASE_DIR / "models" / "sentiment_model.joblib",
    BASE_DIR / "sentiment_model.joblib",
]

NAVY, TEAL, SLATE, CORAL = "#1B2A4A", "#1AA6A0", "#6B7A99", "#E8604C"
ORDER = ["Positive", "Neutral", "Negative"]
COLORS = [TEAL, SLATE, CORAL]
COLOR_BY_LABEL = dict(zip(ORDER, COLORS))
MONTHS = list(calendar.month_name)[1:]

analyzer = SentimentIntensityAnalyzer()

# ---------- look and feel ----------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p, .stApp label, .stApp li {
        font-family: 'Inter', sans-serif;
    }
    .block-container {padding-top: 2rem; max-width: 1240px;}
    [data-testid="stAppDeployButton"], [data-testid="stDecoration"], footer {display: none;}
    h2, h3, h4 {color: #1B2A4A; font-weight: 700;}

    .hero {
        position: relative; overflow: hidden; border-radius: 20px;
        background: linear-gradient(120deg, #1B2A4A 0%, #1F5F7A 55%, #1AA6A0 100%);
        padding: 40px 44px; margin-bottom: 26px;
    }
    .hero::after {
        content: ""; position: absolute; right: -70px; top: -70px;
        width: 260px; height: 260px; border-radius: 50%; background: rgba(255,255,255,0.08);
    }
    .hero .tag {
        display: inline-block; background: rgba(255,255,255,0.16); color: #FFFFFF;
        padding: 4px 14px; border-radius: 999px; font-size: 0.78rem; font-weight: 600;
        letter-spacing: 0.06em; margin-bottom: 14px;
    }
    .hero h1 {color: #FFFFFF; margin: 0 0 10px 0; font-size: 2.2rem; font-weight: 800; line-height: 1.2;}
    .hero p {color: #DDEFEF; margin: 0; font-size: 1.05rem; line-height: 1.6; max-width: 820px;}

    .section {color: #1B2A4A; font-size: 1.35rem; font-weight: 700; margin: 30px 0 14px 0;}

    .stat {
        background: #FFFFFF; border-radius: 16px; padding: 20px 22px;
        box-shadow: 0 2px 14px rgba(27, 42, 74, 0.08);
    }
    .stat-value {font-size: 2rem; font-weight: 800; color: #1B2A4A; line-height: 1.1;}
    .stat-label {color: #6B7A99; font-size: 0.9rem; font-weight: 500; margin-top: 6px;}

    .card {
        background: #FFFFFF; border-radius: 16px; padding: 20px 22px; height: 100%;
        box-shadow: 0 2px 14px rgba(27, 42, 74, 0.08);
    }
    .card-icon {font-size: 1.6rem; margin-bottom: 6px;}
    .card h4 {margin: 0 0 6px 0; font-size: 1.05rem;}
    .card p {margin: 0; color: #4A5878; font-size: 0.93rem; line-height: 1.55;}

    .insight {
        background: #FFFFFF; border-radius: 14px; padding: 16px 20px; margin-bottom: 14px;
        box-shadow: 0 2px 14px rgba(27, 42, 74, 0.08);
    }
    .insight-big {font-size: 1.65rem; font-weight: 800; line-height: 1.15;}
    .insight p {margin: 4px 0 0 0; color: #4A5878; font-size: 0.93rem; line-height: 1.5;}

    div[data-testid="stMetric"] {
        background: #FFFFFF; border-radius: 14px; padding: 14px 18px;
        box-shadow: 0 2px 14px rgba(27, 42, 74, 0.08);
    }
    div[data-testid="stMetricLabel"] {color: #6B7A99;}
    .badge {
        display: inline-block; color: #FFFFFF; padding: 6px 20px;
        border-radius: 999px; font-weight: 700; font-size: 1rem;
    }
    .small-label {color: #6B7A99; font-size: 0.85rem; margin-bottom: 6px;}
    .stTabs [data-baseweb="tab"] {font-weight: 600; font-size: 1rem;}
    .stButton > button, .stLinkButton > a, .stDownloadButton > button {border-radius: 10px; font-weight: 600;}
    [data-testid="stImage"] img {border-radius: 12px; box-shadow: 0 2px 14px rgba(27, 42, 74, 0.15);}

    .brand {font-size: 1.2rem; font-weight: 800; color: #FFFFFF; line-height: 1.3; padding: 8px 0 4px 0;}
    .brand span {display: block; font-size: 0.8rem; font-weight: 500; color: #9FB3D9;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- building blocks ----------

def hero(title, text, tag=""):
    tag_html = f'<div class="tag">{tag}</div>' if tag else ""
    st.markdown(f'<div class="hero">{tag_html}<h1>{title}</h1><p>{text}</p></div>', unsafe_allow_html=True)


def section(text):
    st.markdown(f'<div class="section">{text}</div>', unsafe_allow_html=True)


def stat(label, value, color=NAVY):
    return (
        f'<div class="stat" style="border-top:5px solid {color}">'
        f'<div class="stat-value">{value}</div><div class="stat-label">{label}</div></div>'
    )


def card(icon, title, text, color=TEAL, height=230):
    st.markdown(
        f'<div class="card" style="border-top:4px solid {color}; box-sizing:border-box; height:{height}px">'
        f'<div class="card-icon">{icon}</div><h4>{title}</h4><p>{text}</p></div>',
        unsafe_allow_html=True,
    )


def insight(big, text, color=TEAL, height=150):
    st.markdown(
        f'<div class="insight" style="border-left:6px solid {color}; box-sizing:border-box; height:{height}px">'
        f'<div class="insight-big" style="color:{color}">{big}</div><p>{text}</p></div>',
        unsafe_allow_html=True,
    )


def badge(label):
    color = COLOR_BY_LABEL.get(label, SLATE)
    return f'<span class="badge" style="background:{color}">{label}</span>'


def donut(labels, values, colors):
    df = pd.DataFrame({"Label": labels, "Share": values})
    return (
        alt.Chart(df)
        .mark_arc(innerRadius=55, outerRadius=95, stroke="#EEF1F8", strokeWidth=3)
        .encode(
            theta=alt.Theta("Share:Q"),
            color=alt.Color(
                "Label:N", scale=alt.Scale(domain=labels, range=colors),
                legend=alt.Legend(orient="bottom", title=None, labelFontSize=13, symbolSize=140),
            ),
            tooltip=["Label", alt.Tooltip("Share:Q", format=".1f")],
        )
        .properties(height=280, padding={"top": 20, "bottom": 16, "left": 16, "right": 16})
        .configure_view(stroke=None)
    )


def count_chart(counts):
    df = pd.DataFrame({"Sentiment": ORDER, "Reviews": [int(counts.get(o, 0)) for o in ORDER]})
    return (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X("Sentiment:N", sort=ORDER, title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Reviews:Q", title=None, axis=alt.Axis(tickMinStep=1)),
            color=alt.Color("Sentiment:N", scale=alt.Scale(domain=ORDER, range=COLORS), legend=None),
            tooltip=["Sentiment", "Reviews"],
        )
        .properties(height=240)
    )


# ---------- helpers ----------

def first_existing(paths):
    for p in paths:
        if p.exists():
            return p
    return None


def vader_label(compound):
    if compound >= 0.05:
        return "Positive"
    if compound <= -0.05:
        return "Negative"
    return "Neutral"


def score_label(score):
    if score >= 7:
        return "Positive"
    if score >= 5:
        return "Neutral"
    return "Negative"


def normalize_label(label):
    v = str(label).strip().lower()
    if v in {"positive", "pos"}:
        return "Positive"
    if v in {"negative", "neg"}:
        return "Negative"
    if v in {"neutral", "neu"}:
        return "Neutral"
    return str(label)


def show_agreement(name_a, label_a, name_b, label_b):
    if label_a == label_b:
        st.success(f"{name_a} and {name_b} agree: {label_a}.")
    else:
        st.warning(f"{name_a} says {label_a}, but {name_b} says {label_b}.")


def sort_values(values):
    values = list(values)
    if set(values) <= set(MONTHS):
        return [m for m in MONTHS if m in values]
    try:
        return sorted(values, key=lambda v: float(v))
    except ValueError:
        return sorted(values)


@st.cache_resource
def load_model():
    path = first_existing(MODEL_CANDIDATES)
    if path is None:
        return None, "sentiment_model.joblib was not found in a models/ folder."
    try:
        return joblib.load(path), None
    except Exception as error:
        return None, f"Could not load the model: {error}"


def predict_ml(text, model):
    label = normalize_label(model.predict([text])[0])
    probs = None
    if hasattr(model, "predict_proba"):
        raw = model.predict_proba([text])[0]
        probs = {normalize_label(c): float(p) for c, p in zip(model.classes_, raw)}
    return label, probs


@st.cache_data
def load_summary(path, modified_time):
    df = pd.read_csv(path)
    df["Value"] = df["Value"].astype(str)
    return df


model, ml_error = load_model()


# ==========================================================
# PAGE 1: HOME
# ==========================================================

def page_home():
    hero(
        "AI-Powered Travel Sentiment & Trend Analytics",
        "What do hotel guests really feel? This project reads more than half a million "
        "European hotel reviews, measures their sentiment with VADER and a trained machine "
        "learning model, and presents the findings in an interactive Power BI dashboard.",
        "DATA ANALYTICS · NLP · POWER BI",
    )

    cols = st.columns(4)
    items = [
        ("Reviews analysed", "515,212", NAVY),
        ("Hotels", "1,492", TEAL),
        ("European cities", "6", SLATE),
        ("Positive reviews", "71.8%", CORAL),
    ]
    for col, (label, value, color) in zip(cols, items):
        col.markdown(stat(label, value, color), unsafe_allow_html=True)

    section("Explore the project")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        card("📊", "Dashboard", "Browse all 7 pages of the Power BI report and download the interactive file.", TEAL)
    with c2:
        card("💡", "Key Insights", "The main findings about sentiment, travellers and destinations.", CORAL)
    with c3:
        card("🤖", "Try the AI", "Type any hotel review and see what VADER and the ML model think.", NAVY)
    with c4:
        card("🔎", "Explore the Data", "Compare sentiment across cities, trip types, months and more.", SLATE)

    section("Findings at a glance")
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        insight("71.8%", "of all reviews are positive.", TEAL)
    with f2:
        insight("8.49 vs 7.97", "average score of leisure vs business guests.", NAVY)
    with f3:
        insight("47.6%", "of reviews come from guests in the United Kingdom.", SLATE)
    with f4:
        insight("57.6%", "agreement between VADER and the guest's own score label.", CORAL)

    st.write("")
    b1, b2, _ = st.columns([1, 1, 3])
    if GITHUB_URL:
        b1.link_button("View the code on GitHub", GITHUB_URL)
    if LINKEDIN_URL:
        b2.link_button("Read the LinkedIn post", LINKEDIN_URL)


# ==========================================================
# PAGE 2: DASHBOARD (screenshots + .pbix download)
# ==========================================================

PAGE_NOTES = {
    "Cover": "The entry page. It introduces the report and leads to the six analysis pages.",
    "Overview": "Headline KPIs, which travellers are happiest, how sentiment changes over time, the happiest cities and the hotels that need attention.",
    "Sentiment & AI": "How VADER's labels compare with guests' own scores, how strong the sentiment is, and how review length differs by sentiment.",
    "Destinations": "How sentiment and scores differ across the six cities and their hotels.",
    "Travellers & Trips": "Who the travellers are: trip type, reviewer type, length of stay and nationality.",
    "Time & Trends": "How review volume and sentiment move across months and years.",
    "Insights": "A summary of the main findings from the whole report.",
}


def clean_name(path):
    name = re.sub(r"^\d+_", "", path.stem).replace("_", " ")
    return name.replace(" and ", " & ")


def page_dashboard():
    hero(
        "Power BI Dashboard",
        "A 7-page interactive report built in Power BI Desktop. Browse every page below, "
        "or download the file to explore it with the chips, tabs, filters and Reset button.",
        "DASHBOARD",
    )

    s1, s2, s3 = st.columns(3)
    s1.markdown(stat("Report pages", "7", NAVY), unsafe_allow_html=True)
    s2.markdown(stat("Filters: Year · City · Sentiment", "3", TEAL), unsafe_allow_html=True)
    s3.markdown(stat("Built with", "Power BI", CORAL), unsafe_allow_html=True)

    section("Browse the 7 pages")
    images = sorted((BASE_DIR / "assets" / "dashboard").glob("*.png"))
    if images:
        names = [clean_name(p) for p in images]
        tabs = st.tabs(names)
        for tab, img, name in zip(tabs, images, names):
            with tab:
                note = PAGE_NOTES.get(name)
                if note:
                    st.markdown(f"**{name}:** {note}")
                st.image(str(img), width="stretch")
    else:
        st.info("Add the dashboard screenshots to travel_app/assets/dashboard/ and they will appear here.")

    section("Open the interactive version")
    c1, c2 = st.columns([2, 1])
    with c1:
        card(
            "🖥️",
            "Use it in Power BI Desktop",
            "Download the .pbix file and open it in Power BI Desktop (free, Windows). "
            "Click the sentiment chips, tabs and charts to filter every page. "
            "In Desktop, hold Ctrl while clicking the chips and the Reset button.",
            TEAL,
        )
    with c2:
        st.write("")
        if PBIX_URL:
            st.link_button("⬇️ Download the .pbix file", PBIX_URL)
        else:
            st.info("The download link will appear here.")


# ==========================================================
# PAGE 3: KEY INSIGHTS
# ==========================================================

def page_insights():
    hero(
        "Key Insights",
        "What the 515,212 reviews tell us about guest sentiment, who travels, where they come from "
        "and where the data needs care.",
        "FINDINGS",
    )

    d1, d2 = st.columns(2)
    with d1:
        st.markdown("#### Sentiment of all reviews (%)")
        st.altair_chart(donut(ORDER, [71.8, 7.1, 21.1], COLORS), width="stretch")
    with d2:
        st.markdown("#### Trip type of all reviews (%)")
        st.altair_chart(
            donut(["Leisure", "Business", "Unknown"], [81.0, 16.1, 2.9], [NAVY, TEAL, SLATE]),
            width="stretch",
        )

    section("Sentiment")
    a, b, c = st.columns(3)
    with a:
        insight("71.8% positive", "7.1% of reviews are neutral and 21.1% negative.", TEAL)
    with b:
        insight("57.6% agreement", "VADER and the guest's own score give the same label on just over half of reviews.", CORAL)
    with c:
        insight("27,252 reviews", "in August 2016, the busiest month in the data.", NAVY)

    section("Travellers")
    a, b, c = st.columns(3)
    with a:
        insight("8.49 vs 7.97", "Leisure guests score higher than business guests.", TEAL)
    with b:
        insight("70% repeat guests", "The largest segment is leisure repeat guests: 288,292 reviews (56%).", NAVY)
    with c:
        insight("8.52 → 8.31", "Leisure scores dip slightly from 1-night stays to 7+ nights.", SLATE)
    st.markdown(
        "The guest mix also changes by city: business guests are about 10% of reviews in Barcelona "
        "and about 20% in Milan."
    )

    section("Geography")
    a, b = st.columns(2)
    with a:
        insight("47.6% from the UK", "245,110 reviews come from United Kingdom guests.", NAVY)
    with b:
        insight("63.5% from 5 countries", "The top 5 countries give 327,150 reviews, with average scores between 7.88 and 8.79.", TEAL)

    section("Where to be careful")
    a, b, c = st.columns(3)
    with a:
        insight("6.48 vs 8.40", "Reviews with an unknown stay length score far lower than average. This is probably a data-quality effect.", CORAL)
    with b:
        insight("August 2017", "is a partial month (latest review: 3 August 2017), so its count is low.", SLATE)
    with c:
        insight("2.9% unknown", "of reviews have no trip type recorded.", SLATE)


# ==========================================================
# PAGE 4: TRY THE AI
# ==========================================================

def page_try_ai():
    hero(
        "Try the AI",
        "VADER reads the words using a sentiment dictionary. The machine learning model "
        "(TF-IDF + Logistic Regression) learned from guest scores, so it predicts the label "
        "a guest's score would give.",
        "LIVE DEMO",
    )

    single, batch = st.tabs(["Single review", "Many reviews"])

    with single:
        review = st.text_area(
            "Write or paste a hotel review",
            "The room was spotless and the staff were wonderful, but breakfast was disappointing.",
            height=130,
            key="single_review",
        )
        use_score = st.checkbox("Compare with the guest's score (0 to 10)", key="use_guest_score")
        guest_score = (
            st.slider("Guest score", 0.0, 10.0, 8.0, 0.1, key="guest_score") if use_score else None
        )

        if st.button("Analyze review", type="primary"):
            if not review.strip():
                st.warning("Please enter a review first.")
                return

            scores = analyzer.polarity_scores(review)
            v_label = vader_label(scores["compound"])

            section("VADER")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown('<div class="small-label">Sentiment</div>', unsafe_allow_html=True)
                st.markdown(badge(v_label), unsafe_allow_html=True)
            c2.metric("Compound score", f"{scores['compound']:.3f}")
            c3.metric(
                "Positive / Neutral / Negative",
                f"{scores['pos']:.2f} / {scores['neu']:.2f} / {scores['neg']:.2f}",
            )
            st.progress(
                max(0.0, min(1.0, (scores["compound"] + 1) / 2)),
                text="Negative ← Compound score → Positive",
            )

            ml_label = None
            section("Machine learning model")
            if model is None:
                st.info(f"The ML model is unavailable. {ml_error}")
            else:
                try:
                    ml_label, probs = predict_ml(review, model)
                    m1, m2 = st.columns(2)
                    with m1:
                        st.markdown(
                            '<div class="small-label">Logistic Regression sentiment</div>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(badge(ml_label), unsafe_allow_html=True)
                    with m2:
                        if probs:
                            st.write("Class probabilities")
                            for name, p in sorted(probs.items(), key=lambda x: x[1], reverse=True):
                                st.write(f"{name}: {p:.1%}")
                                st.progress(max(0.0, min(1.0, p)))
                except Exception as error:
                    st.error("ML prediction failed. The VADER result above is still valid.")
                    st.code(str(error))

            section("Agreement")
            if ml_label is not None:
                show_agreement("VADER", v_label, "Logistic Regression", ml_label)
            if guest_score is not None:
                g_label = score_label(guest_score)
                st.write(f"Guest score {guest_score:.1f}/10 corresponds to **{g_label}**.")
                show_agreement("Guest score", g_label, "VADER", v_label)
                if ml_label is not None:
                    show_agreement("Guest score", g_label, "Logistic Regression", ml_label)

    with batch:
        text = st.text_area("Paste several reviews, one per line", height=180, key="batch_reviews")

        if st.button("Analyze all reviews", type="primary"):
            reviews = [l.strip() for l in text.splitlines() if l.strip()]
            if not reviews:
                st.info("Paste at least one review first.")
                st.session_state.pop("batch_results", None)
            else:
                rows = []
                for r in reviews:
                    s = analyzer.polarity_scores(r)
                    ml_label, top = None, None
                    if model is not None:
                        try:
                            ml_label, probs = predict_ml(r, model)
                            top = round(max(probs.values()), 3) if probs else None
                        except Exception:
                            pass
                    rows.append(
                        {
                            "Review": r,
                            "VADER Compound": round(s["compound"], 3),
                            "VADER Sentiment": vader_label(s["compound"]),
                            "ML Sentiment": ml_label,
                            "ML Top Probability": top,
                        }
                    )
                st.session_state["batch_results"] = pd.DataFrame(rows)

        results = st.session_state.get("batch_results")
        if results is not None:
            has_ml = results["ML Sentiment"].notna().any()

            k1, k2, k3 = st.columns(3)
            k1.metric("Reviews analyzed", f"{len(results):,}")
            if has_ml:
                agree = int((results["VADER Sentiment"] == results["ML Sentiment"]).sum())
                k2.metric("Methods agree", agree)
                k3.metric("Methods disagree", len(results) - agree)

            ch1, ch2 = st.columns(2)
            with ch1:
                st.write("VADER")
                st.altair_chart(count_chart(results["VADER Sentiment"].value_counts()), width="stretch")
            if has_ml:
                with ch2:
                    st.write("Logistic Regression")
                    st.altair_chart(count_chart(results["ML Sentiment"].value_counts()), width="stretch")

            st.dataframe(results, width="stretch")
            st.download_button(
                "Download results (CSV)",
                data=results.to_csv(index=False).encode("utf-8"),
                file_name="travel_sentiment_batch_results.csv",
                mime="text/csv",
            )


# ==========================================================
# PAGE 5: EXPLORE THE DATA
# ==========================================================

def page_explore():
    hero(
        "Explore the Data",
        "Pick a category and see how VADER sentiment is split inside each group, "
        "across all 515,212 reviews.",
        "INTERACTIVE",
    )

    path = BASE_DIR / "summary.csv"
    if not path.exists():
        st.info("summary.csv is missing. Run make_summary.py once, then restart the app.")
        return

    summary = load_summary(str(path), path.stat().st_mtime)
    categories = sorted(summary["Category"].unique())
    default = categories.index("City") if "City" in categories else 0
    chosen = st.selectbox("Break sentiment down by", categories, index=default)

    sub = summary[summary["Category"] == chosen]
    counts = sub.pivot_table(
        index="Value", columns="Sentiment", values="Reviews", aggfunc="sum", fill_value=0
    ).reindex(columns=ORDER, fill_value=0)
    counts = counts.reindex(sort_values(counts.index))
    share = counts.div(counts.sum(axis=1).replace(0, 1), axis=0).mul(100).round(1)

    overall = counts.sum()
    total = int(overall.sum())
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Reviews", f"{total:,}")
    k2.metric("Positive", f"{overall['Positive'] / max(total, 1):.1%}")
    k3.metric("Neutral", f"{overall['Neutral'] / max(total, 1):.1%}")
    k4.metric("Negative", f"{overall['Negative'] / max(total, 1):.1%}")

    section(f"Sentiment share (%) by {chosen}")
    long = share.reset_index().melt(id_vars="Value", var_name="Sentiment", value_name="Share")
    long["Rank"] = long["Sentiment"].map({s: i for i, s in enumerate(ORDER)})
    chart = (
        alt.Chart(long)
        .mark_bar()
        .encode(
            y=alt.Y("Value:N", sort=list(share.index), title=None),
            x=alt.X(
                "Share:Q", stack="zero", title="Share of reviews (%)",
                scale=alt.Scale(domain=[0, 100]),
            ),
            color=alt.Color(
                "Sentiment:N", scale=alt.Scale(domain=ORDER, range=COLORS),
                legend=alt.Legend(orient="top", title=None),
            ),
            order=alt.Order("Rank:Q"),
            tooltip=["Value", "Sentiment", alt.Tooltip("Share:Q", format=".1f")],
        )
        .properties(height=max(220, 34 * len(share) + 80))
    )
    st.altair_chart(chart, width="stretch")

    section("Review counts")
    st.dataframe(counts, width="stretch")


# ==========================================================
# PAGE 6: ABOUT & METHOD
# ==========================================================

def page_about():
    hero(
        "About & Method",
        "How the project was built, what the labels mean, and where the results need care.",
        "METHOD",
    )

    section("The pipeline")
    steps = [
        ("📥", "1. Collect", "Hotel reviews for six European cities.", NAVY),
        ("🧹", "2. Clean", "Missing values, dates and engineered features.", TEAL),
        ("🔍", "3. Explore", "Distributions, trends and segments.", SLATE),
        ("💬", "4. VADER", "A compound score from -1 to +1 for every review.", CORAL),
        ("🤖", "5. Machine learning", "TF-IDF + Logistic Regression, trained on the guest-score label.", NAVY),
        ("📊", "6. Power BI", "A 7-page interactive dashboard.", TEAL),
        ("🧳", "7. Streamlit", "This app, where you can try the models yourself.", SLATE),
    ]
    for row in (steps[:4], steps[4:]):
        cols = st.columns(4)
        for col, (icon, title, text, color) in zip(cols, row):
            with col:
                card(icon, title, text, color)
        st.write("")

    section("Labels")
    l1, l2 = st.columns(2)
    with l1:
        card("⭐", "Guest-score label", "7 or higher is Positive, 5 to 6.9 Neutral, below 5 Negative.", TEAL)
    with l2:
        card("💬", "VADER label", "Compound score of +0.05 or higher is Positive, -0.05 or lower Negative, otherwise Neutral.", CORAL)

    section("Model quality")
    c1, c2 = st.columns(2)
    c1.metric("VADER vs guest-score agreement", "57.6%")
    c2.metric("ML test accuracy", ML_ACCURACY or "see notebook")
    st.caption("The ML model was evaluated on a held-out 20% test set (stratified split).")
    report = pd.DataFrame(
        {
            "Precision": [0.80, 0.51, 0.64],
            "Recall": [0.90, 0.40, 0.47],
            "F1-score": [0.85, 0.45, 0.54],
            "Test reviews": [67070, 25488, 10483],
        },
        index=["Positive", "Neutral", "Negative"],
    )
    st.dataframe(report, width="stretch")

    section("Limitations")
    st.markdown(
        "- VADER is a general-purpose dictionary and can misread hotel-specific wording or mixed reviews.\n"
        "- The ML model is weakest on Neutral (F1 0.45) and Negative (recall 0.47) reviews, because most guest scores are Positive.\n"
        "- The ML model learns from guest scores, so it predicts the score-based label, not true emotion.\n"
        "- August 2017 is a partial month, and 2.9% Of reviews have an unknown trip type.\n"
        "- Some accented hotel names were already lost in the source data."
    )

    section("Tools")
    st.write("Python, pandas, scikit-learn, VADER, Power BI, Streamlit.")
    if GITHUB_URL:
        st.link_button("Source code on GitHub", GITHUB_URL)


# ---------- navigation ----------

pages = [
    st.Page(page_home, title="Home", icon="🏠", default=True),
    st.Page(page_dashboard, title="Dashboard", icon="📊"),
    st.Page(page_insights, title="Key Insights", icon="💡"),
    st.Page(page_try_ai, title="Try the AI", icon="🤖"),
    st.Page(page_explore, title="Explore the Data", icon="🔎"),
    st.Page(page_about, title="About & Method", icon="ℹ️"),
]

navigation = st.navigation(pages)

st.sidebar.markdown(
    '<div class="brand">🧳 Travel Sentiment<span>AI-powered travel analytics</span></div>',
    unsafe_allow_html=True,
)
with st.sidebar.expander("Developer info"):
    st.write("Model:", type(model).__name__ if model is not None else ml_error)
    st.write("Classes:", [str(c) for c in getattr(model, "classes_", [])])

navigation.run()
