
import re

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="IMDb Movie Analytics",
    page_icon="🎬",
    layout="wide",
)

TOP_N_GENRES = 6  # number of genres shown in the "Movies by Genre" chart

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown(
    """
<style>
/* ---------- base ---------- */
.stApp { background-color: #0b1322; color: white; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 100%; }
hr { border-color: #1f2d45 !important; margin: 0.8rem 0 !important; }
[data-testid="stWidgetLabel"] p { font-size: 12px; color: #cbd5e1; }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1a2c, #16243a);
    border-right: 1px solid #1f2d45;
}
[data-testid="stSidebar"] * { color: white; }
.imdb-logo {
    display: inline-block; background: #f5c518; color: #000 !important;
    font-weight: 900; font-size: 30px; padding: 2px 16px; border-radius: 6px;
    margin-top: 6px;
}
.side-title { font-size: 22px; font-weight: 800; line-height: 1.2; margin: 10px 0 8px 0; }
[data-testid="stSidebar"] div[role="radiogroup"] { gap: 6px; }
[data-testid="stSidebar"] div[role="radiogroup"] label {
    padding: 10px 12px; border-radius: 8px; width: 100%; margin: 0;
}
[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child { display: none; }
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) { background: #1976d2; }
[data-testid="stSidebar"] div[role="radiogroup"] p { font-size: 13px; line-height: 1.3; }
[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: #16243a; border: 1px solid #25344d; border-radius: 10px;
}
.side-note { font-size: 12px; color: #cbd5e1 !important; }

/* ---------- hero banner ---------- */
.hero {
    display: flex; align-items: center; justify-content: space-between;
    padding: 18px 40px; border-radius: 12px; border: 1px solid #2f3d55; margin-bottom: 16px;
    background:
        radial-gradient(circle at 10% 40%, rgba(255,170,60,.38), transparent 26%),
        radial-gradient(circle at 90% 40%, rgba(255,170,60,.32), transparent 26%),
        linear-gradient(90deg, #1c1713, #101a2e 50%, #1c1713);
}
.hero .emoji { font-size: 62px; filter: drop-shadow(0 4px 8px rgba(0,0,0,.6)); }
.hero .center { text-align: center; }
.hero h1 { color: white; font-size: 32px; font-weight: 800; margin: 0; padding: 0; }
.hero p { color: #e5e7eb; font-size: 18px; margin: 4px 0 0 0; }

/* ---------- KPI cards ---------- */
.kpi {
    display: flex; align-items: center; gap: 16px; padding: 14px 20px;
    border-radius: 12px; color: white; min-height: 84px; margin-bottom: 10px;
}
.kpi-icon {
    font-size: 32px; width: 54px; height: 54px; display: flex;
    align-items: center; justify-content: center;
    background: rgba(255,255,255,.18); border-radius: 12px;
}
.kpi-label { font-size: 14px; font-weight: 600; opacity: .95; }
.kpi-value { font-size: 28px; font-weight: 800; line-height: 1.1; }
.blue   { background: linear-gradient(120deg,#1782dc,#1558a8); }
.green  { background: linear-gradient(120deg,#2ab876,#0a8a50); }
.purple { background: linear-gradient(120deg,#8f4ade,#6429ad); }
.orange { background: linear-gradient(120deg,#ff9f1c,#ee6c00); }

/* ---------- tabs ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: none; background: transparent; }
.stTabs [data-baseweb="tab"] {
    background: #16233a; border-radius: 8px; padding: 8px 20px; height: auto; color: #cbd5e1;
}
.stTabs [aria-selected="true"] { background: #1d78d8; color: white; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

/* ---------- white chart cards ---------- */
div[class*="st-key-chartcard"] {
    background: #ffffff; border-radius: 10px; padding: 10px 12px 2px 12px;
    border: 1px solid #d7dee9;
}
.chart-head { color: #1f2937; font-weight: 700; font-size: 15px; padding: 2px 0 0 4px; }

/* ---------- dark panels ---------- */
div[class*="st-key-darkcard"] {
    background: #111c2f; border: 1px solid #2a3a55; border-radius: 10px; padding: 14px 16px;
}
div[class*="st-key-searchcard"] {
    background: #111c2f; border: 1px solid #7c3aed; border-radius: 10px; padding: 14px 16px;
}
.panel-head { font-size: 18px; font-weight: 700; margin-bottom: 8px; }
.badge {
    display: inline-block; background: #1d78d8; color: white; font-weight: 700;
    font-size: 13px; padding: 7px 14px; border-radius: 8px;
}
[data-testid="stForm"] { border: none; padding: 0; }
[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(90deg,#7c3aed,#6d28d9); color: white; border: none;
    border-radius: 8px; font-weight: 600;
}
.stButton button { border-radius: 8px; }

.result-card {
    display: flex; align-items: center; gap: 14px; margin-top: 10px;
    background: #1b2a44; border: 1px solid #2f4468; border-radius: 10px; padding: 10px 14px;
}
.result-card .poster {
    font-size: 30px; width: 46px; height: 60px; display: flex; align-items: center;
    justify-content: center; background: #0b1322; border-radius: 6px; overflow: hidden;
}
.result-card .poster img { width: 100%; height: 100%; object-fit: cover; }
.result-card .rt { font-size: 17px; font-weight: 700; }
.result-card .rs { font-size: 12px; color: #cbd5e1; }
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# DATASET LOADING
# ==========================================


@st.cache_data
def load_data():
    return pd.read_csv("ToP 250 movies on imdb in 2026.csv")


try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# ==========================================
# FIND DATASET COLUMNS
# ==========================================


def find_column(possible_names):
    normalized = {
        re.sub(r"[^a-z0-9]", "", str(col).lower()): col for col in df.columns
    }
    for name in possible_names:
        key = re.sub(r"[^a-z0-9]", "", name.lower())
        if key in normalized:
            return normalized[key]
    return None


title_col = find_column(["primaryTitle", "title", "movieTitle", "originalTitle"])
genre_col = find_column(["genres", "genre"])
country_col = find_column(["countriesOfOrigin", "country", "countries", "origin"])
rating_col = find_column(["averageRating", "imdbRating", "rating"])
votes_col = find_column(["numVotes", "votes", "numberOfVotes"])
gross_col = find_column(["grossWorldwide", "worldwideGross", "gross"])
poster_col = find_column(["posterUrl", "poster", "image", "imageUrl", "thumbnail"])

if not all([title_col, genre_col, rating_col, votes_col]):
    st.error(
        "Required columns are missing. Check your CSV column names: "
        + str(df.columns.tolist())
    )
    st.stop()

# ==========================================
# DATA CLEANING
# ==========================================

df[rating_col] = pd.to_numeric(df[rating_col], errors="coerce")
df[votes_col] = pd.to_numeric(df[votes_col], errors="coerce")

if gross_col:
    df[gross_col] = pd.to_numeric(
        df[gross_col].astype(str).str.replace(r"[$,]", "", regex=True),
        errors="coerce",
    )


def split_values(value):
    if isinstance(value, list):
        return [str(x).strip() for x in value]
    if pd.isna(value):
        return []
    return [
        x.strip().strip("[]'\"") for x in str(value).split(",") if x.strip()
    ]


ALL_GENRES = sorted(
    {v for vals in df[genre_col].dropna().apply(split_values) for v in vals}
)
ALL_COUNTRIES = (
    sorted({v for vals in df[country_col].dropna().apply(split_values) for v in vals})
    if country_col
    else []
)


def fmt_gross(v):
    if pd.isna(v):
        return "—"
    if v >= 1e9:
        return f"${v / 1e9:.2f}B"
    return f"${v / 1e6:.0f}M"


def build_table(data):
    """Display-friendly version of a (filtered) DataFrame, numbered from 1."""
    t = pd.DataFrame({"Title": data[title_col].values})
    t["Genre"] = data[genre_col].apply(lambda x: ", ".join(split_values(x))).values
    if country_col:
        t["Country"] = data[country_col].apply(lambda x: ", ".join(split_values(x))).values
    t["IMDb Rating"] = data[rating_col].values
    t["Votes"] = data[votes_col].apply(
        lambda v: "—" if pd.isna(v) else f"{v:,.0f}"
    ).values
    if gross_col:
        t["Worldwide Gross"] = data[gross_col].apply(fmt_gross).values
    t.index = range(1, len(t) + 1)
    t.index.name = "#"
    return t


# ==========================================
# UI HELPERS
# ==========================================


def hero(title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
            <div class="emoji">🍿</div>
            <div class="center"><h1>{title}</h1><p>{subtitle}</p></div>
            <div class="emoji">🎬</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi(cls, icon, label, value):
    return (
        f'<div class="kpi {cls}"><div class="kpi-icon">{icon}</div>'
        f'<div><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div></div></div>'
    )


def style_light(fig, height=270):
    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1f2937", size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
    )
    return fig


def chart_card(key, heading, fig):
    with st.container(key=f"chartcard_{key}"):
        st.markdown(f'<div class="chart-head">{heading}</div>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.markdown(
    """
    <div class="imdb-logo">IMDb</div>
    <div class="side-title">Movie Analytics<br>Dashboard</div>
    """,
    unsafe_allow_html=True,
)

NAV_LABELS = {
    "Dashboard": "🏠  Dashboard",
    "Movie Explorer": "🔍  Movie Explorer",
    "Movie Search": "🔎  Movie Search  \n(Form + Session State)",
}

page = st.sidebar.radio(
    "Navigation",
    list(NAV_LABELS.keys()),
    format_func=lambda k: NAV_LABELS[k],
    label_visibility="collapsed",
)

st.sidebar.divider()

with st.sidebar.expander("📁 Dataset Information", expanded=True):
    st.markdown("**Top 250 Movies on IMDb (2026)**")
    st.markdown(f"Rows: **{df.shape[0]}**  \nColumns: **{df.shape[1]}**")
    st.markdown(
        '<div class="side-note">This dataset contains information about the top '
        "250 movies, including titles, rating, votes, genres and worldwide gross.</div>",
        unsafe_allow_html=True,
    )

# ==========================================
# MOVIE EXPLORER (reusable block)
# ==========================================

EXPLORER_DEFAULTS = {
    "genre_filter": "All",
    "country_filter": [],
    "rating_filter": (0.0, 10.0),
    "votes_filter": 0,
    "title_filter": "",
    "sort_filter": "Descending",
}


def reset_filters():
    for k, v in EXPLORER_DEFAULTS.items():
        st.session_state[k] = v


def render_explorer(table_height=190):
    for k, v in EXPLORER_DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v

    st.markdown('<div class="panel-head">🔽 Interactive Movie Explorer</div>', unsafe_allow_html=True)

    f1, f2, f3, f4, f5, f6 = st.columns([1, 1.3, 1.5, 1, 1.3, 1])

    with f1:
        selected_genre = st.selectbox("Genre", ["All"] + ALL_GENRES, key="genre_filter")
    with f2:
        selected_countries = st.multiselect("Countries", ALL_COUNTRIES, key="country_filter")
    with f3:
        rating_range = st.slider("IMDb Rating", 0.0, 10.0, step=0.1, key="rating_filter")
    with f4:
        min_votes = st.number_input("Min Votes", min_value=0, step=10000, key="votes_filter")
    with f5:
        search_title = st.text_input(
            "Search Title", placeholder="Enter movie title...", key="title_filter"
        )
    with f6:
        sort_order = st.radio("Sort Order", ["Ascending", "Descending"], key="sort_filter")

    # ----- apply all filters to the same DataFrame -----
    filtered_df = df.copy()

    if selected_genre != "All":
        filtered_df = filtered_df[
            filtered_df[genre_col].apply(lambda x: selected_genre in split_values(x))
        ]

    if selected_countries and country_col:
        filtered_df = filtered_df[
            filtered_df[country_col].apply(
                lambda x: any(c in split_values(x) for c in selected_countries)
            )
        ]

    filtered_df = filtered_df[
        filtered_df[rating_col].between(rating_range[0], rating_range[1])
    ]
    filtered_df = filtered_df[filtered_df[votes_col] >= min_votes]

    if search_title:
        filtered_df = filtered_df[
            filtered_df[title_col].str.contains(search_title, case=False, na=False)
        ]

    filtered_df = filtered_df.sort_values(
        rating_col, ascending=(sort_order == "Ascending")
    )

    b1, b2, _ = st.columns([1.3, 1, 4])
    with b1:
        st.markdown(
            f'<span class="badge">Filtered Movies: {len(filtered_df)}</span>',
            unsafe_allow_html=True,
        )
    with b2:
        st.button("🔄 Reset Filters", on_click=reset_filters)

    st.dataframe(build_table(filtered_df), use_container_width=True, height=table_height)


# ==========================================
# MOVIE SEARCH (reusable block)
# ==========================================


def render_search():
    st.markdown(
        '<div class="panel-head">🔎 Movie Search (Form + Session State)</div>',
        unsafe_allow_html=True,
    )

    if "selected_movie" not in st.session_state:
        st.session_state.selected_movie = None

    with st.form("movie_search_form"):
        movie_name = st.text_input("Movie Title", placeholder="e.g. Inception")
        preferred_genre = st.selectbox("Preferred Genre", ["All"] + ALL_GENRES)
        min_rating = st.slider("Minimum IMDb Rating", 0.0, 10.0, 8.0, step=0.1)
        submitted = st.form_submit_button("🔍 Search Movie", use_container_width=True)

    if submitted:
        search_df = df.copy()

        if movie_name:
            search_df = search_df[
                search_df[title_col].str.contains(movie_name, case=False, na=False)
            ]
        if preferred_genre != "All":
            search_df = search_df[
                search_df[genre_col].apply(lambda x: preferred_genre in split_values(x))
            ]
        search_df = search_df[search_df[rating_col] >= min_rating]

        if not search_df.empty:
            st.session_state.selected_movie = (
                search_df.sort_values(rating_col, ascending=False).iloc[0].to_dict()
            )
        else:
            st.session_state.selected_movie = None

    movie = st.session_state.selected_movie

    if movie is not None:
        st.success("Movie found successfully!")

        poster = movie.get(poster_col) if poster_col else None
        poster_html = (
            f'<img src="{poster}">' if isinstance(poster, str) and poster.startswith("http") else "🎬"
        )
        votes = movie[votes_col]
        votes_txt = "—" if pd.isna(votes) else f"{votes:,.0f}"
        st.markdown(
            f"""
            <div class="result-card">
                <div class="poster">{poster_html}</div>
                <div>
                    <div class="rt">{movie[title_col]}</div>
                    <div class="rs">Genre: {", ".join(split_values(movie[genre_col]))}
                    &nbsp;|&nbsp; IMDb Rating: {movie[rating_col]}
                    &nbsp;|&nbsp; Votes: {votes_txt}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif submitted:
        st.info("No matching movie found.")
    else:
        st.info("Enter your movie preferences and click Search Movie.")


# ==========================================
# PAGE 1: DASHBOARD
# ==========================================

if page == "Dashboard":

    hero("IMDb Movie Analytics Dashboard", "Explore. Analyze. Discover.")

    # ----- KPI metrics -----
    total_movies = len(df)
    avg_rating = df[rating_col].mean()
    highest_rating = df[rating_col].max()
    total_votes = df[votes_col].sum()

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi("blue", "🎬", "Total Movies", f"{total_movies:,}"), unsafe_allow_html=True)
    k2.markdown(kpi("green", "⭐", "Average IMDb Rating", f"{avg_rating:.1f}"), unsafe_allow_html=True)
    k3.markdown(kpi("purple", "🏆", "Highest Rating", f"{highest_rating:.1f}"), unsafe_allow_html=True)
    k4.markdown(kpi("orange", "👥", "Total Votes", f"{total_votes:,.0f}"), unsafe_allow_html=True)

    # ----- data for charts -----
    genre_counts = (
        df[genre_col].dropna().apply(split_values).explode().value_counts().reset_index()
    )
    genre_counts.columns = ["Genre", "Count"]

    top_movies = None
    if gross_col:
        top_movies = df.dropna(subset=[gross_col]).sort_values(gross_col, ascending=False).head(10)

    tab1, tab2, tab3 = st.tabs(
        ["📊 Genre Analysis", "🥧 Rating Analysis", "💰 Gross Collection"]
    )

    # ===== TAB 1: the 2x2 chart grid =====
    with tab1:
        c1, c2 = st.columns(2)

        # 1) Movies by genre
        with c1:
            top_g = genre_counts.head(TOP_N_GENRES)
            palette = ["#1f7fd6", "#27ae60", "#ff9f1c", "#8e44ad", "#ff9f1c", "#ff9f1c"]
            fig1 = px.bar(top_g, x="Genre", y="Count", text="Count")
            fig1.update_traces(
                marker_color=palette[: len(top_g)],
                textposition="outside",
                textfont=dict(size=12, color="#1f2937"),
            )
            fig1.update_yaxes(range=[0, top_g["Count"].max() * 1.18], title="Count")
            style_light(fig1)
            chart_card("genre", "📊 Movies by Genre", fig1)

        # 2) Rating distribution
        with c2:
            fig2 = px.histogram(df, x=rating_col, nbins=16)
            fig2.update_traces(
                marker_color="#2b8cf0", marker_line_color="white", marker_line_width=1
            )
            fig2.update_layout(xaxis_title="IMDb Rating", yaxis_title="Count", bargap=0.05)
            style_light(fig2)
            chart_card("hist", "📊 IMDb Rating Distribution", fig2)

        c3, c4 = st.columns(2)

        # 3) Rating vs votes
        with c3:
            fig3 = px.scatter(df, x=rating_col, y=votes_col, hover_name=title_col)
            fig3.update_traces(marker=dict(color="#2b8cf0", size=6, opacity=0.85))
            fig3.update_yaxes(type="log", title="Number of Votes")
            fig3.update_xaxes(title="IMDb Rating")
            style_light(fig3)
            chart_card("scatter", "🔹 Rating vs Number of Votes", fig3)

        # 4) Top 10 worldwide gross
        with c4:
            if top_movies is not None and not top_movies.empty:
                tm = top_movies.copy()
                tm["label"] = tm[gross_col].apply(fmt_gross)
                fig4 = px.bar(
                    tm, x=gross_col, y=title_col, orientation="h", text="label"
                )
                fig4.update_traces(
                    marker_color="#ff9f1c",
                    textposition="outside",
                    textfont=dict(size=11, color="#1f2937"),
                    cliponaxis=False,
                )
                max_g = tm[gross_col].max()
                ticks = np.arange(0, max_g * 1.15, 5e8)
                fig4.update_xaxes(
                    title="Worldwide Gross (USD)",
                    tickvals=ticks,
                    ticktext=[f"{t / 1e9:.1f}B" for t in ticks],
                    range=[0, max_g * 1.25],
                )
                fig4.update_yaxes(title="", categoryorder="total ascending")
                style_light(fig4)
                chart_card("gross", "🏆 Top 10 Movies by Worldwide Gross", fig4)
            else:
                st.warning("Worldwide gross column not found.")

    # ===== TAB 2: rating analysis =====
    with tab2:
        r1, r2, r3 = st.columns(3)
        r1.metric("Average Rating", round(avg_rating, 2))
        r2.metric("Highest Rating", highest_rating)
        r3.metric("Lowest Rating", df[rating_col].min())
        st.markdown("**Full genre counts**")
        st.dataframe(genre_counts, use_container_width=True, height=250)

    # ===== TAB 3: gross collection =====
    with tab3:
        if top_movies is not None:
            st.dataframe(
                top_movies[[title_col, gross_col]].rename(
                    columns={title_col: "Title", gross_col: "Worldwide Gross (USD)"}
                ),
                use_container_width=True,
            )
        else:
            st.warning("Worldwide gross column not found.")

    # ----- success message -----
    st.success("Dashboard loaded successfully! Enjoy exploring the top 250 movies on IMDb.")

    # ----- Explorer + Search side by side -----
    left, right = st.columns([2.1, 1])
    with left:
        with st.container(key="darkcard_explorer"):
            render_explorer(table_height=190)
    with right:
        with st.container(key="searchcard_search"):
            render_search()

    st.divider()

    with st.expander("View Complete Dataset Information"):
        st.write("First 10 records:")
        st.dataframe(df.head(10), use_container_width=True)
        st.write("Rows:", df.shape[0], " | Columns:", df.shape[1])
        st.write("Column Names:", df.columns.tolist())
        st.write("Data Types:")
        st.write(df.dtypes.astype(str))
        st.write("Missing Values:")
        st.write(df.isnull().sum())

# ==========================================
# PAGE 2: MOVIE EXPLORER
# ==========================================

elif page == "Movie Explorer":
    hero("🔍 Interactive Movie Explorer", "Search, filter and sort IMDb movies.")
    with st.container(key="darkcard_explorer_full"):
        render_explorer(table_height=480)

# ==========================================
# PAGE 3: MOVIE SEARCH
# ==========================================

elif page == "Movie Search":
    hero("🎬 Movie Search", "Find movies using your preferred information.")
    _, mid, _ = st.columns([1, 1.6, 1])
    with mid:
        with st.container(key="searchcard_full"):
            render_search()