from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Conversation(models.Model):
    consultation = models.OneToOneField('consultations.Consultation', on_delete=models.CASCADE, related_name='conversation', verbose_name=_("Consultation"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Conversation")
        verbose_name_plural = _("Conversations")

    def __str__(self) -> str:
        return f"Conversation #{self.pk}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', verbose_name=_("Conversation"))
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages', verbose_name=_("Expéditeur"))
    content = models.TextField(blank=True, verbose_name=_("Message"))
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True, verbose_name=_("Pièce jointe"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ['created_at']

    def __str__(self) -> str:
        return f"{self.sender.get_full_name()}: {self.content[:30]}"

# Create your models here.
