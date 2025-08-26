from django.db import models

class Tarea(models.Model):
    titulo = models.CharField(max_length=150)
    hecho  = models.BooleanField(default=False)
 
    def __str__(self):
        return self.titulo