from django.shortcuts import render
from django.contrib import admin
from django.urls import path, include

def home(request):
    return render(request, 'base.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signalements/', include('signalements.urls')),
    path('utilisateurs/', include('utilisateurs.urls')),
    path('', home, name='home'),
]
