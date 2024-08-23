from pathlib import Path

import pandas as pd

root_dir = Path(__file__).parent
www_dir = Path(__file__).parent / "www"
main_unicorns_file = root_dir / "unicorns.csv"
main_file_for_map = root_dir / "map_df.csv"
main_file_for_investors = root_dir / "investors_df.csv"

pattern = r',[^,]|(?<![T, Co, Ltd, Corp, Inc, U, S, e.])\.\s*|,,\s*'

df = pd.read_csv(main_unicorns_file)
df["investors_list"] = df["investors"].str.rstrip(",").str.replace("\t", "").str.split(pat=pattern)
df_for_map = pd.read_csv(main_file_for_map)
df_investors_industry = pd.read_csv(main_file_for_investors)

blue_color_main = "#2a7cc4"
