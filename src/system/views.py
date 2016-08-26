from django.shortcuts import render, redirect
from django.http import HttpResponse
import os

# Create your views here.
def index(request):
	return render(request, 'home.html')
