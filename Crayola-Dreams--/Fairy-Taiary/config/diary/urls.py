from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import image_select
from .views import DiaryList,DiaryView,DiaryCreate,DiaryEdit,DiaryDelete

urlpatterns = [
    path('create/', DiaryCreate.as_view(), name='create_diary'),
    path('list/', DiaryList.as_view(), name='diary_list'),
    path('view/<int:pk>/', DiaryView.as_view(), name='view_diary'),
    path('edit/<int:pk>/', DiaryEdit.as_view(), name='edit_diary'),
    path('delete/<int:pk>/', DiaryDelete.as_view(), name='delete_diary'),
    path('imageselect/<int:pk>/',image_select,name='image_select'),

]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
