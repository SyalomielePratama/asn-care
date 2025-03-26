from rest_framework import serializers
from .models import Pegawai, Kehadiran

class PegawaiSerializer(serializers.ModelSerializer):
    fotoPegawai = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    link_file_apps_karpeg = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    link_file_apps_npwp = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    link_file_apps_kpe = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    idRefJabatan = serializers.IntegerField(allow_null=True, required=False)
    email = serializers.EmailField(allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = Pegawai
        fields = '__all__'
        read_only_fields = ('id_pegawai',)

    def create(self, validated_data):
        validated_data['fotoPegawai'] = None
        validated_data['link_file_apps_karpeg'] = None
        validated_data['link_file_apps_npwp'] = None
        validated_data['link_file_apps_kpe'] = None
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['fotoPegawai'] = None
        validated_data['link_file_apps_karpeg'] = None
        validated_data['link_file_apps_npwp'] = None
        validated_data['link_file_apps_kpe'] = None
        return super().update(instance, validated_data)

class KehadiranSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kehadiran
        fields = ['id_kehadiran', 'tanggal_apel', 'status_apel', 'keterangan', 'pegawai'] # Tambahkan 'pegawai' ke fields
        read_only_fields = ('id_kehadiran', 'pegawai') # Jadikan 'pegawai' read_only

class KehadiranListSerializer(serializers.ModelSerializer):
    pegawai_nama = serializers.CharField(source='pegawai.namaPegawai', read_only=True)
    class Meta:
        model = Kehadiran
        fields = ['id_kehadiran', 'pegawai', 'pegawai_nama', 'tanggal_apel', 'status_apel', 'keterangan']
        read_only_fields = ('id_kehadiran', 'pegawai', 'pegawai_nama') # Jadikan 'pegawai' dan 'pegawai_nama' read_only