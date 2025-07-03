from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import (
    Utilisateur, Filiere, AnneeAcademique, Beneficiaire,
    Masterclasse, RapportLecture, Reinscription, Message, Notification
)
from django.contrib.auth.forms import UserCreationForm


#----------------------------------------------CUSTOMUSERCREATION FORM----------------------------------------
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ['username', 'email','telephone', 'photo_profil', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'photo_profil': forms.FileInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'username': '150 caractères maximum. Lettres, chiffres et @/./+/-/_ seulement.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Utilisateur.objects.filter(email=email).exists():
            raise ValidationError("Cet email est déjà utilisé.")
        return email

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if not telephone.isdigit() or len(telephone) < 8:
            raise ValidationError("Numéro de téléphone invalide.")
        return telephone



#---------------------------------------CONNEXION FORM-----------------------------------------------------------
# class CustomLoginForm(AuthenticationForm):
#     username = forms.CharField(
#         label="Nom d'utilisateur ou Email",
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Entrez votre identifiant',
#             'required': 'required'
#         })
#     )
#     password = forms.CharField(
#         label="Mot de passe",
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Entrez votre mot de passe',
#             'required': 'required'
#         })
#     )
#     remember_me = forms.BooleanField(
#         required=False,
#         widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#         label="Se souvenir de moi"
#     )

#---------------------------------------BENEFICIAIRE FORM--------------------------------------------------------
class BeneficiaireForm(forms.ModelForm):
    class Meta:
        model = Beneficiaire
        fields = ['nom', 'prenom', 'numero_cde', 'numero_beneficiaire', 'date_naissance', 'adresse', 'sexe']
        widgets = {
            'numero_cde': forms.TextInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_beneficiaire': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder':'ex: 000100001',
                
    
            }),
            'date_naissance': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'adresse': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 1
            }),
            'sexe': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'numero_beneficiaire': "Numéro bénéficiaire",
            'numero_cde': "Numéro CDE",
        }
        help_texts = {
            'numero_beneficiaire': '(09 chiffres Composés du N° du projet et du numero du beneficiaire)',
            'nom': 'de votre acte de naissance',
            'prenom':'de votre acte de naissance',
        }

    def clean_numero_cde(self):
        numero = self.cleaned_data.get('numero_cde')
        if len(numero) != 4:
            raise ValidationError("Le numéro du CDEJ doit contenir 4 chiffres")
        return numero

    def clean_numero_beneficiaire(self):
        numero = self.cleaned_data.get('numero_beneficiaire')
        if Beneficiaire.objects.filter(numero_beneficiaire=numero).exists():
            raise ValidationError("Ce numéro bénéficiaire existe déjà.")
        if len(numero) != 9:
            raise forms.ValidationError("Le numéro bénéficiaire doit contenir exactement 9 chiffres.")
        return numero

    def clean_date_naissance(self):
        date = self.cleaned_data.get('date_naissance')
        if date and date > timezone.now().date():
            raise ValidationError("La date de naissance ne peut pas être dans le futur.")
        return date



#----------------------------------------REINSCRIPTION FORM-----------------------------------
class ReinscriptionForm(forms.ModelForm):
    class Meta:
        model = Reinscription
        exclude = ['etudiant', 'date_soumission', 'statut', 'valide_par', 'date_validation']
        widgets = {
            'annee_academique': forms.Select(attrs={'class': 'form-select'}),
            'domaine_etude': forms.Select(attrs={'class': 'form-select'}),
            'niveau_scolaire': forms.Select(attrs={'class': 'form-select'}),
            'specialite': forms.TextInput(attrs={'class': 'form-control'}),
            'universite': forms.TextInput(attrs={'class': 'form-control'}),
            'commune_residence': forms.TextInput(attrs={'class': 'form-control'}),
            'ville_residence': forms.TextInput(attrs={'class': 'form-control'}),
            'quartier_residence': forms.TextInput(attrs={'class': 'form-control'}),
            'motif_demande': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'nationalite': forms.TextInput(attrs={'class': 'form-control'}),
            'annee_obtention_diplome': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1900',
                'max': str(timezone.now().year)
            }),
            'moyenne_obtenue': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '20'
            }),
            'montant_loyer_annuel': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '120000'
            }),
            'frais_scolarite': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'besoin_ordinateur': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '450000'
            }),
            'frais_transport': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'releve_note_precedent': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'rapport_stage': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'lettre_recommandation': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'copie_diplome': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'copie_nationalite': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'masterclasses_suivies': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['masterclasses_suivies'].queryset = Masterclasse.objects.filter(est_active=True)

    def clean_annee_obtention_diplome(self):
        annee = self.cleaned_data.get('annee_obtention_diplome')
        current_year = timezone.now().year
        if annee < 1900 or annee > current_year:
            raise ValidationError(f"L'année doit être entre 1900 et {current_year}")
        return annee

    def clean_moyenne_obtenue(self):
        moyenne = self.cleaned_data.get('moyenne_obtenue')
        if moyenne < 0 or moyenne > 20:
            raise ValidationError("La moyenne doit être entre 0 et 20")
        return round(moyenne, 2)

    def clean_montant_loyer_annuel(self):
        montant = self.cleaned_data.get('montant_loyer_annuel')
        if montant and montant > 120000:
            raise ValidationError("Le loyer annuel ne peut dépasser 120 000 FCFA")
        return montant

    def clean_besoin_ordinateur(self):
        montant = self.cleaned_data.get('besoin_ordinateur')
        if montant and montant > 450000:
            raise ValidationError("Le montant pour l'ordinateur ne peut dépasser 450 000 FCFA")
        return montant

    def clean(self):
        cleaned_data = super().clean()
        
        # Validation du montant total
        frais_scolarite = cleaned_data.get('frais_scolarite', 0)
        loyer = cleaned_data.get('montant_loyer_annuel', 0)
        ordinateur = cleaned_data.get('besoin_ordinateur', 0)
        transport = cleaned_data.get('frais_transport', 0)
        
        total = frais_scolarite + loyer + ordinateur + transport + 50000  # assurance
        
        if total > 1200000:
            raise ValidationError("Le montant total demandé ne peut dépasser 1 200 000 FCFA")
        
        # Validation des fichiers
        for field in ['releve_note_precedent', 'lettre_recommandation', 'copie_diplome']:
            fichier = cleaned_data.get(field)
            if fichier:
                if fichier.size > 10*1024*1024:  # 10MB
                    raise ValidationError(f"Le fichier {field} est trop volumineux (>10MB)")
                extension = fichier.name.split('.')[-1].lower()
                if extension not in ['pdf', 'jpg', 'jpeg', 'png']:
                    raise ValidationError("Seuls les formats PDF, JPG, PNG sont acceptés")

        return cleaned_data



