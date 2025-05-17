from django.urls import path
from . import views
from .views import CustomLogoutView

urlpatterns = [
path('', views.dashboard, name='dashboard'),
path('perfil/', views.perfil_view, name='perfil'),
path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
]
