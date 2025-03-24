from rest_framework import generics, permissions
from .models import Pegawai, Kehadiran
from .serializers import PegawaiSerializer, KehadiranSerializer, KehadiranListSerializer
from user.permissions import IsSuperUser, IsPegawaiOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class PegawaiListCreateView(generics.ListCreateAPIView):
    queryset = Pegawai.objects.all()
    serializer_class = PegawaiSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]

class PegawaiRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pegawai.objects.all()
    serializer_class = PegawaiSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]
    lookup_field = 'id_pegawai'

class PegawaiProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = PegawaiSerializer
    permission_classes = [IsAuthenticated, IsPegawaiOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_pegawai:
            try:
                pegawai = Pegawai.objects.get(email=user.email)
                return Pegawai.objects.filter(id_pegawai=pegawai.id_pegawai)
            except Pegawai.DoesNotExist:
                raise PermissionDenied("Data pegawai tidak ditemukan untuk akun ini.")
        elif user.is_superuser:
            return Pegawai.objects.all()
        else:
            raise PermissionDenied("Anda tidak memiliki izin untuk mengakses data ini.")

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        if self.request.user.is_pegawai:
            try:
                return queryset.get()
            except Pegawai.DoesNotExist:
                raise PermissionDenied("Data pegawai tidak ditemukan untuk akun ini.")
        return super().get_object()

class KehadiranListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return KehadiranListSerializer
        return KehadiranSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Kehadiran.objects.all()
        elif user.is_pegawai:
            try:
                pegawai = Pegawai.objects.get(email=user.email)
                return Kehadiran.objects.filter(pegawai=pegawai)
            except Pegawai.DoesNotExist:
                return Kehadiran.objects.none()
        return Kehadiran.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_pegawai:
            try:
                pegawai = Pegawai.objects.get(email=user.email)
                serializer.save(pegawai=pegawai)
            except Pegawai.DoesNotExist:
                raise PermissionDenied("Data pegawai tidak ditemukan untuk akun ini.")
        elif user.is_superuser:
            serializer.save()
        else:
            raise PermissionDenied("Anda tidak memiliki izin untuk membuat data kehadiran.")