from pathlib import Path
import pandas as pd
from scripts import map_data_frame, investor_industry_data_frame
import os

root_dir = Path(__file__).parent
www_dir = Path(__file__).parent / "www"
main_unicorns_file = root_dir / "unicorns.csv"

pattern = r',[^,]|(?<![T, Co, Ltd, Corp, Inc, U, S, e.])\.\s*|,,\s*'

df = pd.read_csv(main_unicorns_file)
df[["year_joined", "month_joined", "day_joined"]] = df["date_joined"].str.split('-', expand=True)
df["investors_list"] = df["investors"].str.rstrip(",").str.replace("\t", "").str.split(pat=pattern)

def get_df_for_map():
    return map_data_frame(df)


def get_investor_industry_data_frame():
    return investor_industry_data_frame(df)


blue_color_main = "#2a7cc4"
#blue_color_main = "#23669d"
