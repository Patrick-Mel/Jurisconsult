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

        # Purge éventuelle de Jean Dupont
        try:
            jd = User.objects.get(first_name="Jean", last_name="Dupont", role=User.Roles.LAWYER)
            jd.delete()
        except User.DoesNotExist:
            pass

        # 5 autres avocats crédibles
        demo_lawyers = [
            {"first_name":"Brigitte","last_name":"Ewondo","city":"Yaoundé","exp":8,"firm":"Cabinet Ewondo","specs":[civil]},
            {"first_name":"Samuel","last_name":"Abega","city":"Douala","exp":12,"firm":"Abega Legal","specs":[penal]},
            {"first_name":"Mireille","last_name":"Ngono","city":"Bafoussam","exp":6,"firm":"Ngono & Associés","specs":[civil]},
            {"first_name":"Armand","last_name":"Ewane","city":"Garoua","exp":10,"firm":"Ewane Law","specs":[penal, civil]},
            {"first_name":"Cynthia","last_name":"Mbarga","city":"Limbe","exp":4,"firm":"CM Avocats","specs":[civil]},
        ]
        for dl in demo_lawyers:
            username = (dl["first_name"].lower() + "." + dl["last_name"].lower()).replace(" ", "")
            u, _ = User.objects.get_or_create(username=username, defaults={
                "first_name": dl["first_name"], "last_name": dl["last_name"], "city": dl["city"], "role": User.Roles.LAWYER
            })
            u.set_password("password123"); u.save()
            lp, _ = LawyerProfile.objects.get_or_create(user=u, defaults={"years_of_experience": dl["exp"], "law_firm": dl["firm"]})
            lp.specialties.set(dl["specs"]) 

        cl1_username = "amina.ndiaye"
        cl1, _ = User.objects.get_or_create(username=cl1_username, defaults={
            "first_name": "Amina", "last_name": "Ndiaye", "city": "Yaoundé", "role": User.Roles.CLIENT
        })
        cl1.set_password("password123"); cl1.save()
        ClientProfile.objects.get_or_create(user=cl1)

        # Créer une consultation de démo avec le premier avocat existant
        first_lawyer = User.objects.filter(role=User.Roles.LAWYER).first()
        if first_lawyer:
            Consultation.objects.get_or_create(
                client=cl1, lawyer=first_lawyer, scheduled_at=timezone.now() + timezone.timedelta(days=1), specialty=civil
            )

        self.stdout.write(self.style.SUCCESS("Données de démo créées."))


