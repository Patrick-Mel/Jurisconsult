from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Conversation, Message
from consultations.models import Consultation


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(consultation__client=request.user) | Conversation.objects.filter(consultation__lawyer=request.user)
    conversations = conversations.select_related('consultation').order_by('-created_at')
    return render(request, 'messaging/inbox.html', {'conversations': conversations})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'attachment']


@login_required
def thread(request, pk):
    conv = get_object_or_404(Conversation, pk=pk)
    if request.user not in [conv.consultation.client, conv.consultation.lawyer]:
        return redirect('messaging:inbox')
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.conversation = conv
            msg.sender = request.user
            msg.save()
            return redirect('messaging:thread', pk=conv.pk)
    else:
        form = MessageForm()
    return render(request, 'messaging/thread.html', {'conversation': conv, 'form': form})

# Create your views here.
