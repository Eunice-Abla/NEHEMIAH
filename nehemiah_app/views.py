from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Utilisateur, Beneficiaire, Filiere
from .forms import CustomUserCreationForm, BeneficiaireForm

# Create your views here.

#----------------------------------------------INSCRIPTION-------------------------------------------

def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, request.FILES)
        beneficiaire_form = BeneficiaireForm(request.POST)
        
        if user_form.is_valid() and beneficiaire_form.is_valid():
           
            # Création de l'utilisateur
            user = user_form.save(commit=False)
            user.is_active = True
            user.save()
            
            # Création du bénéficiaire
            beneficiaire = beneficiaire_form.save(commit=False)
            beneficiaire.utilisateur = user
            beneficiaire.save()
            
            messages.success(request, 'Le bénéficiaire a été créé avec succès!')
            return redirect('dashboard')
    
        else:   
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
            return render(request, 'register.html', context)
    else:
        user_form = CustomUserCreationForm()
        beneficiaire_form = BeneficiaireForm()

    context = {
        'user_form': user_form,
        'beneficiaire_form': beneficiaire_form,
        'filieres': Filiere.objects.all(),
        'title': 'Inscription Bénéficiaire',
    }
    return render(request, 'register.html', context)






def index (request):
    return render(request, "administrateur/index.html")

def inscription (request):
    return render(request, "administrateur/inscription/form.html")


def statut_inscription (request):
    return render(request, "administrateur/inscription/statut.html")


def liste_masterclasses (request):
    return render(request, "administrateur/masterclasses/liste.html")

def details_masterclasses (request):
    return render(request, "administrateur/masterclasses/details.html")

def conversation (request):
    return render(request, "administrateur/messages/conversation.html")

def inbox (request):
    return render(request, "administrateur/messages/inbox.html")

def profil (request):
    return render(request, "administrateur/profil/vue.html")

def modifier_profil (request):
    return render(request, "administrateur/profil/modifier.html")


def liste_rapports (request):
    return render(request, "administrateur/rapports/liste.html")

def soumettre_rapports (request):
    return render(request, "administrateur/rapports/soumettre.html")

def details_rapports (request):
    return render(request, "administrateur/rapports/details.html")


def informatique (request):
    return render(request, "administrateur/filieres/informatique.html")

def mode (request):
    return render(request, "administrateur/filieres/mode.html")

def ingenierie (request):
    return render(request, "administrateur/filieres/ingenierie.html")
