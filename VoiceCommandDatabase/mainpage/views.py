from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "mainpage/index.html")

def add_voice(request):
    return render(request, "mainpage/add_voice.html")

def record_voice(request):
    return render(request, "mainpage/record_voice.html")

def show_voices(request):
    return render(request, "mainpage/show_voices.html")