from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from dev_sistema_escolar_api.models import EventosAcademicos
from dev_sistema_escolar_api.serializers import EventoAcademicoSerializer


def user_is_admin(user):
    return user.groups.filter(name='administrador').exists()


def user_is_teacher(user):
    return user.groups.filter(name='maestro').exists()


def user_is_student(user):
    return user.groups.filter(name='alumno').exists()


def can_view_event(user, evento):
    if user_is_admin(user):
        return True
    if user_is_teacher(user):
        return any(option in evento.publico_objetivo for option in ['Profesores', 'Publico general'])
    if user_is_student(user):
        return any(option in evento.publico_objetivo for option in ['Estudiantes', 'Publico general'])
    return False


class EventosAcademicosAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        eventos = EventosAcademicos.objects.all().order_by('-fecha_realizacion', 'hora_inicio')

        if user_is_admin(request.user):
            filtered = eventos
        elif user_is_teacher(request.user):
            filtered = eventos.filter(
                Q(publico_objetivo__contains=['Profesores']) |
                Q(publico_objetivo__contains=['Publico general'])
            )
        elif user_is_student(request.user):
            filtered = eventos.filter(
                Q(publico_objetivo__contains=['Estudiantes']) |
                Q(publico_objetivo__contains=['Publico general'])
            )
        else:
            filtered = EventosAcademicos.objects.none()

        serializer = EventoAcademicoSerializer(filtered, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventosAcademicosView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        evento = get_object_or_404(EventosAcademicos, id=request.GET.get("id"))
        if not can_view_event(request.user, evento):
            return Response({"details": "No autorizado para consultar este evento"}, status=status.HTTP_403_FORBIDDEN)
        serializer = EventoAcademicoSerializer(evento)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if not user_is_admin(request.user):
            return Response({"details": "Solo un administrador puede crear eventos."}, status=status.HTTP_403_FORBIDDEN)

        serializer = EventoAcademicoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        if not user_is_admin(request.user):
            return Response({"details": "Solo un administrador puede editar eventos."}, status=status.HTTP_403_FORBIDDEN)

        evento = get_object_or_404(EventosAcademicos, id=request.data.get("id"))
        serializer = EventoAcademicoSerializer(evento, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Evento actualizado correctamente", "evento": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        if not user_is_admin(request.user):
            return Response({"details": "Solo un administrador puede eliminar eventos."}, status=status.HTTP_403_FORBIDDEN)

        evento = get_object_or_404(EventosAcademicos, id=request.GET.get("id"))
        evento.delete()
        return Response({"details": "Evento eliminado"}, status=status.HTTP_200_OK)

