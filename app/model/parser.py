"""
Module for parsing and validating data from yaml configuration file.
"""

import os
import yaml
import matplotlib.pyplot as plt
from matplotlib.colors import is_color_like

REQUIRED_DICT_KEYS = {
    "default_view": ["quantity", "station", "time", "model"],
    "forecast_settings": ["forecast_range", "forecast_step"],
    "knn_model_params": [],
    "svr_model_params": [],
    "gbr_model_params": []
}

REQUIRED_KEYS = {
    "quantities": list,
    "graph_colors": list,
    "contour_color_schemes": list,
    "forecast_settings": dict,
    "default_view": dict,
    "knn_model_params": dict,
    "svr_model_params": dict,
    "gbr_model_params": dict
}

class Parser:
    """
    Parse and validate data from yaml configration file.
    """

    def __init__(self, config_file):
        """
        Initalize all required informations and constants and parse the configuration file. 
        """

        self.quantities = []
        self.graph_colors = []
        self.contour_color_schemes = []
        self.forecast_settings = {}
        self.knn_model_params = {}
        self.svr_model_params = {}
        self.gbr_model_params = {}
        self.default_view = {}

        self.parse_config(config_file)

    def parse_config(self, config_file):
        """
        Parse the yaml configuration file and validate based on data constants defined in class.
        """

        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(root_dir, config_file)

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, 'r', encoding='utf8') as file:
            config_data = yaml.safe_load(file)

        self.validate_config(config_data)
        self.validate_config_colors_nr()
        self.validate_config_colors()
        self.validate_config_color_schemes()

    def validate_list(self, config_data, list_name):
        """
        Validate if a given variable is a list.
        """

        if list_name in config_data and isinstance(config_data[list_name], list):
            setattr(self, list_name, config_data[list_name])
        else:
            raise ValueError(f"Invalid or missing '{list_name}' in configuration.")

    def validate_dict(self, config_data, dict_name):
        """
        Validate if a given variable is a dictionary and if it contains all required information.
        """

        if dict_name in config_data and isinstance(config_data[dict_name], dict):
            setattr(self, dict_name, config_data[dict_name])
            for key in REQUIRED_DICT_KEYS[dict_name]:
                if key not in eval(f'self.{dict_name}'):
                    raise ValueError(f"Ivalid or missing '{key}' in '{dict_name}'.")
        else:
            raise ValueError(f"Invalid or missing '{dict_name}' in configuration.")


    def validate_config(self, config_data):
        """
        Validate all the required informaiton. 
        """

        for key, val in REQUIRED_KEYS.items():
            if val == list:
                self.validate_list(config_data, key)
            else:
                self.validate_dict(config_data, key)

    def validate_config_colors(self):
        """
        Validate if the defined color in configuration is valid and can be interpreted by matplotlib.
        """

        for color in self.graph_colors:
            if not is_color_like(color):
                raise ValueError(f"Invalid color: {color}")

    def validate_config_color_schemes(self):
        """
        Validate if the defined colorscheme in configuratin is valid and can be interpreted by matplotlib.
        """

        for color_scheme in self.contour_color_schemes:
            if color_scheme not in plt.colormaps():
                raise ValueError(f"Invalid colorscheme: {color_scheme}")

    def validate_config_colors_nr(self):
        """
        Validate if in the configuration is defined enough colors relative to number of quantities.
        """

        min_thrs = len(self.quantities)

        if min_thrs > len(self.graph_colors):
            raise ValueError("Not enough colors defined.")

        if min_thrs > len(self.contour_color_schemes):
            raise ValueError("Not enough colorschemes defined")
        