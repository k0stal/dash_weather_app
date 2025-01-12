"""
Module for testing the View class.
"""

import pytest
import pandas as pd
import numpy as np
from flexmock import flexmock
from view.view import View
from model.parser import Parser
from model.model import Model

@pytest.fixture
def mock_parser():
    """
    Fixture to create a mock Parser.
    """

    parser = flexmock(Parser)

    parser.quantities = ["Air Temperature", "Ground Temperature", "Air Humidity", "Wind Direction", "Wind"]
    parser.graph_colors = ["blue", "red", "black", "gray", "maroon"]
    parser.contour_color_schemes = ["viridis", "inferno", "magma", "cividis", "plasma"]
    parser.forecast_settings = {
        "forecast_range": 5,
        "forecast_step": 6
    }
    parser.default_view = {
        "quantity": "Air Temperature",
        "station": 0,
        "time": 0,
        "model": 0
    }
    parser.knn_model_params = {"n_neighbors": 2, "algorithm": "auto", "weights": "uniform"}
    parser.svr_model_params = {"C": 1.0, "kernel": "rbf", "gamma": "scale"}
    parser.gbr_model_params = {"learning_rate": 0.1, "n_estimators": 100, "subsample": 1.0}

    return parser

@pytest.fixture
def mock_model(mock_parser):
    """
    Fixture to create a mock Model.
    """

    model = Model()
    model.stations_pos = pd.DataFrame({
        'lon': [10.0, 20.0, 30.0, 40.0],
        'lat': [30.0, 40.0, 50.0, 60.0]
    })
    model.data = np.random.rand(20, 4, 5)
    model.time = 0
    model.quantity = 0
    model.station = 0
    model.ex_model = 0
    model.parser = mock_parser
    return model

@pytest.fixture
def view(mock_model):
    """
    Fixture to create a View instance.
    """

    return View(mock_model)


def test_generate_labels(view):
    """
    Test the generate_labels method.
    """

    view.generate_labels()
    assert view.station_options == [
        {"label": "Station 0", "value": 0},
        {"label": "Station 1", "value": 1},
        {"label": "Station 2", "value": 2},
        {"label": "Station 3", "value": 3},
    ]
    assert view.quantity_options == [
        {"label": "Air Temperature", "value": 0},
        {"label": "Ground Temperature", "value": 1},
        {"label": "Air Humidity", "value": 2},
        {"label": "Wind Direction", "value": 3},
        {"label": "Wind", "value": 4}
    ]
    expected_time_labels = {
        0: "0h",
        1: "6h",
        2: "12h",
        3: "18h",
        4: "24h",
    }
    assert view.time_labels == expected_time_labels

@pytest.mark.parametrize("quantities", [
    ["Air Temperature", "Ground Temperature", "Air Humidity", "Wind Direction", "Wind"],
])
def test_init_figures(view, mock_model, quantities):
    """
    Test the init_figures method.
    """
    mock_model.quantities = quantities
    init_figs = view.init_figures()

    assert len(init_figs) == len(quantities)

    for _, fig in enumerate(init_figs):
        assert "data" in fig
        assert "layout" in fig
        assert len(fig["data"]) > 0
        assert fig["data"][0]["type"] == "scatter"
