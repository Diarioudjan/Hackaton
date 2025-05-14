from django.urls import path
from . import views
from django.conf import settings

app_name = 'signalements'

urlpatterns = [
    path('', views.list_signalements, name='list'),
    path('carte/', views.map_view, name='map'),
    path('nouveau/', views.create_signalement, name='create'),
    path('<int:pk>/', views.detail_signalement, name='detail'),
    path('<int:pk>/modifier/', views.update_signalement, name='update'),
    path('<int:pk>/supprimer/', views.delete_signalement, name='delete'),
    path('<int:pk>/vote/', views.vote_signalement, name='vote'),
] 