from django.urls import path
from .views import (
    PegawaiListCreateView,
    PegawaiRetrieveUpdateDestroyView,
    KehadiranListCreateView,
    PegawaiProfileRetrieveUpdateView,
)

urlpatterns = [
    path('pegawai/', PegawaiListCreateView.as_view(), name='pegawai-list-create'),
    path('pegawai/<int:id_pegawai>/', PegawaiRetrieveUpdateDestroyView.as_view(), name='pegawai-retrieve-update-destroy'),
    path('pegawai/profile/', PegawaiProfileRetrieveUpdateView.as_view(), name='pegawai-profile'),
    path('kehadiran/', KehadiranListCreateView.as_view(), name='kehadiran-list-create'),
]