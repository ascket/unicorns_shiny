import plotly.express as px
from shiny import Inputs, Outputs, Session, ui, module
from shinywidgets import render_plotly, output_widget

from shared import get_investor_industry_data_frame

df_investors_industry = get_investor_industry_data_frame()


@module.ui
def nav_panel_about_ui(name: str):
    return ui.nav_panel(
        ui.tags.span(name),
        ui.card(
            ui.card_header(
                "Investors"
            ),
            "This is about page"
        ),
        icon=ui.tags.i({"class": "lni lni-license"})
    )


@module.server
def nav_panel_about_server(input: Inputs, output: Outputs, session: Session):
    pass
