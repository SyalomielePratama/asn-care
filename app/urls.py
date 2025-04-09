from django.urls import path
from .views import (
    PegawaiListCreateView,
    PegawaiRetrieveUpdateDestroyView,
    KehadiranListCreateView,
    PegawaiProfileRetrieveUpdateView,
    CutiPNSCreateListView,
    CutiPPPKCreateListView,
    CutiPPTCreateListView,
    CutiESIIICreateListView,
    
)

urlpatterns = [
    path('pegawai/', PegawaiListCreateView.as_view(), name='pegawai-list-create'),
    path('pegawai/<int:id_pegawai>/', PegawaiRetrieveUpdateDestroyView.as_view(), name='pegawai-retrieve-update-destroy'),
    path('pegawai/profile/', PegawaiProfileRetrieveUpdateView.as_view(), name='pegawai-profile'),
    path('kehadiran/', KehadiranListCreateView.as_view(), name='kehadiran-list-create'),
    path('cuti/pns/', CutiPNSCreateListView.as_view(), name='cuti-pns-list-create'),
    path('cuti/pppk/', CutiPPPKCreateListView.as_view(), name='cuti-pppk-list-create'),
    path('cuti/ppt/', CutiPPTCreateListView.as_view(), name='cuti-ppt-list-create'),
    path('cuti/esiii/', CutiESIIICreateListView.as_view(), name='cuti-esiii-list-create'),
]