from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import os
import requests
from dotenv import load_dotenv
from django.contrib.auth import get_user_model
from app.models import Pegawai
from django.utils import timezone
from app.serializers import PegawaiSerializer
import logging
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsSuperUser
from rest_framework import generics
from user.serializers import UserSerializer, ChangePasswordSerializer
from user.permissions import IsSuperUser, IsPegawai

load_dotenv()

User = get_user_model()
logger = logging.getLogger(__name__)

class LoginView(APIView):
    def post(self, request):
        email = os.environ.get('API_EMAIL')
        password = os.environ.get('API_PASSWORD')
        login_url = os.environ.get('API_LOGIN_URL')
        payload = {"email": email, "password": password}

        try:
            response = requests.post(login_url, json=payload, verify=False)
            response.raise_for_status()
            data = response.json()
            token = data.get('token')
            if token:
                return Response({'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Token tidak ditemukan'}, status=status.HTTP_401_UNAUTHORIZED)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Gagal menghubungi API login: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CreatePegawaiUserSerializer(serializers.Serializer):
    email = serializers.EmailField()

class CreatePegawaiUserView(APIView):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def post(self, request):
        serializer = CreatePegawaiUserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if User.objects.filter(email=email).exists():
                return Response({'error': 'User dengan email ini sudah terdaftar.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                pegawai = Pegawai.objects.get(email=email)
                nama_depan = pegawai.namaPegawai.split(' ')[0].lower()
                username = f"{nama_depan}@{email.split('@')[1]}"
                password = '123456789'
                user = User.objects.create_user(username=username, email=email, password=password, is_pegawai=True)
                return Response({'message': f'User pegawai dengan username "{username}" berhasil dibuat.'}, status=status.HTTP_201_CREATED)
            except Pegawai.DoesNotExist:
                return Response({'error': 'Data pegawai dengan email ini tidak ditemukan.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]
    lookup_field = 'id'

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, IsPegawai] # Hanya pegawai yang bisa mengakses

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response({'error': 'Password lama salah.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password berhasil diubah.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)