#-------------------------------------FILIERE FORM----------------------------------------------
class FiliereForm(forms.ModelForm):
    class Meta:
        model = Filiere
        fields = '__all__'
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'couleur': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color'
            }),
            'icone': forms.TextInput(attrs={'class': 'form-control'}),
        }




#---------------------------------------ANNEE ACADEMIQUE FORM--------------------------------------------
class AnneeAcademiqueForm(forms.ModelForm):
    class Meta:
        model = AnneeAcademique
        fields = '__all__'
        widgets = {
            'debut': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '2000'
            }),
            'fin': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '2000'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        debut = cleaned_data.get('debut')
        fin = cleaned_data.get('fin')
        
        if debut and fin and fin != debut + 1:
            raise ValidationError("Une année académique doit couvrir deux années consécutives (ex: 2023-2024)")
        
        return cleaned_data
    



#-------------------------------------MASTERCLASSE FORM----------------------------------------------------
class MasterclasseForm(forms.ModelForm):
    class Meta:
        model = Masterclasse
        fields = '__all__'
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'filieres': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'url_video': forms.URLInput(attrs={'class': 'form-control'}),
            'duree': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'ressources': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_duree(self):
        duree = self.cleaned_data.get('duree')
        if duree < 1 or duree > 600:  # 10 heures max
            raise ValidationError("La durée doit être entre 1 et 600 minutes")
        return duree

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5*1024*1024:  # 5MB
                raise ValidationError("L'image ne doit pas dépasser 5MB")
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise ValidationError("Format d'image non supporté (JPG/PNG seulement)")
        return image
    



#-------------------------------------------RAPPORT LECTURE FORM--------------------------------------
class RapportLectureForm(forms.ModelForm):
    class Meta:
        model = RapportLecture
        fields = '__all__'
        widgets = {
            'etudiant': forms.Select(attrs={'class': 'form-select'}),
            'titre_livre': forms.TextInput(attrs={'class': 'form-control'}),
            'auteur': forms.TextInput(attrs={'class': 'form-control'}),
            'resume': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5
            }),
            'apprentissages_cles': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5
            }),
            'fichier': forms.FileInput(attrs={'class': 'form-control'}),
            'commentaires_mentor': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

    def clean_fichier(self):
        fichier = self.cleaned_data.get('fichier')
        if fichier:
            if fichier.size > 5*1024*1024:  # 5MB
                raise ValidationError("Le fichier ne doit pas dépasser 5MB")
            if not fichier.name.lower().endswith(('.pdf', '.doc', '.docx')):
                raise ValidationError("Format de fichier non supporté (PDF/Word seulement)")
        return fichier





#-----------------------------------------MESSAGE FORM-------------------------------------------
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        widgets = {
            'expediteur': forms.Select(attrs={'class': 'form-select'}),
            'destinataire': forms.Select(attrs={'class': 'form-select'}),
            'sujet': forms.TextInput(attrs={'class': 'form-control'}),
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5
            }),
            'filiere_concernee': forms.Select(attrs={'class': 'form-select'}),
        }





#-------------------------------------------------NOTIFICATION FORM---------------------------------------------
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'
        widgets = {
            'utilisateur': forms.Select(attrs={'class': 'form-select'}),
            'type_notification': forms.Select(attrs={'class': 'form-select'}),
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'url_liee': forms.URLInput(attrs={'class': 'form-control'}),
        }