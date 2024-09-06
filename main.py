from shiny import App, Inputs, Outputs, Session, ui
from modules import nav_panel_table_ui, nav_panel_table_server, nav_panel_map_ui, nav_panel_map_server, nav_panel_investors_ui, nav_panel_investors_server, nav_panel_about_server, nav_panel_about_ui
from shared import pill_list_js_path, styles_file_path, www_dir
import uvicorn

app_ui = ui.page_fluid(
    ui.head_content(
        ui.include_css(styles_file_path),
        ui.tags.link(
            {
                "rel": "shortcut icon", "href": "https://steelsport.de/img/favicon.ico"
            }
        )
    ),
    ui.navset_pill_list(
        nav_panel_table_ui("nav_panel_table", "Table"),
        nav_panel_map_ui("nav_panel_map", "Map"),
        nav_panel_investors_ui("nav_panel_investors", "Investors"),
        nav_panel_about_ui("nav_panel_about", "About"),
        widths=(2, 10),
        header=ui.TagList(
            ui.tags.div(
                {"class": "d-flex"},
                ui.tags.button(
                    {"class": "toggle-btn", "type": "button"},
                    ui.tags.i(
                        {"class": "lni lni-menu"}
                    )
                )
            )
        )
    ),
    ui.include_js(pill_list_js_path),
    title="Unicorn companies"
)


def server(input: Inputs, output: Outputs, session: Session):
    nav_panel_table_server("nav_panel_table")
    nav_panel_map_server("nav_panel_map")
    nav_panel_investors_server("nav_panel_investors")


app = App(app_ui, server, static_assets=www_dir)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
