from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #connexion
    path('', views.connexion, name="login" ),
    path("logout", views.deconnexion, name= "logout"),

    #inscription
    path("inscription", views.register, name="inscription"),
    # path("depot", views.inscription, name='inscription'),

    #tableau de bord
    path('dashboard', views.dashboard, name="dashboard" ),

    # masterclasses
    path("masterclass/liste", views.liste_masterclasses, name='liste_masterclasses'),
    path("masterclass/details", views.details_masterclasses, name='details_masterclasse'),

    # rapports
    path("rapports/liste", views.liste_rapports, name='liste_rapports'),
    path("rapports/soumettre", views.soumettre_rapports, name='soumettre_rapport'),
    path("rapports/details", views.details_rapports, name='details_rapport'),

    #messages
    path("messages/conversation", views.conversation, name='conversation'),
    path("messages/inbox", views.inbox, name='inbox'),

    #profil
    path("profil/", views.profil, name='profil'),
    path("profil/modifier", views.modifier_profil, name='modifier_profil'),

    #filière
    path("filiere/informatique", views.informatique, name='informatique'),
    path("filiere/mode", views.mode, name='mode'),
    path("filiere/ingenierie", views.ingenierie, name='ingenierie'),

    path("inscription/statut", views.statut_inscription, name='statut_inscription'),

    #erreur 404
    # path("erreur", views.erreur_404, name="erreur_404"),


]