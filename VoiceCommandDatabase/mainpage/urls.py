from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# http://127.0.0.1:8000 => mainpage

urlpatterns = [
    path("", views.index, name="index"),
    path("ses_ekle/", views.add_voice, name="add_voice"),
    path("ses_kaydet/", views.record_voice, name="record_voice"),
    path("sesleri_goruntule/", views.show_voices, name="show_voices"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)