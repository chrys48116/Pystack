from . import views
from django.urls import path, include

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro')
]
