from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . models import Evento
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants

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