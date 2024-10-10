from shiny import Inputs, Outputs, Session, ui, module
from shinywidgets import render_plotly, output_widget
from openai import AsyncOpenAI
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

gpt = AsyncOpenAI(api_key=os.getenv("OPEN_AI_PAY_KEY"), organization=os.getenv("ORG_PAY_ID"))
mistral = ChatMistralAI(api_key=os.getenv("MISTRAL_API"), model="mistral-large-latest")
llama = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
    model_name="llama-3.1-70b-versatile",
    # model_kwargs = {
    #     "response_format": {"type": "json_object"}
    # }
)

start_messages = "Hallo. Wie kann ich Ihnen helfen?"

@module.ui
def nav_panel_llm_charts_ui(name: str):
    return ui.nav_panel(
            ui.tags.span(name),
            ui.layout_columns(
                ui.card(
                    ui.card_header("GPT"),
                    ui.chat_ui("gpt_chat"),
                ),
                ui.card(
                    ui.card_header("Mistral"),
                    ui.chat_ui("mistral_chat"),
                ),
                ui.card(
                    ui.card_header("Llama"),
                    ui.chat_ui("llama_chat"),
                )
            ),
            icon=ui.tags.i({"class": "lni lni-comments-alt-2"})
        )


@module.server
def nav_panel_llm_charts_server(input: Inputs, output: Outputs, session: Session):
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
            model="gpt-4o",
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
