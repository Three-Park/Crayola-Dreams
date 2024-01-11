from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from diary.models import Diary
from .apps import GenimgConfig
from django.core.files.base import ContentFile
import openai

import io
import os
import warnings
from IPython.display import display
from PIL import Image
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

def generate_prompt(request, diary_id):
    user = request.user
    base_text = GenimgConfig.base_text
    diary_content = get_object_or_404(Diary, pk=diary_id, user=user).content

    completion = openai.Completion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"{base_text} {diary_content.strip()}"},]
    )    
    generated_text = completion["choices"][0]["message"]["content"]     # type: ignore
    output_text=generated_text.split('\n')
    prompts = [v for v in output_text if v]
    return render(request, 'generate_text.html', {'generated_text': generated_text})

def generate_img(request, diary_id):
    #prompt = generate_prompt(request, diarry_id)
    stability_api=GenimgConfig.stability_api
    answers = stability_api.generate(
            prompt="expansive landscape rolling greens with gargantuan yggdrasil, intricate world-spanning roots towering under a blue alien sky, masterful, ghibli", #prompts (from chatgpt)
            style_preset ="anime", 
            seed=4253978046, 
            steps=50,
            cfg_scale=8.0, 
            width=1024, 
            height=1024,
            samples=3,
        )

    for resp in answers:
        for artifact in resp.artifacts: # type: ignore
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                image_content = ContentFile(artifact.binary)
                diary = Diary.objects.get(pk=diary_id)
                diary.image_url.save(f"generated_image_{diary_id}.png", image_content, save=True)
    return HttpResponse("Images generated and saved to Diary's image_url field.")        
            
    
def generatedimg_view(request, diary_id):
    # Call your generate_img function
    generated_image_url = get_object_or_404(Diary, pk=diary_id, user=request.user).image_url

    # Pass the generated_image_url to the template context
    return render(request, 'generated_img.html', {'generated_image': generated_image_url})
