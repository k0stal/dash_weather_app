The project consists of two parts.

The first is a Jupyter Notebook, which contains data processing from meteorological stations. It also deals with model creation based on GFS data and data measured at meteorological stations. All models are ultimately compared with each other as well as with the reference GFS model. At the end, it includes the preparation of sample data for demonstrating the visualization application.

The second part is a web application built with Dash. The application receives a CSV file containing the positions of meteorological stations in the format **('lon', 'lat')** and a three-dimensional NumPy array in the format **(time, station, variable)**. Both files are stored in the folder */app/model/data*. The application visualizes the data using contour plots and time-dependent plots for individual variables. For data extrapolation, three models are available: kNN Regressor, Support Vector Regressor, and GradientBoostingRegressor, which enable forecasting for the entire region. Users can choose to display data for any variable, for a specific station and time. The application architecture follows the MVC pattern.

The web application is launched from the CLI using the command `python3 app.py`, which starts a local server that can be accessed via a web browser. Testing can be run using the `pytest` command. The application can be configured using the **config.yaml** file, where one must specify which variables the data matrix contains, the forecast time step, and its range. Additionally, one can configure the colors and color schemes for the graphs, as well as the parameters of the extrapolation models.

The requirements.txt file contains only the necessary modules to run the web application.
