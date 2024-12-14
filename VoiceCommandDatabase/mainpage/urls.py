from . import views
from django.urls import path

# http://127.0.0.1:8000 => mainpage

urlpatterns = [
    path("", views.index, name="index")
]