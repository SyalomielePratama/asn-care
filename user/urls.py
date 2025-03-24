from django.urls import path
from .views import LoginView, CreatePegawaiUserView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('create-pegawai-user/', CreatePegawaiUserView.as_view(), name='create-pegawai-user'),
]