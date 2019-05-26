from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
app_name = 'hatespeech'

urlpatterns = [
    path('index/', views.classify, name='classify'),
    path('api/', views.classifyApi, name='classifyApi'),
    path('index1/', views.classify, name='classify'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)