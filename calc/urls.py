from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página principal
    path('tree/', views.generate_tree, name='generate_tree'),  # Endpoint para generar el árbol
]
