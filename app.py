"""India Food Commodity Insights Monitor - Streamlit entry point.  Run:  streamlit run app.py"""
import hashlib
import pathlib
import sys
import zipfile

# Simple-upload mode: the code and data folders arrive packed in bundle.zip. Unpack on first start, and again
# whenever a different bundle.zip is uploaded (its fingerprint is remembered in .bundle_hash).
_root = pathlib.Path(__file__).resolve().parent
_bundle, _mark = _root / "bundle.zip", _root / ".bundle_hash"
if _bundle.exists():
    _h = hashlib.sha1(_bundle.read_bytes()).hexdigest()
    if not (_root / "fci").exists() or (_mark.read_text() if _mark.exists() else "") != _h:
        with zipfile.ZipFile(_bundle) as _z:
            _z.extractall(_root)
        _mark.write_text(_h)
        for _name in [n for n in sys.modules if n.split(".")[0] in ("fci", "views")]:
            del sys.modules[_name]  # make a running server use the newly unpacked code

import streamlit as st

st.set_page_config(page_title="India Food Commodity Insights Monitor", page_icon="🌾", layout="wide")

from fci import autoload, ui  # noqa: E402
from views import alerts, commodity, geography, insights, newsmap, newsroom, overview, policy, sources  # noqa: E402

st.markdown(ui.CSS, unsafe_allow_html=True)
st.session_state["_card_n"] = 0

PAGES = [
    st.Page(overview.page, title="India Overview", icon="🇮🇳", url_path="overview", default=True),
    st.Page(alerts.page, title="Price Alerts", icon="🚨", url_path="alerts"),
    st.Page(commodity.page, title="Commodity Explorer", icon="📈", url_path="commodity"),
    st.Page(geography.page, title="State & District Explorer", icon="🗺️", url_path="geography"),
    st.Page(newsmap.page, title="India News Map", icon="📍", url_path="newsmap"),
    st.Page(newsroom.page, title="Local Market News", icon="📰", url_path="news"),
    st.Page(policy.page, title="Policy & International Developments", icon="🏛️", url_path="policy"),
    st.Page(insights.page, title="Weekly & Monthly Insights", icon="📝", url_path="insights"),
    st.Page(sources.page, title="Data Upload & Fetch", icon="🗄️", url_path="sources"),
]
nav = st.navigation(PAGES)
st.sidebar.markdown("## 🌾 India Food Commodity Insights Monitor")

load = autoload.start_if_needed()
st.session_state["agmarknet_load"] = load
df = ui.prices()
filtered, chosen = ui.sidebar_filters(df)
st.session_state["ctx"] = {"all": df, "df": filtered, "filters": chosen}
nat = df[df["level"] == "national"]
mandi = df[df["level"] != "national"]
st.sidebar.divider()
st.sidebar.caption(
    f"All-India retail prices to **{nat['date'].max():%d %b %Y}**" if len(nat) else "No all-India data loaded")
st.sidebar.caption(
    (f"Mandi prices to **{mandi[mandi['grade'] == 'Monthly average']['date'].max():%B %Y}**" if (mandi["grade"] == "Monthly average").any() else "Mandi prices loading")
    if len(mandi) else "No mandi data loaded")
nav.run()
