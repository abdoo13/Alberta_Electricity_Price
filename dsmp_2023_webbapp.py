import streamlit as st
import pandas as pd
import numpy as np
import joblib
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
data = pd.read_csv('df_.csv')
# Get column names
column_names = list(data.columns)[1:-1]
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
st.sidebar.markdown('<h2 style="color: blue;"> Select the values of input variables to predict the electricity prices</h2>', unsafe_allow_html=True)
user_input_prediction = {}
for column in column_names:
  if data[column].dtype != 'O':
    user_input_prediction[column] = st.sidebar.slider(f'{column}', float(data[column].min()), float(data[column].max()), float(data[column].mean()))

st.sidebar.button("Predict Electricity Prices")      
""""""""""""""""""""""""""""""""""""""""""""""""
st.title('Predicting Electricity Prices in the Alberta Region')
st.markdown('This app allows predicting Electricty prices for the Alberta region considering the "Residential", "Commercial" and the "Industrial" Sectors.')

df = pd.DataFrame()
list_ = sorted(data['Sector'].unique().tolist())
#
for sector_ in list_:
  #print(sector_)
  user_input_prediction['Sector'] = list_.index(sector_)
  df = pd.concat([df, pd.DataFrame([user_input_prediction])], axis = 0, ignore_index=True)
df['Sector'] = df['Sector'].astype('float')

# Load the ML Model
model = joblib.load('rfr_model.sav')

# Predict and display the results
#prediction = model.predict(temp.values.reshape(1, -1))
preds = model.predict(df.values)
st.subheader('Prediction')
st.write(f'The predicted Electricity Price is: {np.round(preds,2)}')

# Predict Button
st.button("Predict Electricity Prices")
#
if st.button("Predict Electricity Prices"):
  result = model.predict(df.values)
  st.text(np.round(preds,2))

# Generate Plot
df_output = pd.DataFrame(np.round(preds,2)).T
df_output.columns = list_
#df_output
#
#

"""fig, ax=plt.subplots(figsize=(8,5))
colors_ = sns.color_palette("deep")
ax = sns.barplot(df_output, palette=colors_)
for i in range(len(list_)):
  ax.bar_label(ax.containers[i], fontsize=10);
#ax.grid(axis='y')
plt.ylabel('Electricity Price - (CAD Cents/KWh)')
plt.show()
st.pyplot(fig)
"""

st.bar_chart(df_output)
