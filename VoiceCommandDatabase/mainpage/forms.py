from django import forms
from mainpage.models import Voices
from django.contrib.auth import get_user_model

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Voices
        fields = ['word', 'file', 'duration', 'owner_name', 'owner_gender', 'language', 'created_by']

    # Adding a custom validation for the 'created_by' field to make sure the user is logged in
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the initial user for created_by if the user is logged in
        if 'request' in kwargs:
            self.fields['created_by'].initial = kwargs['request'].user

    # Optional: You can add custom validation if you need, for example, checking file size
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 10 * 1024 * 1024:  # Limiting file size to 10 MB
                raise forms.ValidationError("Dosya boyutu 10 MB'ı aşamaz.")
        return file
