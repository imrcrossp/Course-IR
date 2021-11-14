import hw.models as mod
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
@ensure_csrf_cookie
def index(request):
	if request.method == 'POST':
		msg = request.POST.get('msg')
		if msg == 'cloud':
			data = mod.fromcloud()
			return HttpResponse(json.dumps(data))
		if msg == 'adv_search':
			data = mod.advancedsearching(request.POST.get('key'), request.POST.get('upper'), request.POST.get('lower'))
			return HttpResponse(json.dumps(data))
	else:
		return render(request, 'hw/index.html')

def docs(request):
	token = request.GET.get('msg')
	if token == "cloud":
		fn = request.GET.get('fn')
		token = request.GET.get('token')
		data = mod.showcntxt(fn, token)
		return HttpResponse(json.dumps(data))
	return render(request, 'hw/docs.html')

def detail(reauest, q_id):
	return HttpResponse("You're looking at question %s."% q_id)

def stat(request):
	if 'text' in request.GET:
		text = request.GET['text']
		if text == "":
			text = "-info"
	else:
		text = "-info"
	cntxt = mod.DashBoard(text)
	return render(request, 'hw/statictis.html', cntxt)