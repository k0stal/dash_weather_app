"""
Module for testing the Model Class.
"""

import pytest
import numpy as np
import pandas as pd
from flexmock import flexmock
from model.model import Model
from model.parser import Parser

@pytest.fixture
def mock_parser():
    """
    Fixture to create a mock Parser without calling the constructor using FlexMock.
    """

    parser = flexmock(Parser)

    parser.quantities = ["Air Temperature", "Ground Temperature", "Air Humidity", "Wind Direction", "Wind"]
    parser.graph_colors = ["blue", "red", "black", "gray", "maroon"]
    parser.contour_color_schemes = ["viridis", "inferno", "magma", "cividis", "plasma"]
    parser.forecast_settings = {
        "forecast_range": 20,
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
    Fixture to create a mock Model with a mocked Parser using FlexMock.
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

def test_build_range(mock_model):
    """
    Test the build_range method.
    """

    xrange, yrange = mock_model.build_range(mesh_size=0.1, margin=1.0)

    assert np.isclose(xrange[0], 9.0)
    assert np.isclose(xrange[-1], 41.0)
    assert np.isclose(yrange[0], 29.0)
    assert np.isclose(yrange[-1], 61.0)

@pytest.mark.parametrize("mesh_size, margin, expected_xrange, expected_yrange", [
    (0.1, 0.5, (9.5, 40.5), (29.5, 60.5)),
    (0.2, 1.0, (9.0, 41.0), (29.0, 61.0)),
    (0.5, 7.0, (3.0, 47.0), (23.0, 67.0))
])
def test_build_range_parametrize(mock_model, mesh_size, margin, expected_xrange, expected_yrange):
    """
    Test build_range with multiple mesh sizes and margins.
    """

    xrange, yrange = mock_model.build_range(mesh_size=mesh_size, margin=margin)

    assert np.isclose(xrange[0], expected_xrange[0])
    assert np.isclose(xrange[-1], expected_xrange[1])
    assert np.isclose(yrange[0], expected_yrange[0])
    assert np.isclose(yrange[-1], expected_yrange[1])

@pytest.mark.parametrize("model, expected_shape", [
    (0, (311, 311)),
    (1, (311, 311)),
    (2, (311, 311))
])
def test_calc_grid(mock_model, model, expected_shape):
    """
    Test the calc_grid method with different KNN parameters.
    """

    mock_model.ex_model = model
    xrange, yrange = mock_model.build_range(mesh_size=0.1, margin=0.5)
    Z = mock_model.calc_grid(xrange, yrange)

    assert Z.shape == expected_shape

@pytest.mark.parametrize("model", [
    (0),
    (1),
    (2),
    (3),
    (4)
])
def test_update_contour_figure(mock_model, model):
    """
    Test the update_contour_figure method.
    """

    mock_model.ex_model = model
    fig = mock_model.update_contour_figure()

    assert fig is not None
    assert len(fig.data) >= 3
    assert fig.data[0].type == "contour"
    assert fig.data[1].type == "scatter"
    assert fig.data[2].type == "scatter"

@pytest.mark.parametrize("quantity_idx, expected_color", [
    (0, "blue"),
    (1, "red"),
    (2, "black"),
    (3, "gray"),
    (4, "maroon")
])
def test_update_graph_figure(mock_model, quantity_idx, expected_color):
    """
    Test the update_graph_figure method.
    """

    fig = mock_model.update_graph_figure(quantity_idx)

    assert fig is not None
    assert len(fig.data) == 1
    assert fig.data[0].line.color == expected_color
    assert fig.data[0].type == "scatter"
