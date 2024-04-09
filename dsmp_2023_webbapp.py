import streamlit as st
import pandas as pd
import numpy as np
import joblib
import altair as alt
import plotly.graph_objects as go
import matplotlib.pyplot as plt
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
data = pd.read_csv('df_.csv')
# Get column names
column_names = list(data.columns)[1:-1]
column_names.remove('Sources')
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

st.title('Predicting Electricity Prices in the Alberta Region')
st.markdown('This webb application allows predicting electricty prices in the Alberta region for the following sectors: "Residential", "Commercial" and "Industrial".')
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Predict Button
if st.sidebar.button("Predict Electricity Prices"):
  df = pd.DataFrame()
  cols_ = []
  for key_ in user_input_prediction.keys():
    cols_.append(key_)
    if key_ == 'Daily End-Use Demand (GWh)':
      df[key_] = [round(float(temp['Daily End-Use Demand (GWh)'].min())), user_input_prediction[key_], round(float(temp['Daily End-Use Demand (GWh)'].max()))]
    else:
      df[key_] = [user_input_prediction[key_]]*3
  df['Daily GHG Emmisions (Tons_CO2_Equivalent)'] = df['Daily End-Use Demand (GWh)']*0.4688
  #
  df = df[column_names[1:]]
  #st.dataframe(df, hide_index=True)
  
  #Load the ML Model
  model = joblib.load('rfr_model.sav')

  #Predict and display the results
  st.subheader('Prediction')
  result = model.predict(df.values)
  #st.text(np.round(result,2))
  df_2 = pd.DataFrame({'Cat':['Low', 'Price', 'Top'], 'Daily End-Use Demand':df['Daily End-Use Demand (GWh)'], 'Electricity Price':np.round(result,2)})
  st.dataframe(df_2)
  #st.bar_chart(df_2, x='Cat', y=['Daily End-Use Demand', 'Electricity Price'])
  
  """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  delta_ = df_2['Daily End-Use Demand'][2] - df_2['Daily End-Use Demand'][0]
  df_3 = pd.DataFrame(columns=column_names[1:])
  df_3['Daily End-Use Demand (GWh)'] = [df['Daily End-Use Demand (GWh)'][0] + j*(delta_/10) for j in range(0, 11)]
  df_3['Daily GHG Emmisions (Tons_CO2_Equivalent)'] = df_3['Daily End-Use Demand (GWh)']*0.4688
  for col in list(df_3.columns)[2:]:
    df_3[col] = df[col][0]
  df_3['Electricity Price (CAD Cents/KWh'] = model.predict(df_3.values)
  #st.dataframe(df_3)
  cols_3 = list(df_3.columns)
  #st.line_chart(df_3, x=cols_3[0], y=cols_3[-1])

  c = (alt.Chart(df_3).mark_line().encode(
                                        x = alt.X(cols_3[0]),
                                        y = alt.Y(cols_3[-1], scale=alt.Scale(domain=[np.round(df_3['Electricity Price (CAD Cents/KWh'].min(), 1)-0.2, 
                                                                                      np.round(df_3['Electricity Price (CAD Cents/KWh'].max(), 1)+0.2]))
                                        )
      #+alt.Chart(pd.DataFrame({'y': [12.3]})).mark_rule().encode(y='y'))
       + alt.Chart(annotations).mark_text().encode(x=120, y=15, text='dd'))
  st.altair_chart(c, use_container_width=True)
