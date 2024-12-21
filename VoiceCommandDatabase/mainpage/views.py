from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Voices
from django.core.paginator import Paginator
from .forms import ReceiptForm
from django.contrib.auth.models import User

def index(request):
    # You can add any context data needed for the main page
    context = {
        'total_voices': Voices.objects.count(),
        # Add any other statistics or featured content
    }
    return render(request, "mainpage/index.html", context)

def add_voice(request):
    # If you have a form for adding voices, you'd handle form submission here
    if request.method == 'POST':
        form = ReceiptForm(request.POST, request.FILES)
        if form.is_valid():
            # if request.user.is_authenticated:
            #     form.instance.created_by = request.user
            # else: 
            #     form.instance.created_by = User.objects.first()
            form.save()
            return redirect('index')
        print(form.errors)
    else:
        form = ReceiptForm()    
    return render(request, "mainpage/add_voice.html", {'form':form})

def record_voice(request):
    # Logic for recording voices would be implemented here
    return render(request, "mainpage/record_voice.html")

def show_voices(request):
    # Retrieve all voices, ordered by most recent first
    voices_list = Voices.objects.all().order_by('-created_at')

    return render(request, "mainpage/show_voices.html", {'voices' : voices_list})