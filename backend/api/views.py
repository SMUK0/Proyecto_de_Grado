from django.shortcuts import render
from rest_framework import viewsets
from .models import Tarea
from .serializers import TareaSerializer

# PAGINA DE INICIO ( INDEX)
from rest_framework.decorators import api_view
from rest_framework.response import Response
###############################################

class TareaViewSet(viewsets.ModelViewSet):
    queryset         = Tarea.objects.all().order_by("-id")
    serializer_class = TareaSerializer


# PAGINA DE INICIO ( INDEX)
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def home_info(request):
    data = {
        "brand": "Resoluciones Integrales",
        "tagline": "Servicios de intervención terapéutica integral multidisciplinaria y personalizada.",
        "about": (
            "Somos un consultorio que brinda intervención terapéutica integral y personalizada. "
            "Contáctanos para recibir apoyo profesional."
        ),
        "services": [
            {
                "name": "Apoyo terapéutico por adicciones",
                "description": "Acompañamiento clínico y psicoeducativo orientado a la recuperación.",
                "slug": "adicciones"
            },
            {
                "name": "Intervención terapéutica integral",
                "description": "Atención multidisciplinaria centrada en la persona.",
                "slug": "intervencion-integral"
            }
        ],
        "contact": {
            "whatsapp": "https://walink.co/e3e2a6"
        },
        "social": {
            "facebook": "https://www.facebook.com/resolucionesintegrales?locale=es_LA",
            "instagram": "https://www.instagram.com/resolucionesintegrales/?hl=es-la"
        }
    }
    return Response(data)
