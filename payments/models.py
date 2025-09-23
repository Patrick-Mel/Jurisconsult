from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("En attente")
        PAID = "paid", _("Payé")
        FAILED = "failed", _("Échoué")

    consultation = models.OneToOneField('consultations.Consultation', on_delete=models.CASCADE, related_name='payment', verbose_name=_("Consultation"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Montant"))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name=_("Statut"))
    provider = models.CharField(max_length=50, blank=True, verbose_name=_("Fournisseur"))
    reference = models.CharField(max_length=100, blank=True, verbose_name=_("Référence"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Paiement")
        verbose_name_plural = _("Paiements")

    def __str__(self) -> str:
        return f"{self.amount} {self.get_status_display()}"

# Create your models here.
