from django.shortcuts import render
from django.db.models import Q
from .models import Specialty, Availability
from accounts.models import User


def list_lawyers(request):
    query = request.GET.get('q', '')
    city = request.GET.get('ville', '')
    specialty_id = request.GET.get('specialite', '')

    lawyers = User.objects.filter(role=User.Roles.LAWYER)
    if query:
        lawyers = lawyers.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
    if city:
        lawyers = lawyers.filter(city__icontains=city)
    if specialty_id:
        lawyers = lawyers.filter(lawyer_profile__specialties__id=specialty_id)

    specialties = Specialty.objects.all()
    return render(request, 'lawyers/list.html', {
        'lawyers': lawyers.distinct(),
        'specialties': specialties,
        'q': query,
        'ville': city,
        'specialite': specialty_id,
    })


def profile(request, pk):
    from django.shortcuts import get_object_or_404
    lawyer = get_object_or_404(User, pk=pk, role=User.Roles.LAWYER)
    availabilities = Availability.objects.filter(lawyer=lawyer)
    return render(request, 'lawyers/profile.html', {'lawyer': lawyer, 'availabilities': availabilities})

# Create your views here.
