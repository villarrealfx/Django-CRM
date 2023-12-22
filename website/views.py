from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm

def home(request):
    # Chequear si se encuentra logeado
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Autenticación
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Usted se ha logeado correctamente")
            return redirect('home')
        else:
            messages.success(request, 'Error al intentar autenticarse, por favor verifique e intentelo de nuevo')
            return redirect('home')
    else:
        return render(request, 'home.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "Usted ha sido 'Loged Out' ....")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Autenticación y logeado
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Usted se ha registrado correctamente Bienvenido")
            return redirect('home')
        # else:
        #     messages.success(request, 'Error al intentar registrarse, por favor verifique e intentelo de nuevo')
        #     return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    
    return render(request, 'register.html', {'form':form})