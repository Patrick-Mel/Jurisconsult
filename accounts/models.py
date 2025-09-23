from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Roles(models.TextChoices):
        CLIENT = "client", _("Client")
        LAWYER = "lawyer", _("Avocat")
        ADMIN = "admin", _("Administrateur")

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.CLIENT,
        verbose_name=_("Rôle")
    )
    phone = models.CharField(max_length=30, blank=True, verbose_name=_("Téléphone"))
    city = models.CharField(max_length=100, blank=True, verbose_name=_("Ville"))

    def is_client(self) -> bool:
        return self.role == self.Roles.CLIENT

    def is_lawyer(self) -> bool:
        return self.role == self.Roles.LAWYER


class ClientProfile(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='client_profile')
    # Additional client fields
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Profil client")
        verbose_name_plural = _("Profils clients")

    def __str__(self) -> str:
        return f"Client: {self.user.get_full_name()}"


class LawyerProfile(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='lawyer_profile')
    law_firm = models.CharField(max_length=255, blank=True, verbose_name=_("Cabinet"))
    specialties = models.ManyToManyField('lawyers.Specialty', blank=True, related_name='lawyers', verbose_name=_("Spécialités"))
    years_of_experience = models.PositiveIntegerField(default=0, verbose_name=_("Années d’expérience"))
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name=_("Photo de profil"))
    bar_id_document = models.FileField(upload_to='documents/', blank=True, null=True, verbose_name=_("Carte d’avocat"))
    degrees = models.FileField(upload_to='documents/', blank=True, null=True, verbose_name=_("Diplômes/Certifications"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Profil avocat")
        verbose_name_plural = _("Profils avocats")

    def __str__(self) -> str:
        return f"Avocat: {self.user.get_full_name()}"

# Create your models here.
