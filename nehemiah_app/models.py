from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



#-----------------------------------MODELE UTILISATEUR--------------------------------
class Utilisateur(AbstractUser):
    """Modèle personnalisé pour les utilisateurs avec champs supplémentaires"""
    
    is_admin = models.BooleanField(default=False)
    telephone = models.CharField(max_length=20, blank=True)
    photo_profil = models.ImageField(upload_to='profils/', blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return self.username



#-----------------------------------MODELE FILIERE-----------------------------
class Filiere(models.Model):
    """Filières d'étude disponibles"""
    nom = models.CharField(max_length=100)
    description = models.TextField()
    couleur = models.CharField(max_length=7)
    icone = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nom


#--------------------------------MODELE ANNEE ACADEMIQUE-------------------------
class AnneeAcademique(models.Model):
    """Année académique utilisée dans tout le système"""
    debut = models.PositiveIntegerField()
    fin = models.PositiveIntegerField()

    class Meta:
        unique_together = ('debut', 'fin')
        ordering = ['-debut']

    def __str__(self):
        return f"{self.debut}-{self.fin}"

    def est_courante(self):
        """Retourne True si on est actuellement dans cette année"""
        annee_en_cours = timezone.now().year
        return self.debut <= annee_en_cours <= self.fin



#-----------------------------------------MODELE BENEFICIAIRE-----------------------------------
class Beneficiaire(models.Model):
    """Profil complémentaire pour les étudiants bénéficiaires"""
    
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    numero_cde = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    numero_beneficiaire = models.CharField(unique=True, max_length=9)
    date_naissance = models.DateField(null=True)
    adresse = models.TextField(blank=True)
    sexe = models.CharField(max_length=20, choices=(("F", "Féminin"), ("M", "Masculin")))



#----------------------------------MODELE MASTERCLASSE------------------------------------------
class Masterclasse(models.Model):
    """Masterclasses du programme"""
    titre = models.CharField(max_length=200)
    description = models.TextField()
    filieres = models.ManyToManyField(Filiere)
    image = models.ImageField(blank=True, null=True, upload_to="masterclasses/ressources")
    url_video = models.URLField()
    duree = models.PositiveIntegerField(help_text="Durée en minutes")
    date_publication = models.DateTimeField(auto_now_add=True)
    est_active = models.BooleanField(default=True)
    ressources = models.FileField(upload_to='masterclasses/ressources/', blank=True)



#-------------------------------------PROGRESSION MASTERCLASSE---------------------------------
class ProgressionMasterclasse(models.Model):
    """Suivi de progression des étudiants"""
    etudiant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    masterclasse = models.ForeignKey(Masterclasse, on_delete=models.CASCADE)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_completion = models.DateTimeField(null=True, blank=True)
    est_terminee = models.BooleanField(default=False)
    progression = models.PositiveIntegerField(default=0)




#------------------------------------------RAPPORT DE LECTURE---------------------------------------
class RapportLecture(models.Model):
    """Rapports de lecture soumis par les étudiants"""
    STATUT_RAPPORT = [
        ('soumis', 'Soumis'),
        ('en_revue', 'En revue'),
        ('a_reviser', 'À réviser'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
    ]
    
    etudiant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    titre_livre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=200)
    resume = models.TextField()
    apprentissages_cles = models.TextField()
    date_soumission = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_RAPPORT, default='soumis')
    fichier = models.FileField(upload_to='rapports/', blank=True)
    commentaires_mentor = models.TextField(blank=True)
    date_evaluation = models.DateTimeField(null=True, blank=True)




