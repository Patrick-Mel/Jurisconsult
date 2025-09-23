from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone


class Specialty(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name=_("Nom"))
    description = models.TextField(blank=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Spécialité juridique")
        verbose_name_plural = _("Spécialités juridiques")

    def __str__(self) -> str:
        return self.name


class Availability(models.Model):
    lawyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='availabilities', verbose_name=_("Avocat"))
    start = models.DateTimeField(verbose_name=_("Début"))
    end = models.DateTimeField(verbose_name=_("Fin"))
    notes = models.CharField(max_length=255, blank=True, verbose_name=_("Notes"))

    class Meta:
        verbose_name = _("Disponibilité")
        verbose_name_plural = _("Disponibilités")
        ordering = ['start']

    def __str__(self) -> str:
        return f"{self.lawyer.get_full_name()} - {self.start:%d/%m %H:%M} → {self.end:%H:%M}"

    def is_future(self) -> bool:
        return self.start >= timezone.now()

# Create your models here.
