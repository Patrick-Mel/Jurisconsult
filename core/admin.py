from django.contrib import admin
from accounts.models import User, ClientProfile, LawyerProfile
from lawyers.models import Specialty
from consultations.models import Consultation
from messaging.models import Conversation, Message
from payments.models import Payment

# Register your models here.

admin.site.register(User)
admin.site.register(ClientProfile)
admin.site.register(LawyerProfile)
admin.site.register(Specialty)
admin.site.register(Consultation)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Payment)
