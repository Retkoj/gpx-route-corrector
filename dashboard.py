import os

import streamlit as st
import pydeck as pdk

from read_gpx import get_gpx_points

st.header('GPX')

data_path = './data/'
files = os.listdir(data_path)
file_name = st.selectbox('Selecteer een GPX bestand', files)
file_path = os.path.join(data_path, file_name)
df = get_gpx_points(file_path)

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(#compute_view(df['latitude'], df[; ])
    #     (df)     #
        latitude=df['latitude'][0],
        longitude=df['longitude'][0],
        zoom=11,
        # pitch=50,
    ),
    layers=[
        pdk.Layer(
            'Hexagonlayer',
            data=df,
            get_position='[longitude, latitude]',
            radius=10,
            # elevation_scale=4,
            # elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
        pdk.Layer(
            "ScatterplotLayer",
            df,
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=6,
            radius_min_pixels=1,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_position='[longitude, latitude]',
            get_radius="exits_radius",
            get_fill_color=[255, 140, 0],
            get_line_color=[0, 0, 0],
            # 'ScatterplotLayer',
            # data=df,
            # get_position='[longitude, latitude]',
            # get_color='[200, 30, 0, 160]',
            # get_radius=10,
        ),
    ],
    tooltip={"text": "lat: {latitude}\nlon: {longitude}\nTime: {timestamp}"}
))
