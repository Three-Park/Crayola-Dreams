from asyncio.windows_events import NULL
from django.apps import AppConfig
import openai
from stability_sdk import client
from IPython.display import display


class GenimgConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'genimg'

    base_text = open("./genimg/genTextBase.txt", 'r', encoding='utf-8').readlines()
    openai.api_key=""# API Key
    stability_api = client.StabilityInference(
        key="",# API Key reference.
        verbose=True, 
        engine="stable-diffusion-xl-1024-v1-0"
        )
