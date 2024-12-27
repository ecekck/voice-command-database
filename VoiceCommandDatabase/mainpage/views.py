from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Voices, Users
from django.core.paginator import Paginator
from .forms import VoiceForm, VoiceRecorderForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse, Http404, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import os
from django.views.decorators.http import require_POST
from VoiceCommandDatabase import settings
from django.core.exceptions import ObjectDoesNotExist

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
                return JsonResponse({'status': 'success', 'message': 'Ses başarıyla yüklendi.'})
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
        users_list = User.objects.all()
    else:
        # Eğer normal kullanıcı ise sadece kendi seslerini göster
        voices_list = Voices.objects.filter(created_by=request.user).order_by('-created_at')
        users_list = []

    return render(request, "mainpage/show_voices.html", {'voices': voices_list, 'users': users_list})

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
    
os.environ['GIO_EXTRA_MODULES'] = 'NUL'  # views.py dosyanızın en üstüne ekleyin

@login_required
def download_voice_list(request):
    try:
        import logging
        logging.getLogger('weasyprint').setLevel(logging.ERROR)  # Sadece hataları göster
        
        if request.user.is_superuser:
            voices = Voices.objects.all()
        else:
            voices = Voices.objects.filter(created_by=request.user)
        
        html_content = render_to_string('mainpage/download_voice_list.html', {'voices': voices})
        pdf_file = HTML(string=html_content, base_url=request.build_absolute_uri('/')).write_pdf()
        
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="voice_list.pdf"'
        return response
    except Exception as e:
        print(f"PDF oluşturma hatası: {str(e)}")
        messages.error(request, "PDF oluşturulurken bir hata oluştu.")
        return redirect('your_list_view_name')

@require_POST
@login_required
def edit_voice(request):
    try:
        voice_id = request.POST.get('voice_id')
        voice = Voices.objects.get(id=voice_id)
        
        voice.word = request.POST.get('word')
        voice.owner_name = request.POST.get('owner_name')
        voice.owner_surname = request.POST.get('owner_surname')
        voice.owner_gender = request.POST.get('owner_gender')
        voice.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
@login_required
def admin_panel(request):
    if not request.user.is_superuser:
        return redirect('index')
    
    users = User.objects.all()
    return render(request, 'mainpage/admin_panel.html', {'users': users})

@login_required
def update_user(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            
            # Gönderilen verileri kontrol et
            username = request.POST.get('username')
            first_name = request.POST.get('name')
            last_name = request.POST.get('surname')
            email = request.POST.get('email')
            
            print(first_name, last_name, email)

            # Alanların boş olup olmadığını kontrol et
            if not email:
                return JsonResponse({'success': False, 'error': 'Email alanı boş olamaz.'})
            
            # Email formatı kontrolü (opsiyonel)
            from django.core.validators import validate_email
            from django.core.exceptions import ValidationError
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({'success': False, 'error': 'Geçersiz email formatı.'})
            
            # Güncellemeyi yap
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            
            return JsonResponse({'success': True})
        except ObjectDoesNotExist:
            return JsonResponse({'success': False, 'error': 'Kullanıcı bulunamadı.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Geçersiz istek yöntemi.'})

@login_required
def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            user.delete()
            return JsonResponse({'success': True})
        except ObjectDoesNotExist:
            return JsonResponse({'success': False, 'error': 'Kullanıcı bulunamadı.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Geçersiz istek yöntemi.'})

import csv

@login_required
def download_voice_list_csv(request):
    if request.user.is_superuser:
        voices = Voices.objects.all()
        header = ['created_by', 'word', 'duration', 'owner_name', 'owner_surname', 'owner_gender', 'created_at']
    else:
        voices = Voices.objects.filter(created_by=request.user)
        header = ['word', 'duration', 'owner_name', 'owner_surname', 'owner_gender', 'created_at']

    # Create the HttpResponse object with the appropriate CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="voice_list.csv"'

    writer = csv.writer(response)

    # Write the header row
    writer.writerow(header)

    # Write data rows
    for voice in voices:
        if request.user.is_superuser:
            writer.writerow([
                voice.created_by,
                voice.word,
                voice.duration,
                voice.owner_name,
                voice.owner_surname,
                voice.owner_gender,
                voice.created_at.strftime("%Y-%m-%d %H:%M:%S")
            ])
        else:
            writer.writerow([
                voice.word,
                voice.duration,
                voice.owner_name,
                voice.owner_surname,
                voice.owner_gender,
                voice.created_at.strftime("%Y-%m-%d %H:%M:%S")
            ])

    return response
