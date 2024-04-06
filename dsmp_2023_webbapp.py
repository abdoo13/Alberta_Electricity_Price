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
    temp = data[data['Sector] == 'Residential']
    user_input_prediction[column] = st.sidebar.slider(f'{column}', float(temp[column].min()), float(temp[column].max()), float(temp[column].mean()))
  elif data[column].dtype != 'O' and 'GHG' not in column:
    user_input_prediction[column] = st.sidebar.slider(f'{column}', float(data[column].min()), float(data[column].max()), float(data[column].mean()))

st.title('Predicting Electricity Prices in the Alberta Region')
st.markdown('This app allows predicting electricty price for the Alberta region considering "Residential", "Commercial" and "Industrial" Sectors.')

# Predict Button
if st.sidebar.button("Predict Electricity Prices"):
  df = pd.DataFrame()
  #
  df = pd.concat([pd.DataFrame([user_input_prediction]), pd.DataFrame([user_input_prediction])], axis=0)
  #
  df['Daily GHG Emmisions (Tons_CO2_Equivalent)'] = df['Daily End-Use Demand (GWh)']*0.4688
  #
  df = df[column_names[1:]]
  st.dataframe(df, hide_index=True)

  #Load the ML Model
  model = joblib.load('rfr_model.sav')

  #Predict and display the results
  st.subheader('Prediction')
  result = model.predict(df.values)
  st.text(np.round(result[0],2))
