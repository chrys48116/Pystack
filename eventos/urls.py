from . import views
from django.urls import path, include

urlpatterns = [
    path('novo_evento/', views.novo_evento, name='novo_evento'),
]
