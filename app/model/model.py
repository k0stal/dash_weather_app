"""
Module for storage and maintenance of data of the application.
"""

import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.ensemble import GradientBoostingRegressor

from model.parser import Parser


class Model:
    """
    Store and maintain all the data used in our application.
    """

    def __init__(self):
        """
        Initialize the Parser and load the information from configuration file.
        Adjust the default state of the application based on the parsed information.
        """

        self.parser = Parser("config.yaml")

        self.quantity = self.parser.quantities.index(self.parser.default_view["quantity"])
        self.station = self.parser.default_view["station"]
        self.time = self.parser.default_view["time"]
        self.ex_model = self.parser.default_view["model"]

        self.load_data()

    def build_range(self, mesh_size=0.05, margin=0.5):
        """
        Based on latitude and longitude of stations calculate steps of the x and y axes with the accuracy mesh_size.
        Add margin to both ends of both axes.
        """

        x_min = self.stations_pos['lon'].min() - margin
        x_max = self.stations_pos['lon'].max() + margin
        y_min = self.stations_pos['lat'].min() - margin
        y_max = self.stations_pos['lat'].max() + margin

        xrange = np.linspace(x_min, x_max, num=int((x_max - x_min) / mesh_size) + 1)
        yrange = np.linspace(y_min, y_max, num=int((y_max - y_min) / mesh_size) + 1)

        return xrange, yrange

    def calc_grid(self, xrange, yrange):
        """
        Based on steps of accuracy of x and y axes calculate the prediction for the whole plane.
        """

        xx, yy = np.meshgrid(xrange, yrange)
        grid_input = np.c_[xx.ravel(), yy.ravel()]

        regressor = None
        if self.ex_model == 0:
            regressor = KNeighborsRegressor(**self.parser.knn_model_params)
        elif self.ex_model == 1:
            regressor = SVR(**self.parser.svr_model_params)
        else:
            regressor = GradientBoostingRegressor(**self.parser.gbr_model_params)

        regressor.fit(self.stations_pos.values, self.data[self.time, :, self.quantity])

        return regressor.predict(grid_input).reshape(xx.shape)

    def update_contour_figure(self):
        """
        Create Contour figure based on the data from calc_grid. Use the color schemes defined in configuration file.
        Mark all of the stations from stations_pos using markers and also highlight the currently selected station.
        """

        fig = go.Figure()
        xrange, yrange = self.build_range()
        Z = self.calc_grid(xrange, yrange)

        fig.add_trace(go.Contour(
            z=Z,
            x=xrange,
            y=yrange,
            colorscale=self.parser.contour_color_schemes[self.quantity],
            colorbar={"title": f'{self.parser.quantities[self.quantity]}'},
            line_smoothing=1,
            contours={
                "showlabels": True,
                "labelfont": {"size": 7, "color": 'white'},
                "start": Z.min(),
                "end": Z.max(),
                "size": (Z.max() - Z.min()) / 7
            },
            line_width=0,
            opacity=1
        ))

        fig.add_trace(go.Scatter(
            x=self.stations_pos['lon'],
            y=self.stations_pos['lat'],
            mode='markers',
            name='Stations',
            marker={
                "color": 'white',
                "size": 8,
                "symbol": 'circle',
                "line": {"color": 'black', "width": 1}
            },
            opacity=1,
            showlegend=False
        ))

        fig.add_trace(go.Scatter(
            x=[self.stations_pos['lon'].iloc[self.station]],
            y=[self.stations_pos['lat'].iloc[self.station]],
            mode='markers',
            marker={
                "color": 'red',
                "size": 10,
                "symbol": 'circle',
                "line": {"color": 'black', "width": 1}
            },
            opacity=1,
            showlegend=False
        ))

        fig.update_layout(
            autosize=True,
            xaxis_title=None,
            yaxis_title=None,
            template="plotly",
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            paper_bgcolor="#f8f9fa",
            mapbox={
                "style": 'carto-positron',
                "zoom": 6,
                "center": {
                    "lat": self.stations_pos['lat'].mean(),
                    "lon": self.stations_pos['lon'].mean()
                }
            }
        )
        return fig

    def update_graph_figure(self, quantity_idx):
        """
        Based on quantity index return graph of quantity of a currently selected station.
        """

        fig = go.Figure()
        data = self.data[:self.parser.forecast_settings["forecast_range"], self.station, quantity_idx]

        fig.add_trace(go.Scatter(
            x=np.arange(len(data)) * self.parser.forecast_settings["forecast_step"],
            y=data,
            mode="lines",
            name=f'{self.quantity}',
            line={"color": self.parser.graph_colors[quantity_idx]}
        ))

        fig.add_vline(
            x=self.time * self.parser.forecast_settings["forecast_step"],
            line={
                "color": 'black',
                "width": 2,
                "dash": 'dash'
            }
        )

        fig.update_layout(
            title=f"Station {self.station}: {self.parser.quantities[quantity_idx]}",
            template="plotly",
            margin={"r": 10, "t": 50, "l": 10, "b": 10},
            paper_bgcolor="#f8f9fa",
            plot_bgcolor="#f8f9fa",
            autosize=True
        )

        return fig

    def load_data(self):
        """
        Load both station positions and sample data from file '/data'. Sample stations are stored as csv, sample data as npy.
        If files aren't accessible, return error.
        """

        base_dir = os.path.dirname(os.path.abspath(__file__))
        stations_file_path = os.path.join(base_dir, 'data', 'sample_stations.csv')
        data_file_path = os.path.join(base_dir, 'data', 'sample_data.npy')

        if os.path.exists(stations_file_path) and os.path.exists(data_file_path):
            self.stations_pos = pd.read_csv(stations_file_path)
            self.data = np.load(data_file_path)
        else:
            raise FileNotFoundError(f"Could not find data files at {stations_file_path} or {data_file_path}")
