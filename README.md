# Electricity_Prices_Alberta
This project was carried out as part of the 2023 SPE Calgary Data Science Metentoring Program (DSMP)
Summary:
  The machine learning (ML) solution that was built as part of this challenge aims to forecast electricity prices in the Alberta region for the following sectors: “Residential”, “Commercial” and “Industrial”.
Initially, we started by seeking for parameters that are likely to influence electricity price, then trying to get or integrate the data that we came across in a single and a comprehensive dataset. Our primary findings indicated electricity price being affected by or correlated to:
-	Amount/Price of energy source.
-	GHG emissions of every used energy source.
-	Generation/Distribution costs.
-	Weather conditions.
-	Macroeconomic indicators.
  Using Python, the data scraping process was carried out using the Selenium package. Electricity data grasped from the Canada Energy Regulator website (CER) [1] : Electricity data (prices, energy sources, energy consumption, etc.), macroeconomic indicators and GHG emission data. On the other hand, weather data have been scraped from Weather Underground [2] (temperature, humidity, wind speed).
After gathering all the data using multiple join/merge operations on Pandas, the final dataset that we intended to work on covered the period spanning from 2014-2023 and we ended up dealing with a dataset having 416,580 rows and 23 variables. The exploratory data analysis process was then initiated and it turned out that electricity price for the three aforementioned sectors is correlated to end-use energy demand, GHG emissions, real gross domestic product, average and minimum daily temperatures.
  With regards to the ML process, different ML algorithms were investigated (Random Forest, LightGBM and Xgboost) in order to come up with best regressor that will help us predict electricity prices with minimum error and without any likelihood to overfit. The training and testing process was carried out along with hyperparameters fine tuning (HyperOpt package). The simulations indicated the best goodness of fit can be obtained by the Random Forest regressor.
 	This web application has been implemented based on the Streamlit framework where one can easily have an idea of what electricity would be for each of the three sectors.

References:
[1]: https://apps.cer-rec.gc.ca/ftrppndc/dflt.aspx?GoCTemplateCulture=en-CA

[2]: https://www.wunderground.com/
