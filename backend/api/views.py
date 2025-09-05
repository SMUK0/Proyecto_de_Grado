# backend/api/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from .models import Psicologo, Paciente, Cita
from .serializers import PsicologoSerializer, PacienteSerializer, CitaSerializer

@api_view(["GET"])
def home_info(request):
    return Response({
        "brand": "Resoluciones Integrales",
        "tagline": "Servicios de intervención terapéutica integral multidisciplinaria y personalizada.",
        "about": ("Somos un consultorio que brinda intervención terapéutica integral y personalizada. "
                  "Contáctanos para recibir apoyo profesional."),
        "services": [
            {"name": "Apoyo terapéutico por adicciones",
             "description": "Acompañamiento clínico y psicoeducativo orientado a la recuperación.",
             "slug": "adicciones"},
            {"name": "Intervención terapéutica integral",
             "description": "Atención multidisciplinaria centrada en la persona.",
             "slug": "intervencion-integral"},
        ],
        "contact": {"whatsapp": "https://walink.co/e3e2a6"},
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    u = request.user
    return Response({"username": u.username, "email": u.email})

# (si ya tienes estos viewsets, déjalos tal cual)
class PsicologoViewSet(viewsets.ModelViewSet):
    queryset = Psicologo.objects.all().order_by("id_psicologo")
    serializer_class = PsicologoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["nombre", "apellido", "numero_matricula"]

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all().order_by("id_paciente")
    serializer_class = PacienteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["nombre", "apellido", "numero_celular"]

class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.select_related("paciente", "psicologo").order_by("-fecha_hora")
    serializer_class = CitaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["paciente__nombre","paciente__apellido","psicologo__nombre","psicologo__apellido"]
