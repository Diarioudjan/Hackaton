from django.db import models
from django.conf import settings

# Create your models here.
class Signalement(models.Model):
    TYPE_CHOICES = [
        ('ROUTE', 'Problème de route'),
        ('ELECTRICITE', 'Coupure électrique'),
        ('DECHETS', 'Dépôt de déchets'),
        ('AUTRE', 'Autre'),
    ]
    
    STATUS_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('EN_COURS', 'En cours de traitement'),
        ('RESOLU', 'Résolu'),
        ('REJETE', 'Rejeté'),
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EN_ATTENTE')
    latitude = models.FloatField()
    longitude = models.FloatField()
    adresse = models.CharField(max_length=255)
    images = models.ImageField(upload_to='signalements/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    createur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='signalements'
    )

    class Meta:
        verbose_name = 'Signalement'
        verbose_name_plural = 'Signalements'
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.titre} - {self.get_type_display()}"

    @property
    def nombre_votes(self):
        return self.votes.count()

class Vote(models.Model):
    signalement = models.ForeignKey(
        Signalement,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
        unique_together = ['signalement', 'utilisateur']  # Un utilisateur ne peut voter qu'une fois
        ordering = ['-date_creation']

    def __str__(self):
        return f"Vote de {self.utilisateur} pour {self.signalement}"