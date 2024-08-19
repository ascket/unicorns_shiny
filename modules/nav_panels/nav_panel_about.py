import plotly.express as px
from shiny import Inputs, Outputs, Session, ui, module
from shinywidgets import render_plotly, output_widget
from modules.custom_ui.about_company_box import about_company_box
import faicons


# Source: The Complete List Of Unicorn Companies (CB Insights)
# February 2023
@module.ui
def nav_panel_about_ui(name: str):
    return ui.nav_panel(
        ui.tags.span(name),
        ui.layout_column_wrap(
            ui.card(
                ui.card_header(
                    "Developer"
                ),
                ui.TagList(
                    ui.tags.div(
                        {"class": "box-body box-profile"},
                        ui.tags.div(
                            {"class": "img-wrapper"},
                            ui.tags.img(
                                {"class": "about-page custom-user-img img-responsive",
                                 "src": "https://media-exp1.licdn.com/dms/image/C4E03AQHdXBPARNVJkA/profile-displayphoto-shrink_200_200/0/1658841255159?e=2147483647&v=beta&t=8-j0yuFnc1Ojkc8abCV_Rq4DlNt6diHqxJa85ZF3eCI",
                                 "alt": "Firm logo picture"}
                            )
                        ),
                        ui.tags.h3(
                            {"class": "profile-username text-center"},
                            "Alexey Shapovalov",
                        ),
                        ui.tags.p(
                            {"class": "text-center"},
                            "MSc Student - Applied Computer Science"
                        ),
                        ui.row(
                            ui.column(
                                6,
                                faicons.icon_svg("linkedin"),
                                ui.tags.a(
                                    {"href": "https://www.linkedin.com/in/a-shapovalov/", "target": "_blank"},
                                    "Linkedin"
                                )
                            ),
                            ui.column(
                                6,
                                faicons.icon_svg("square-xing"),
                                ui.tags.a(
                                    {"href": "https://www.xing.com/profile/Alexey_Shapovalov", "target": "_blank"},
                                    "Xing"
                                )
                            ),
                            class_="about-page-card-row"
                        ),
                    ),
                ),
                class_="about-page-card-developer"
            ),
            width=1 / 4
        ),
        ui.layout_column_wrap(
            ui.card(
                ui.card_header(
                    "Source"
                ),
                ui.TagList(
                    ui.tags.ul(
                        {"class": "list-group list-group-unbordered"},
                        ui.tags.li(
                            {"class": "list-group-item"},
                            "Data Source",
                            ui.tags.p(
                                {"class": "pull-right"},
                                ui.tags.a(
                                    {"href": "https://www.cbinsights.com/research-unicorn-companies",
                                     "target": "_blank"},
                                    "www.cbinsights.com"
                                ),
                            )
                        ),
                        ui.tags.li(
                            {"class": "list-group-item"},
                            "Last update",
                            ui.tags.p(
                                {"class": "pull-right"},
                                "19.08.2024"
                            )
                        ),
                    ),
                ),
                class_="about-page-card-source"
            ),
            width=1 / 4
        ),
        icon=ui.tags.i({"class": "lni lni-license"})
    )


@module.server
def nav_panel_about_server(input: Inputs, output: Outputs, session: Session):
    pass
