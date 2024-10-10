# EGYM -> Country Germany
# Helsing -> City Munich

from shiny import App, Inputs, Outputs, Session, ui
from modules import (
    nav_panel_table_ui,
    nav_panel_table_server,
    nav_panel_map_ui,
    nav_panel_map_server,
    nav_panel_investors_ui,
    nav_panel_investors_server,
    nav_panel_about_server,
    nav_panel_about_ui
)
from shared import pill_list_js_path, styles_file_path, www_dir
import uvicorn

from openai import AsyncOpenAI
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from shared import (
    ModelsMistral,
    ModelsGPT,
    ModelsLlama
)

load_dotenv()

gpt = AsyncOpenAI(api_key=os.getenv("OPEN_AI_PAY_KEY"), organization=os.getenv("ORG_PAY_ID"))
mistral = ChatMistralAI(api_key=os.getenv("MISTRAL_API"), model=ModelsMistral.small)
llama = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
    model_name=ModelsLlama.llama8b_8b_instant,
    # model_kwargs = {
    #     "response_format": {"type": "json_object"}
    # }
)

start_messages = "Hello. How can I help you?"

app_ui = ui.page_fluid(
    ui.head_content(
        ui.include_css(styles_file_path),
        ui.tags.link(
            {
                "rel": "shortcut icon", "href": "https://steelsport.de/img/favicon.ico"
            }
        )
    ),
    ui.navset_pill_list(
        nav_panel_table_ui("nav_panel_table", "Table"),
        nav_panel_map_ui("nav_panel_map", "Map"),
        nav_panel_investors_ui("nav_panel_investors", "Investors"),
        ui.nav_panel(
            ui.tags.span("LLM's"),
            ui.layout_columns(
                ui.card(
                    ui.card_header("OpenAI GPT-4o mini"),
                    ui.chat_ui("gpt_chat"),
                ),
                ui.card(
                    ui.card_header("Mistral Small"),
                    ui.chat_ui("mistral_chat"),
                ),
                ui.card(
                    ui.card_header("Meta Llama 3.1 8B"),
                    ui.chat_ui("llama_chat"),
                )
            ),
            icon=ui.tags.i({"class": "lni lni-comments-alt-2"})
        ),
        nav_panel_about_ui("nav_panel_about", "About"),
        widths=(2, 10),
        header=ui.TagList(
            ui.tags.div(
                {"class": "d-flex"},
                ui.tags.button(
                    {"class": "toggle-btn", "type": "button"},
                    ui.tags.i(
                        {"class": "lni lni-menu"}
                    )
                )
            )
        )
    ),
    ui.include_js(pill_list_js_path),
    title="Unicorn companies"
)


def server(input: Inputs, output: Outputs, session: Session):
    nav_panel_table_server("nav_panel_table")
    nav_panel_map_server("nav_panel_map")
    nav_panel_investors_server("nav_panel_investors")
    chatgpt = ui.Chat(id="gpt_chat", messages=[
        start_messages,
    ])

    chatmistral = ui.Chat(id="mistral_chat", messages=[
        start_messages,
    ])

    chatllama = ui.Chat(id="llama_chat", messages=[
        start_messages,
    ])

    @chatgpt.on_user_submit
    async def chat_gpt():
        messages = chatgpt.messages(format="openai")
        response = await gpt.chat.completions.create(
            model=ModelsGPT.gpt4o_mini,
            messages=messages,
            stream=True
        )
        await chatgpt.append_message_stream(response)

    @chatmistral.on_user_submit
    async def chat_mistral():
        messages = chatmistral.messages(format="langchain")
        response = mistral.astream(messages)
        await chatmistral.append_message_stream(response)

    @chatllama.on_user_submit
    async def chat_llama():
        messages = chatllama.messages(format="langchain")
        response = llama.astream(messages)
        await chatllama.append_message_stream(response)


app = App(app_ui, server, static_assets=www_dir)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
