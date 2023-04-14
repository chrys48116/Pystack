from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . models import Evento
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants
from django.http import Http404
import csv
from secrets import token_urlsafe
import os
from django.conf import settings

# Create your views here.
@login_required
def novo_evento(request):
    if request.method == 'GET':
        return render(request, 'novo_evento.html')
    
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        data_inicio = request.POST.get('data_inicio')
        data_termino = request.POST.get('data_termino')
        carga_horaria = request.POST.get('carga_horaria')
        logo = request.FILES.get('logo')
        cor_principal = request.POST.get('cor_principal')
        cor_secundaria = request.POST.get('cor_secundaria')
        cor_fundo = request.POST.get('cor_fundo')

        evento = Evento(
            criador = request.user,
            nome = nome,
            descricao = descricao,
            data_inicio = data_inicio,
            data_termino = data_termino,
            carga_horaria = carga_horaria,
            logo = logo,
            cor_principal = cor_principal,
            cor_secundaria = cor_secundaria,
            cor_fundo = cor_fundo
        )
        
        evento.save()

        messages.add_message(request, messages.SUCCESS, 'Evento criado com sucesso!')
        return redirect(reverse('novo_evento'))

def gerenciar_evento(request):
    if request.method == 'GET':
        nome = request.GET.get('nome')
        eventos = Evento.objects.filter(criador=request.user)
        
        if nome:
            eventos = eventos.filter(nome__icontains=nome)

        return render(request, 'gerenciar_evento.html', {'eventos':eventos})
    
@login_required
def inscrever_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'GET':
        return render(request, 'inscrever_evento.html', {'evento':evento})
    
    if request.method == 'POST':
        evento.participantes.add(request.user)
        evento.save()

        messages.add_message(request, messages.SUCCESS, 'Inscrição realizada com sucesso!')
        return redirect(f'/eventos/inscrever_evento/{id}')

def participantes_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if not evento.criador == request.user:
        raise Http404('Este evento não é seu.')
    
    if request.method == 'GET':
        participantes = evento.participantes.all()
        return render(request, 'participantes_evento.html', {'participantes':participantes, 'evento':evento})
    
def gerar_csv(request, id):
    evento = get_object_or_404(Evento, id=id)
    if not evento.criador == request.user:
        raise Http404('Este evento não é seu.')
    participantes = evento.participantes.all()

    token = f'{token_urlsafe(6)}.csv'
    path = os.path.join(settings.MEDIA_ROOT, token)

    with open(path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')

        for participante in participantes:
            dados = (participante.username, participante.email)
            writer.writerow(dados)

    return redirect(f'/media/{token}')