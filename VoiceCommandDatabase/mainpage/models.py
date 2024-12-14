from django.db import models

class Voices(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = 
    word = models.CharField(max_length=255, blank=True, null=True)  # Optional title for the recording
    file = models.FileField(upload_to="voices/")  # File path for the uploaded audio
    duration = models.FloatField(blank=True, null=True)  # Duration of the audio in seconds
    owner_name = 
    owner_gender = 
    language = 
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the recording is created

    def __str__(self):
        return self.title if self.title else f"Voice Recording {self.id}"
