from django import forms
from mainpage.models import Voices
import mimetypes
from django.core.exceptions import ValidationError

class VoiceForm(forms.ModelForm):
    class Meta:
        model = Voices
        fields = ['word', 'file', 'duration', 'owner_name', 'owner_surname','owner_gender']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_file(self):
        file = self.cleaned_data.get('file')
        valid_extensions = ['.mp3', '.wav', '.ogg']
        extension = mimetypes.guess_extension(file.content_type)

        if file and file.size > 10 * 1024 * 1024:  # Limit file size to 10 MB
            raise forms.ValidationError("Dosya boyutu 10 MB'ı aşamaz.")
        elif extension not in valid_extensions:
            raise forms.ValidationError("Dosya formatı desteklenmiyor. Lütfen .mp3, .wav veya .ogg formatında dosya yükleyin.")
        return file

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.request and self.request.user.is_authenticated:
            instance.created_by = self.request.user
        if commit:
            instance.save()
        return instance
