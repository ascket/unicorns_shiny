from typing import NamedTuple
from datetime import datetime


class CompanyFromTable(NamedTuple):
    company_name: str
    valuation: float
    date_joined: datetime
    country: str
    city: str
    industry: str
    investors: str


class CompanyFull(NamedTuple):
    company_name: str
    valuation: float
    date_joined: datetime | str
    country: str
    city: str
    industry: str
    investors: str
    founded_year: str | None
    total_raised: str | None
    about_company: str | None
    company_address_street: str | None
    company_address_city_state_zip: str | None
    company_address_city_country: str | None
    company_address_city_phone: str | None
    company_url: str | None
    company_img: str | None
    financials_investors_count: str | None
    financials_investments: str | None
    iso_alpha: str
    continent: str


class CompanyOverview(NamedTuple):
    founded_year: str | None
    total_raised: str | None
    about_company: str | None
    company_address_street: str | None
    company_address_city_state_zip: str | None
    company_address_city_country: str | None
    company_address_city_phone: str | None
    company_url: str | None
    company_img: str | None


class CompanyFinancials(NamedTuple):
    financials_investors_count: str | None
    financials_investments: str | None
