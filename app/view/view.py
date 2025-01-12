"""
Module to display the HTML output of the application.
"""

from dash import html, dcc

class View:
    """
    Class to display the HTML output of the application.
    """

    def __init__(self, model):
        """
        Assignt the data model and initalize options and labels.
        """

        self.model = model

        self.station_options = []
        self.quantity_options = []
        self.radio_labels = []
        self.time_labels = {}


    def generate_labels(self):
        """
        Return generated labels for interactive comopnents.
        """

        self.station_options = [{'label': f"Station {idx}", 'value': idx} for idx in self.model.stations_pos.index.tolist()]
        self.quantity_options = [{'label': name, 'value': i} for i, name in enumerate(self.model.parser.quantities)]
        self.time_labels = {i: f"{i * self.model.parser.forecast_settings['forecast_step']}h" for i in range(self.model.parser.forecast_settings['forecast_range'])}
        self.radio_labels = [{"label": name, "value": idx} for idx, name in enumerate(["kNN", "SVR", "GBR"])]


    def init_figures(self):
        """
        Initializes graph figures when the application is first loaded.
        """

        figs = []
        for i, _ in enumerate(self.model.parser.quantities):
            figs.append(self.model.update_graph_figure(i))
        return figs

    def create_layout(self):
        """
        Creates HTML layout with contour grah, interactive pannel and grpahs for each quantity.
        """

        self.generate_labels()

        init_figs = self.init_figures()    ### dash error

        return html.Div(
            [
                html.Div(
                    [
                        html.H4("Weather Prediction Model Dashboard"),
                    ],
                    className="top-bar-container",
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Loading(dcc.Graph(id="contour-graph", figure=self.model.update_contour_figure())),
                                html.Div(
                                    dcc.Slider(
                                        min=0,
                                        max=self.model.parser.forecast_settings["forecast_range"] - 1,
                                        step=1, ####
                                        value=self.model.time,
                                        marks=self.time_labels,
                                        id="slider-time",
                                        tooltip={"placement": "bottom", "always_visible": True},
                                        className="slider",
                                    ),
                                )
                            ],
                            className="contour-graph-container",
                        ),

                        html.Div(
                            [
                                html.Div(
                                    [
                                    html.Div(
                                        [
                                            html.P("Select Quantity:", className="dropdown-label"),
                                            dcc.Dropdown(
                                                options=self.quantity_options,
                                                value=self.model.quantity,
                                                id="dropdown-quantity",
                                                className="dropdown",
                                                clearable=False
                                            ),
                                        ],
                                        className="dropdown-container"
                                    ),
                                    html.Div(
                                        [
                                            html.P("Select Station:", className="dropdown-label"),
                                            dcc.Dropdown(
                                                options=self.station_options,
                                                value=self.model.station,
                                                id="dropdown-station",
                                                className="dropdown",
                                                clearable=False
                                            ),
                                        ],
                                        className="dropdown-container"
                                    ),
                                    html.Div(
                                        [
                                            html.P("Select Extrapolation Model:", className="radio-label"),
                                            dcc.RadioItems(
                                                options=self.radio_labels,
                                                value=0,
                                                id="radio-items-model",
                                                inline=True,
                                                className="radio-items",
                                            ),
                                        ],
                                        className="radio-container"
                                    )
                                    ],
                                    className="top-control-panel-container"
                                ),
                            ],
                            className="control-panel-container",
                        ),
                    ],
                    className="top-content-container",
                ),
                html.Div(
                    [
                        html.Div(
                            dcc.Loading(
                                dcc.Graph(
                                    id=f"graph-{quantity.lower().replace(' ', '-')}",
                                    className="station-graph",
                                    figure=init_figs[i]
                                )
                            ),
                            className="quantity-plot-container"
                        )
                        for i, quantity in enumerate(self.model.parser.quantities)
                    ],
                    className="bottom-content-container"
                )
            ],
            className="body-container"
        )
