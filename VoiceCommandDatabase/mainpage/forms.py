from django import forms
from mainpage.models import Voices
import mimetypes
from django.core.exceptions import ValidationError
from mutagen import File

class VoiceForm(forms.ModelForm):
    class Meta:
        model = Voices
        fields = ['word', 'file', 'owner_name', 'owner_surname','owner_gender']

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
        
        audio = File(file)
        if not audio or not hasattr(audio, 'info') or not hasattr(audio.info, 'length'):
            raise forms.ValidationError("Dosya içeriği geçersiz. Lütfen başka bir dosya yükleyin.")
        duration = audio.info.length

        if duration > 60:
            raise forms.ValidationError("Ses kaydı 60 saniyeyi aşamaz.")
        self.cleaned_data['duration'] = float(duration)
        print(self.cleaned_data.get('duration'))

        return file
                
    def save(self, commit=True):
        instance = super().save(commit=False)
        print(self.cleaned_data.get('duration'))
        instance.duration = self.cleaned_data.get('duration', "Bilinmiyor")
        print(self.cleaned_data.get('duration'))

        if self.request and self.request.user.is_authenticated:
            instance.created_by = self.request.user
        if commit:
            instance.save()
        return instance

from django.core.files.base import ContentFile
import wave
import io

class VoiceRecorderForm(forms.ModelForm):
    class Meta:
        model = Voices
        fields = ['word', 'owner_name', 'owner_surname', 'owner_gender']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def validate_audio_file(self, audio_file):
        """
        Validates the audio file using wave module for WAV files
        Returns duration in seconds
        """
        try:
            # Create a temporary copy of the file in memory
            file_copy = io.BytesIO(audio_file.read())
            
            # Reset file pointer for future reads
            audio_file.seek(0)
            
            try:
                with wave.open(file_copy, 'rb') as wav_file:
                    frames = wav_file.getnframes()
                    rate = wav_file.getframerate()
                    duration = frames / float(rate)
                    return duration
            except Exception as wave_error:
                raise forms.ValidationError(f"WAV dosyası okunamadı: {str(wave_error)}")
                
        except Exception as e:
            raise forms.ValidationError(f"Ses dosyası işlenemedi: {str(e)}")

    def clean(self):
        cleaned_data = super().clean()
        audio_file = self.files.get('audio_file')

        if not audio_file:
            raise forms.ValidationError("Ses kaydı gereklidir.")

        # Check file size (10 MB limit)
        if audio_file.size > 10 * 1024 * 1024:
            raise forms.ValidationError("Dosya boyutu 10 MB'ı aşamaz.")

        try:
            # Validate audio duration
            duration = self.validate_audio_file(audio_file)
            
            if duration > 60:
                raise forms.ValidationError("Ses kaydı 60 saniyeyi aşamaz.")
            
            cleaned_data['duration'] = duration
            cleaned_data['file'] = audio_file

        except forms.ValidationError as e:
            raise e
        except Exception as e:
            raise forms.ValidationError(f"Ses dosyası işlenirken bir hata oluştu: {str(e)}")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        try:
            instance.file = self.cleaned_data.get('file')
            instance.duration = self.cleaned_data.get('duration', 0)

            if self.request and self.request.user.is_authenticated:
                instance.created_by = self.request.user

            if commit:
                instance.save()
            
            return instance
            
        except Exception as e:
            raise forms.ValidationError(f"Kayıt sırasında bir hata oluştu: {str(e)}")
