from django.urls import path
from . import views

app_name = 'lawyers'

urlpatterns = [
    path('', views.list_lawyers, name='list'),
    path('<int:pk>/', views.profile, name='profile'),
]


