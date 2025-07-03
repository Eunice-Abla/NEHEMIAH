from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Utilisateur, Beneficiaire, Filiere
from .forms import CustomUserCreationForm, BeneficiaireForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def login_function(request, username, password):
    user = authenticate(request, username = username, password = password)
    if user:
        login(request, user)
        return user
    else:
        return None

#----------------------------------------------INSCRIPTION-------------------------------------------

def register(request):
    
    user_form = CustomUserCreationForm(request.POST, request.FILES)
    beneficiaire_form = BeneficiaireForm(request.POST)

    context = {
        'user_form': user_form,
        'beneficiaire_form': beneficiaire_form,
        'filieres': Filiere.objects.all(),
        'title': 'Inscription Bénéficiaire',
    }


    if request.method == 'POST':
        
        if user_form.is_valid() and beneficiaire_form.is_valid():
           
            # Création de l'utilisateur
            user = user_form.save(commit=False)
            user.is_active = True
            user.save()
            
            # Création du bénéficiaire
            beneficiaire = beneficiaire_form.save(commit=False)
            beneficiaire.utilisateur = user
            beneficiaire.save()


            username = user_form.cleaned_data.get("username")
            password = user_form.cleaned_data.get("password1")

            login_function(request, username, password)
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



#------------------------------------------CONNEXION---------------------------------------------------

def connexion(request):

    if request.user.is_authenticated:
        return redirect('dashboard') 
    
    if request.method == 'POST':
           
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = Utilisateur.objects.get(email=email)
            username = user.username
        except Utilisateur.DoesNotExist:
            username = None 

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            messages.success(request, "connexion réussie")
            return redirect('dashboard')
        else:
            messages.error(request, "Identifiants incorrects. Veuillez réessayer.")
    
    return render(request, 'login.html')



def deconnexion(request):
    logout(request)
    return redirect("login")

#-----------------------------------DASHBOARD---------------------------------------------------------


@login_required
def dashboard (request):
    user = request.user

    context = {
        "user":user,
    }

    if user.is_admin:
        return render(request, 'administrateur/index.html', context)

    return render(request, "user/index.html", context)


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
    
    beneficiaire = get_object_or_404(Beneficiaire, utilisateur = request.user)
    if beneficiaire:
        context = {
            "beneficiaire" : beneficiaire
        }
    
    return render(request, "administrateur/profil/vue.html", context)

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
