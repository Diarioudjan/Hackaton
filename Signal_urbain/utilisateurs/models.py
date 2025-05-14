from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('USER', 'Utilisateur'),
        ('ADMIN', 'Administrateur'),
    ]
    
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    is_verified = models.BooleanField(default=False)
    date_modified = models.DateTimeField(auto_now=True)
    
    groups= models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='user_set',
        related_query_name='custom_user_groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    def __str__(self):
        return self.email
