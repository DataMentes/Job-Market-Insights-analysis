"""Job Market Analysis — Egypt & Saudi Arabia.

Reads the cleaned tables from data/database.db, renders one page at a time and
caches every aggregation, so switching pages does not recompute the whole app.
"""
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from wordcloud import WordCloud


def _database_path() -> Path:
    """Locate data/database.db regardless of the directory the app is started from."""
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "data" / "database.db"
        if candidate.exists():
            return candidate
    raise FileNotFoundError("data/database.db not found")


DB_PATH = _database_path()
RAW_ROWS = {"Egypt": 4094, "Saudi Arabia": 5520}

PAGES = ["Home", "Egypt Market", "Saudi Market", "Comparison"]

SCHEMA_MAP = pd.DataFrame(
    [
        ("location", "city", "split on ·"),
        ("career_level", "type / exp / no_exp", "split into three columns"),
        ("title", "title", "numbers and level markers stripped, mapped to standard titles"),
        ("experience", "experience_", "merged with exp"),
        ("num_of_exp", "num_of_exp_years", "merged with no_exp, converted to numeric"),
        ("sex", "gender", "No Preference as the default"),
        ("remote", "remote", "On-site / Remote / Hybrid"),
        ("salary, age, qualification, description, skills", "—", "dropped"),
    ],
    columns=["raw column", "clean column", "rule"],
)

DISPLAY_COLUMNS = ["title", "company_name", "city", "remote", "job_level", "gender"]

st.set_page_config(page_title="Job Market Analysis", layout="wide")


# ---------------------------------------------------------------- data access
@st.cache_data(show_spinner="Loading data…")
def load_markets() -> dict[str, pd.DataFrame]:
    con = sqlite3.connect(DB_PATH)
    try:
        return {
            "Egypt": pd.read_sql("SELECT * FROM EGYPT", con),
            "Saudi Arabia": pd.read_sql("SELECT * FROM [saudi-arabia]", con),
        }
    finally:
        con.close()


