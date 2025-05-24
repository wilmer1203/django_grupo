# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Curso, Calificacion, UsuarioPersonalizado

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos', {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser',
                'groups', 
                'user_permissions'
            ),
        }),
        ('Roles', {'fields': ('rol',)}),  # ← Usar el nuevo campo 'rol'
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'rol'),
        }),
    )
    list_display = ('username', 'email', 'rol', 'is_staff')
    list_filter = ('rol', 'is_staff', 'is_superuser')

admin.site.register(Curso)
admin.site.register(Calificacion)
admin.site.register(UsuarioPersonalizado, CustomUserAdmin)