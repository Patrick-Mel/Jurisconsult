from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages

def home(request):
    return render(request, 'core/home.html')


class ContactForm(forms.Form):
    name = forms.CharField(label='Nom', max_length=150)
    email = forms.EmailField(label='Email')
    message = forms.CharField(label='Message', widget=forms.Textarea)


def about_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Merci, votre message a bien été envoyé.')
            return redirect('core:about')
    else:
        form = ContactForm()
    return render(request, 'core/about.html', {'form': form})
