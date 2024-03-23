from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import DiaryList,DiaryView,DiaryCreate
urlpatterns = [

    path('list/', DiaryList.as_view(), name='diary_list'),
    path('view/<int:pk>/', DiaryView.as_view(), name='view_diary'),
    path('create/',DiaryCreate.as_view(), name='create_diary')
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
