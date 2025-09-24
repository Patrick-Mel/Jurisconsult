from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Consultation, Review
from accounts.models import User
from lawyers.models import Specialty
from lawyers.models import Availability


class BookingForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['lawyer', 'specialty', 'scheduled_at', 'notes']
        widgets = {
            'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the dropdown shows real lawyer names instead of usernames
        self.fields['lawyer'].queryset = User.objects.filter(role=User.Roles.LAWYER).order_by('first_name', 'last_name')
        self.fields['lawyer'].label_from_instance = lambda obj: (obj.get_full_name() or obj.username)
        lawyer_id = None
        if 'initial' in kwargs:
            lawyer_id = kwargs['initial'].get('lawyer')
        if lawyer_id and not self.is_bound:
            try:
                self.fields['lawyer'].initial = int(lawyer_id)
            except Exception:
                pass


@login_required
def book(request):
    initial = {}
    if 'lawyer' in request.GET:
        initial['lawyer'] = request.GET.get('lawyer')
    if request.method == 'POST':
        form = BookingForm(request.POST, initial=initial)
        if form.is_valid():
            cons = form.save(commit=False)
            cons.client = request.user
            cons.status = Consultation.Status.PENDING
            # Nouvelle règle: tous les avocats sont disponibles de 07:00 à 18:00
            hour = cons.scheduled_at.hour
            within_hours = 7 <= hour < 18
            if not within_hours:
                form.add_error('scheduled_at', _('Veuillez choisir un horaire entre 07:00 et 18:00.'))
            else:
                cons.save()
                return redirect('accounts:dashboard')
    else:
        form = BookingForm(initial=initial)
    return render(request, 'consultations/book.html', {'form': form})


@login_required
def list_my_consultations(request):
    if request.user.role == User.Roles.LAWYER:
        consultations = Consultation.objects.filter(lawyer=request.user)
    else:
        consultations = Consultation.objects.filter(client=request.user)
    return render(request, 'consultations/list.html', {'consultations': consultations})


@login_required
def review(request, pk):
    from django.shortcuts import get_object_or_404
    cons = get_object_or_404(Consultation, pk=pk, client=request.user, status=Consultation.Status.COMPLETED)
    class ReviewForm(forms.ModelForm):
        class Meta:
            model = Review
            fields = ['rating', 'comment']
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.consultation = cons
            rev.save()
            return redirect('accounts:dashboard')
    else:
        form = ReviewForm()
    return render(request, 'consultations/review.html', {'form': form, 'consultation': cons})

# Create your views here.
