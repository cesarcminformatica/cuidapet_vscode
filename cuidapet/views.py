
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from math import ceil
from .models import Usuario, Cuidador, Pet, Agendamento
from .forms import (
    UsuarioTutorForm, UsuarioCuidadorForm, CuidadorForm,
    PetForm, AgendamentoForm, AvaliacaoForm, AtualizacaoForm
)

def cadastro_home(request):
    return render(request, 'cadastro.html')

def cadastro_tutor(request):
    if request.method == 'POST':
        form = UsuarioTutorForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.tipo_usuario = Usuario.TipoUsuario.TUTOR
            user.save()
            messages.success(request, 'Cadastro de Tutor realizado com sucesso! Faça login para continuar.')
            return redirect('login')
    else:
        form = UsuarioTutorForm()
    return render(request, 'tutor_form.html', {'form': form})

def cadastro_cuidador(request):
    if request.method == 'POST':
        user_form = UsuarioCuidadorForm(request.POST)
        cuidador_form = CuidadorForm(request.POST)
        if user_form.is_valid() and cuidador_form.is_valid():
            user = user_form.save(commit=False)
            user.tipo_usuario = Usuario.TipoUsuario.CUIDADOR
            user.save()
            cuidador = cuidador_form.save(commit=False)
            cuidador.usuario = user
            cuidador.save()
            cuidador_form.save_m2m()
            messages.success(request, 'Cadastro de Cuidador realizado com sucesso! Faça login para continuar.')
            return redirect('login')
    else:
        user_form = UsuarioCuidadorForm()
        cuidador_form = CuidadorForm()
    return render(request, 'cuidador_form.html', {'user_form': user_form, 'cuidador_form': cuidador_form})

@login_required
def usuarios_list(request):
    q = request.GET.get('q', '').strip()
    usuarios = Usuario.objects.all().order_by('-date_joined')
    if q:
        usuarios = usuarios.filter(Q(username__icontains=q) | Q(first_name__icontains=q) | Q(email__icontains=q) | Q(tipo_usuario__icontains=q))
    return render(request, 'usuarios_list.html', {'usuarios': usuarios, 'q': q})

@login_required
def cuidadores_list(request):
    q = request.GET.get('q', '').strip()
    cidade = request.GET.get('cidade', '').strip()
    uf = request.GET.get('uf', '').strip()
    cuidadores = Cuidador.objects.select_related('usuario').all().order_by('usuario__first_name')
    if q:
        cuidadores = cuidadores.filter(Q(usuario__first_name__icontains=q) | Q(usuario__username__icontains=q) | Q(descricao__icontains=q))
    if cidade:
        cuidadores = cuidadores.filter(cidade__icontains=cidade)
    if uf:
        cuidadores = cuidadores.filter(uf=uf)
    return render(request, 'cuidadores_list.html', {'cuidadores': cuidadores, 'q': q, 'cidade': cidade, 'uf': uf})

@login_required
def tutor_home(request):
    pets = Pet.objects.filter(usuario=request.user).order_by('nome')
    agendamentos = Agendamento.objects.filter(usuario=request.user).order_by('-data_criacao')[:5]
    return render(request, 'tutor_home.html', {'pets': pets, 'agendamentos': agendamentos})

