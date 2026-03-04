
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as v

urlpatterns = [
    path('', v.cadastro_home, name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('tutor/', v.cadastro_tutor, name='tutor'),
    path('cuidador/', v.cadastro_cuidador, name='cuidador'),

    path('usuarios/', v.usuarios_list, name='usuarios_list'),
    path('cuidadores/', v.cuidadores_list, name='cuidadores_list'),

    path('tutor/home/', v.tutor_home, name='tutor_home'),
    path('tutor/pets/novo/', v.pet_create, name='pet_create'),
    path('tutor/pets/', v.pets_list, name='pets_list'),

    path('buscar-cuidadores/', v.buscar_cuidadores, name='buscar_cuidadores'),
    path('agendar/<int:cuidador_id>/', v.agendamento_criar, name='agendamento_criar'),
    path('agendamentos/', v.agendamentos_list, name='agendamentos_list'),
    path('agendamentos/<int:agendamento_id>/', v.agendamento_detalhe, name='agendamento_detalhe'),
    path('agendamentos/<int:agendamento_id>/avaliar/', v.avaliar_agendamento, name='avaliar_agendamento'),
    path('agendamentos/<int:agendamento_id>/enviar/', v.enviar_atualizacao, name='enviar_atualizacao'),
]
