from ctypes import HRESULT
import streamlit as st
import pandas as pd
import numpy as np



st.title('Uber Pickups')
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

loading = st.text('Loading data......')
data = load_data(2000)

loading.text('Data is loaded......')

st.markdown('Show sample data ?')
check_b = st.checkbox('yes')
if check_b:
    st.subheader('Sample data')
    st.write(data.head(20))

his = np.histogram(data[DATE_COLUMN].dt.hour , bins = 24, range=(0,24))[0]
st.subheader('Pickups per hour')
st.bar_chart(his)


all_map = st.checkbox('Show all map')
if all_map:
    st.map(data)
    
custom_hour = st.checkbox('Show with specific hour')

def filerd_data_map(h):
    filtered_data = data[data[DATE_COLUMN].dt.hour == h]
    if h<=12:
        AM_PM = 'AM'
    if h>12:
        AM_PM = 'PM'
    st.subheader(f'Map of {h}:00 {AM_PM} pickups')
    st.map(filtered_data)
if custom_hour:
    hr = st.text_input('Enter the time you want to see')

    if hr:
        filerd_data_map(int(hr))