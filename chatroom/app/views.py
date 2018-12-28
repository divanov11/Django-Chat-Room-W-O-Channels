from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *

@csrf_exempt
def thread(request, contact, other_contact):
	user = contact
	other_user = other_contact
	thread = Thread.objects.get_or_new(user, other_user)

	form = MessageForm()

	if request.method == 'POST':
		sender = Contact.objects.get(name__icontains=contact)
		form = MessageForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.thread = thread
			instance.sender = sender
			instance.save()

	context = {'thread':thread, 'form':form}
	return render(request, 'app/thread.html', context)


