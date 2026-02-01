import os
import requests
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

BACKEND_ADDRESS = os.getenv("BACKEND_ADDRESS")
NEWS_URL = os.getenv('NEWS_URL')


if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode


st.set_page_config(
    page_title="Autó adatbázis",
    page_icon="🚗",
    layout="wide"
)


if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #1e1b2e;
            color: #e9d5ff;
        }
        div[data-testid="stDataFrame"] {
            background-color: #2a2540;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    theme_label = "🌙 Sötét mód"
else:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #e6fffa;
            color: #134e4a;
        }
        div[data-testid="stDataFrame"] {
            background-color: #ccfbf1;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    theme_label = "🌊 Világos mód"


st.button(f"{theme_label} váltása", on_click=toggle_theme)

st.markdown("## 🚗 Autó adatbázis dashboard")
st.markdown("Tárolt autók egy részének megjelenítése és tároló adatbázis módosítása")
st.divider()

resp = requests.get(f"{BACKEND_ADDRESS}/auto/get")
resp.raise_for_status()
data = resp.json()

df = pd.DataFrame(data["auto"])

st.markdown("### 📋 Autók listája")
st.dataframe(df, hide_index=True, use_container_width=True)

st.divider()
st.markdown("### ⚙️ Műveletek")

col1, col2 = st.columns(2)

# ADD
with col1:
    st.markdown("#### ➕ Autó hozzáadása")

    gyarto = st.text_input("Gyártó")
    modell = st.text_input("Modell")
    ajtok = st.number_input("Ajtók száma", min_value=2, max_value=5, step=1)
    uzemanyag = st.selectbox("Üzemanyag", ["Benzin", "Dízel"])
    henger = st.number_input("Hengerűrtartalom (cm³)", min_value=800, step=100)

    if st.button("➕ Hozzáadás", use_container_width=True):
        res = requests.post(
            f"{BACKEND_ADDRESS}/auto/add",
            json={
                "gyarto": gyarto,
                "modell": modell,
                "ajtok_szama": ajtok,
                "uzemanyag": uzemanyag,
                "hengerurtartalom": henger
            }
        )
        if res.status_code == 200:
            st.success("Autó sikeresen hozzáadva 🚘")
        else:
            st.error("Hiba történt a hozzáadás során")

# DELETE
with col2:
    st.markdown("#### 🗑️ Autó törlése")

    auto_id = st.number_input("Autó ID", min_value=1, step=1)
    if st.button("🗑️ Törlés", use_container_width=True):
        res = requests.delete(f"{BACKEND_ADDRESS}/auto/delete/{auto_id}")
        if res.status_code == 200:
            st.warning("Autó törölve")
        else:
            st.error("Nem sikerült törölni")

# GRAF
st.divider()
st.markdown("### 📊 Hengerűrtartalom modellenként")

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=df["modell"],
        y=df["hengerurtartalom"],
        marker_color="#7c3aed" if st.session_state.dark_mode else "#0d9488",
        name="Hengerűrtartalom (cm³)"
    )
)

fig.update_layout(
    height=500,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Modell",
    yaxis_title="Hengerűrtartalom (cm³)"
)

st.plotly_chart(fig, use_container_width=True)

page = requests.get(NEWS_URL)
soup = BeautifulSoup(page.text, "html.parser") 
articles = soup.find_all("article")

# st.write(articles)
st.subheader("Friss újdonságok a motor1.com íróitól")

for article in articles[:5]:
    #title
    title_elem = article.find('h2') or article.find('a', class_='newslink')
    title = title_elem.get_text(strip=True)
    st.write(title)
    
    #link
    link_elem = title_elem.find('a') if title_elem else article.find('a')
    link = link_elem['href'] if link_elem and 'href' in link_elem.attrs else ""
    if link and not link.startswith('http'):
        link = f"https://www.motor1.com{link}"
    st.write(link)
