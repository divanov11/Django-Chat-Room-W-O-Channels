from django.urls import path
from . import views

urlpatterns = [
	path('<slug:contact>/<slug:other_contact>/', views.thread, name="thread"),
]