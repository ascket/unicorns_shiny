import pandas as pd
import os
from typing import NamedTuple

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

class ModelsMistral(NamedTuple):
    """
    Mistral Models
    """
    small = "mistral-small-latest"
    medium = "mistral-medium-latest"
    large = "mistral-large-latest"


class ModelsGPT(NamedTuple):
    """
    OpenAI GPT Models
    """
    turbo3 = "gpt-3.5-turbo"
    turbo3_instruct = "gpt-3.5-turbo-instruct"
    gpt4 = "gpt-4"
    gpt4_turbo = "gpt-4-turbo"
    gpt4o = "gpt-4o"
    gpt4o_mini = "gpt-4o-mini"


class ModelsLlama(NamedTuple):
    """
    Llama Models
    """
    llama7 = "meta/llama-2-7b-chat",
    llama13 = "meta/llama-2-13b-chat",
    llama70 = "meta/llama-2-70b-chat"
    llama70_instruct = "meta/meta-llama-3-70b-instruct"
    llama70_versatile = "llama-3.1-70b-versatile"
    llama70_8192 = "llama3-70b-8192"
    llama8b_8b_instant = "llama-3.1-8b-instant"
    llama70_8192_groq = "llama3-groq-70b-8192-tool-use-preview"
