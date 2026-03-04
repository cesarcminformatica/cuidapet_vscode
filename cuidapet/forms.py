
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Usuario, Cuidador, Servico, Pet, Agendamento, Avaliacao, Atualizacao

class UsuarioTutorForm(UserCreationForm):
    first_name = forms.CharField(label="Nome", max_length=150)
    email = forms.EmailField(label="E-mail")
    telefone = forms.CharField(label="Telefone (apenas dígitos)", max_length=11)
    class Meta:
        model = Usuario
        fields = ("username", "first_name", "email", "telefone", "password1", "password2")

class UsuarioCuidadorForm(UserCreationForm):
    first_name = forms.CharField(label="Nome", max_length=150)
    email = forms.EmailField(label="E-mail")
    telefone = forms.CharField(label="Telefone (apenas dígitos)", max_length=11)
    class Meta:
        model = Usuario
        fields = ("username", "first_name", "email", "telefone", "password1", "password2")

class CuidadorForm(ModelForm):
    servicos = forms.ModelMultipleChoiceField(
        label="Serviços oferecidos",
        queryset=Servico.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Cuidador
        fields = ("descricao", "valor_diaria", "cidade", "uf", "servicos")

class PetForm(ModelForm):
    class Meta:
        model = Pet
        fields = ("nome", "especie", "raca", "data_nascimento")

class AgendamentoForm(ModelForm):
    class Meta:
        model = Agendamento
        fields = ("pet", "forma_pagamento", "data_inicio", "data_fim")
        widgets = {
            'data_inicio': forms.DateTimeInput(attrs={'type':'datetime-local'}),
            'data_fim': forms.DateTimeInput(attrs={'type':'datetime-local'}),
        }

class AvaliacaoForm(ModelForm):
    class Meta:
        model = Avaliacao
        fields = ("nota", "comentario")

class AtualizacaoForm(ModelForm):
    class Meta:
        model = Atualizacao
        fields = ("mensagem", "imagem")
