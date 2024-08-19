from datetime import datetime, timedelta

import faicons
from shiny import Inputs, Outputs, Session, render, ui, reactive, req
from shiny import module

from modules.custom_ui.about_company_box import about_company_box
from shared import df



date_joined_date_range_params = {
    "min": df["date_joined"].min(),
    "max": df["date_joined"].max(),
    "start": df["date_joined"].min(),
    "end": df["date_joined"].max()
}

df_min_date_datetime = datetime.strptime(df["date_joined"].min(), "%Y-%m-%d").date()
df_max_date_datetime = datetime.strptime(df["date_joined"].max(), "%Y-%m-%d").date()
date_joined_slider_params = {
    "min": df_min_date_datetime,
    "max": df_max_date_datetime,
    "value": (df_min_date_datetime, df_max_date_datetime)
}

df_min_valuation = df["valuation"].min()
df_max_valuation = df["valuation"].max()
valuation_slider_params = {
    "min": df_min_valuation,
    "max": df_max_valuation,
    "value": (df_min_valuation, df_max_valuation)
}

#two_days = timedelta(days=2)

# pattern = r',[^,]|(?<![T, Co, Ltd, Corp, Inc, U, S, e.])\.\s*|,,\s*'
# df_dropna_investors = df.dropna(subset=["investors"])
# all_investors_from_df = df_dropna_investors["investors"].str.split(pat=pattern)

all_investors_list = []
for investors in df["investors_list"]:
    if not isinstance(investors, float):
        all_investors_list += investors

all_investors_list = list(set(all_investors_list))


@module.ui
def nav_panel_table_ui(name: str):
    return ui.nav_panel(
        ui.tags.span(name),
        ui.layout_column_wrap(
            ui.value_box(
                "Total Number of Companies".upper(),
                ui.output_ui("value_box_total_number_companies"),
                showcase=faicons.icon_svg("building", fill="white!important", margin_left="8px"),
                class_="text-white bg-primary company-table-value-box",
            ),
            ui.value_box(
                "Total Valuation ($B)".upper(),
                ui.output_ui("value_box_total_valuation"),
                showcase=faicons.icon_svg("dollar-sign", fill="white!important", margin_left="8px"),
                class_="text-white bg-primary company-table-value-box"
            ),
            ui.value_box(
                "Total Number of Industries".upper(),
                ui.output_ui("value_box_total_number_industries"),
                showcase=faicons.icon_svg("industry", fill="white!important", margin_left="8px"),
                class_="text-white bg-primary company-table-value-box"
            ),
            fill=False,
        ),
        ui.layout_columns(
            ui.input_select("companys", "Company", choices=df["company_name"].unique().tolist(),
                            selectize=True, multiple=True,
                            options=({"placeholder": "All", "plugins": ["clear_button"]})),
            ui.input_slider("valuation", "Valuation", step=1, **valuation_slider_params),
            # ui.input_date_range("date_joined_slider", "Date", **date_joined_date_range_params),
            ui.input_slider("date_joined_slider", "Date Joined", time_format="%Y-%m",
                            **date_joined_slider_params),
            # слайдер для фильтра по дате
            ui.input_select("country", "Country", choices=df["country"].unique().tolist(),
                            selectize=True,
                            multiple=True,
                            options=({"placeholder": "All", "plugins": ["clear_button"]})),
            ui.input_select("city", "City", choices=df["city"].unique().tolist(), selectize=True,
                            multiple=True,
                            options=({"placeholder": "All", "plugins": ["clear_button"]})),
            ui.input_select("industry", "Industry", choices=df["industry"].unique().tolist(),
                            selectize=True, multiple=True,
                            options=({"placeholder": "All", "plugins": ["clear_button"]})),
            ui.input_select("investors", "Investors", choices=all_investors_list,
                            selectize=True, multiple=True,
                            options=({"placeholder": "All", "plugins": ["clear_button"]})),
        ),
        ui.layout_columns(
            ui.input_action_button("cleat_filter_btn", "Reset filters", class_="btn-primary",
                                   disabled=True),
            ui.card(style="display: none;"),
            ui.popover(
                faicons.icon_svg("circle-exclamation"),
                ui.tags.p(
                    ui.tags.b("CTRL + left mouse button"),
                    " to select or deselect multiple table rows ",
                    ui.tags.b("and scroll down"),
                    " to see more information about company"
                ),
                title="Hint: select rows",
                style="text-align: right; font-size: 1.2rem; color: #23669d",
            ),
            # ui.input_switch("save_selected_rows_switch", "Save rows?"),
            col_widths=(2, 8, 2)
        ),
        # ui.layout_columns(
        #     ui.input_action_button("deselect_rows", "Deselect rows")
        # ),
        ui.output_data_frame("tbl"),
        ui.output_ui("clearrowspanel"),
        ui.output_ui("tbl_row_output"),
        icon=ui.tags.i({"class": "lni lni-layout"})
    )


