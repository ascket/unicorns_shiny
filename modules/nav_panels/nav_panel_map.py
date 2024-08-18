import faicons
import plotly.express as px
from shiny import Inputs, Outputs, Session, ui, module, reactive, render
from shinywidgets import render_plotly, output_widget

from scripts import company_per_year_data_frame
from shared import get_df_for_map, df, blue_color_main

df_for_map = get_df_for_map()

COUNTRY_CONTINENT_MAP = {
    "Country": "country",
    "Continent": "continent",
    "Total valuation": "count_valuation_per_country",
    "Total unicorns": "count_per_country"
}

max_count_per_country = df_for_map["count_per_country"].max()
max_count_valuation = df_for_map["count_valuation_per_country"].max()


@module.ui
def nav_panel_map_ui(name: str):
    return ui.nav_panel(
        ui.tags.span(name),
        ui.card(
            ui.card_header(
                "Country Continent Statistic",
                ui.popover(
                    faicons.icon_svg("gear"),
                    ui.input_select(
                        "graph_map_type_choroplet",
                        "Graph type",
                        choices=["Map", "Chart"]
                    ),
                    ui.input_radio_buttons(
                        "valuation_count_color_choroplet",
                        None,
                        ["Total valuation", "Total unicorns"],
                        inline=True
                    ),
                    title="Add a color",
                    placement="top",
                    style="font-size: 1.2rem; color: #23669d",
                ),
                class_="d-flex justify-content-between align-items-center"
            ),
            output_widget("choroplet_map_valuation_count"),
            full_screen=True
        ),
        ui.card(
            ui.card_header(
                "Companies per year"
            ),
            output_widget("line_plot_company_per_year"),
            full_screen=True
        ),
        ui.card(
            ui.card_header(
                "Industry in country",
            ),
            ui.input_select("select_county_pie_chart", "Select country", choices=df_for_map["country"].tolist(), selected="Germany"),
            output_widget("pie_chart_industry_in_country"),
            full_screen=True
        ),
        ui.card(
            ui.card_header(
                "Compare countries by investors"
            ),
            ui.input_numeric("amount_countries_compare", "How many countries to compare", value=2, max=4, min=1),
            ui.output_ui("countries_compare_ui"),
            full_screen=True
        ),
        icon=ui.tags.i({"class": "lni lni-map"})
    )


@module.server
def nav_panel_map_server(input: Inputs, output: Outputs, session: Session):
    @render_plotly
    def choroplet_map_valuation_count():
        size = input.valuation_count_color_choroplet()
        chart_or_map = input.graph_map_type_choroplet()
        if chart_or_map == "Map":
            fig = px.choropleth(
                df_for_map,
                locations="iso_alpha",
                color=COUNTRY_CONTINENT_MAP[size],
                #color_continuous_scale=[[0, "rgb(196, 213, 237)"], [0.5, "rgb(78, 130, 202)"], [1, "rgb(17, 34, 57)"]],
                color_continuous_scale=[[0, "lightyellow"], [0.5, "lightgreen"], [1, "rgb(35, 102, 157)"]],
                range_color=[0, max_count_per_country] if size == "Total unicorns" else [0, max_count_valuation],  # Задаем диапазон значений для цвета
                scope="world",
                hover_data={"country": True, "count_per_country": True,
                            "count_valuation_per_country": ":.2f", "iso_alpha": False,
                            "continent": False},
                labels={"count_per_country": "Total unicorns", "continent": "Continent",
                        "country": "Country", "count_valuation_per_country": "Valuation ($B)"},
            )
        else:
            fig = px.bar(df_for_map, y=COUNTRY_CONTINENT_MAP[size], x="country", text=COUNTRY_CONTINENT_MAP[size],
                         labels={"count_per_country": "Total unicorns", "continent": "Continent", "country": "Country",
                                 "count_valuation_per_country": "Valuation ($B)"}, color_discrete_sequence=[blue_color_main])
            fig.update_traces(texttemplate="%{text:.2f}", textposition="outside") if COUNTRY_CONTINENT_MAP[
                                                                                         size] == "count_valuation_per_country" else fig.update_traces(
                texttemplate="%{text}", textposition="outside")
            fig.update_layout(xaxis={'categoryorder': 'total descending'}, font={"size": 14}, uniformtext_minsize=9,
                              uniformtext_mode="show")
        return fig


    @render_plotly
    def line_plot_company_per_year():
        data_frame = company_per_year_data_frame(df)
        fig = px.line(data_frame, x="year_joined", y="n", text="n", labels={"year_joined": "Year joined", "n": "Total unicorns"}, color_discrete_sequence=[blue_color_main])
        fig.update_traces(textposition="bottom right")
        return fig


    @render_plotly
    def pie_chart_industry_in_country():
        result = df.groupby(["country", "industry"])[["industry"]].agg(n=("industry", "count")).reset_index()
        result_df = result[result["country"] == input.select_county_pie_chart()]
        fig = px.pie(result_df, values="n", names="industry", labels={"industry": "Industry", "n": "Total unicorns"}, color_discrete_sequence=px.colors.diverging.delta)
        fig.update_layout(legend_title_text="Industries")

        return fig

    @reactive.calc
    def col_names():
        return [f"countries_compare{x}" for x in range(input.amount_countries_compare())]

    @render.ui
    @reactive.event(input.amount_countries_compare)
    def countries_compare_ui():
        result = [
            ui.card(
                ui.input_select(f"{x}_select", "Select country", choices=df_for_map["country"].tolist(),
                                selected="Germany"),
                output_widget(f"{x}_pie_chart"),
            ) for x in col_names()
        ]
        return ui.layout_columns(
            *result
        )

    @render_plotly
    def countries_compare0_pie_chart():
        result = df.groupby(["country", "industry"])[["industry"]].agg(n=("industry", "count")).reset_index()
        input.amount_countries_compare()
        with reactive.isolate():
            result_df = result[result["country"] == input.countries_compare0_select()]
        fig = px.pie(result_df, values="n", names="industry", labels={"industry": "Industry", "n": "Total unicorns"},
                     color_discrete_sequence=px.colors.diverging.delta)
        fig.update_layout(legend_title_text="Industries")

        return fig

    @render_plotly
    def countries_compare1_pie_chart():
        result = df.groupby(["country", "industry"])[["industry"]].agg(n=("industry", "count")).reset_index()
        result_df = result[result["country"] == input.countries_compare1_select()]
        fig = px.pie(result_df, values="n", names="industry", labels={"industry": "Industry", "n": "Total unicorns"},
                     color_discrete_sequence=px.colors.diverging.delta)
        fig.update_layout(legend_title_text="Industries")

        return fig

    @render_plotly
    def countries_compare2_pie_chart():
        result = df.groupby(["country", "industry"])[["industry"]].agg(n=("industry", "count")).reset_index()
        result_df = result[result["country"] == input.countries_compare2_select()]
        fig = px.pie(result_df, values="n", names="industry", labels={"industry": "Industry", "n": "Total unicorns"},
                     color_discrete_sequence=px.colors.diverging.delta)
        fig.update_layout(legend_title_text="Industries")

        return fig

    @render_plotly
    def countries_compare3_pie_chart():
        result = df.groupby(["country", "industry"])[["industry"]].agg(n=("industry", "count")).reset_index()
        result_df = result[result["country"] == input.countries_compare3_select()]
        fig = px.pie(result_df, values="n", names="industry", labels={"industry": "Industry", "n": "Total unicorns"},
                     color_discrete_sequence=px.colors.diverging.delta)
        fig.update_layout(legend_title_text="Industries")

        return fig
