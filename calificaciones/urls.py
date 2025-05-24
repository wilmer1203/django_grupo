from django.urls import path
from . import views
from .views import (
    dashboard,
    perfil_estudiante,
    gestion_calificaciones,
    CustomLogoutView
    )


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('perfil/', views.perfil_estudiante, name='perfil_estudiante'),
    path('redireccion/', views.redireccion_rol, name='redireccion_rol'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('gestion-calificaciones/', views.gestion_calificaciones, name='gestion_calificaciones'),
    path('gestion-calificaciones/editar/<int:calificacion_id>/', views.gestion_calificaciones, name='editar_calificacion'),
    path('gestion-calificaciones/eliminar/<int:calificacion_id>/', views.eliminar_calificacion, name='eliminar_calificacion'),
    ]