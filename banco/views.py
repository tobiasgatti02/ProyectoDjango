from django.shortcuts import render, redirect
from .models import Cliente
from .forms import ClienteForm
from django.http import HttpResponse
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


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
        "precio_dolar": precio_dolar[1]
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




def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Si las credenciales son válidas, iniciar sesión
            login(request, user)
            return redirect('index')  # Redirigir a la página principal
        else:
            # Si las credenciales no son válidas, mostrar un mensaje de error
            error_message = "Credenciales inválidas. Por favor, inténtalo de nuevo."
            return render(request, "login.html", {"error_message": error_message})
    else:
        # Si la solicitud no es de tipo POST, renderizar el formulario de inicio de sesión
        return render(request, "login.html")
