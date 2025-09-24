from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
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


class NameOrUsernameAuthenticationForm(forms.Form):
    username = forms.CharField(label=_('Nom complet ou nom d’utilisateur'))
    password = forms.CharField(label=_('Mot de passe'), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _('Veuillez entrer un identifiant et un mot de passe valides.'),
        'inactive': _('Ce compte est inactif.'),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        username_or_name = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = None
        if username_or_name and password:
            # 1) Try direct username login
            user = authenticate(self.request, username=username_or_name, password=password)
            if not user:
                # 2) Try by full name (first_name + space + last_name)
                try:
                    # Case-insensitive exact match on full name
                    first_last_qs = User.objects.filter(
                        first_name__isnull=False, last_name__isnull=False
                    ).extra(
                        where=["LOWER(first_name || ' ' || last_name) = LOWER(%s)"],
                        params=[username_or_name]
                    )
                except Exception:
                    first_last_qs = User.objects.none()
                if not first_last_qs.exists():
                    # Fallback: try splitting on space to match first and last separately
                    parts = username_or_name.strip().split()
                    if len(parts) >= 2:
                        first = parts[0]
                        last = ' '.join(parts[1:])
                        first_last_qs = User.objects.filter(first_name__iexact=first, last_name__iexact=last)
                if first_last_qs.count() == 1:
                    candidate = first_last_qs.first()
                    user = authenticate(self.request, username=candidate.username, password=password)

            if user is None:
                raise forms.ValidationError(self.error_messages['invalid_login'], code='invalid_login')

            if not user.is_active:
                raise forms.ValidationError(self.error_messages['inactive'], code='inactive')

            self.user_cache = user
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


def signin(request):
    if request.method == 'POST':
        form = NameOrUsernameAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('core:home')
    else:
        form = NameOrUsernameAuthenticationForm(request)
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
