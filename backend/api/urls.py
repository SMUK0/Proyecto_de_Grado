# backend/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import home_info, me, PsicologoViewSet, PacienteViewSet, CitaViewSet

router = DefaultRouter()
router.register(r"psicologos", PsicologoViewSet, basename="psicologo")
router.register(r"pacientes", PacienteViewSet, basename="paciente")
router.register(r"citas", CitaViewSet, basename="cita")

urlpatterns = [
    path("", include(router.urls)),

    # Inicio (JSON para el Home del frontend)
    path("home/", home_info, name="home-info"),

    # Auth (JWT)
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me/", me, name="auth-me"),
]