#----------------------------------------REINSCRIPTION-------------------------------------
class Reinscription(models.Model):
    """Demande de réinscription annuelle"""
    
    STATUT_REINSCRIPTION = [
        ('en_attente', 'En attente de validation'),
        ('selectionne', 'Sélectionné'),
        ('non_selectionne', 'Non sélectionné'),
    ]

    DOMAINE_ETUDE_CHOICES = [
        ('btp', 'Bâtiment & Travaux Publics'),
        ('info_eco_num', 'Informatique & Economie Numérique'),
        ('mgi', 'Mécanique et Génie industriel (MGI)'),
        ('communication', 'Communication'),
        ('energie', 'Energies Renouvelables et Efficacité Energétique'),
        ('agrobusiness', 'Agrobusiness et Industrie Agroalimentaire'),
        ('gestion', 'Gestion (Administration, Finances, Marketing, GRH, Comptabilité)'),
        ('sante', 'Sciences de la santé'),
        ('stylisme', 'Stylisme et modélisme'),
    ]
    
    
    NIVEAU_SCOLAIRE_CHOICES = [
        ('bt', 'BT'),
        ('bac2', 'BAC 2'),
        ('bts', 'BTS'),
        ('licence', 'Licence'),
        ('semestre1_2', 'Semestre 1 et 2'),
        ('semestre3_4', 'Semestre 3 et 4'),
        ('semestre5_6', 'Semestre 5 et 6'),
        ('semestre7', 'Semestre 7'),
    ]
    
    # Informations de base
    etudiant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.PROTECT)
    date_soumission = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_REINSCRIPTION, default='en_attente')
    
    # Suivi des masterclasses
    masterclasses_suivies = models.ManyToManyField(Masterclasse, blank=True)
    
    # Informations académiques
    domaine_etude = models.CharField(
        max_length=50,
        choices=DOMAINE_ETUDE_CHOICES,
        verbose_name="Domaine d'étude"
    )
    niveau_scolaire = models.CharField(max_length=20, choices=NIVEAU_SCOLAIRE_CHOICES)
    annee_obtention_diplome = models.PositiveIntegerField()
    moyenne_obtenue = models.DecimalField(max_digits=4, decimal_places=2)
    specialite = models.CharField(max_length=100)
    universite = models.CharField(max_length=100)
    
    # Informations géographiques
    commune_residence = models.CharField(max_length=100)
    ville_residence = models.CharField(max_length=100)
    quartier_residence = models.CharField(max_length=100)
    
    # Détails du crédit
    besoin_logement = models.BooleanField(default=False)
    montant_loyer_annuel = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    frais_scolarite = models.DecimalField(max_digits=10, decimal_places=2)
    besoin_ordinateur = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    frais_transport = models.DecimalField(max_digits=10, decimal_places=2)
    frais_assurance = models.DecimalField(max_digits=10, decimal_places=2, default=50000)
    
    # Motifs et détails supplémentaires
    motif_demande = models.TextField()
    nationalite = models.CharField(max_length=100, blank=True, null=True)
    
    # Fichiers joints
    releve_note_precedent = models.FileField(upload_to='reinscription/releves/', blank=True, null=True)
    rapport_stage = models.FileField(upload_to='reinscription/rapports/', blank=True, null=True)
    lettre_recommandation = models.FileField(upload_to='reinscription/recommandations/', blank=True, null=True)
    copie_diplome = models.FileField(upload_to='reinscription/diplomes/', blank=True, null=True)
    copie_nationalite = models.FileField(upload_to='reinscription/nationalites/', blank=True, null=True)
    
    class Meta:
        unique_together = ('etudiant', 'annee_academique')
        verbose_name = "Demande de réinscription"
        verbose_name_plural = "Demandes de réinscription"
    
    def __str__(self):
        return f"Réinscription {self.annee_academique} - {self.etudiant}"
    
    def montant_total_demande(self):
        """Calcule le montant total du crédit demandé"""
        return (self.frais_scolarite + self.montant_loyer_annuel + 
                self.besoin_ordinateur + self.frais_transport + self.frais_assurance)

    def clean(self):
        """Validation des données avant sauvegarde"""
        from django.core.exceptions import ValidationError
        
        # Validation du montant maximum
        if self.montant_total_demande() > 1200000:
            raise ValidationError("Le montant total demandé ne peut pas dépasser 1 200 000 FCFA")
        
        if self.montant_loyer_annuel > 120000:
            raise ValidationError("Le loyer annuel ne peut pas dépasser 120 000 FCFA")
        
        if self.besoin_ordinateur > 450000:
            raise ValidationError("Le montant pour l'ordinateur ne peut pas dépasser 450 000 FCFA")

        # Appel au clean() parent pour les validations par défaut
        super().clean()
    
    def est_complete(self):
        """Vérifie si tous les documents requis sont fournis"""
        return all([
            self.releve_note_precedent,
            self.lettre_recommandation,
            self.copie_diplome,
            self.motif_demande,
            self.frais_scolarite is not None
        ])


#-------------------------------------------DISCUSSION DE GROUPE----------------------------------------
class GroupeDiscussion(models.Model):
    """Groupe de discussion par domaine d'étude"""
    domaine_etude = models.CharField(max_length=50, choices=Reinscription.DOMAINE_ETUDE_CHOICES, unique=True)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom



#----------------------------------------------MESSAGE--------------------------------------------------
class Message(models.Model):
    """Messagerie interne (privée ou par groupe)"""
    expediteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinataire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='messages_recus', null=True, blank=True)
    groupe = models.ForeignKey(GroupeDiscussion, on_delete=models.CASCADE, null=True, blank=True)

    sujet = models.CharField(max_length=200, blank=True)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    def est_message_groupe(self):
        return self.groupe is not None



#--------------------------------------------NOTIFICATION---------------------------------------------
class Notification(models.Model):
    """Notifications système"""
    TYPE_NOTIFICATION = [
        ('rapport', 'Rapport de lecture'),
        ('masterclasse', 'Masterclasse'),
        ('reinscription', 'Réinscription'),
        ('message', 'Message'),
    ]
    
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    type_notification = models.CharField(max_length=20, choices=TYPE_NOTIFICATION)
    titre = models.CharField(max_length=200)
    message = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    lue = models.BooleanField(default=False)
    url_liee = models.URLField(blank=True) 


