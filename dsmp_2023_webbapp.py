import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
data = pd.read_csv('df_.csv')
# Get column names
column_names = list(data.columns)[1:-1]
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
st.sidebar.markdown('<h2 style="color: blue;"> Select the values of input variables to predict electricity prices</h2>', unsafe_allow_html=True)
category = st.sidebar.selectbox(
                             "Choose a category?",
                              sorted(list(data['Sector'].unique()))
                             )
labels_ = sorted(list(data['Sector'].unique()))
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
user_input_prediction = {}
for column in column_names:
  if data[column].dtype != 'O':
    user_input_prediction[column] = st.sidebar.slider(f'{column}', float(data[column].min()), float(data[column].max()), float(data[column].mean()))

st.title('Predicting Electricity Prices in the Alberta Region')
st.markdown('This app allows predicting electricty price for the Alberta region considering "Residential", "Commercial" and "Industrial" Sectors.')


# Predict Button

#
if st.sidebar.button("Predict Electricity Prices"):
  df = pd.DataFrame()
  list_ = sorted(data['Sector'].unique().tolist())
  #
  for sector_ in list_:
    #print(sector_)
    user_input_prediction['Sector'] = list_.index(sector_)
    df = pd.concat([df, pd.DataFrame([user_input_prediction])], axis = 0, ignore_index=True)
  df['Sector'] = labels_.index(category)
  df['Sector'] = df['Sector'].astype('float')
  df = df[column_names]
  st.dataframe(df, hide_index=True)

  #Load the ML Model
  model = joblib.load('rfr_model.sav')

  #Predict and display the results
  st.subheader('Prediction')
  result = model.predict(df.values)
  st.text(np.round(result,2))

# Generate Plot
#df_output = pd.DataFrame(np.round(preds,2))
#df_output.columns = list_
#df_output
#
#

"""
fig, ax=plt.subplots(figsize=(8,5))
colors_ = sns.color_palette("deep")
ax = sns.barplot(df_output, palette=colors_)
for i in range(len(list_)):
  ax.bar_label(ax.containers[i], fontsize=10);
#ax.grid(axis='y')
plt.ylabel('Electricity Price - (CAD Cents/KWh)')
plt.show()
st.pyplot(fig)
"""

#st.bar_chart(df_output)
