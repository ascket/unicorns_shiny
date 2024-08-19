import faicons
import plotly.express as px
from shiny import Inputs, Outputs, Session, ui, module, reactive, render
from shinywidgets import render_plotly, output_widget

from scripts import company_per_year_data_frame
from shared import df, blue_color_main, df_for_map

COUNTRY_CONTINENT_MAP = {
    "Country": "country",
    "Continent": "continent",
    "Total Valuation": "count_valuation_per_country",
    "Total Unicorns": "count_per_country"
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
                        ["Total Valuation", "Total Unicorns"],
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
                "Compare countries by industries"
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
                range_color=[0, max_count_per_country] if size == "Total Unicorns" else [0, max_count_valuation],  # Задаем диапазон значений для цвета
                scope="world",
                hover_data={"country": True, "count_per_country": True,
                            "count_valuation_per_country": ":.2f", "iso_alpha": False,
                            "continent": False},
                labels={"count_per_country": "Total Unicorns", "continent": "Continent",
                        "country": "Country", "count_valuation_per_country": "Valuation ($B)"},
            )
        else:
            fig = px.bar(df_for_map, y=COUNTRY_CONTINENT_MAP[size], x="country", text=COUNTRY_CONTINENT_MAP[size],
                         labels={"count_per_country": "Total Unicorns", "continent": "Continent", "country": "Country",
                                 "count_valuation_per_country": "Valuation ($B)"}, color_discrete_sequence=[blue_color_main])
            fig.update_traces(texttemplate="%{text:.2f}", textposition="outside") if COUNTRY_CONTINENT_MAP[
                                                                                         size] == "count_valuation_per_country" else fig.update_traces(
                texttemplate="%{text}", textposition="outside")
            #font = {"size": 14} - можно добавить в fig.update_layout
            fig.update_layout(xaxis={'categoryorder': 'total descending'}, uniformtext_minsize=9,
                              uniformtext_mode="show", modebar_remove=["autoscale", "lasso", "reset", "select"])
        return fig


    @render_plotly
    def line_plot_company_per_year():
        data_frame = company_per_year_data_frame(df)
        fig = px.line(data_frame, x="year_joined", y="n", text="n", labels={"year_joined": "Year Joined", "n": "Total Unicorns"}, color_discrete_sequence=[blue_color_main])
        fig.update_traces(textposition="bottom right")
        return fig


    reactive_first = reactive.value("Germany")
    reactive_second = reactive.value("United States")
    reactive_third = reactive.value("China")
    reactive_fourth = reactive.value("India")
    reactives = [reactive_first, reactive_second, reactive_third, reactive_fourth]

    @reactive.calc
    def col_names():
        return [
            (f"countries_compare{x}", reactives[x]) for x in range(input.amount_countries_compare())
        ]

    @render.ui
    @reactive.event(input.amount_countries_compare)
    def countries_compare_ui():
        result = [
            ui.card(
                ui.input_select(f"{order_num}_select", "Select country", choices=df_for_map["country"].tolist(),
                                selected=reactive_value.get()),
                output_widget(f"{order_num}_pie_chart"),
            ) for order_num, reactive_value in col_names()
        ]
        return ui.layout_columns(
            *result
        )

    @render_plotly
    def countries_compare0_pie_chart():
        result = df.groupby(["country", "industry"])[["industry"]].agg(n=("industry", "count")).reset_index()
        input.countries_compare0_select()
        with reactive.isolate():
            reactive_first.set(input.countries_compare0_select())
            result_df = result[result["country"] == reactive_first.get()]
        fig = px.pie(result_df, values="n", names="industry", labels={"industry": "Industry", "n": "Total Unicorns"},
                     color_discrete_sequence=px.colors.diverging.delta)
        fig.update_layout(legend_title_text="Industries")

        return fig

    @render_plotly
    def countries_compare1_pie_chart():
        result = df.groupby(["country", "industry"])[["industry"]].agg(n=("industry", "count")).reset_index()
        input.countries_compare1_select()
        with reactive.isolate():
            reactive_second.set(input.countries_compare1_select())
            result_df = result[result["country"] == reactive_second.get()]
        fig = px.pie(result_df, values="n", names="industry", labels={"industry": "Industry", "n": "Total Unicorns"},
                     color_discrete_sequence=px.colors.diverging.delta)
        fig.update_layout(legend_title_text="Industries")

        return fig

    @render_plotly
    def countries_compare2_pie_chart():
        result = df.groupby(["country", "industry"])[["industry"]].agg(n=("industry", "count")).reset_index()
        input.countries_compare2_select()
        with reactive.isolate():
            reactive_third.set(input.countries_compare2_select())
            result_df = result[result["country"] == reactive_third.get()]
        fig = px.pie(result_df, values="n", names="industry", labels={"industry": "Industry", "n": "Total Unicorns"},
                     color_discrete_sequence=px.colors.diverging.delta)
        fig.update_layout(legend_title_text="Industries")

        return fig

    @render_plotly
    def countries_compare3_pie_chart():
        result = df.groupby(["country", "industry"])[["industry"]].agg(n=("industry", "count")).reset_index()
        input.countries_compare3_select()
        with reactive.isolate():
            reactive_fourth.set(input.countries_compare3_select())
            result_df = result[result["country"] == reactive_fourth.get()]
        fig = px.pie(result_df, values="n", names="industry", labels={"industry": "Industry", "n": "Total Unicorns"},
                     color_discrete_sequence=px.colors.diverging.delta)
        fig.update_layout(legend_title_text="Industries")

        return fig
