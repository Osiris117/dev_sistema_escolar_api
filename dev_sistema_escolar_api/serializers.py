from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from dev_sistema_escolar_api.models import *
import re

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Administradores
        fields = '__all__'
        
class AlumnoSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Alumnos
        fields = "__all__"

class MaestroSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Maestros
        fields = '__all__'

class EventoAcademicoSerializer(serializers.ModelSerializer):
    PUBLICO_OPCIONES = ["Estudiantes", "Profesores", "Publico general"]
    PROGRAMAS_FCC = [
        "Ingeniería en Ciencias de la Computación",
        "Licenciatura en Ciencias de la Computación",
        "Ingeniería en Tecnologías de la Información"
    ]

    responsable_info = UserSerializer(source='responsable', read_only=True)
    publico_objetivo = serializers.ListField(
        child=serializers.ChoiceField(choices=PUBLICO_OPCIONES),
        allow_empty=False
    )
    fecha_realizacion = serializers.DateField(input_formats=['%Y-%m-%d', '%d/%m/%Y'])
    hora_inicio = serializers.TimeField(format='%H:%M', input_formats=['%H:%M'])
    hora_fin = serializers.TimeField(format='%H:%M', input_formats=['%H:%M'])
    responsable = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name__in=['maestro', 'administrador']).distinct()
    )

    class Meta:
        model = EventosAcademicos
        fields = [
            'id',
            'nombre_evento',
            'tipo_evento',
            'fecha_realizacion',
            'hora_inicio',
            'hora_fin',
            'lugar',
            'publico_objetivo',
            'programa_educativo',
            'responsable',
            'responsable_info',
            'descripcion_breve',
            'cupo_maximo',
            'creation',
            'update'
        ]
        read_only_fields = ('creation', 'update', 'responsable_info')

    def validate_nombre_evento(self, value):
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$', value):
            raise serializers.ValidationError("El nombre solo permite letras, números y espacios.")
        return value

    def validate_lugar(self, value):
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$', value):
            raise serializers.ValidationError("El lugar solo permite caracteres alfanuméricos y espacios.")
        return value

    def validate_descripcion_breve(self, value):
        if len(value) > 300:
            raise serializers.ValidationError("La descripción no debe exceder 300 caracteres.")
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ,.;:()¡!¿?"\'-]+$', value):
            raise serializers.ValidationError("La descripción solo permite signos de puntuación básicos.")
        return value

    def validate_cupo_maximo(self, value):
        if value <= 0 or value > 999:
            raise serializers.ValidationError("El cupo máximo debe ser un número positivo de hasta 3 dígitos.")
        return value

    def validate(self, attrs):
        instance = getattr(self, 'instance', None)
        fecha = attrs.get('fecha_realizacion') or (instance.fecha_realizacion if instance else None)
        hora_inicio = attrs.get('hora_inicio') or (instance.hora_inicio if instance else None)
        hora_fin = attrs.get('hora_fin') or (instance.hora_fin if instance else None)
        publico = attrs.get('publico_objetivo') or (instance.publico_objetivo if instance else [])
        programa = attrs.get('programa_educativo') or (instance.programa_educativo if instance else None)
        programa = programa or None

        if fecha and fecha < timezone.localdate():
            raise serializers.ValidationError({"fecha_realizacion": "La fecha no puede ser anterior al día actual."})

        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise serializers.ValidationError({"hora_fin": "La hora de finalización debe ser mayor a la inicial."})

        if not publico:
            raise serializers.ValidationError({"publico_objetivo": "Debes seleccionar al menos un público objetivo."})

        if "Estudiantes" in publico:
            if not programa:
                raise serializers.ValidationError({"programa_educativo": "Selecciona un programa educativo para estudiantes."})
            if programa not in self.PROGRAMAS_FCC:
                raise serializers.ValidationError({"programa_educativo": "Programa educativo no válido."})
        elif programa:
            raise serializers.ValidationError({"programa_educativo": "El programa educativo solo aplica para estudiantes."})

        return attrs