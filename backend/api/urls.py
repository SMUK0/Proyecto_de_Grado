# PAGINA DE INICIO (INDEX)

from django.urls import path
from .views import home_info

urlpatterns = [
    path("home/", home_info, name="home-info"),
]
