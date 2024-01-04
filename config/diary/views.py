from django.shortcuts import render, get_object_or_404, redirect
from .models import Diary
from .forms import DiaryForm
from django.contrib.auth.decorators import login_required

import logging

logger = logging.getLogger(__name__)

@login_required
def create_diary(request):
    if request.method == 'POST':
        form = DiaryForm(request.POST)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.user = request.user
            diary.save()
            return redirect('image_select',pk=diary.pk) 
    else:
        form = DiaryForm()

    return render(request, 'create_diary.html', {'form': form})

@login_required
def diary_list(request):
    diaries = Diary.objects.filter(user=request.user)
    return render(request, 'diary_list.html', {'diaries': diaries})

@login_required
def view_diary(request, pk):
    user = request.user
    diary = get_object_or_404(Diary, pk=pk, user=user)
    return render(request, 'view_diary.html', {'diary': diary})

@login_required
def edit_diary(request, pk):
    user = request.user
    diary = get_object_or_404(Diary, pk=pk, user=user)

    if request.method == 'POST':
        form = DiaryForm(request.POST, instance=diary)
        if form.is_valid():
            form.save()
            return redirect('diary_list')  
    else:
        form = DiaryForm(instance=diary)

    return render(request, 'edit_diary.html', {'form': form, 'diary': diary})

@login_required
def delete_diary(request, pk):
    user = request.user
    diary = get_object_or_404(Diary, pk=pk, user=user)

    if request.method == 'POST':
        diary.delete()
        return redirect('diary_list') 
    return render(request, 'delete_diary.html', {'diary': diary})

