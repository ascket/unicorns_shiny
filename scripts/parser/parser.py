import threading
import time
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from requests import HTTPError

from scripts.parser.iso_continent_codes import iso_alpha_dict, continents_dict
from scripts.parser.models import CompanyFull, CompanyFinancials, CompanyOverview
from shared import root_dir
import os

INVESTORS_SPLIT_PATTERN = r',[^,]|(?<![T, Co, Ltd, Corp, Inc, U, S, e.])\.\s*|,,\s*'


class Parser:
    URI = r"https://www.cbinsights.com/research-unicorn-companies"

    def __init__(self):
        self.all_companies: List[CompanyFull] = []
        self.main_soup: BeautifulSoup = self.get_soup()
        self.table: BeautifulSoup = self.get_table()

    @staticmethod
    def get_soup(url: str = URI) -> BeautifulSoup:
        ua = UserAgent()
        user_agent = ua.random
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "User-Agent": user_agent
        }
        try:
            req = requests.get(url, headers=headers)
        except requests.ConnectTimeout:
            print("Sleep for 10 sec because of ConnectionTimeout")
            time.sleep(10)
            req = requests.get(url, headers=headers)
        req.raise_for_status()
        soup = BeautifulSoup(req.text, "lxml")
        return soup

    def get_overview(self, url: str) -> CompanyOverview:
        NO_LOGO_IMG_URL = "https://steelsport.de/img/nologo.png"
        try:
            soup_overview = self.get_soup(url)
            overview_and_products = soup_overview.find("div", {"data-test": "section-component"}).find_all("div", {
                "class": "Kpi_kpiItem__2CwXD"})

            result_dict = {}
            for result in overview_and_products:
                key = result.find("h2").text
                result_dict.setdefault(key)
                result_dict[key] = result.find("span").text

            overview_founded_year = result_dict.get("Founded Year")
            overview_total_raised = result_dict.get("Total Raised")

            company_info = soup_overview.find("div", {"data-test": "company-info"})
            about_company = company_info.find("p", {"data-test": "description"}).text
            company_headquater = company_info.find("address", {"data-test": "address"})
            company_address_street = company_headquater.find("p", {"data-test": "street"}).text
            company_address_city_state_zip = company_headquater.find("p", {"data-test": "city-state-zip"}).text
            company_address_city_country = company_headquater.find("p", {"data-test": "country"}).text
            company_address_city_phone = company_headquater.find("p", {"data-test": "phone"}).text

            header = soup_overview.find("main").find_all("header")

            try:
                company_img = header[1].find("img").attrs["src"]
            except AttributeError:
                print(f"Company image url error: {url}")
                company_img = NO_LOGO_IMG_URL

            company_url = header[1].find("a", {"class": "color--blue"}).attrs["href"]

            company = CompanyOverview(
                founded_year=overview_founded_year,
                total_raised=overview_total_raised,
                about_company=about_company,
                company_address_street=company_address_street,
                company_address_city_state_zip=company_address_city_state_zip,
                company_address_city_country=company_address_city_country,
                # company_address_city_phone=company_address_city_phone if company_address_city_phone else "No phone number found",
                company_address_city_phone=company_address_city_phone,
                company_url=company_url if company_url != "https://" else None,
                company_img=company_img
            )
        except HTTPError:
            print(f"Overview site not found: {url}")
            company = CompanyOverview(
                founded_year=None,
                total_raised=None,
                about_company=None,
                company_address_street=None,
                company_address_city_state_zip=None,
                company_address_city_country=None,
                company_address_city_phone=None,
                company_url=None,
                company_img=NO_LOGO_IMG_URL
            )
        return company

    def get_financials(self, url: str) -> CompanyFinancials:
        URI = f"{url}/financials"
        try:
            soup_financials = self.get_soup(URI)
            try:
                financials = soup_financials.find("div", {"data-test": "kpi-section"}).find_all("div", {
                    "class": "Kpi_kpiItem__2CwXD"})
            except AttributeError:
                print(f"Financials site not found: {URI}")
                return CompanyFinancials(
                    financials_investments=None,
                    financials_investors_count=None
                )
            result_dict = {}
            for result in financials:
                key = result.find("h2").text
                result_dict.setdefault(key)
                result_dict[key] = result.find("span").text

            financials_investors_count = result_dict.get("Investors Count")
            financials_investments = result_dict.get("Investments")
            company = CompanyFinancials(
                financials_investors_count=financials_investors_count,
                financials_investments=financials_investments
            )
        except HTTPError:
            company = CompanyFinancials(
                financials_investments=None,
                financials_investors_count=None
            )
        return company

    def get_table(self) -> BeautifulSoup:
        table = self.main_soup.find("table", class_="sortable-theme-bootstrap")
        return table

    def get_table_head(self) -> List[str]:
        t_head = self.table.find("thead").find_all("th")
        table_header = [head.text for head in t_head]
        return table_header

    def set_full_company_info_threading(self, how_many_companies: int = 0) -> None:
        print("Start working...")
        tbody_tr = self.table.find_all("tr")
        tbody_tr_len = len(tbody_tr)
        if how_many_companies >= tbody_tr_len:
            raise ValueError(f"Company count must be less than {tbody_tr_len - 2}")
        if how_many_companies:
            count = how_many_companies + 1
        else:
            count = tbody_tr_len - 1

        def download_companies(start, stop):
            right_cb_company_url = {'Moon Active': 'https://www.cbinsights.com/company/moon-active',
                                    'bolttech': 'https://www.cbinsights.com/company/bolttech',
                                    'Printful': 'https://www.cbinsights.com/company/printful-1',
                                    'Rappi': 'https://www.cbinsights.com/company/rappi',
                                    'REEF Technology': 'https://www.cbinsights.com/company/reef-technology',
                                    '21.co': 'https://www.cbinsights.com/company/21e6',
                                    'Gaussian Robotics': 'https://www.cbinsights.com/company/gaussian-robotics',
                                    'People.ai': 'https://www.cbinsights.com/company/peopleai',
                                    'Lambda Labs': 'https://www.cbinsights.com/company/lambda-labs-1',
                                    'Iluvatar CoreX': 'https://www.cbinsights.com/company/iluvatar-corex',
                                    'Articulate': 'https://www.cbinsights.com/company/articulate-1',
                                    'Island': 'https://www.cbinsights.com/company/island-2',
                                    'Imbue': 'https://www.cbinsights.com/company/imbue-ai'}
            for tr in tbody_tr[start:stop]:
                all_td = tr.find_all("td")
                company_name: str = all_td[0].text
                cb_company_url = right_cb_company_url.get(company_name)
                if cb_company_url is None:
                    cb_company_url: str = all_td[0].find("a").attrs["href"]
                overview = self.get_overview(cb_company_url)
                valuation: float = float(all_td[1].text.replace("$", ""))
                date_str = all_td[2].text
                date_joined: datetime = datetime.strptime(date_str,
                                                          '%m/%d/%Y')  # чтобы парсить дату сразу в формате даты. Но в этом случае дата в таблице в дашборде выходит в некрасивом формате
                month_joined, day_joined, year_joined = date_str.split("/")
                # date_joined: str = all_td[2].text
                city: str = all_td[4].text
                country: str = all_td[3].text if city != "Hong Kong" else "Hong Kong"
                industry: str = all_td[5].text
                investors: str = all_td[6].text
                financials = self.get_financials(cb_company_url)
                iso_alpha = iso_alpha_dict.get(country, None)
                continent = continents_dict.get(country, None)
                self.all_companies.append(
                    CompanyFull(
                        company_name=company_name,
                        valuation=valuation,
                        date_joined=date_joined,
                        country=country if country != "" else "Singapore",
                        # у единственной компании Quest Global пропущена страна, поэтому Singapore
                        city=city,
                        industry=industry,
                        investors=investors,
                        founded_year=overview.founded_year,
                        total_raised=overview.total_raised,
                        about_company=overview.about_company,
                        company_address_street=overview.company_address_street,
                        company_address_city_state_zip=overview.company_address_city_state_zip,
                        company_address_city_country=overview.company_address_city_country,
                        company_address_city_phone=overview.company_address_city_phone,
                        company_url=overview.company_url,
                        company_img=overview.company_img,
                        financials_investors_count=financials.financials_investors_count,
                        financials_investments=financials.financials_investments,
                        iso_alpha=iso_alpha,
                        continent=continent,
                        year_joined=year_joined,
                        month_joined=month_joined,
                        day_joined=day_joined
                    )
                )
            print(f"Companies [{start}: {stop}] was downloaded!")

        start_working = time.perf_counter()
        download_threads = []
        for i in range(1, count, 20):
            # download_thread = threading.Timer(interval=5.0, function=download_companies, args=(i, i+20))
            download_thread = threading.Thread(target=download_companies, args=(i, i + 20))
            download_threads.append(download_thread)
            download_thread.start()
        for thread in download_threads:
            thread.join()
        stop_working = time.perf_counter() - start_working
        print(
            f"Done. Working time: {stop_working:.0f} sec. Companies downloaded: {len(self.all_companies)} of {tbody_tr_len - 1}")

    def get_full_company_info_threading(self, how_many_companiest_to_parse: int = 0) -> List[CompanyFull]:
        if len(self.all_companies) == 0:
            self.set_full_company_info_threading(how_many_companiest_to_parse)
        return self.all_companies

    def write_results_as_csv(self, file_name: str) -> None:
        """
        Записывает общие результаты для ТАБЛИЦЫ в csv-файл. В получившемся csv-файле должен быть столбец investors_list с данными в формате list, но формат list не может быть записан в формат csv. Поэтому, основной метод для записи файлов - write_results_as_csv_with_pandas. В этом методе я сначала перегоняю данные из парсера в pd.DataFrame, сохраняю этот дата фрейм в csv файл, потом добавляю в этот дата фрейм столбец investors_list и делаю из дополненного дата фрейма ещё 2 дата фрейма для карты и инвесторов.
        """
        if len(self.all_companies) == 0:
            raise AttributeError("First run get_full_company_info()-function to collect all companies")

        import csv
        with open(f"{file_name}.csv", "w", newline='', encoding='utf-8') as file_names:
            writer = csv.writer(file_names, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(CompanyFull.__dict__["__annotations__"].keys())  # шапка (если нужна шапка)
            for company in self.all_companies:
                writer.writerow([
                    company.company_name,
                    company.valuation,
                    datetime.strftime(company.date_joined, "%Y-%m-%d"),
                    company.country,
                    company.city,
                    company.industry,
                    company.investors,
                    company.founded_year,
                    company.total_raised,
                    company.about_company,
                    company.company_address_street,
                    company.company_address_city_state_zip,
                    company.company_address_city_country,
                    company.company_address_city_phone,
                    company.company_url,
                    company.company_img,
                    company.financials_investors_count,
                    company.financials_investments,
                    company.iso_alpha,
                    company.continent,
                    company.year_joined,
                    company.month_joined,
                    company.day_joined
                ])
        print("Data is saved in the .csv-file")

    def write_results_as_csv_with_pandas(self, file_name: str) -> None:
        """
        The main method for writing data and creating dataframes
        """
        import pandas as pd
        from scripts import map_data_frame, investor_industry_data_frame
        pattern = r',[^,]|(?<![T, Co, Ltd, Corp, Inc, U, S, e.])\.\s*|,,\s*'
        # self.write_results_as_csv(file_name)
        df_from_parser = pd.DataFrame(self.all_companies)
        df_from_parser.to_csv(os.path.join(root_dir, f"{file_name}.csv"), index=False)
        print(f"{file_name}.csv saved")
        df_from_parser["investors_list"] = df_from_parser["investors"].str.rstrip(",").str.replace("\t", "").str.split(
            pat=pattern)
        df_for_map = map_data_frame(df_from_parser)
        df_for_investors = investor_industry_data_frame(df_from_parser)
        df_for_map.to_csv(os.path.join(root_dir, "map_df22.csv"), index=False)
        print(f"map_df.csv saved")
        df_for_investors.to_csv(os.path.join(root_dir, "investors_df22.csv"), index=False)
        print(f"investors_df.csv saved")

    def __len__(self):
        return len(self.all_companies)


if __name__ == '__main__':
    parser = Parser()
    parser.get_full_company_info_threading()
    parser.write_results_as_csv_with_pandas("unicorns22")
