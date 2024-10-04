from django.urls import path
from yandex_disc.views import index, download_file

urlpatterns = [
    path('', index, name='index'),
    path('download/<str:file_url>/', download_file, name='download_file'),
]
