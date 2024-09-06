import pandas as pd
import os

root_dir = os.path.dirname(__file__)
www_dir = os.path.join(root_dir, "www")
css_dir = os.path.join(www_dir, "css")
js_dir = os.path.join(www_dir, "js")
styles_file_path = os.path.join(css_dir, "styles.css")
pill_list_js_path = os.path.join(js_dir, "pill_list_nav.js")
main_unicorns_file = os.path.join(root_dir, "unicorns.csv")
main_file_for_map = os.path.join(root_dir, "map_df.csv")
main_file_for_investors = os.path.join(root_dir, "investors_df.csv")

# main_unicorns_file = root_dir / "unicorns.csv"
# main_file_for_map = root_dir / "map_df.csv"
# main_file_for_investors = root_dir / "investors_df.csv"

pattern = r',[^,]|(?<![T, Co, Ltd, Corp, Inc, U, S, e.])\.\s*|,,\s*'

df = pd.read_csv(main_unicorns_file)
df["investors_list"] = df["investors"].str.rstrip(",").str.replace("\t", "").str.split(pat=pattern)
df_for_map = pd.read_csv(main_file_for_map)
df_investors_industry = pd.read_csv(main_file_for_investors)

blue_color_main = "#2a7cc4"
