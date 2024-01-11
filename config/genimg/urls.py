from django.urls import path
from .views import generate_prompt,generatedimg_view,generate_img

app_name = 'genimg'

urlpatterns = [
    path('generate_prompt/<int:diary_id>/', generate_prompt, name='generate_prompt'),
    path('generate_img/<int:diary_id>/', generate_img, name='generate_img'),
    path('generatedimg_view/<int:diary_id>/', generatedimg_view, name='generatedimg_view'),
]