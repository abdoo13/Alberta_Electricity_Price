import streamlit as st
import pandas as pd
import numpy as np
import joblib
import shap
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
data = pd.read_csv('df_.csv')
# Get column names
column_names = list(data.columns)[1:-1]
column_names.remove('Sources')
#st.text(column_names)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
st.sidebar.markdown('<h2 style="color: blue;"> Select the values of input variables to predict electricity prices</h2>', unsafe_allow_html=True)
sector_ = st.sidebar.selectbox(
                             "Sector",
                              sorted(list(data['Sector'].unique()))
                             )
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
user_input_prediction = {}
for column in column_names:
  if column == 'Daily End-Use Demand (GWh)':
    temp = data[data['Sector'] == sector_]
    user_input_prediction[column] = st.sidebar.slider(f'{column}', round(float(temp[column].min()),0), round(float(temp[column].max()),0), float(temp[column].mean()))
  elif data[column].dtype != 'O' and 'GHG' not in column:
    user_input_prediction[column] = st.sidebar.slider(f'{column}', round(float(data[column].min()),0), round(float(data[column].max()),0), float(data[column].mean()))
del temp
temp = pd.DataFrame(user_input_prediction)
df = pd.DataFrame(np.repeat(temp.values, 3, axis=0))
st.dataframe(df)

