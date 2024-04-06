import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
data = pd.read_csv('df_.csv')
# Get column names
column_names = list(data.columns)[1:-1]
column_names.remove('Sources')
st.text(column_names[1,:])
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
st.sidebar.markdown('<h2 style="color: blue;"> Select the values of input variables to predict electricity prices</h2>', unsafe_allow_html=True)
category = st.sidebar.selectbox(
                             "Choose a category?",
                              sorted(list(data['Sector'].unique()))
                             )
sectors = sorted(list(data['Sector'].unique()))
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
user_input_prediction = {}
for column in column_names:
  if data[column].dtype != 'O':
    user_input_prediction[column] = st.sidebar.slider(f'{column}', float(data[column].min()), float(data[column].max()), float(data[column].mean()))

st.title('Predicting Electricity Prices in the Alberta Region')
st.markdown('This app allows predicting electricty price for the Alberta region considering "Residential", "Commercial" and "Industrial" Sectors.')
