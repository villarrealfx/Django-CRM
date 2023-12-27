from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Record

def home(request):

    records = Record.objects.all()

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
        print(records)
        return render(request, 'home.html', {'records':records})

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
        
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    
    return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        # Encontrar Registro
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    
    else:
        messages.success(request, "Registro no encontrado")
        return redirect('home')