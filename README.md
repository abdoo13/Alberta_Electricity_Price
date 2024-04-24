# Electricity_Prices_Alberta
This project was carried out as part of the 2023 SPE Calgary Data Science Metentoring Program (DSMP)

## Summary

  The machine learning (ML) solution that was built as part of this challenge aims to forecast electricity prices in the Alberta region for the following sectors: “Residential”, “Commercial” and “Industrial”.
Initially, we started by seeking for parameters that are likely to influence electricity price, then trying to get or integrate the data that we came across in a single and a comprehensive dataset. Initially, it was thought that electricity price is being affected by or correlated to:
-	Amount/Price of energy source.
-	GHG emissions of every used energy source.
-	Generation/Distribution costs.
-	Weather conditions.
-	Macroeconomic indicators.

  Using the Selenium package, electricity data grasped from the Canada Energy Regulator website (CER) [1] (prices, energy sources, energy consumption, macroeconomic indicators and GHG emission data). On the other hand, weather data have been scraped from Weather Underground [2] (temperature, humidity, wind speed). The EDA process indicated that "Daily Electricity Price" is strongly correlated to the followinf daily parameters: End-Use Demand, Real Gross Domestic Product, Temp_Max, Temp_Min & Hum_Min.

  With regards to the ML process, different ML algorithms were investigated (Random Forest, LightGBM and Xgboost) in order to come up with best regressor that will help us predict electricity prices with minimum error and without any likelihood to overfit. The training and testing process was carried out along with hyperparameters fine tuning (HyperOpt package). The simulations indicated the best goodness of fit can be obtained by the Random Forest regressor.
 	This web application has been implemented based on the Streamlit framework where one can easily have an idea of what electricity would be for each of the three sectors.

[1]: https://apps.cer-rec.gc.ca/ftrppndc/dflt.aspx?GoCTemplateCulture=en-CA

[2]: https://www.wunderground.com/
