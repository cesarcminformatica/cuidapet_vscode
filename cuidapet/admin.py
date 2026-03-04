
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Cuidador, Servico, Pet, Disponibilidade, Agendamento, Avaliacao, Atualizacao

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Dados adicionais', {'fields': ('telefone', 'tipo_usuario')}),
    )
    list_display = ('username', 'first_name', 'email', 'tipo_usuario', 'telefone', 'is_staff')
    search_fields = ('username', 'first_name', 'email', 'telefone')

admin.site.register(Cuidador)
admin.site.register(Servico)
admin.site.register(Pet)
admin.site.register(Disponibilidade)
admin.site.register(Agendamento)
admin.site.register(Avaliacao)
admin.site.register(Atualizacao)
