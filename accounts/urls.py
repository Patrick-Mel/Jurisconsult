from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('inscription/', views.signup, name='signup'),
    path('connexion/', views.signin, name='signin'),
    path('deconnexion/', LogoutView.as_view(next_page='core:home'), name='logout'),
    path('tableau-de-bord/', views.dashboard, name='dashboard'),
]


