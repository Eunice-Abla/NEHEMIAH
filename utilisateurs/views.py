from django.shortcuts import render

# Create your views here.
def index (request):
    return render(request, "admin/index.html")

def inscription (request):
    return render(request, "admin/inscription/form.html")


def statut_inscription (request):
    return render(request, "admin/inscription/statut.html")


def liste_masterclasses (request):
    return render(request, "admin/masterclasses/liste.html")

def details_masterclasses (request):
    return render(request, "admin/masterclasses/details.html")

def conversation (request):
    return render(request, "admin/messages/conversation.html")

def inbox (request):
    return render(request, "admin/messages/inbox.html")

def profil (request):
    return render(request, "admin/profil/vue.html")

def modifier_profil (request):
    return render(request, "admin/profil/modifier.html")


def liste_rapports (request):
    return render(request, "admin/rapports/liste.html")

def soumettre_rapports (request):
    return render(request, "admin/rapports/soumettre.html")

def details_rapports (request):
    return render(request, "admin/rapports/details.html")


def informatique (request):
    return render(request, "admin/filieres/informatique.html")

def mode (request):
    return render(request, "admin/filieres/mode.html")

def ingenierie (request):
    return render(request, "admin/filieres/ingenierie.html")
