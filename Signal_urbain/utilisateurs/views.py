from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    """Vue pour l'inscription des utilisateurs"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Votre compte a été créé avec succès !')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'utilisateurs/register.html', {'form': form})

def login_view(request):
    """Vue pour la connexion des utilisateurs"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue, {username} !')
                # Rediriger vers la page précédente si elle existe
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'utilisateurs/login.html', {'form': form})

def logout_view(request):
    """Vue pour la déconnexion des utilisateurs"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('home')

@login_required
def profile(request):
    """Vue pour afficher et modifier le profil utilisateur"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès.')
            return redirect('utilisateurs:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'signalements': request.user.signalements.all()[:5],  # 5 derniers signalements
        'votes': request.user.votes.all()[:5],  # 5 derniers votes
    }
    return render(request, 'utilisateurs/profile.html', context)

@login_required
def mes_signalements(request):
    """Vue pour afficher les signalements de l'utilisateur"""
    signalements = request.user.signalements.all()
    return render(request, 'utilisateurs/mes_signalements.html', {
        'signalements': signalements
    })
