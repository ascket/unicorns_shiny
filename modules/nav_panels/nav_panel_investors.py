import plotly.express as px
from shiny import Inputs, Outputs, Session, ui, module
from shinywidgets import render_plotly, output_widget

from shared import df_investors_industry


@module.ui
def nav_panel_investors_ui(name: str):
    return ui.nav_panel(
        ui.tags.span(name),
        ui.card(
            ui.card_header(
                "Investors"
            ),
            ui.input_select("top_investors", "Top Investors", choices=[str(x) for x in range(5, 41, 5)], selected="10"),
            output_widget("investors_industry_count"),
            full_screen=True
        ),
        icon=ui.tags.i({"class": "lni lni-briefcase-alt"})
    )


@module.server
def nav_panel_investors_server(input: Inputs, output: Outputs, session: Session):
    @render_plotly
    def investors_industry_count():
        #df = df_investors_industry.sort_values(by="Total", ascending=False).head(20)
        #investors_names = df["Investor"]

        # fig = go.Figure(data=[
        #     go.Bar(name="Media & Entertainment", x=investors_names, y=df["Media & Entertainment"], hovertemplate="%{y}", text=df["Total"]),
        #     go.Bar(name="Enterprise Tech", x=investors_names, y=df["Enterprise Tech"], hovertemplate="%{y}"),
        #     go.Bar(name="Healthcare & Life Sciences", x=investors_names, y=df["Healthcare & Life Sciences"], hovertemplate="%{y}"),
        #     go.Bar(name="Financial Services", x=investors_names, y=df["Financial Services"], hovertemplate="%{y}"),
        #     go.Bar(name="Consumer & Retail", x=investors_names, y=df["Consumer & Retail"], hovertemplate="%{y}"),
        #     go.Bar(name="Industrials", x=investors_names, y=df["Industrials"], hovertemplate="%{y}"),
        #     go.Bar(name="Insurance", x=investors_names, y=df["Insurance"], hovertemplate="%{y}"),
        #     go.Bar(name="Health", x=investors_names, y=df["Health"], hovertemplate="%{y}"),
        # ])
        #
        # fig.update_layout(barmode='stack', title="Stock Price Changes", legend_title_text = "Industries")
        # fig.update_xaxes(title_text="Investors")
        # fig.update_yaxes(title_text="Industries")
        # fig.update_traces(texttemplate="%{text}", textposition="outside")

        df = df_investors_industry.sort_values(by="Total", ascending=False).head(int(input.top_investors()))

        fig = px.bar(df, x="Investor", y=['Media & Entertainment', 'Enterprise Tech', 'Healthcare & Life Sciences', 'Financial Services','Consumer & Retail', 'Industrials', 'Insurance', 'Health', 'Total'], labels={"value": "Amount industry", "variable": "Industrie", "Investor": "Investor", "Total": "Total unicorns"}, text=df["Total"])
        #title="Stock Price Changes" - зайдёт в fig.update_layout
        fig.update_layout(legend_title_text="Industries")
        fig.update_xaxes(title_text="Investors")
        fig.update_yaxes(title_text="Industries")
        fig.update_traces(textposition="none")
        return fig