@module.server
def nav_panel_table_server(input: Inputs, output: Outputs, session: Session):
    val = reactive.value(set())

    @reactive.calc
    def selected_table():
        dates = input.date_joined_slider()
        # На локальной машине даты, кот. приходят из слайдера, на 1 час меньше реальных дат, кот. передаются в слайдер. Поэтому, даты из слайдера после "округления" не совпадают на 1 день с реальными датами. Чтобы это исправить, дорабатываю даты из слайдена так: отнимаю 2 дня от начальной даты и прибаляю 2 дня к конечной дате. Это просто расширяет диапазон дат, по которым берутся данные из дата фрейма.
        #start_time = dates[0] - two_days
        #end_time = dates[1] + two_days
        start_time = dates[0]
        end_time = dates[1]
        # print(start_time)
        # print(end_time)
        # print(dates[0])
        # print(dates[1])
        # mask = (df['date_joined'] >= dates[0].strftime("%Y-%m-%d")) & (df['date_joined'] <= dates[1].strftime("%Y-%m-%d"))
        # date_table = df.loc[mask]
        date_table = df[df['date_joined'].between(start_time.strftime("%Y-%m-%d"), end_time.strftime("%Y-%m-%d"))]
        if input.companys():
            date_table = date_table.loc[(date_table['company_name'].isin(input.companys()))]
        if input.valuation():
            date_table = date_table.loc[(date_table['valuation'].between(*input.valuation()))]
        if input.country():
            date_table = date_table.loc[(date_table['country'].isin(input.country()))]
        if input.city():
            date_table = date_table.loc[(date_table['city'].isin(input.city()))]
        if input.industry():
            date_table = date_table.loc[(date_table['industry'].isin(input.industry()))]
        if input.investors():
            date_table = date_table[date_table["investors_list"].apply(
                lambda x: any(name in x for name in input.investors() if not isinstance(x, float)))]

        val.set(
            set())  # обнуляю выбранные ячейки, иначе в консоль выходит IndexError("single positional indexer is out-of-bounds"), если в таблице выбираешь самые нижние строки и дёргаешь какой-нибудь фильтр. На работу приложения эта ошибка не влияет, просто выходит в консоль, но для верности решил здесь обнулять переменную
        return date_table

    # @reactive.calc
    # @reactive.event(input.tbl_selected_rows)
    # def get_selected_rows():
    #     req(input.save_selected_rows_switch())
    #     # req(input.tbl_selected_rows()) #можно так, но тогда, если выбираешь ячейки, а потом их делаешь невыбранными, то последняя невыбранная остаётся сохранённой в выводе
    #
    #     with reactive.isolate():
    #         x = input.tbl_selected_rows()
    #     return list(x)

    # @reactive.effect
    # def _():
    #     print(get_selected_rows())
    #     print(f"Selected rows: {input.tbl_selected_rows()}")
    #     print(len(input.tbl_selected_rows()))

    @reactive.effect
    @reactive.event(input.tbl_selected_rows)
    def _():
        val.set(input.tbl_selected_rows())

    @reactive.effect
    @reactive.event(input.deselect_rows)
    async def _():
        val.set(set())
        await tbl.update_cell_selection(None)

    @render.data_frame
    def tbl():
        date_table = selected_table()[
            ['company_name', 'valuation', 'date_joined', 'country', 'city', 'industry', 'investors']].rename(
            columns={
                "company_name": "Company",
                "valuation": "Valuation ($B)",
                "date_joined": "Date Joined",
                "country": "Country",
                "city": "City",
                "industry": "Industry",
                "investors": "Investors"
            }
        )
        return render.DataGrid(
            date_table,
            selection_mode="rows",
            height="550px",
            width="100%"
        )

    @render.ui
    def tbl_row_output():
        req(val.get())
        df = selected_table()
        result = [
            ui.card(
                about_company_box(
                    "about_company_box",
                    df.iloc[x]["company_img"],
                    df.iloc[x]["company_name"],
                    df.iloc[x]["date_joined"],
                    df.iloc[x]["industry"],
                    df.iloc[x]["valuation"],
                    df.iloc[x]["total_raised"],
                    df.iloc[x]["financials_investors_count"],
                    df.iloc[x]["founded_year"],
                    df.iloc[x]["about_company"],
                    ui.HTML(
                        f'{df.iloc[x]["company_address_street"]}<br>{df.iloc[x]["company_address_city_state_zip"]}<br>{df.iloc[x]["company_address_city_country"]}<br>{df.iloc[x]["company_address_city_phone"]}'
                    ) if str(df.iloc[x]["company_address_city_phone"]) != "nan" else ui.HTML(
                        f'{df.iloc[x]["company_address_street"]}<br>{df.iloc[x]["company_address_city_state_zip"]}<br>{df.iloc[x]["company_address_city_country"]}'
                    ),
                    df.iloc[x]["company_url"]
                ),
                class_="box-success"
            ) for x in val.get()
        ]
        return ui.layout_column_wrap(
            *result, width=1 / 4
        )

    @render.ui
    def clearrowspanel():
        req(val.get())
        return ui.layout_columns(
            ui.input_action_button("deselect_rows", "Deselect rows", class_="btn-primary"),
            col_widths=(2,),
            id="clearrowspanel"
        )

    @reactive.effect
    @reactive.event(input.cleat_filter_btn)
    def _():
        ui.update_select("companys", selected=[])
        ui.update_slider("valuation", **valuation_slider_params)
        ui.update_slider("date_joined_slider", **date_joined_slider_params)
        ui.update_select("country", selected=[])
        ui.update_select("city", selected=[])
        ui.update_select("industry", selected=[])
        ui.update_select("investors", selected=[])

    @reactive.effect
    @reactive.event(input.companys, input.country, input.city, input.industry, input.valuation,
                    input.date_joined_slider, input.investors)
    def _():
        # timedelta(days=1) прибавляю 1 день, т.к. из слайдера приходят даты на 1-2 часа меньше реальных. Проблема выходит на локальной машине. Думаю, что проблема из-за часовых поясов, при заливке на сервер shinyapps проблема исчезает, т.к. сервер бежит в USA. Если запускаешь на локальной машине, то замени input.date_joined_slider() != date_joined_slider_params["value"] на
        #(input.date_joined_slider()[0] + timedelta(days=1), input.date_joined_slider()[1] + timedelta(days=1)) != date_joined_slider_params["value"]
        if input.companys() \
                or input.country() \
                or input.investors() \
                or input.city() \
                or input.industry() \
                or input.valuation() != valuation_slider_params["value"] \
                or input.date_joined_slider() != date_joined_slider_params["value"]:
            ui.update_action_button("cleat_filter_btn", disabled=False)
        else:
            ui.update_action_button("cleat_filter_btn", disabled=True)

    @render.ui
    def value_box_total_number_companies():
        result = len(selected_table())
        return f"{result}"

    @render.ui
    def value_box_total_valuation():
        result = selected_table()["valuation"].sum()
        return f"{result:.2f}"

    @render.ui
    def value_box_total_number_industries():
        result = len(selected_table()["industry"].unique())
        return f"{result}"
