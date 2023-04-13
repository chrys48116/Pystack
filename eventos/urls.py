from . import views
from django.urls import path, include

urlpatterns = [
    path('novo_evento/', views.novo_evento, name='novo_evento'),
    path('gerenciar_evento/', views.gerenciar_evento, name='gerenciar_evento'),
    path('inscrever_evento/<int:id>/', views.inscrever_evento, name='inscrever_evento'),
]