"""
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import openai
from IPython.display import display
from PIL import Image
import os
import io
import uuid

@login_required
def image_select(request, pk):
    user = request.user
    diary = get_object_or_404(Diary, pk=pk, user=user)
    form =  DiaryForm(request.POST, instance=diary)
    if request.method == 'POST':
        if form.is_valid():
            logger.info("Form is valid")
            
            diary_content = form.cleaned_data['content']
            logger.info(diary_content)
            
            generated_image_url = generate_image_url(diary_content)
            logger.info(f"Generated Image URL: {generated_image_url}")
            
            diary.image_url = generated_image_url
            diary.save()

            return redirect('view_diary')
    else:
        logger.error(f"Form is invalid. Errors: {form.errors}")
        form = DiaryForm(instance=diary)

    return render(request, 'image_select.html', {'diary': diary})


def generate_image_url(content):
    stability_api = client.StabilityInference(
        key='grpc.stability.ai:443', 
        verbose=False, 
        engine="stable-diffusion-xl-1024-v1-0"
    )
        
    prompt = generate_prompt(content)    
    print(prompt)
    answers = stability_api.generate(
        prompt = prompt,
        style_preset ="anime", 
        seed=4253978046,
        steps=50, 
        cfg_scale=8.0,
        width=1024, 
        height=1024, 
        samples=3,
        sampler=generation.SAMPLER_K_DPMPP_2M, 
    )
    
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
    if img is None:
        # Handle the case where no valid image is found
        raise ValueError("No valid image found in the response artifacts.")   
             
    generated_image = img
    filename = f'{uuid.uuid4()}.png'
    image_path = os.path.join(settings.MEDIA_ROOT, 'generated_images', filename)
    generated_image.save(image_path)
    image_url = f'/media/{os.path.basename(image_path)}'
    
    return image_url

def generate_image(content):
    stability_api = client.StabilityInference(
        key='grpc.stability.ai:443', 
        verbose=False, 
        engine="stable-diffusion-xl-1024-v1-0"
    )
        
    prompt = generate_prompt(content)    
    
    answers = stability_api.generate(
        prompt = prompt,
        style_preset ="anime", 
        seed=4253978046,
        steps=50, 
        cfg_scale=8.0,
        width=1024, 
        height=1024, 
        samples=3,
        sampler=generation.SAMPLER_K_DPMPP_2M, 
    )
    
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
    return img

def generate_prompt(content):
    predefined_text = '''I want you to help me make prompts for the Stable Diffusion. 
        Stable Diffusion is a text-based image generation model that can create diverse and high-quality images based on users' requests. In order to get the best results from Stable diffusion, you need to follow some guidelines when composing prompts.

        Here are some tips for writing prompts for Stable Diffusion:

        1. Be as specific as possible in the requests. Stable diffusion handles concrete prompts better than abstract or ambiguous ones. For example, instead of “portrait of a woman,” it is better to write “portrait of a Korean woman with brown eyes and red hair in Renaissance style.”
        2. Specify specific art styles or materials. If you want to get an image in a certain style or with a certain texture, then specify this in the request. For example, instead of “landscape,” it is better to write “watercolor landscape with mountains and lake."
        3. Specify specific artists for reference. If you want to get an image similar to the work of some artist, then specify his name in the request. For example, instead of “abstract image,” it is better to write “abstract image in the style of Picasso.”
        4. Don't use any pronouns.
        5. Avoid using thesr words: in a, a, an, the, with, of, and, is, of, by
        6. Weigh your keywords. You can use token:1.3 to specify the weight of keywords in your query. The greater the weight of the keyword, the more it will affect the result. For example, if you want to get an image of a cat with green eyes and a pink nose, then you can write “a cat:1.5, green eyes:1.3, pink nose:1.” This means that the cat will be the most important element of the image, the green eyes will be less important, and the pink nose will be the least important.
        Another way to adjust the strength of a keyword is to use () and []. (keyword) increases the strength of the keyword by 1.1 times and is equivalent to (keyword:1.1). [keyword] reduces the strength of the keyword by 0.9 times and corresponds to (keyword:0.9).

        You can use several of them, as in algebra... The effect is multiplicative.
        (keyword): 1.1
        ((keyword)): 1.21
        (((keyword))): 1.33

        Similarly, the effects of using multiple [] are as follows
        [keyword]: 0.9
        [[keyword]]: 0.81
        [[[keyword]]]: 0.73

        I will also give some examples of good prompts for Stable Diffusion so that you can study them and focus on them.
        Here are Examples.

        Examples:
        a cute kitten made out of metal, (cyborg:1.1), ([tail | detailed wire]:1.3), (intricate details), hdr, (intricate details, hyperdetailed:1.2), cinematic shot, vignette, centered

        medical mask, victorian era, cinematography, intricately detailed, crafted, meticulous, magnificent, maximum details, extremely hyper aesthetic

        a Korean girl, wearing a tie, cupcake in her hands, school, indoors, (soothing tones:1.25), (hdr:1.25), (artstation:1.2), dramatic, (intricate details:1.14), (hyperrealistic 3d render:1.16), (filmic:0.55), (rutkowski:1.1), (faded:1.3)

        Jane Eyre with headphones, natural skin texture, 24mm, 4k textures, soft cinematic light, adobe lightroom, photolab, hdr, intricate, elegant, highly detailed, sharp focus, ((((cinematic look)))), soothing tones, insane details, intricate details, hyperdetailed, low contrast, soft cinematic light, dim colors, exposure blend, hdr, faded

        a portrait of a laughing, toxic, muscle, god, elder, (hdr:1.28), bald, hyperdetailed, cinematic, warm lights, intricate details, hyperrealistic, dark radial background, (muted colors:1.38), (neutral colors:1.2)

        My query may be in other languages. In that case, Your answer is exclusively in English (IMPORTANT!!!), since the model only understands English.
        Also, you should not copy my request directly in your response, you should compose a new one, observing the format given in the examples. Finally, give three prompts always. Insert two empty lines after the end of each prompt.
        Don't add your comments. you must answer right away.
        my query is : 
        '''
    combined_text=f"{predefined_text}+{content}"
    logger.info(f"TEXT: {combined_text}")
    completed_prompt = get_completion(combined_text)
    return completed_prompt


def get_completion(combined_text):
    openai.api_key = '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'
    query = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
		messages=[
        	{'role':'user','content': combined_text}
    	], 
		max_tokens=1024, 
		n=1, 
		stop=None, 
		temperature=0.5, 
	) 
    output_text = query["choices"][0]["message"]["content"]
    output_text = output_text.split('\n')
    prompts = [v for v in output_text if v]
    logger.info(f"TEXT: {prompts}")
    return prompts
"""