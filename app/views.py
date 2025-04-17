from rest_framework import generics, permissions, serializers
from .models import Pegawai, Kehadiran, CutiPNS, CutiPPPK, CutiPPT, CutiESIII, JENIS_CUTI_MELAHIRKAN
from .serializers import PegawaiSerializer, KehadiranSerializer, KehadiranListSerializer, CutiPNSSerializer, CutiPPPKSerializer, CutiPPTSerializer, CutiESIIISerializer
from user.permissions import IsSuperUser, IsPegawaiOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
import os
from rest_framework.views import APIView
from rest_framework import status
from dotenv import load_dotenv
from datetime import date, timedelta, timezone
from django.db.models import Sum
from django.db.models.functions import ExtractDay
from django.db import models
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

load_dotenv()
User = get_user_model()

class PegawaiListCreateView(generics.ListCreateAPIView):
    queryset = Pegawai.objects.all()
    serializer_class = PegawaiSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]

    def perform_create(self, serializer):
        instance = serializer.save()
        email_pegawai = instance.email
        if email_pegawai and not User.objects.filter(email=email_pegawai).exists():
            nama_depan = instance.namaPegawai.split(' ')[0].lower()
            username = f"{nama_depan}@{os.environ.get('API_EMAIL').split('@')[1]}"
            password = '123456789'
            user = User.objects.create_user(username=username, email=email_pegawai, password=password, is_pegawai=True)
            user.save()

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
        queryset = Kehadiran.objects.none()
        if user.is_superuser:
            queryset = Kehadiran.objects.all()
        elif user.is_pegawai:
            try:
                pegawai = Pegawai.objects.get(email=user.email)
                queryset = Kehadiran.objects.filter(pegawai=pegawai)
            except Pegawai.DoesNotExist:
                return Kehadiran.objects.none()

        tanggal_mulai = self.request.query_params.get('tanggal_mulai')
        tanggal_akhir = self.request.query_params.get('tanggal_akhir')

        if tanggal_mulai and tanggal_akhir:
            queryset = queryset.filter(tanggal_apel__gte=tanggal_mulai, tanggal_apel__lte=tanggal_akhir)
        elif tanggal_mulai:
            queryset = queryset.filter(tanggal_apel__gte=tanggal_mulai)
        elif tanggal_akhir:
            queryset = queryset.filter(tanggal_apel__lte=tanggal_akhir)

        return queryset

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
        
class CutiCreateListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsPegawaiOrReadOnly]
    model = None # Akan diisi di subclass
    serializer_class = None # Akan diisi di subclass
    jenis_pegawai_allowed = None # Akan diisi di subclass

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            try:
                pegawai = Pegawai.objects.get(email=user.email)
                if self.jenis_pegawai_allowed is not None and pegawai.jenisPegawai not in self.jenis_pegawai_allowed:
                    raise PermissionDenied(f"Anda tidak memiliki izin untuk mengajukan cuti ini. Jenis pegawai Anda adalah {pegawai.jenisPegawai}.")
            except Pegawai.DoesNotExist:
                pass
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            try:
                pegawai = Pegawai.objects.get(email=user.email)
                if self.jenis_pegawai_allowed is not None and pegawai.jenisPegawai not in self.jenis_pegawai_allowed:
                    raise PermissionDenied(f"Anda tidak memiliki izin untuk mengajukan cuti ini. Jenis pegawai Anda adalah {pegawai.jenisPegawai}.")
            except Pegawai.DoesNotExist:
                pass
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        try:
            pegawai = Pegawai.objects.get(email=user.email)
            return self.model.objects.filter(nama=pegawai)
        except Pegawai.DoesNotExist:
            return self.model.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        user = request.user
        try:
            pegawai = Pegawai.objects.get(email=user.email)
            tahun_ini = date.today().year

            total_cuti_diambil = 0
            cuti_tahun_ini = self.model.objects.filter(
                nama=pegawai,
                tanggal_mulai__year=tahun_ini
            )
            for cuti in cuti_tahun_ini:
                lama = (cuti.tanggal_selesai - cuti.tanggal_mulai).days + 1
                total_cuti_diambil += lama

            sisa_cuti = 12 - total_cuti_diambil

            response_data = {
                'total_cuti_diambil': total_cuti_diambil,
                'sisa_cuti': sisa_cuti,
                'results': serializer.data
            }
            return Response(response_data)

        except Pegawai.DoesNotExist:
            return Response({'error': 'Data pegawai tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        user = self.request.user
        try:
            pegawai = Pegawai.objects.get(email=user.email)

            tanggal_mulai = serializer.validated_data.get('tanggal_mulai')
            tanggal_selesai = serializer.validated_data.get('tanggal_selesai')
            jenis_cuti = serializer.validated_data.get('jenis_cuti')

            if tanggal_mulai and tanggal_selesai and jenis_cuti:
                lama_cuti_diajukan = (tanggal_selesai - tanggal_mulai).days + 1
                tahun_pengajuan = tanggal_mulai.year

                total_cuti_diambil_tahun_ini = 0
                cuti_tahun_ini = self.model.objects.filter(
                    nama=pegawai,
                    tanggal_mulai__year=tahun_pengajuan
                )
                for cuti in cuti_tahun_ini:
                    lama = (cuti.tanggal_selesai - cuti.tanggal_mulai).days + 1
                    total_cuti_diambil_tahun_ini += lama

                if jenis_cuti != JENIS_CUTI_MELAHIRKAN:
                    if total_cuti_diambil_tahun_ini + lama_cuti_diajukan > 12:
                        raise serializers.ValidationError(f"Jatah cuti tahunan Anda hanya 12 hari. Anda telah menggunakan {total_cuti_diambil_tahun_ini} hari dan pengajuan cuti ini sebanyak {lama_cuti_diajukan} hari akan melebihi batas.")
                elif jenis_cuti == JENIS_CUTI_MELAHIRKAN:
                    if lama_cuti_diajukan > (3 * 30): # Maksimal 3 bulan (asumsi 1 bulan = 30 hari)
                        raise serializers.ValidationError("Cuti melahirkan tidak boleh lebih dari 3 bulan.")

                serializer.save(nama=pegawai, nip=pegawai.nipBaru, jabatan=pegawai.namaJabatan)

            else:
                raise serializers.ValidationError("Tanggal mulai, tanggal selesai, dan jenis cuti harus diisi.")

        except Pegawai.DoesNotExist:
            raise serializers.ValidationError("Data pegawai tidak ditemukan.")

class CutiPNSCreateListView(CutiCreateListView):
    model = CutiPNS
    serializer_class = CutiPNSSerializer
    jenis_pegawai_allowed = ['PNS']

class CutiPPPKCreateListView(CutiCreateListView):
    model = CutiPPPK
    serializer_class = CutiPPPKSerializer
    jenis_pegawai_allowed = ['PPPK']

class CutiPPTCreateListView(CutiCreateListView):
    model = CutiPPT
    serializer_class = CutiPPTSerializer
    jenis_pegawai_allowed = ['PPT']

class CutiESIIICreateListView(CutiCreateListView):
    model = CutiESIII
    serializer_class = CutiESIIISerializer
    jenis_pegawai_allowed = ['ESIII']

class SisaCutiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            pegawai = Pegawai.objects.get(email=user.email)
            tahun_ini = date.today().year
            jenis_pegawai = pegawai.jenisPegawai

            total_cuti_diambil = 0
            sisa_cuti = 12

            if jenis_pegawai == 'PNS':
                cuti_tahun_ini = CutiPNS.objects.filter(nama=pegawai, tanggal_mulai__year=tahun_ini)
            elif jenis_pegawai == 'PPPK':
                cuti_tahun_ini = CutiPPPK.objects.filter(nama=pegawai, tanggal_mulai__year=tahun_ini)
            elif jenis_pegawai == 'PPT':
                cuti_tahun_ini = CutiPPT.objects.filter(nama=pegawai, tanggal_mulai__year=tahun_ini)
            elif jenis_pegawai == 'ESIII':
                cuti_tahun_ini = CutiESIII.objects.filter(nama=pegawai, tanggal_mulai__year=tahun_ini)
            else:
                return Response({'error': f'Jenis pegawai "{jenis_pegawai}" tidak dikenali.'}, status=status.HTTP_400_BAD_REQUEST)

            for cuti in cuti_tahun_ini:
                lama = (cuti.tanggal_selesai - cuti.tanggal_mulai).days + 1
                total_cuti_diambil += lama

            sisa_cuti -= total_cuti_diambil

            return Response({
                'total_cuti_diambil': total_cuti_diambil,
                'sisa_cuti': sisa_cuti
            })

        except Pegawai.DoesNotExist:
            return Response({'error': 'Data pegawai tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
