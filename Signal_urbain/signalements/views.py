from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import Signalement, Vote
from .forms import SignalementForm

def list_signalements(request):
    """Vue pour afficher la liste des signalements avec filtres et pagination"""
    signalements = Signalement.objects.all()
    
    # Filtres
    type_filtre = request.GET.get('type')
    status_filtre = request.GET.get('status')
    
    if type_filtre:
        signalements = signalements.filter(type=type_filtre)
    if status_filtre:
        signalements = signalements.filter(status=status_filtre)
        
    # Pagination
    paginator = Paginator(signalements, 9)  # 9 signalements par page
    page = request.GET.get('page')
    signalements = paginator.get_page(page)
    
    context = {
        'signalements': signalements,
        'type_choices': Signalement.TYPE_CHOICES,
        'status_choices': Signalement.STATUS_CHOICES,
    }
    return render(request, 'signalements/list.html', context)

def map_view(request):
    """Vue pour afficher la carte des signalements"""
    signalements = Signalement.objects.all()
    
    # Filtres
    type_filtre = request.GET.get('type')
    status_filtre = request.GET.get('status')
    
    if type_filtre:
        signalements = signalements.filter(type=type_filtre)
    if status_filtre:
        signalements = signalements.filter(status=status_filtre)
    
    context = {
        'signalements': signalements,
        'type_choices': Signalement.TYPE_CHOICES,
        'status_choices': Signalement.STATUS_CHOICES,
    }
    return render(request, 'signalements/map.html', context)

def detail_signalement(request, pk):
    """Vue pour afficher les détails d'un signalement"""
    signalement = get_object_or_404(Signalement, pk=pk)
    
    # Trouver des signalements similaires (même type et proximité)
    signalements_similaires = Signalement.objects.filter(
        Q(type=signalement.type) | 
        Q(adresse__icontains=signalement.adresse)
    ).exclude(pk=pk)[:3]
    
    context = {
        'signalement': signalement,
        'signalements_similaires': signalements_similaires,
    }
    return render(request, 'signalements/detail.html', context)

@login_required
def create_signalement(request):
    """Vue pour créer un nouveau signalement"""
    if request.method == 'POST':
        form = SignalementForm(request.POST, request.FILES)
        if form.is_valid():
            signalement = form.save(commit=False)
            signalement.createur = request.user
            signalement.save()
            messages.success(request, 'Votre signalement a été créé avec succès.')
            return redirect('signalements:detail', pk=signalement.pk)
    else:
        form = SignalementForm()
    
    return render(request, 'signalements/create.html', {'form': form})

@login_required
def update_signalement(request, pk):
    """Vue pour modifier un signalement"""
    signalement = get_object_or_404(Signalement, pk=pk)
    
    # Vérifier que l'utilisateur est le créateur ou un admin
    if request.user != signalement.createur and not request.user.is_staff:
        messages.error(request, "Vous n'avez pas la permission de modifier ce signalement.")
        return redirect('signalements:detail', pk=pk)
    
    if request.method == 'POST':
        form = SignalementForm(request.POST, request.FILES, instance=signalement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le signalement a été modifié avec succès.')
            return redirect('signalements:detail', pk=pk)
    else:
        form = SignalementForm(instance=signalement)
    
    return render(request, 'signalements/create.html', {
        'form': form,
        'signalement': signalement,
    })

@login_required
def delete_signalement(request, pk):
    """Vue pour supprimer un signalement"""
    signalement = get_object_or_404(Signalement, pk=pk)
    
    # Vérifier que l'utilisateur est le créateur ou un admin
    if request.user != signalement.createur and not request.user.is_staff:
        messages.error(request, "Vous n'avez pas la permission de supprimer ce signalement.")
        return redirect('signalements:detail', pk=pk)
    
    if request.method == 'POST':
        signalement.delete()
        messages.success(request, 'Le signalement a été supprimé avec succès.')
        return redirect('signalements:list')
    
    return redirect('signalements:detail', pk=pk)

@login_required
def vote_signalement(request, pk):
    """Vue pour voter/retirer son vote sur un signalement"""
    signalement = get_object_or_404(Signalement, pk=pk)
    
    # Vérifier si l'utilisateur a déjà voté
    vote = Vote.objects.filter(signalement=signalement, utilisateur=request.user).first()
    
    if vote:
        # Si l'utilisateur a déjà voté, on retire son vote
        vote.delete()
        messages.success(request, 'Votre vote a été retiré.')
    else:
        # Sinon, on ajoute son vote
        Vote.objects.create(signalement=signalement, utilisateur=request.user)
        messages.success(request, 'Votre vote a été enregistré.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'nombre_votes': signalement.nombre_votes,
            'a_vote': False if vote else True
        })
    
    return redirect('signalements:detail', pk=pk)