from django.urls import path
from .views import  RegisterAPIView,AuthAPIView,ProfileAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('auth/', AuthAPIView.as_view()),
    path('profile/', ProfileAPIView.as_view()),
]