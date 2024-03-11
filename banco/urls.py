from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('banco', views.index, name='index'),
    path('eliminar_cliente/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('modificar_cliente/<int:cliente_id>/', views.modificar_cliente, name='modificar_cliente'),   
    path('transferir_dinero/', views.transferir_dinero, name='transferir_dinero'),

]
