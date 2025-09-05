# backend/api/models.py
from datetime import date
from django.db import models


# ------------ Núcleo (usuarios/roles) ------------
class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=55, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "roles"
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    correo_electronico = models.EmailField(max_length=255, unique=True)
    contrasena = models.CharField(max_length=255)
    rol = models.ForeignKey(
        Rol, on_delete=models.PROTECT, db_column="id_rol", related_name="usuarios"
    )

    class Meta:
        db_table = "usuarios"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.correo_electronico


# ------------ Personal de salud ------------
class Psicologo(models.Model):
    id_psicologo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    # se autocalcula en save()
    edad = models.PositiveSmallIntegerField(blank=True, null=True, editable=False)
    numero_matricula = models.CharField(max_length=50, unique=True)
    direccion = models.TextField(blank=True, null=True)
    numero_contacto = models.CharField(max_length=20, blank=True, null=True)
    correo_electronico = models.EmailField(max_length=255, blank=True, null=True)
    lugar_expedicion_certificado = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "psicologos"
        verbose_name = "Psicólogo"
        verbose_name_plural = "Psicólogos"

    def __str__(self):
        return f"{self.nombre} {self.apellido}".strip()

    def save(self, *args, **kwargs):
        if self.fecha_nacimiento:
            hoy = date.today()
            self.edad = (
                hoy.year
                - self.fecha_nacimiento.year
                - ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
            )
        super().save(*args, **kwargs)


# ------------ Pacientes ------------
class Paciente(models.Model):
    PRIORIDAD = (("alto", "Alto"), ("medio", "Medio"), ("bajo", "Bajo"))

    id_paciente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    numero_celular = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    edad = models.PositiveSmallIntegerField(blank=True, null=True, editable=False)
    trastorno_salud_mental = models.TextField(blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)
    prioridad_clinica = models.CharField(max_length=10, choices=PRIORIDAD, default="medio")
    psicologo = models.ForeignKey(
        Psicologo, on_delete=models.SET_NULL, null=True, db_column="id_psicologo", related_name="pacientes"
    )
    usuario = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, db_column="id_usuario", related_name="pacientes"
    )

    class Meta:
        db_table = "pacientes"
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return f"{self.nombre} {self.apellido}".strip()

    def save(self, *args, **kwargs):
        if self.fecha_nacimiento:
            hoy = date.today()
            self.edad = (
                hoy.year
                - self.fecha_nacimiento.year
                - ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
            )
        super().save(*args, **kwargs)


# ------------ Citas ------------
class Cita(models.Model):
    ESTADO = (("pendiente", "Pendiente"), ("completada", "Completada"), ("cancelada", "Cancelada"))

    id_cita = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, db_column="id_paciente", related_name="citas"
    )
    psicologo = models.ForeignKey(
        Psicologo, on_delete=models.CASCADE, db_column="id_psicologo", related_name="citas"
    )
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=50, choices=ESTADO, default="pendiente")
    motivo = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "citas"
        ordering = ("-fecha_hora",)
        indexes = [models.Index(fields=["fecha_hora"])]

    def __str__(self):
        return f"Cita #{self.id_cita} - {self.paciente} con {self.psicologo}"


# ------------ Sesiones ------------
class Sesion(models.Model):
    id_sesion = models.AutoField(primary_key=True)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, db_column="id_cita", related_name="sesiones")
    fecha = models.DateField(blank=True, null=True)
    grabacion_audio = models.BinaryField(blank=True, null=True)
    transcripcion = models.TextField(blank=True, null=True)
    resumen = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "sesiones"
        ordering = ("-fecha",)

    def __str__(self):
        return f"Sesión #{self.id_sesion} de {self.cita}"

    def save(self, *args, **kwargs):
        if not self.fecha and self.cita and self.cita.fecha_hora:
            self.fecha = self.cita.fecha_hora.date()
        super().save(*args, **kwargs)


