from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    # Champs à afficher dans la liste des utilisateurs
    list_display = ('username', 'email', 'is_admin', 'is_staff', 'is_superuser')
    list_filter = ('is_admin', 'is_staff', 'is_superuser')
    
    # Organisation des champs dans le formulaire d'édition
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('email', 'telephone', 'photo_profil')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'groups', 'user_permissions'),
        }),
    )
    
    # Organisation des champs dans le formulaire de création
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_admin'),
        }),
    )
    
    search_fields = ('username', 'email')
    ordering = ('-date_inscription',)
    filter_horizontal = ('groups', 'user_permissions',)