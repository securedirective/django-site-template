from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

# Create your views here.
def index(request):
	context = {'settings_file': settings.CONFIG_FILE_IN_USE}
	return render(request, 'home.html', context)