@st.cache_data
def data_quality(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for column in df.columns:
        if column == "index":
            continue
        values = df[column]
        rows.append(
            {
                "column": column,
                "type": str(values.dtype),
                "missing %": round(100 * values.isna().mean(), 1),
                "unknown %": round(100 * values.astype(str).eq("Unknown").mean(), 1),
                "distinct": int(values.nunique(dropna=True)),
            }
        )
    return pd.DataFrame(rows)


@st.cache_data
def top_counts(df: pd.DataFrame, column: str, n: int = 8) -> pd.DataFrame:
    counts = df[column].replace("Unknown", pd.NA).dropna().value_counts().head(n)
    return counts.rename_axis(column).reset_index(name="postings")


@st.cache_data
def full_counts(df: pd.DataFrame, column: str) -> pd.DataFrame:
    counts = df[column].value_counts()
    return counts.rename_axis(column).reset_index(name="postings")


@st.cache_data
def monthly_postings(df: pd.DataFrame) -> pd.DataFrame:
    dates = pd.to_datetime(df["date"], errors="coerce")
    counts = dates.dropna().dt.to_period("M").value_counts().sort_index()
    return pd.DataFrame(
        {"month": counts.index.to_timestamp(), "postings": counts.to_numpy()}
    )


@st.cache_data
def city_level_matrix(df: pd.DataFrame, cities: int = 8) -> pd.DataFrame:
    top = df["city"].replace("Unknown", pd.NA).value_counts().head(cities).index
    subset = df[df["city"].isin(top)]
    return subset.pivot_table(
        index="city", columns="job_level", values="index", aggfunc="count", fill_value=0
    )


@st.cache_data
def experience_frame(df: pd.DataFrame) -> pd.DataFrame:
    min_years = pd.to_numeric(df["min_num_of_years"], errors="coerce")
    max_years = pd.to_numeric(df["max_num_of_years"], errors="coerce")
    return pd.DataFrame(
        {
            "requirement": ["minimum"] * min_years.notna().sum()
            + ["maximum"] * max_years.notna().sum(),
            "years": pd.concat([min_years.dropna(), max_years.dropna()]).to_numpy(),
        }
    )


@st.cache_data
def wordcloud_image(df: pd.DataFrame) -> np.ndarray:
    text = " ".join(df["title"].dropna().astype(str))
    cloud = WordCloud(width=1200, height=600, background_color="white").generate(text)
    return cloud.to_array()


@st.cache_data
def summary(df: pd.DataFrame) -> pd.Series:
    top_city = df["city"].replace("Unknown", pd.NA).dropna().value_counts()
    experience = pd.to_numeric(df["min_num_of_years"], errors="coerce")
    return pd.Series(
        {
            "postings": len(df),
            "top city": top_city.index[0] if len(top_city) else "—",
            "top city share": top_city.iloc[0] / len(df) if len(top_city) else 0.0,
            "on-site share": df["remote"].eq("On-site").mean(),
            "remote share": df["remote"].eq("Remote").mean(),
            "no gender preference": df["gender"].eq("No Preference").mean(),
            "level stated": (~df["job_level"].eq("No Preference")).mean(),
            "unknown job type": df["type"].eq("Unknown").mean(),
            "experience stated": experience.notna().mean(),
            "median min experience": experience.median(),
        }
    )


DATA = load_markets()


# ------------------------------------------------------------------ UI parts
def kpi_row(market: str) -> None:
    s = summary(DATA[market])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Postings", f"{int(s['postings']):,}")
    c2.metric(
        f"{s['top city']} share",
        f"{s['top city share']:.0%}",
        help=f"share of all {market} postings",
    )
    c3.metric("On-site", f"{s['on-site share']:.0%}")
    c4.metric(
        "Remote",
        f"{s['remote share']:.0%}",
        help="fully remote roles",
    )


def market_charts(frame: pd.DataFrame) -> None:
    cities = top_counts(frame, "city")
    remote = frame["remote"].value_counts().reset_index()
    levels = top_counts(frame, "job_level", 6)

    c1, c2, c3 = st.columns(3)
    with c1:
        fig = px.bar(cities, x="postings", y="city", orientation="h", title="Top cities")
        fig.update_layout(yaxis_title="", height=340, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.pie(
            remote, names="remote", values="count", hole=0.55, title="Work arrangement"
        )
        fig.update_layout(height=340, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig, use_container_width=True)
    with c3:
        fig = px.bar(levels, x="job_level", y="postings", title="Job level")
        fig.update_layout(xaxis_title="", height=340, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------------------------- pages
def home() -> None:
    st.title("Job Market Analysis")
    st.caption("Egypt and Saudi Arabia · postings collected 2024-11-18 → 2025-04-15")

    egypt, saudi = summary(DATA["Egypt"]), summary(DATA["Saudi Arabia"])
    combined = pd.concat([DATA["Egypt"], DATA["Saudi Arabia"]], ignore_index=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Postings cleaned", f"{int(egypt['postings'] + saudi['postings']):,}")
    c2.metric("Highest volume city", f"{egypt['top city']} / {saudi['top city']}")
    c3.metric("On-site", f"{combined['remote'].eq('On-site').mean():.0%}")
    c4.metric(
        "Unknown job type",
        f"{combined['type'].eq('Unknown').mean():.0%}",
        help="documentation gap shared by both markets",
    )

    st.divider()
    left, middle, right = st.columns([1, 1.15, 1.2], gap="large")

    with left:
        st.subheader("Cleaning funnel")
        st.write("Almost every posting survives cleaning; the work happens in the columns.")
        for market, df in DATA.items():
            st.metric(
                f"{market}: rows kept",
                f"{len(df):,}",
                delta=f"{len(df) - RAW_ROWS[market]:,} vs raw",
                delta_color="off",
            )
            st.progress(len(df) / RAW_ROWS[market])

    with middle:
        st.subheader("Columns before and after")
        st.dataframe(SCHEMA_MAP, hide_index=True, height=300)

    with right:
        st.subheader("Data quality")
        market = st.radio("Market", list(DATA), horizontal=True, label_visibility="collapsed")
        st.dataframe(
            data_quality(DATA[market]).sort_values("distinct", ascending=False),
            hide_index=True,
            height=300,
        )

    st.divider()
    st.subheader("Inspect the data")
    st.write("Browse a sample here; download the full table when you need all rows.")

    c1, c2, c3 = st.columns([1, 1, 2])
    market = c1.selectbox("Market", list(DATA), key="sample_market")
    rows = c2.slider("Rows", 20, 300, 40, step=20)
    columns = c3.multiselect(
        "Columns",
        list(DATA[market].columns),
        default=[c for c in DISPLAY_COLUMNS if c in DATA[market].columns],
    )
    st.dataframe(DATA[market][columns].head(rows), height=360, hide_index=True)
    st.download_button(
        f"Download {market} ({len(DATA[market]):,} rows, CSV)",
        DATA[market].to_csv(index=False).encode("utf-8"),
        file_name=f"{market.lower().replace(' ', '_')}_clean.csv",
        mime="text/csv",
    )


def market_page(market: str) -> None:
    st.title(f"{market} job market")
    kpi_row(market)

    level = st.multiselect(
        "Filter by job level",
        sorted(DATA[market]["job_level"].unique()),
        placeholder="All levels",
    )
    frame = DATA[market]
    if level:
        frame = frame[frame["job_level"].isin(level)]

    market_charts(frame)

    s = summary(frame)
    st.divider()
    st.subheader("What the numbers say")
    bullets = [
        f"**{s['top city']}** accounts for **{s['top city share']:.0%}** of postings; the market "
        f"is capital-heavy rather than spread across cities.",
        f"**{s['on-site share']:.0%}** of roles are on-site, **{s['remote share']:.0%}** are "
        f"fully remote.",
        f"**{s['no gender preference']:.0%}** of postings state no gender preference.",
        f"Job type is **Unknown** for **{s['unknown job type']:.0%}** of postings, so it cannot "
        f"be used to compare contract types.",
    ]
    st.markdown("\n".join(f"- {bullet}" for bullet in bullets))


def _bar_chart(df: pd.DataFrame, column: str, n: int, horizontal: bool) -> go.Figure:
    data = top_counts(df, column, n)
    if horizontal:
        fig = px.bar(data, x="postings", y=column, orientation="h")
        fig.update_layout(yaxis_title="")
    else:
        fig = px.bar(data, x=column, y="postings")
        fig.update_layout(xaxis_title="")
    return fig


def _donut(df: pd.DataFrame, column: str) -> go.Figure:
    data = full_counts(df, column)
    return px.pie(data, names=column, values="postings", hole=0.55)


def _paired(builder, title: str, note: str | None = None) -> None:
    st.subheader(title)
    if note:
        st.caption(note)
    left, right = st.columns(2)
    for column, market in ((left, "Egypt"), (right, "Saudi Arabia")):
        fig = builder(DATA[market])
        fig.update_layout(height=340, margin=dict(l=0, r=0, t=30, b=0), title=market)
        column.plotly_chart(fig, use_container_width=True)


def comparison() -> None:
    st.title("Comparison: Egypt vs Saudi Arabia")
    st.caption("Same 9,514 cleaned postings, same collection window, same columns.")

    egypt, saudi = summary(DATA["Egypt"]), summary(DATA["Saudi Arabia"])

    rows = [
        ("Postings", f"{int(egypt['postings']):,}", f"{int(saudi['postings']):,}"),
        ("Top city", egypt["top city"], saudi["top city"]),
        ("Top city share", f"{egypt['top city share']:.0%}", f"{saudi['top city share']:.0%}"),
        ("On-site", f"{egypt['on-site share']:.0%}", f"{saudi['on-site share']:.0%}"),
        ("Remote", f"{egypt['remote share']:.0%}", f"{saudi['remote share']:.0%}"),
        (
            "No gender preference",
            f"{egypt['no gender preference']:.0%}",
            f"{saudi['no gender preference']:.0%}",
        ),
        (
            "Job level stated",
            f"{egypt['level stated']:.0%}",
            f"{saudi['level stated']:.0%}",
        ),
        ("Unknown job type", f"{egypt['unknown job type']:.0%}", f"{saudi['unknown job type']:.0%}"),
        (
            "Experience stated",
            f"{egypt['experience stated']:.0%}",
            f"{saudi['experience stated']:.0%}",
        ),
        (
            "Median min. experience",
            f"{egypt['median min experience']:.0f} yrs",
            f"{saudi['median min experience']:.0f} yrs",
        ),
    ]
    st.dataframe(
        pd.DataFrame(rows, columns=["metric", "Egypt", "Saudi Arabia"]),
        hide_index=True,
        height=390,
    )

    st.divider()
    _paired(lambda df: _bar_chart(df, "city", 8, True), "Job distribution by city")
    _paired(lambda df: _bar_chart(df, "company_name", 10, True), "Postings by company")
    _paired(lambda df: _bar_chart(df, "title", 10, True), "Most common job titles")
    _paired(lambda df: _donut(df, "remote"), "Work arrangement")
    _paired(lambda df: _bar_chart(df, "gender", 3, False), "Gender preference")
    _paired(lambda df: _bar_chart(df, "job_level", 8, False), "Job level")

    st.subheader("Postings over time")
    left, right = st.columns(2)
    for column, market in ((left, "Egypt"), (right, "Saudi Arabia")):
        fig = px.line(monthly_postings(DATA[market]), x="month", y="postings", markers=True)
        fig.update_layout(
            height=340, margin=dict(l=0, r=0, t=30, b=0), title=market, xaxis_title=""
        )
        column.plotly_chart(fig, use_container_width=True)

    _paired(lambda df: _bar_chart(df, "industry_", 8, True), "Postings by industry")
    _paired(lambda df: _donut(df, "type"), "Job type")
    _paired(
        lambda df: px.box(experience_frame(df), x="requirement", y="years"),
        "Experience requirements",
        "Only a minority of postings state a number, so read the boxes as a sample.",
    )

    st.subheader("Jobs by city and job level")
    left, right = st.columns(2)
    for column, market in ((left, "Egypt"), (right, "Saudi Arabia")):
        fig = px.imshow(
            city_level_matrix(DATA[market]),
            aspect="auto",
            text_auto=True,
            color_continuous_scale="Blues",
        )
        fig.update_layout(
            height=360, margin=dict(l=0, r=0, t=30, b=0), title=market, coloraxis_showscale=False
        )
        column.plotly_chart(fig, use_container_width=True)

    st.subheader("Most common job titles")
    market = st.radio("Word cloud market", ["Egypt", "Saudi Arabia"], horizontal=True)
    if st.toggle("Render word cloud"):
        st.image(wordcloud_image(DATA[market]), use_container_width=True)

    st.divider()
    st.subheader("Where the two markets differ")
    onsite_gap = saudi["on-site share"] - egypt["on-site share"]
    bullets = [
        f"**Both markets are capital-heavy**, but Riyadh spreads wider than Cairo: "
        f"{egypt['top city share']:.0%} of Egyptian postings are in {egypt['top city']}, "
        f"against {saudi['top city share']:.0%} of Saudi postings in {saudi['top city']}.",
        f"**Saudi Arabia is more office-bound**: {onsite_gap:+.0%} on-site than Egypt "
        f"({saudi['on-site share']:.0%} against {egypt['on-site share']:.0%}).",
        f"**Egypt publishes seniority far more often**: job level is stated in "
        f"{egypt['level stated']:.0%} of Egyptian postings but only {saudi['level stated']:.0%} "
        f"of Saudi ones, so a seniority comparison would mostly measure missing data.",
        f"**Job type is unusable in both**: Unknown for {egypt['unknown job type']:.0%} and "
        f"{saudi['unknown job type']:.0%} of postings, which rules out a contract-type comparison.",
        f"**Experience is too sparse to compare**: only {egypt['experience stated']:.0%} and "
        f"{saudi['experience stated']:.0%} of postings state a minimum, so the medians "
        f"({egypt['median min experience']:.0f} and {saudi['median min experience']:.0f} years) "
        f"describe a small subset rather than each market.",
    ]
    st.markdown("\n".join(f"- {bullet}" for bullet in bullets))


def main() -> None:
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select Page", PAGES)

    if page == "Home":
        home()
    elif page == "Egypt Market":
        market_page("Egypt")
    elif page == "Saudi Market":
        market_page("Saudi Arabia")
    else:
        comparison()

    st.divider()
    st.caption("Created by DataMentes Team | Job Market Analysis Tool")


if __name__ == "__main__":
    main()
