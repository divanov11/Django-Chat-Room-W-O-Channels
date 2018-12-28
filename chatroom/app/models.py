from django.db import models
from django.db.models import Q

class Contact(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class ThreadManager(models.Manager):
	def get_or_new(self, user, other_user):
		if user == other_user:
			return None

		try:
			qlookup1 = Q(first__name__icontains=user) & Q(second__name__icontains=other_user)
			qlookup2 = Q(first__name__icontains=other_user) & Q(second__name__icontains=user)
			qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
			print(qs)
			if qs.count() > 0:
				return qs.order_by('created').first()
			else:
				if user != other_user:
					obj = self.model(
						first=user,
						second=other_user
						)
					obj.save()
					return obj
				return None
		except:
			return None

class Thread(models.Model):
	first = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='chat_thread_first')
	second = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='chat_thread_second')
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True) 

	objects = ThreadManager()

	def __str__(self):
		return str(self.first) + '/' + str(self.second) + '/' + str(self.message_set.all().count())

class Message(models.Model):
	thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
	sender = models.ForeignKey(Contact, null=True, blank=True, on_delete=models.SET_NULL)
	message = models.TextField()
	created   = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.message

	class Meta:
		ordering = ['-created']


