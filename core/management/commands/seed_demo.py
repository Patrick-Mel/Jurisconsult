from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User, LawyerProfile, ClientProfile
from lawyers.models import Specialty
from consultations.models import Consultation


class Command(BaseCommand):
    help = "Crée des données de démonstration (utilisateurs, spécialités, consultations)."

    def handle(self, *args, **options):
        civil = Specialty.objects.get_or_create(name="Droit civil")[0]
        penal = Specialty.objects.get_or_create(name="Droit pénal")[0]

        av1, _ = User.objects.get_or_create(username="avocat1", defaults={
            "first_name": "Jean", "last_name": "Dupont", "city": "Douala", "role": User.Roles.LAWYER
        })
        av1.set_password("password123"); av1.save()
        LawyerProfile.objects.get_or_create(user=av1, defaults={"years_of_experience": 5})[0].specialties.set([civil, penal])

        cl1, _ = User.objects.get_or_create(username="client1", defaults={
            "first_name": "Amina", "last_name": "Ndiaye", "city": "Yaoundé", "role": User.Roles.CLIENT
        })
        cl1.set_password("password123"); cl1.save()
        ClientProfile.objects.get_or_create(user=cl1)

        Consultation.objects.get_or_create(
            client=cl1, lawyer=av1, scheduled_at=timezone.now() + timezone.timedelta(days=1), specialty=civil
        )

        self.stdout.write(self.style.SUCCESS("Données de démo créées."))


