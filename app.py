"""India Food Commodity Insights Monitor - Streamlit entry point.  Run:  streamlit run app.py"""
import pathlib
import zipfile

# First start after a simple upload: the code and data folders arrive packed in bundle.zip; unpack them once.
_root = pathlib.Path(__file__).resolve().parent
if (_root / "bundle.zip").exists() and not (_root / "fci").exists():
    with zipfile.ZipFile(_root / "bundle.zip") as _z:
        _z.extractall(_root)

import streamlit as st

st.set_page_config(page_title="India Food Commodity Insights Monitor", page_icon="🌾", layout="wide")

from fci import ui  # noqa: E402
from views import alerts, commodity, geography, insights, newsmap, newsroom, overview, policy, sources  # noqa: E402

st.markdown("""<style>
.block-container{padding-top:2.2rem;max-width:1500px}
[data-testid="stMetricValue"]{font-size:1.5rem}
h1{font-size:1.7rem!important} h2{font-size:1.25rem!important} h3{font-size:1.05rem!important}
</style>""", unsafe_allow_html=True)

PAGES = [
    st.Page(overview.page, title="India Overview", icon="🇮🇳", url_path="overview", default=True),
    st.Page(alerts.page, title="Price Alerts", icon="🚨", url_path="alerts"),
    st.Page(commodity.page, title="Commodity Explorer", icon="📈", url_path="commodity"),
    st.Page(geography.page, title="State & District Explorer", icon="🗺️", url_path="geography"),
    st.Page(newsmap.page, title="India News Map", icon="📍", url_path="newsmap"),
    st.Page(newsroom.page, title="Local Market News", icon="📰", url_path="news"),
    st.Page(policy.page, title="Policy & International Developments", icon="🏛️", url_path="policy"),
    st.Page(insights.page, title="Weekly & Monthly Insights", icon="📝", url_path="insights"),
    st.Page(sources.page, title="Data Sources & Uploads", icon="🗄️", url_path="sources"),
]
nav = st.navigation(PAGES)
st.sidebar.markdown("## 🌾 India Food Commodity Insights Monitor")

df = ui.prices()
filtered, chosen = ui.sidebar_filters(df)
st.session_state["ctx"] = {"all": df, "df": filtered, "filters": chosen}
nat = df[df["level"] == "national"]
mandi = df[df["level"] != "national"]
st.sidebar.divider()
st.sidebar.caption(
    f"All-India (DoCA) data to **{nat['date'].max():%d %b %Y}**" if len(nat) else "No all-India data loaded")
st.sidebar.caption(
    (f"Mandi data to **{mandi['date'].max():%d %b %Y}**" + (" — SAMPLE" if mandi["is_sample"].any() else ""))
    if len(mandi) else "No mandi data loaded")
nav.run()
