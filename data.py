import time
import streamlit as st
from nba_api.stats.endpoints import shotchartdetail, commonallplayers

SEASON = '2025-26'


@st.cache_data
def get_all_players():
    df = commonallplayers.CommonAllPlayers(
        is_only_current_season=0,
        league_id='00',
        season=SEASON,
    ).get_data_frames()[0]
    df = df[(df['GAMES_PLAYED_FLAG'] == 'Y') & (df['TO_YEAR'] == '2026')]
    return (
        df[['PERSON_ID', 'DISPLAY_FIRST_LAST']]
        .sort_values('DISPLAY_FIRST_LAST')
        .reset_index(drop=True)
    )


@st.cache_data
def get_shot_data(player_id):
    time.sleep(1)
    df = shotchartdetail.ShotChartDetail(
        team_id=0,
        player_id=player_id,
        season_nullable=SEASON,
        season_type_all_star='Regular Season',
        context_measure_simple='FGA',
    ).get_data_frames()[0]
    df['LOC_X_FT'] = df['LOC_X'] / 10
    df['LOC_Y_FT'] = df['LOC_Y'] / 10
    return df[df['LOC_Y_FT'] <= 50]
