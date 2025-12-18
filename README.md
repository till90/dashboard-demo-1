# Master-Thesis Script and Dashboard Collection
Organisationsdokument: https://docs.google.com/document/d/1zsVnndl9v4J6o7ALQeoT81acEyEsGXLSAgL20Vz0KRI/edit#    
Forschungskonzept: https://docs.google.com/document/d/1ayj0AM7XCu0Z45zKTS16Ver4bvHuBAksdFoIwth_CpQ/edit#    

Collection of jupyter notebooks and python code snippets to collect, investigate, manipulate and learn from radon and relevant paramters.    

## notebooks/
**download_nearest_dwd_station_data.ipynb**
Downloa data from the nearest dwd station to given coordinates and create folders with daily JSON files for desired parameters.

**updating_dwd_data.ipynb**
Request every n seconds new data from a DWD Station for desired parameters and save as daily JSON file or update existing JSON file

**Statistical_Analysis_of_DWD_Time_Series.ipynb**
Analyse DataFrame for missing values and interpolate them. Make Statistical Analysis with Seasonal Decompose, Partial/Auto-Correlation, Argumented Dickey-Fuller Test, More in work....

**univariate_onestep_time_series_forcasting.ipynb**
Create Models for univariate Time Series Forcasting and predict the next step in future. Create Figures for some statistics(Seasonal decompose, Autocorelation, Stationarity) and for evaluating the model.

## radon_dashboard/
Dash dashboard

## Python Modules used:

**Dashboard, Layout, Visualization**    
[Dash - Dashboard, Visualizations and more](https://dash.plotly.com/)  
[Seaborn - High lvl API for matplotlib](https://seaborn.pydata.org/)    
[Matplotlib - Low lvl API for plotting](https://matplotlib.org/)    
    
**Data acquisition, Data handling**   
[Pandas](https://pandas.pydata.org/)    
[Wetterdienst - Request data from different Sources like DWD, EA, NOA ...](https://wetterdienst.readthedocs.io/en/latest/)    
[ObsPy - Python framework for processing seismological data](https://docs.obspy.org/)   
    
**Statistics, Machine Learning**    
[Keras - High lvl API for Tensorflow](https://keras.io/)      
[Tensorflow - Low lvl API for Machine Learning](https://www.tensorflow.org/)      
[sklearn - Machine Learning](https://scikit-learn.org/stable/)      
[statsmodels - Statistic library](https://www.statsmodels.org/stable/index.html)      
    
## Data Sources:      
[Wetter Daten - DWD](https://opendata.dwd.de/)    
[Seismologische Daten - European Integrated Data Archive (GBR)](https://eida.bgr.de/)   
