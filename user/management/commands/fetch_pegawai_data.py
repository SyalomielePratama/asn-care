import os
import requests
import urllib3
import re
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from django.contrib.auth import get_user_model
from app.models import Pegawai
from app.serializers import PegawaiSerializer
from django.utils import timezone

# Menonaktifkan peringatan InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

User  = get_user_model()

def is_valid_email(email):
    """Fungsi untuk memvalidasi format email."""
    if email is None:
        return False
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

class Command(BaseCommand):
    help = 'Mengambil dan menyimpan data pegawai dari API eksternal'

    def handle(self, *args, **options):
        email = os.environ.get('API_EMAIL')
        password = os.environ.get('API_PASSWORD')
        login_url = os.environ.get('API_LOGIN_URL')
        get_pegawai_url = os.environ.get('API_GET_PEGAWAI_URL')
        kode_unor = "651301400"   # Kode Unor yang ingin diambil datanya
        payload = {"email": email, "password": password}

        self.stdout.write(self.style.SUCCESS('Mencoba login ke API...'))
        try:
            login_response = requests.post(login_url, json=payload, verify=False)
            login_response.raise_for_status()
            login_data = login_response.json()
            token = login_data.get('token')
            if not token:
                self.stderr.write(self.style.ERROR('Token tidak ditemukan dari API login.'))
                return
            self.stdout.write(self.style.SUCCESS(f'Berhasil mendapatkan token: {token}'))

            headers = {'Authorization': f'Bearer {token}'}
            url = f"{get_pegawai_url}{kode_unor}"

            self.stdout.write(self.style.SUCCESS(f'Mengambil data pegawai dari URL: {url}'))
            pegawai_response = requests.get(url, headers=headers, verify=False)
            pegawai_response.raise_for_status()
            pegawai_data = pegawai_response.json()
            pegawai_list = pegawai_data.get('data',)

            created_count = 0
            updated_count = 0

            for pegawai_record in pegawai_list:
                # Bersihkan data tanggal jika formatnya '0000-00-00'
                for key, value in pegawai_record.items():
                    if isinstance(value, str) and value == '0000-00-00':
                        pegawai_record[key] = None

                nip_baru = pegawai_record.get('nipBaru')
                if nip_baru:
                    try:
                        pegawai_instance = Pegawai.objects.get(nipBaru=nip_baru)
                        # Update data yang ada
                        for key, value in pegawai_record.items():
                            if key not in ['idtbPegawai', 'created_at', 'id_pegawai']:   # Jangan update ID eksternal, waktu pembuatan, dan ID internal
                                setattr(pegawai_instance, key, value)
                        pegawai_instance.updated_at = timezone.now()
                        pegawai_instance.save()
                        updated_count += 1
                    except Pegawai.DoesNotExist:
                        # Validasi idRefJabatan
                        if 'idRefJabatan' in pegawai_record and not isinstance(pegawai_record['idRefJabatan'], (int, type(None))):
                            pegawai_record['idRefJabatan'] = None  # Atau nilai default yang sesuai

                        # Validasi dan pembuatan email otomatis jika tidak valid atau tidak ada
                        email_pegawai = pegawai_record.get('email')
                        if not is_valid_email(email_pegawai):
                            nama_depan = pegawai_record.get('namaPegawai', '').split(' ')[0].lower()
                            email_domain = "jwt.id"
                            email_pegawai = f"{nama_depan}@{email_domain}"
                            pegawai_record['email'] = email_pegawai

                        # Buat pegawai baru
                        serializer = PegawaiSerializer(data=pegawai_record)
                        if serializer.is_valid():
                            serializer.save()
                            created_count += 1

                            # Buat user pegawai jika belum ada
                            nama_depan = pegawai_record.get('namaPegawai', '').split(' ')[0].lower()
                            email_domain = "jwt.id"
                            username = f"{nama_depan}@{email_domain}"

                            if email_pegawai and not User.objects.filter(email=email_pegawai).exists():
                                user = User.objects.create_user(
                                    username=username,
                                    email=email_pegawai,
                                    password='123456789',
                                    is_pegawai=True
                                )
                                user.save()
                        else:
                            self.stderr.write(self.style.ERROR(f'Validasi serializer gagal untuk pegawai dengan nipBaru {nip_baru}: {serializer.errors}'))

            self.stdout.write(self.style.SUCCESS(
                f'Berhasil menambahkan {created_count} pegawai baru dan memperbarui {updated_count} pegawai.'
            ))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Gagal menghubungi API: {e}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Terjadi kesalahan: {e}'))