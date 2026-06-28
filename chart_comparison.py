import streamlit as st
from nba_api.stats.endpoints import shotchartdetail, commonallplayers
import matplotlib.pyplot as plt
from draw_court import draw_court
from matplotlib.patches import Circle, Rectangle, Arc
import pandas as pd
import numpy as np
import time

st.set_page_config(layout="wide", page_title="NBA Shot Chart", page_icon="🏀")

# --- Custom CSS ---
st.markdown("""
    <style>
        /* Main background */
        .stApp {
            background-color: #0e1117;
        }

        /* Title */
        h1 {
            color: #ffffff;
            font-family: 'Arial Black', sans-serif;
            font-size: 2.2rem;
            letter-spacing: 1px;
            padding-bottom: 0.2rem;
        }

        /* Dropdown labels */
        label {
            color: #aaaaaa !important;
            font-size: 0.85rem !important;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        /* Dropdown box */
        .stSelectbox > div > div {
            background-color: #1e2130 !important;
            color: #ffffff !important;
            border: 1px solid #2e3250 !important;
            border-radius: 8px !important;
        }

        /* Metric labels */
        [data-testid="stMetricLabel"] {
            color: #aaaaaa !important;
            font-size: 0.8rem !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Metric values */
        [data-testid="stMetricValue"] {
            color: #ffffff !important;
            font-size: 1.8rem !important;
            font-weight: 700;
        }

        /* Divider */
        hr {
            border-color: #2e3250 !important;
        }

        /* Remove default padding */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("# 🏀 NBA Shot Chart Comparison")
st.markdown("<p style='color:#aaaaaa; margin-top:-10px; font-size:0.95rem;'>2025–26 Regular Season</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Player List ---
@st.cache_data
def get_all_players():
    all_players = commonallplayers.CommonAllPlayers(
        is_only_current_season=0,
        league_id='00',
        season='2025-26'
    ).get_data_frames()[0]
    all_players = all_players[
        (all_players['GAMES_PLAYED_FLAG'] == 'Y') &
        (all_players['TO_YEAR'] == '2026')
    ]
    return all_players[['PERSON_ID', 'DISPLAY_FIRST_LAST']].sort_values('DISPLAY_FIRST_LAST').reset_index(drop=True)

# --- Shot Data ---
@st.cache_data
def get_shot_data(player_id):
    time.sleep(1)
    shotchart = shotchartdetail.ShotChartDetail(
        team_id=0,
        player_id=player_id,
        season_nullable='2025-26',
        season_type_all_star='Regular Season',
        context_measure_simple='FGA'
    ).get_data_frames()[0]
    shotchart['LOC_X_FT'] = shotchart['LOC_X'] / 10
    shotchart['LOC_Y_FT'] = shotchart['LOC_Y'] / 10
    shotchart = shotchart[shotchart['LOC_Y_FT'] <= 50]
    return shotchart

# --- Plot Function ---
def plot_shot_chart(ax, df, player_name):
    made = df[df['SHOT_MADE_FLAG'] == 1]
    missed = df[df['SHOT_MADE_FLAG'] == 0]
    draw_court(ax)
    ax.scatter(missed['LOC_X_FT'], missed['LOC_Y_FT'], c='red', alpha=0.4, s=15, label='Missed')
    ax.scatter(made['LOC_X_FT'], made['LOC_Y_FT'], c='green', alpha=0.4, s=15, label='Made')
    ax.set_xlim(-25, 25)
    ax.set_ylim(0, 50)
    ax.legend(loc='upper right', fontsize=11)
    ax.set_title(f"{player_name}", fontsize=14, fontweight='bold', pad=10)
    ax.set_xlabel("Horizontal Position (feet)", fontsize=11)
    ax.set_ylabel("Distance from Basket (feet)", fontsize=11)
    ax.tick_params(labelsize=10)

# --- Player Selection ---
all_players = get_all_players()
player_list = all_players['DISPLAY_FIRST_LAST'].tolist()

col1, spacer, col2 = st.columns([10, 1, 10])
with col1:
    player1_name = st.selectbox("Select Player 1", player_list, index=0)
    player1_id = all_players[all_players['DISPLAY_FIRST_LAST'] == player1_name]['PERSON_ID'].values[0]
with col2:
    player2_name = st.selectbox("Select Player 2", player_list, index=1)
    player2_id = all_players[all_players['DISPLAY_FIRST_LAST'] == player2_name]['PERSON_ID'].values[0]

# --- Fetch Data ---
df1 = get_shot_data(player1_id)
df2 = get_shot_data(player2_id)

# --- Two separate figures side by side ---
col1, spacer, col2 = st.columns([10, 1, 10])

with col1:
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    plot_shot_chart(ax1, df1, player1_name)
    plt.tight_layout()
    st.pyplot(fig1, use_container_width=True)
    plt.close(fig1)

with col2:
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    plot_shot_chart(ax2, df2, player2_name)
    plt.tight_layout()
    st.pyplot(fig2, use_container_width=True)
    plt.close(fig2)

# --- Stats row at the bottom ---
st.divider()
col1, spacer, col2 = st.columns([10, 1, 10])

with col1:
    made1 = df1[df1['SHOT_MADE_FLAG'] == 1]
    s1, s2 = st.columns(2)
    s1.metric("Total Shots", len(df1))
    s2.metric("FG%", f"{len(made1)/len(df1)*100:.1f}%")

with col2:
    made2 = df2[df2['SHOT_MADE_FLAG'] == 1]
    s1, s2 = st.columns(2)
    s1.metric("Total Shots", len(df2))
    s2.metric("FG%", f"{len(made2)/len(df2)*100:.1f}%")
