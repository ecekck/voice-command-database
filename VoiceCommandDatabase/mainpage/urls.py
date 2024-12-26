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
    path("sesi_sil/<int:voice_id>/", views.delete_voice, name="delete_voice"),
    path("sesi_indir/<int:voice_id>/", views.download_voice, name="download_voice"),
    path("listeyi_indir/", views.download_voice_list, name="download_voice_list"),
    path('edit_voice/', views.edit_voice, name='edit_voice'),
    path("admin_paneli/", views.admin_panel, name="admin_panel"),
    path("update_user/", views.update_user, name="update_user"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)