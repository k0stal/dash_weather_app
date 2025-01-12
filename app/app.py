"""
Module for initializing and running the WeatherApp.
"""

from dash import Dash
from model.model import Model
from view.view import View
from controller.controller import Controller

class WeatherApp:
    """
    Simple visualization application for meteorological data.
    """

    def __init__(self):
        """
        Initialize the model, view and controller and set up callbacks.
        """
        self.app = Dash(__name__, suppress_callback_exceptions=True, assets_folder="assets")
        self.model = Model()
        self.view = View(self.model)
        self.controller = Controller(self.app, self.model)
        self.app.layout = self.view.create_layout()
        self.register_callbacks()

    def register_callbacks(self):
        """
        Method for registering callbacks.
        """
        self.controller.register_callbacks()

    def run(self, debug=False):
        """
        Run the application.
        """
        self.app.run_server(debug=debug)


if __name__ == "__main__":
    mvc_app = WeatherApp()
    mvc_app.run()
