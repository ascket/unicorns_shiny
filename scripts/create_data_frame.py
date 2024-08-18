import pandas as pd
from collections import Counter


def map_data_frame(df_main: pd.DataFrame) -> pd.DataFrame:
    total_company_count_per_country = df_main.value_counts("country").reset_index().rename(
        columns={"count": "count_per_country"}).sort_values(by="country")

    total_valuation_count_per_country = df_main.groupby("country")[["valuation"]].agg(
        n=("valuation", "sum")).reset_index().rename(columns={"n": "count_valuation_per_country"}).sort_values(
        by="country")

    df_continent_alpha = df_main.drop_duplicates(subset="country")[["country", "iso_alpha", "continent"]].sort_values(
        by="country")

    merged_df = total_company_count_per_country.merge(total_valuation_count_per_country, on=["country"]).merge(
        df_continent_alpha, on=["country"])

    return merged_df


def company_per_year_data_frame(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("year_joined").size().reset_index().rename(columns={0: "n"})


def investor_industry_data_frame(df: pd.DataFrame) -> pd.DataFrame:
    investors_industry_dict = {}
    for _, row in df.iterrows():
        if not isinstance(row["investors_list"], float):
            for investor in row["investors_list"]:
                investors_industry_dict.setdefault(investor, list()).append(row["industry"])

    i2 = {}

    for key, values in investors_industry_dict.items():
        i2.setdefault(key, dict())
        counter = Counter(values)
        i2[key] = dict(Counter(values))
        i2[key]["Total"] = counter.total()

    new_df = pd.DataFrame(i2).T.fillna(0).astype(int)
    return new_df.reset_index().rename(columns={"index": "Investor"})

# def investor_industry_data_frame(df: pd.DataFrame) -> pd.DataFrame:
#     investors_industry_dict = {}
#     for _, row in df.iterrows():
#         if not isinstance(row["investors_list"], float):
#             for investor in row["investors_list"]:
#                 investors_industry_dict.setdefault(investor, list()).append(row["industry"])
#
#     new_df = pd.DataFrame.from_dict(investors_industry_dict, orient='index')
#     new_df = new_df.stack().reset_index()[["level_0", 0]].rename(columns={"level_0": "investor", 0: "industry"})
#
#     return new_df
