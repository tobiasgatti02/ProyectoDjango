from django.shortcuts import render, redirect
from .models import Cliente
from .forms import ClienteForm
from django.http import HttpResponse
import requests

def index(request):
    precio_dolar = obtener_precio_dolar()
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ClienteForm()
    return render(request, "banco/index.html", {
        "clientes": Cliente.objects.all(),
        "form": form,
        "precio_dolar": precio_dolar[0]
    })

def eliminar_cliente(request, cliente_id):
    cliente = Cliente.objects.get(pk=cliente_id )
    cliente.delete()
    return redirect('index')

def modificar_cliente(request, cliente_id):
    cliente = Cliente.objects.get(pk=cliente_id)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, "banco/modificar_cliente.html", {"form": form, "cliente_id": cliente_id})



def obtener_precio_dolar():
    response = requests.get('https://dolarapi.com/v1/dolares/blue')
    data = response.json()
    print(data)  # Imprime la respuesta de la API
    if 'compra' in data and 'venta' in data:
        return data['compra'], data['venta']
    else:
        return None, None


from django.core.exceptions import ObjectDoesNotExist

def transferir_dinero(request):
    if request.method == "POST":
        id_origen = request.POST.get('id_origen')
        id_destino = request.POST.get('id_destino')
        cantidad = int(request.POST.get('cantidad'))

        # Comprueba si la cantidad es negativa
        if cantidad < 0:
            return HttpResponse('Error: No puedes transferir una cantidad negativa de dinero.')

        try:
            origen = Cliente.objects.get(pk=id_origen)
            destino = Cliente.objects.get(pk=id_destino)
        except ObjectDoesNotExist:
            return HttpResponse('Error: Uno o ambos usuarios no existen.')

        if origen.dinero < cantidad:
            return HttpResponse('Error: Saldo insuficiente.')
        
        origen.dinero -= cantidad
        destino.dinero += cantidad

        origen.save()
        destino.save()

    return redirect('index')
