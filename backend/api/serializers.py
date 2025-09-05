from rest_framework import serializers
from .models import Psicologo, Paciente, Cita

class PsicologoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Psicologo
        fields = "__all__"

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = "__all__"

class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = "__all__"
