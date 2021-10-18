from django.urls import path
from . import views

urlpatterns = [
	#path('(showing name)', views.(function name in views), name='裡面用的名稱(?'),
	path('', views.index, name = 'home'),
	path('index', views.index, name = 'index'),
] 