# ------------ Diario emocional ------------
class DiarioEmocional(models.Model):
    id_diario = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, db_column="id_paciente", related_name="diarios"
    )
    psicologo = models.ForeignKey(
        Psicologo, on_delete=models.SET_NULL, null=True, db_column="id_psicologo", related_name="diarios"
    )
    descripcion = models.TextField()
    titulo_dia = models.CharField(max_length=55, blank=True, null=True)
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "diario_emocional"
        ordering = ("-fecha",)

    def __str__(self):
        return f"Diario {self.id_diario} - {self.paciente}"


# ------------ Auditoría / control de acceso ------------
class ControlAcceso(models.Model):
    id_evento = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, db_column="id_usuario", related_name="eventos_acceso"
    )
    fecha_hora = models.DateTimeField(auto_now_add=True)
    modulo = models.CharField(max_length=100)
    accion = models.CharField(max_length=30)
    resultado = models.BooleanField(default=True)

    class Meta:
        db_table = "control_acceso"
        verbose_name = "Control de acceso"
        verbose_name_plural = "Control de acceso"
        ordering = ("-fecha_hora",)

    def __str__(self):
        return f"{self.fecha_hora} {self.usuario} {self.modulo}:{self.accion} ({self.resultado})"


# ------------ Modelos de ML / Entrenamientos ------------
class ModeloML(models.Model):
    TIPOS = (("random_forest", "Random Forest"), ("pln", "PLN"))

    id_modelo = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=30, choices=TIPOS)
    nombre = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    fecha_entrenamiento = models.DateTimeField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    tamano_bytes = models.BigIntegerField(blank=True, null=True)
    formato = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "modelos_ml"

    def __str__(self):
        return f"{self.nombre} ({self.version})"


class EntrenamientoML(models.Model):
    id_entrenamiento = models.AutoField(primary_key=True)
    modelo = models.ForeignKey(
        ModeloML, on_delete=models.CASCADE, db_column="id_modelo", related_name="entrenamientos"
    )
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    dataset = models.CharField(max_length=255)
    hiperparametros = models.JSONField(blank=True, null=True)
    metricas = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "entrenamientos_ml"
        ordering = ("-fecha_inicio",)

    def __str__(self):
        return f"Entrenamiento #{self.id_entrenamiento} - {self.modelo}"


# ------------ Sugerencias de citas (Random Forest) ------------
class CitaSugerida(models.Model):
    ESTADO = (("pendiente", "Pendiente"), ("aceptada", "Aceptada"), ("rechazada", "Rechazada"))

    id_sugerencia = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, db_column="id_paciente", related_name="sugerencias"
    )
    psicologo = models.ForeignKey(
        Psicologo, on_delete=models.CASCADE, db_column="id_psicologo", related_name="sugerencias"
    )
    fecha_hora_sugerida = models.DateTimeField(blank=True, null=True)
    score = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    orden = models.PositiveIntegerField(default=0)
    origen = models.CharField(max_length=30, default="random_forest")
    estado = models.CharField(max_length=20, choices=ESTADO, default="pendiente")
    modelo = models.ForeignKey(
        ModeloML, on_delete=models.SET_NULL, null=True, db_column="id_modelo", related_name="sugerencias"
    )
    cita_aceptada = models.ForeignKey(
        "Cita",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="id_cita_aceptada",
        related_name="sugerencias_asociadas",
    )
    features = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "citas_sugeridas"
        ordering = ("orden",)

    def __str__(self):
        return f"Sugerencia #{self.id_sugerencia} - {self.paciente}"


# ------------ Procesos PLN por sesión ------------
class PLNProceso(models.Model):
    id_proceso = models.AutoField(primary_key=True)
    sesion = models.ForeignKey(
        Sesion, on_delete=models.CASCADE, db_column="id_sesion", related_name="pln_procesos"
    )
    modelo = models.ForeignKey(
        ModeloML, on_delete=models.SET_NULL, null=True, db_column="id_modelo", related_name="pln_procesos"
    )
    fecha_proceso = models.DateTimeField(auto_now_add=True)
    resumen_generado = models.TextField(blank=True, null=True)
    calidad = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True)

    class Meta:
        db_table = "pln_procesos"
    def __str__(self):
        return f"PLN {self.id_proceso} (sesión {self.sesion_id})"
