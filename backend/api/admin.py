from django.contrib import admin
from .models import (
    Rol, Usuario, Psicologo, Paciente, Cita, Sesion,
    DiarioEmocional, ControlAcceso, ModeloML, EntrenamientoML,
    CitaSugerida, PLNProceso
    # Si mantuviste Tarea, descomenta:
    # Tarea,
)

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ("id_rol", "nombre", "descripcion")
    search_fields = ("nombre",)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id_usuario", "correo_electronico", "rol")
    search_fields = ("correo_electronico",)
    list_filter = ("rol",)

@admin.register(Psicologo)
class PsicologoAdmin(admin.ModelAdmin):
    list_display = ("id_psicologo", "nombre", "apellido", "numero_matricula", "edad")
    search_fields = ("nombre", "apellido", "numero_matricula")

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("id_paciente", "nombre", "apellido", "psicologo", "prioridad_clinica", "edad")
    search_fields = ("nombre", "apellido")
    list_filter = ("prioridad_clinica",)

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ("id_cita", "paciente", "psicologo", "fecha_hora", "estado")
    list_filter = ("estado", "psicologo")
    search_fields = ("paciente__nombre", "paciente__apellido")

@admin.register(Sesion)
class SesionAdmin(admin.ModelAdmin):
    list_display = ("id_sesion", "cita", "fecha")
    list_filter = ("fecha",)

@admin.register(DiarioEmocional)
class DiarioAdmin(admin.ModelAdmin):
    list_display = ("id_diario", "paciente", "psicologo", "fecha", "titulo_dia")
    list_filter = ("fecha",)
    search_fields = ("paciente__nombre", "paciente__apellido")

@admin.register(ControlAcceso)
class ControlAccesoAdmin(admin.ModelAdmin):
    list_display = ("id_evento", "usuario", "modulo", "accion", "resultado", "fecha_hora")
    list_filter = ("modulo", "accion", "resultado")

@admin.register(ModeloML)
class ModeloMLAdmin(admin.ModelAdmin):
    list_display = ("id_modelo", "nombre", "tipo", "version", "fecha_entrenamiento")

@admin.register(EntrenamientoML)
class EntrenamientoAdmin(admin.ModelAdmin):
    list_display = ("id_entrenamiento", "modelo", "fecha_inicio", "fecha_fin")
    list_filter = ("modelo",)

@admin.register(CitaSugerida)
class CitaSugeridaAdmin(admin.ModelAdmin):
    list_display = ("id_sugerencia", "paciente", "psicologo", "fecha_hora_sugerida", "estado", "score", "orden")
    list_filter = ("estado", "psicologo")

@admin.register(PLNProceso)
class PLNProcesoAdmin(admin.ModelAdmin):
    list_display = ("id_proceso", "sesion", "modelo", "fecha_proceso")

# Si mantuviste Tarea:
# @admin.register(Tarea)
# class TareaAdmin(admin.ModelAdmin):
#     list_display = ("id", "titulo", "hecho")
#     list_editable = ("hecho",)
