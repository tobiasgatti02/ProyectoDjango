from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'dinero']

    def clean_dinero(self):
            dinero = self.cleaned_data.get('dinero')
            if dinero < 0:
                raise forms.ValidationError('El dinero no puede ser negativo.')
            return dinero