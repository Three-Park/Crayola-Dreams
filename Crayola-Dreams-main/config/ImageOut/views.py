import io
import os
import warnings
from django.conf import settings
from .forms import YourForm
from CGPT import query_view
from IPython.display import display
from PIL import Image
from django.shortcuts import render
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

api_key = 'sk-Dy'

# Set up our connection to the API.
stability_api = client.StabilityInference(
    key=api_key,
    verbose=True, # Print debug messages.
    engine="stable-diffusion-xl-1024-v1-0", # Set the engine to use for generation.
    # Check out the following link for a list of available engines: https://platform.stability.ai/docs/features/api-parameters#engine
)

def Image_out(request):
    img_url = None
    if request.method == 'POST':
        form = YourForm(request.POST, request.FILES)
        if form.is_valid():
            # 이미지 생성 및 가져오기
            # 여기서는 stability_api.generate()를 사용하고, 이미지를 img 변수에 할당
            # Set up our initial generation parameters.
            answers = stability_api.generate(
            prompt=query_view(), #prompts (from chatgpt)
            style_preset ="anime", #image style : anime, comic books, etc...
            seed=4253978046, #seed << the parameters that fixed the genenrated images per prompts
            steps=50, # Amount of inference steps performed on image generation.
            cfg_scale=8.0, # Influences how strongly your generation is guided to match your prompt.
                   # Setting this value higher increases the strength in which it tries to match your prompt.
            width=1024, # Generation width, defaults to 512 if not included.
            height=1024, # Generation height, defaults to 512 if not included.
            samples=3, # Number of images to generate, defaults to 1 if not included.
            sampler=generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
                                                 # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
                                                 # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m, k_dpmpp_sde)
            )

            # Save generated images
            for resp in answers:
                for artifact in resp.artifacts:
                    if artifact.finish_reason == generation.FILTER:
                        warnings.warn(
                            "Your request activated the API's safety filters and could not be processed."
                            "Please modify the prompt and try again.")
                    if artifact.type == generation.ARTIFACT_IMAGE:
                        img = Image.open(io.BytesIO(artifact.binary))
                        display(img)

                        # 이미지 저장 경로 설정 (MEDIA_ROOT 사용)
                        image_path = os.path.join(settings.MEDIA_ROOT, 'generated_images', 'image.png')  # settings.MEDIA_ROOT와 조합하여 절대 경로 생성
                        img.save(image_path)

                        # 이미지 URL 설정 (MEDIA_URL 사용)
                        img_url = os.path.join(settings.MEDIA_URL, 'generated_images', 'image.png')  # settings.MEDIA_URL과 조합하여 이미지 URL 생성


    return render(request, 'create_diary.html', {'form': form, 'img_url': img_url})
