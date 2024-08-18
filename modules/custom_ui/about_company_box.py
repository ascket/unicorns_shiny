from shiny import ui, module


@module.ui
def about_company_box(company_photo: str, company_name: str, date_joined: str, company_industry: str, company_valuation: float,
                      company_total_raised: str, company_inverstors_company: float, company_founded_year: str,
                      about_company: str, company_location: str, company_url: str):
    result = ui.TagList(
        ui.tags.div(
            {"class": "box-body box-profile"},
            ui.tags.div(
                {"class": "img-wrapper"},
                ui.tags.img(
                    {"class": "custom-user-img img-responsive", "src": company_photo, "alt": "Firm logo picture"}
                )
            ),
            ui.tags.h3(
                {"class": "profile-username text-center"},
                company_name,
            ),
            ui.tags.p(
                {"class": "text-center"},
                company_industry
            ),
            ui.tags.ul(
                {"class": "list-group list-group-unbordered"},
                ui.tags.li(
                    {"class": "list-group-item"},
                    ui.tags.b("Valuation"),
                    ui.tags.p(
                        {"class": "pull-right"},
                        f"${company_valuation}B"
                    )
                ),
                ui.tags.li(
                    {"class": "list-group-item"},
                    ui.tags.b("Total raised"),
                    ui.tags.p(
                        {"class": "pull-right"},
                        company_total_raised if str(company_total_raised) != "nan" else "-"
                    )
                ),
                ui.tags.li(
                    {"class": "list-group-item"},
                    ui.tags.b("Inverstors count"),
                    ui.tags.p(
                        {"class": "pull-right"},
                        int(company_inverstors_company) if str(company_inverstors_company) != "nan" else "-"
                    )
                ),
                ui.tags.li(
                    {"class": "list-group-item"},
                    ui.tags.b("Founded year"),
                    ui.tags.p(
                        {"class": "pull-right"},
                        f"{company_founded_year:.0f}" if str(company_founded_year) != "nan" else "-"
                    )
                ),
                ui.tags.li(
                    {"class": "list-group-item"},
                    ui.tags.b("Joined year"),
                    ui.tags.p(
                        {"class": "pull-right"},
                        f"{date_joined.split('-')[0]}" if str(date_joined) != "nan" else "-"
                    )
                )
            )
        ),
        ui.tags.div(
            {"class": "box-body"},
            ui.tags.strong(
                ui.tags.i(
                    {"class": "lni lni-book"},
                    ui.tags.span(
                        {"class": "nav-text"},
                        "About"
                    )
                )
            ),
            ui.tags.p(
                about_company if str(about_company) != "nan" else "-"
            ),
            ui.tags.hr(),
            ui.tags.strong(
                ui.tags.i(
                    {"class": "lni lni-map-marker"},
                    ui.tags.span(
                        {"class": "nav-text"},
                        "Location"
                    )
                )
            ),
            ui.tags.p(
                company_location if company_location != " <br>nan<br>nan" else "-"
            ),
            ui.tags.hr(),
            ui.tags.strong(
                ui.tags.i(
                    {"class": "lni lni-link"},
                    ui.tags.span(
                        {"class": "nav-text"},
                        "Link"
                    )
                )
            ),
            ui.tags.p(
                ui.tags.a(
                    {"href": company_url, "target": "_blank"},
                    company_url
                ) if str(company_url) != "nan" else "-"
            )
        )
    )
    return result
