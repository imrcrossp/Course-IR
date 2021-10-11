from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return render(request, 'hw1/index.html')
def detail(reauest, q_id):
	return HttpResponse("You're looking at question %s."% q_id)