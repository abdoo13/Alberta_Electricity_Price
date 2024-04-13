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
st.markdown('This web application allows predicting electricty prices in the Alberta region for the following sectors: "Residential", "Commercial" and "Industrial".')
st.markdown('A machine learning model is embeded to this app and predictions are made according to this model. This ML model was built on data from the "Canada’s Energy Future 2023" report published online by the Canada Energy Regulator (CER) in addition to some weather data pulled out from the "Weather Underground" official website".')
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
  
  #Load the ML Model
  model = joblib.load('rfr_model.sav')

  #Predict and display the results
  st.subheader('Prediction Results')
  result = model.predict(df.values)
  #st.text(np.round(result,2))
  df_2 = pd.DataFrame({'Threshold':['Lower', 'Prediction', 'Upper'], 'Daily End-Use Demand':df['Daily End-Use Demand (GWh)'], 'Electricity Price':np.round(result,2)})
  #st.markdown(df_2.style.hide(axis="index").to_html(), unsafe_allow_html=True)
  """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  fig1 = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = df_2['Daily End-Use Demand'][1],
    title = {'text': "Daily End-Use Demand (GWh)"},
    domain = {'x': [0, 1], 'y': [0, 1]},
    gauge = {'axis': {'range': [np.round(df_2['Daily End-Use Demand'].min(),0)-1, np.round(df_2['Daily End-Use Demand'].max(),0)]}, 'bar': {'color': "crimson"}}
  ))
  fig2 = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = np.round(result[1],2),
    title = {'text': "Electricity Price (CAD Cents/KWh)"},
    domain = {'x': [0, 1], 'y': [0, 1]},
    gauge = {'axis': {'range': [np.round(result.min(),0)-1, np.round(result.max(),0)+1]}, 'bar': {'color': "royalblue"}}
  ))
  #st.plotly_chart(fig1, use_container_width=True)
  data_container = st.container()
  with data_container:
    plot1, plot2 = st.columns(2)
    with plot1:
        st.plotly_chart(fig1, use_container_width=True)
    with plot2:
        st.plotly_chart(fig2, use_container_width=True)
  """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  delta_ = df_2['Daily End-Use Demand'][2] - df_2['Daily End-Use Demand'][0]
  df_3 = pd.DataFrame(columns=column_names[1:])
  df_3['Daily End-Use Demand (GWh)'] = [df['Daily End-Use Demand (GWh)'][0] + j*(delta_/50) for j in range(0, 51)]
  df_3['Daily GHG Emmisions (Tons_CO2_Equivalent)'] = df_3['Daily End-Use Demand (GWh)']*0.4688
  for col in list(df_3.columns)[2:]:
    df_3[col] = df[col][0]
  df_3['Electricity Price (CAD Cents/KWh)'] = model.predict(df_3.values)
  cols_3 = list(df_3.columns)
  
  fig_3 = go.Figure(data=go.Scatter(x=df_3[cols_3[0]], y=df_3[cols_3[-1]], mode='lines+markers', marker_color='RoyalBlue'))
  fig_3.update_layout(xaxis_title=cols_3[0], yaxis_title=cols_3[-1], width=1000)
  fig_3.add_annotation(
        text="Here's your price",
        x=df_2['Daily End-Use Demand'][1],
        y=np.round(result[1],2),
        showarrow=True,
        arrowhead=4,
        xanchor="right",
        font=dict(size=20, color="#242526"),
    )
  st.plotly_chart(fig_3)
