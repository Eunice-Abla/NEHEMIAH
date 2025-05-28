from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.register, name="register" ),
    path('d', views.index, name="dashboard" ),
    path("masterclass/liste", views.liste_masterclasses, name='liste_masterclasses'),
    path("masterclass/details", views.details_masterclasses, name='details_masterclasse'),
    path("rapports/liste", views.liste_rapports, name='liste_rapports'),
    path("rapports/soumettre", views.soumettre_rapports, name='soumettre_rapport'),
    path("rapports/details", views.details_rapports, name='details_rapport'),
    path("messages/conversation", views.conversation, name='conversation'),
    path("messages/inbox", views.inbox, name='inbox'),
    path("profil/", views.profil, name='profil'),
    path("profil/modifier", views.modifier_profil, name='modifier_profil'),
    path("filiere/informatique", views.informatique, name='informatique'),
    path("filiere/mode", views.mode, name='mode'),
    path("filiere/ingenierie", views.ingenierie, name='ingenierie'),
    path("inscription", views.inscription, name='inscription'),
    path("inscription/statut", views.statut_inscription, name='statut_inscription'),


]