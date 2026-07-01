import streamlit as st

from data import get_all_players, get_shot_data
from template import render_compare_card

st.set_page_config(layout="wide", page_title="NBA Shot Chart", page_icon="🏀")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }

    h1 {
        color: #ffffff;
        font-family: 'Arial Black', sans-serif;
        font-size: 2.2rem;
        letter-spacing: 1px;
        padding-bottom: 0.2rem;
    }

    label {
        color: #aaaaaa !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    .stSelectbox > div > div {
        background-color: #1e2130 !important;
        color: #ffffff !important;
        border: 1px solid #2e3250 !important;
        border-radius: 8px !important;
    }

    hr { border-color: #2e3250 !important; }

    .block-container { padding-top: 2rem; padding-bottom: 2rem; }

    /* Expand the compare card iframe to fill the container */
    iframe.stIFrame { width: 100% !important; min-width: 100% !important; }
    .stElementContainer.element-container { width: 100% !important; max-width: 100% !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🏀 NBA Shot Chart Comparison")
st.markdown(
    "<p style='color:#aaaaaa; margin-top:-10px; font-size:0.95rem;'>2025–26 Regular Season</p>",
    unsafe_allow_html=True,
)
st.markdown("<br>", unsafe_allow_html=True)

all_players = get_all_players()
player_list = all_players['DISPLAY_FIRST_LAST'].tolist()

col1, _spacer, col2 = st.columns([10, 1, 10])
with col1:
    player1_name = st.selectbox("Select Player 1", player_list, index=0)
    player1_id = all_players.loc[all_players['DISPLAY_FIRST_LAST'] == player1_name, 'PERSON_ID'].values[0]
with col2:
    player2_name = st.selectbox("Select Player 2", player_list, index=1)
    player2_id = all_players.loc[all_players['DISPLAY_FIRST_LAST'] == player2_name, 'PERSON_ID'].values[0]

df1 = get_shot_data(player1_id)
df2 = get_shot_data(player2_id)

st.components.v1.html(
    render_compare_card(df1, player1_name, df2, player2_name),
    height=820,
    scrolling=False,
)
