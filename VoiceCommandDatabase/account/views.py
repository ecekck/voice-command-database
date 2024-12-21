from django.shortcuts import render, redirect

# Create your views here.

def login_request(request):
    return render(request, "account/login.html")

def register_request(request):
    return render(request, "account/register.html")
    
def logout_request(request):
    return redirect("login")