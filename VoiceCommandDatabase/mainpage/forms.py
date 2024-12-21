from django import forms
from mainpage.models import Voices

class VoiceForm(forms.ModelForm):
    class Meta:
        model = Voices
        fields = ['word', 'file', 'duration', 'owner_name', 'owner_surname','owner_gender']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file and file.size > 10 * 1024 * 1024:  # Limit file size to 10 MB
            raise forms.ValidationError("Dosya boyutu 10 MB'ı aşamaz.")
        return file

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.request and self.request.user.is_authenticated:
            instance.created_by = self.request.user
        if commit:
            instance.save()
        return instance
