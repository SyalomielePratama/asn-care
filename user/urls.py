from django.urls import path
from .views import LoginView, CreatePegawaiUserView, UserListView, UserDeleteView, ChangePasswordView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('create-pegawai-user/', CreatePegawaiUserView.as_view(), name='create-pegawai-user'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:id>/', UserDeleteView.as_view(), name='user-delete'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'), # Tambahkan path ini
]