"""
Module for testing the Parser class.
"""

import pytest
import yaml
from model.parser import Parser

@pytest.fixture
def valid_config():
    """
    Return valid configuration.
    """

    return {
        'quantities': ['Wind Direction', 'Wind Speed', 'Soil Temperature', 'Wind Speed'],
        'graph_colors': ['pink', 'yellow', 'green', 'maroon'],
        'contour_color_schemes': ['viridis', 'plasma', 'inferno', 'cividis'],
        'default_view': {'quantity': 'Wind Direction', 'station': 0, 'time': 0, 'model': 0},
        'forecast_settings': {'forecast_range': 11, 'forecast_step': 6},
        'knn_model_params': {'n_neighbors': 3, 'algorithm': 'auto', 'weights': 'uniform'},
        'svr_model_params': {},
        'gbr_model_params': {}
    }

@pytest.fixture
def invalid_config():
    """
    Return invalid configuration.
    """

    return {
        'quantities': ['Wind Direction', 'Air Temperature', 'Wind Speed'], 
        'graph_colors': ['green', 'blue'],  
        'contour_color_schemes': ['viridis', 'inferno'],  
        'default_view': {'quantity': 'Wind Direction', 'station': 0},
        'forecast_settings': {'forecast_range': 11, 'forecast_step': 6},
        'knn_model_params': {'n_neighbors': 3, 'algorithm': 'auto', 'weights': 'uniform'},
        'svr_model_params': {},
        'gbr_model_params': {}
    }

@pytest.fixture
def invalid_color_config():
    """
    Return invalid configuration, contains invalid colors.
    """

    return {
        'quantities': ['Wind Direction', 'Air Temperature', 'Wind Speed'], 
        'graph_colors': ['abc', 'blue', 'green'],  
        'contour_color_schemes': ['viridis', 'inferno', 'cividis'],  
        'default_view': {'quantity': 'Wind Direction', 'station': 0, 'time': 0, 'model': 0},
        'forecast_settings': {'forecast_range': 11, 'forecast_step': 6},
        'knn_model_params': {'n_neighbors': 3, 'algorithm': 'auto', 'weights': 'uniform'},
        'svr_model_params': {},
        'gbr_model_params': {}
    }

@pytest.fixture
def invalid_colorscheme_config():
    """
    Return invalid configuration, contains invalid colorscheme.
    """

    return {
        'quantities': ['Wind Direction', 'Air Temperature', 'Wind Speed'], 
        'graph_colors': ['yellow', 'blue', 'green'],  
        'contour_color_schemes': ['viridis', 'abc', 'cividis'],  
        'default_view': {'quantity': 'Wind Direction', 'station': 0, 'time': 0, 'model': 0},
        'forecast_settings': {'forecast_range': 11, 'forecast_step': 6},
        'knn_model_params': {'n_neighbors': 3, 'algorithm': 'auto', 'weights': 'uniform'},
        'svr_model_params': {},
        'gbr_model_params': {}
    }

@pytest.fixture
def invalid_color_nr_config():
    """
    Return invalid configuration, number of quantities and colors / colorschemes doesn't match.
    """

    return {
        'quantities': ['Wind Direction', 'Air Temperature', 'Wind Speed'], 
        'graph_colors': ['abc', 'blue'],  
        'contour_color_schemes': ['viridis', 'cividis'],  
        'default_view': {'quantity': 'Wind Direction', 'station': 0, 'time': 0, 'model': 0},
        'forecast_settings': {'forecast_range': 11, 'forecast_step': 6},
        'knn_model_params': {'n_neighbors': 3, 'algorithm': 'auto', 'weights': 'uniform'},
        'svr_model_params': {},
        'gbr_model_params': {}
    }

@pytest.fixture
def create_config_file(tmp_path):
    """
    Helper fixture to create a temporary configuration file.
    Accepts a configuration dictionary and filename.
    """

    def _create_config_file(config, filename="config.yaml"):
        config_path = tmp_path / filename
        with open(config_path, "w") as f:
            yaml.dump(config, f)
        return config_path

    return _create_config_file

def test_parse_config(create_config_file, valid_config, tmp_path):
    """
    Test the parse_config method.
    """

    config_path = create_config_file(valid_config, filename="mock_config.yaml")
    parser = Parser(config_path)

    assert parser.quantities == ['Wind Direction', 'Wind Speed', 'Soil Temperature', 'Wind Speed']
    assert parser.graph_colors == ['pink', 'yellow', 'green', 'maroon']
    assert parser.contour_color_schemes == ['viridis', 'plasma', 'inferno', 'cividis']
    assert parser.default_view == {'quantity': 'Wind Direction', 'station': 0, 'time': 0, 'model': 0}
    print(parser.knn_model_params)
    assert parser.knn_model_params == {'n_neighbors': 3, 'algorithm': 'auto', 'weights': 'uniform'}

    with pytest.raises(FileNotFoundError):
        Parser(tmp_path / "non_existent.yaml")

def test_validate_config(create_config_file, valid_config, invalid_config):
    """
    Test the method for validation configuration.
    """

    valid_path = create_config_file(valid_config, filename="valid_config.yaml")
    invalid_path = create_config_file(invalid_config, filename="invalid_config.yaml")

    parser = Parser(valid_path)
    assert parser.quantities
    assert parser.graph_colors
    assert parser.contour_color_schemes
    assert parser.default_view
    assert parser.knn_model_params

    with pytest.raises(ValueError):
        Parser(invalid_path)

def test_validate_config_colors(create_config_file, invalid_color_config):
    """
    Test the method for validation of colors.
    """

    config_path = create_config_file(invalid_color_config, filename="invalid_colors.yaml")

    with pytest.raises(ValueError, match="Invalid color: abc"):
        Parser(config_path)

def test_validate_config_color_schemes(create_config_file, invalid_colorscheme_config):
    """
    Test the method for validation of color schemes.
    """

    config_path = create_config_file(invalid_colorscheme_config, filename="invalid_color_schemes.yaml")

    with pytest.raises(ValueError, match="Invalid colorscheme: abc"):
        Parser(config_path)

def test_validate_config_colors_nr(create_config_file, invalid_color_nr_config):
    """
    Test the method for validation of matching colors / colorschemes / quantities.
    """

    config_path = create_config_file(invalid_color_nr_config, filename="invalid_colors_nr.yaml")

    with pytest.raises(ValueError, match="Not enough colors defined."):
        Parser(config_path)
