from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_request(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "account/login.html", {
                "error": "Kullanıcı adı ya da parola yanlış."})
    return render(request, "account/login.html")

def register_request(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                return render(request, "account/register.html", {
                    "error": "Bu kullanıcı adı zaten alınmış."})
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "account/register.html", {
                        "error": "Bu e-posta adresi zaten alınmış."})
                else:
                    user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
                    user.save()
                    return redirect("login")
        else:
            return render(request, "account/register.html", {
                "error": "Parolalar eşleşmiyor."})
    return render(request, "account/register.html")

@login_required
def logout_request(request):
    logout(request)
    return redirect("login")