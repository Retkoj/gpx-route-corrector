import os
from pathlib import Path

import streamlit as st
import pydeck as pdk

from correct_gpx import correct_gpx_file
from read_gpx import get_gpx_points

st.header('GPX')

data_path = './data/'
st.text(f'Put your GPX files in the folder "{data_path}"')
files = os.listdir(data_path)
file_name = st.selectbox('Select a GPX file', files)
file_path = os.path.join(data_path, file_name)
df = get_gpx_points(file_path)

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=df['latitude'][0],
        longitude=df['longitude'][0],
        zoom=13,
        # pitch=50,
    ),
    layers=[
        pdk.Layer(
            'Hexagonlayer',
            data=df,
            get_position='[longitude, latitude]',
            radius=10,
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
            get_line_color=[0, 0, 0]
        ),
    ],
    tooltip={"text": "lat: {latitude}\nlon: {longitude}\nTime: {timestamp}\nIndex: {index}"}
))

st.text('Set a lower and upper bound of point indexes to remove from the GPX track. Once set,\n'
        'click "Correct GPX" and see the resulting GPX track below.\n'
        'Corrected files are saved in the folder "./data/corrected"')
exlude_lower_bound = st.text_input('Exclude index lower bound', value=0)
exlude_upper_bound = st.text_input('Exclude index upper bound', value=0)


def click_button():
    correct_gpx_file(file_path,
                     int(exlude_lower_bound),
                     int(exlude_upper_bound))


st.button("Correct GPX", on_click=click_button)


st.header('Corrected GXP')

corrected_data_path = Path('./data/corrected')
file_path = Path(file_path)
corrected_file_path = corrected_data_path / (file_path.stem + '_gecorrigeerd.gpx')
if corrected_file_path.exists():
    corrected_df = get_gpx_points(corrected_file_path)

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(  # compute_view(df['latitude'], df[; ])
            #     (df)     #
            latitude=corrected_df['latitude'][0],
            longitude=corrected_df['longitude'][0],
            zoom=13,
            # pitch=50,
        ),
        layers=[
            pdk.Layer(
                'Hexagonlayer',
                data=corrected_df,
                get_position='[longitude, latitude]',
                radius=10,
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                corrected_df,
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
                get_line_color=[0, 0, 0]
            ),
        ],
        tooltip={"text": "lat: {latitude}\nlon: {longitude}\nTime: {timestamp}\nIndex: {index}"}
    ))

else:
    st.text('No corrected file found')

