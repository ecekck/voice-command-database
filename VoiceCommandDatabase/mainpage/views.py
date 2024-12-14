from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Voices
from django.core.paginator import Paginator

def index(request):
    # You can add any context data needed for the main page
    context = {
        'total_voices': Voices.objects.count(),
        # Add any other statistics or featured content
    }
    return render(request, "mainpage/index.html", context)

def add_voice(request):
    # If you have a form for adding voices, you'd handle form submission here
    return render(request, "mainpage/add_voice.html")

def record_voice(request):
    # Logic for recording voices would be implemented here
    return render(request, "mainpage/record_voice.html")

def show_voices(request):
    # Retrieve all voices, ordered by most recent first
    voices_list = Voices.objects.all().order_by('-created_at')
    
    # Implement pagination
    paginator = Paginator(voices_list, 10)  # Show 10 voices per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'voices': page_obj,  # Pass paginated voices to the template
        'total_voices': voices_list.count(),
        'total_turkish_voices': voices_list.filter(language='Turkish').count(),
        'total_english_voices': voices_list.filter(language='English').count(),
        'total_male_voices': voices_list.filter(owner_gender='male').count(),
        'total_female_voices': voices_list.filter(owner_gender='female').count(),
    }
    
    return render(request, "mainpage/show_voices.html", context)