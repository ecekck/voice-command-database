from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Voices, Users
from django.core.paginator import Paginator
from .forms import VoiceForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    # You can add any context data needed for the main page
    context = {
        'total_voices': Voices.objects.count(),
        # Add any other statistics or featured content
    }
    return render(request, "mainpage/index.html", context)

@login_required
def add_voice(request):
    # If you have a form for adding voices, you'd handle form submission here
    if request.method == 'POST':
        form = VoiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            return redirect('index')
        print(form.errors)
    else:
        form = VoiceForm()    
    return render(request, "mainpage/add_voice.html", {'form':form, 'error' : form.errors})

@login_required
def record_voice(request):
    # Logic for recording voices would be implemented here
    return render(request, "mainpage/record_voice.html")

@login_required
def show_voices(request):
    # Retrieve all voices, ordered by most recent first
    voices_list = Voices.objects.all().order_by('-created_at')

    return render(request, "mainpage/show_voices.html", {'voices' : voices_list})