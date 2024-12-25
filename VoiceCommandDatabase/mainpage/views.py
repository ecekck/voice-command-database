from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Voices, Users
from django.core.paginator import Paginator
from .forms import VoiceForm, VoiceRecorderForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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
            return redirect('show_voices')
        print(form.errors)
    else:
        form = VoiceForm()    
    return render(request, "mainpage/add_voice.html", {'form':form, 'error' : form.errors})

def record_voice(request):
    if request.method == 'POST':
        try:
            form = VoiceRecorderForm(request.POST, request.FILES, request=request)
            if form.is_valid():
                form.save()
                print("forms save edildi")
                return redirect('show_voices')
            else:
                errors = form.errors.as_json()
                return JsonResponse({'status': 'error', 'errors': errors}, status=400)
                
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Bir hata oluştu: {str(e)}'
            }, status=500)
    else:
        form = VoiceRecorderForm()
    
    return render(request, 'mainpage/record_voice.html', {'form': form, 'error': form.errors})

@login_required
def show_voices(request):
    # Retrieve all voices, ordered by most recent first
    voices_list = Voices.objects.all().order_by('-created_at')

    return render(request, "mainpage/show_voices.html", {'voices' : voices_list})