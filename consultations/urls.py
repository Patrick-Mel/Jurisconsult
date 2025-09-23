from django.urls import path
from . import views

app_name = 'consultations'

urlpatterns = [
    path('', views.list_my_consultations, name='list'),
    path('reserver/', views.book, name='book'),
    path('<int:pk>/avis/', views.review, name='review'),
]


