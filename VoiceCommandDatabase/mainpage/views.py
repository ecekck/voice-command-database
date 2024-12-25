from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Voices, Users
from django.core.paginator import Paginator
from .forms import VoiceForm, VoiceRecorderForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse, Http404
import os

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
    if request.user.is_superuser:
        # Eğer kullanıcı superuser ise tüm sesleri göster
        voices_list = Voices.objects.all().order_by('-created_at')
    else:
        # Eğer normal kullanıcı ise sadece kendi seslerini göster
        voices_list = Voices.objects.filter(created_by=request.user).order_by('-created_at')

    return render(request, "mainpage/show_voices.html", {'voices': voices_list})

@login_required
def delete_voice(request, voice_id):
    voice = Voices.objects.get(id=voice_id)
    voice.delete()
    return redirect('show_voices')

@login_required
def download_voice(request, voice_id):
    try:
        voice = Voices.objects.get(id=voice_id)
        file_path = voice.file.path  # Get the actual file path on the filesystem
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
    except Voices.DoesNotExist:
        raise Http404("Voice not found")
    except ValueError:
        raise Http404("Invalid file path")
    except FileNotFoundError:
        raise Http404("File not found")