@login_required
def pet_create(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.usuario = request.user
            pet.save()
            messages.success(request, 'Pet cadastrado com sucesso!')
            return redirect('tutor_home')
    else:
        form = PetForm()
    return render(request, 'pet_form.html', {'form': form})

@login_required
def pets_list(request):
    pets = Pet.objects.filter(usuario=request.user).order_by('nome')
    return render(request, 'pets_list.html', {'pets': pets})

@login_required
def buscar_cuidadores(request):
    q = request.GET.get('q', '').strip()
    cidade = request.GET.get('cidade', '').strip()
    uf = request.GET.get('uf', '').strip()
    pet_id = request.GET.get('pet')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    cuidadores = Cuidador.objects.select_related('usuario').all()
    if q:
        cuidadores = cuidadores.filter(Q(usuario__first_name__icontains=q) | Q(descricao__icontains=q))
    if cidade:
        cuidadores = cuidadores.filter(cidade__icontains=cidade)
    if uf:
        cuidadores = cuidadores.filter(uf=uf)

    especie = None
    if pet_id:
        try:
            pet = Pet.objects.get(id=pet_id, usuario=request.user)
            especie = pet.especie
            cuidadores = cuidadores.filter(Q(servicos__descricao__iexact=especie) | Q(servicos__descricao__icontains=especie))
        except Pet.DoesNotExist:
            raise Http404('Pet não encontrado')

    from datetime import datetime
    fmt = '%Y-%m-%dT%H:%M'
    if data_inicio and data_fim:
        try:
            inicio_dt = datetime.strptime(data_inicio, fmt)
            fim_dt = datetime.strptime(data_fim, fmt)
            from .models import Disponibilidade
            cuidadores = cuidadores.filter(disponibilidades__data_inicio__lte=inicio_dt, disponibilidades__data_fim__gte=fim_dt).distinct()
        except ValueError:
            messages.warning(request, 'Datas inválidas. Use o formato correto.')

    return render(request, 'buscar_cuidadores.html', {
        'cuidadores': cuidadores.distinct().order_by('usuario__first_name'),
        'q': q, 'cidade': cidade, 'uf': uf,
        'pets': Pet.objects.filter(usuario=request.user),
        'pet_id': pet_id,
        'data_inicio': data_inicio, 'data_fim': data_fim,
        'especie': especie
    })

@login_required
def agendamento_criar(request, cuidador_id):
    try:
        cuidador = Cuidador.objects.select_related('usuario').get(id=cuidador_id)
    except Cuidador.DoesNotExist:
        raise Http404('Cuidador não encontrado')

    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        form.fields['pet'].queryset = Pet.objects.filter(usuario=request.user)
        if form.is_valid():
            ag = form.save(commit=False)
            ag.usuario = request.user
            ag.cuidador = cuidador
            delta = (ag.data_fim - ag.data_inicio).total_seconds() / 86400.0
            dias = max(1, ceil(delta))
            ag.valor_total = cuidador.valor_diaria * dias
            ag.save()
            messages.success(request, 'Agendamento criado!')
            return redirect('agendamentos_list')
    else:
        form = AgendamentoForm()
        form.fields['pet'].queryset = Pet.objects.filter(usuario=request.user)
    return render(request, 'agendamento_form.html', {'form': form, 'cuidador': cuidador})

@login_required
def agendamentos_list(request):
    ags = Agendamento.objects.filter(usuario=request.user).select_related('cuidador__usuario', 'pet').order_by('-data_inicio')
    return render(request, 'agendamentos_list.html', {'agendamentos': ags})

@login_required
def agendamento_detalhe(request, agendamento_id):
    ag = Agendamento.objects.select_related('cuidador__usuario', 'pet', 'usuario').get(id=agendamento_id)
    if ag.usuario != request.user and ag.cuidador.usuario != request.user:
        raise Http404('Agendamento não encontrado')
    atualizacoes = ag.atualizacoes.select_related('autor').all()
    form = AtualizacaoForm()
    avaliacao = getattr(ag, 'avaliacao', None)
    return render(request, 'agendamento_detalhe.html', {'ag': ag, 'avaliacao': avaliacao, 'atualizacoes': atualizacoes, 'form_atualizacao': form})

@login_required
def enviar_atualizacao(request, agendamento_id):
    ag = Agendamento.objects.select_related('cuidador__usuario', 'usuario').get(id=agendamento_id)
    if ag.usuario != request.user and ag.cuidador.usuario != request.user:
        raise Http404('Não autorizado')
    if request.method == 'POST':
        form = AtualizacaoForm(request.POST, request.FILES)
        if form.is_valid():
            upd = form.save(commit=False)
            upd.autor = request.user
            upd.agendamento = ag
            if not upd.mensagem and not upd.imagem:
                messages.warning(request, 'Envie uma mensagem e/ou uma imagem.')
            else:
                upd.save()
                messages.success(request, 'Atualização enviada!')
        else:
            messages.error(request, 'Verifique os campos do formulário.')
    return redirect('agendamento_detalhe', agendamento_id=ag.id)

@login_required
def avaliar_agendamento(request, agendamento_id):
    ag = Agendamento.objects.select_related('cuidador__usuario', 'pet').get(id=agendamento_id)
    if ag.usuario != request.user:
        raise Http404('Agendamento não encontrado')
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            if hasattr(ag, 'avaliacao'):
                messages.warning(request, 'Este agendamento já foi avaliado.')
            else:
                av = form.save(commit=False)
                av.agendamento = ag
                av.save()
                messages.success(request, 'Avaliação registrada. Obrigado!')
            return redirect('agendamento_detalhe', agendamento_id=ag.id)
    else:
        form = AvaliacaoForm()
    return render(request, 'avaliacao_form.html', {'form': form, 'ag': ag})
