"""
Module for controlling the runtime of the application.
"""

import dash
from dash import callback_context, Input, Output

class Controller:
    """
    Class for propagating information between View and Model
    """

    def __init__(self, app, model):
        self.app = app
        self.model = model

    def register_callbacks(self):
        """
        Registers callbacks from user and adjusts the model accordingly.
        """

        @self.app.callback(
            Output("contour-graph", "figure"),
            [Input("dropdown-quantity", "value"),
             Input("slider-time", "value"),
             Input("radio-items-model", "value"),
             Input("dropdown-station", "value")]
        )
        def update_contour(quantity, time, ex_model, station):
            """
            If new quantity is selected or new time is selected or new model is selected, adjust the model and update the contour figure.
            """

            ctx = callback_context
            if not ctx.triggered:
                return dash.no_update

            triggered_input = ctx.triggered[0]["prop_id"].split(".")[0]

            if triggered_input == "dropdown-quantity":
                self.model.quantity = quantity

            elif triggered_input == "slider-time":
                self.model.time = time

            elif triggered_input == "radio-items-model":
                self.model.ex_model = ex_model

            elif triggered_input == "dropdown-station":
                self.model.station = station

            return self.model.update_contour_figure()

        @self.app.callback(
            [Output(f"graph-{quantity.lower().replace(' ', '-')}", "figure") for quantity in self.model.parser.quantities],
            [Input("dropdown-station", "value"),
             Input("slider-time", "value")]
        )
        def update_graphs(station, time):
            """
            If new station is selected, update all graphs.
            """

            ctx = callback_context
            if not ctx.triggered:
                return tuple(dash.no_update for _ in self.model.parser.quantities)

            triggered_input = ctx.triggered[0]["prop_id"].split(".")[0]

            if triggered_input == "dropdown-station":
                self.model.station = station

            elif triggered_input == "slider-time":
                self.model.time = time

            figures = []
            for i, _ in enumerate(self.model.parser.quantities):
                figures.append(self.model.update_graph_figure(i))

            return tuple(figures)
