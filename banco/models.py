from django.db import models

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField(max_length=64)
    dinero = models.IntegerField()
    

    def __str__(self) -> str:
        return f"{self.id}: {self.nombre} tiene {self.dinero} pesos :)"