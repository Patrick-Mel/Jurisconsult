from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Consultation(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("En attente")
        ACCEPTED = "accepted", _("Acceptée")
        DECLINED = "declined", _("Refusée")
        COMPLETED = "completed", _("Terminée")

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_consultations', verbose_name=_("Client"))
    lawyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lawyer_consultations', verbose_name=_("Avocat"))
    specialty = models.ForeignKey('lawyers.Specialty', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Spécialité"))
    scheduled_at = models.DateTimeField(verbose_name=_("Date et heure"))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name=_("Statut"))
    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Consultation")
        verbose_name_plural = _("Consultations")
        ordering = ['-scheduled_at']

    def __str__(self) -> str:
        return f"{self.client.get_full_name()} ↔ {self.lawyer.get_full_name()} ({self.scheduled_at:%Y-%m-%d %H:%M})"


class Review(models.Model):
    consultation = models.OneToOneField('consultations.Consultation', on_delete=models.CASCADE, related_name='review', verbose_name=_("Consultation"))
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name=_("Note"))
    comment = models.TextField(blank=True, verbose_name=_("Commentaire"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Avis")
        verbose_name_plural = _("Avis")

    def __str__(self) -> str:
        return f"{self.rating}/5"

# Create your models here.
