from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import User


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Mot de passe'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirmation du mot de passe'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'city', 'role']

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password1') != cleaned.get('password2'):
            raise forms.ValidationError(_('Les mots de passe ne correspondent pas.'))
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('Compte créé avec succès. Bienvenue !'))
            return redirect('core:home')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('core:home')
    else:
        form = AuthenticationForm(request)
    return render(request, 'accounts/signin.html', {'form': form})


@login_required
def dashboard(request):
    user = request.user
    context = {"user": user}
    template = 'accounts/dashboard_client.html'
    if hasattr(user, 'lawyer_profile') and user.is_lawyer():
        template = 'accounts/dashboard_lawyer.html'
    return render(request, template, context)

# Create your views here.
