from rest_framework import serializers
from .models import Pegawai, Kehadiran, CutiPNS, CutiPPPK, CutiPPT, CutiESIII

class PegawaiSerializer(serializers.ModelSerializer):
    umur = serializers.IntegerField(read_only=True) # Tambahkan field umur
    fotoPegawai = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    link_file_apps_karpeg = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    link_file_apps_npwp = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    link_file_apps_kpe = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    idRefJabatan = serializers.IntegerField(allow_null=True, required=False)
    email = serializers.EmailField(allow_blank=True, allow_null=True, required=False)
    waktu_kenaikan_pangkat = serializers.SerializerMethodField()
    waktu_kenaikan_gaji = serializers.SerializerMethodField()

    class Meta:
        model = Pegawai
        fields = '__all__'
        read_only_fields = ('id_pegawai','umur', 'waktu_kenaikan_pangkat', 'waktu_kenaikan_gaji')
    
    def get_waktu_kenaikan_pangkat(self, obj):
        return obj.waktu_kenaikan_pangkat()

    def get_waktu_kenaikan_gaji(self, obj):
        return obj.waktu_kenaikan_gaji()

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

class CutiSerializer(serializers.ModelSerializer):
    nama = serializers.CharField(source='nama.namaPegawai', read_only=True)
    nip = serializers.CharField(read_only=True)
    jabatan = serializers.CharField(read_only=True)
    pimpinan_1 = serializers.PrimaryKeyRelatedField(queryset=Pegawai.objects.all(), allow_null=True, required=False, label='Pimpinan 1 (Pilih Nama Pegawai)')
    pimpinan_2 = serializers.PrimaryKeyRelatedField(queryset=Pegawai.objects.all(), allow_null=True, required=False, label='Pimpinan 2 (Pilih Nama Pegawai)')
    pimpinan_3 = serializers.PrimaryKeyRelatedField(queryset=Pegawai.objects.all(), allow_null=True, required=False, label='Pimpinan 3 (Pilih Nama Pegawai)')

    class Meta:
        abstract = True

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['pimpinan_1_nama'] = instance.pimpinan_1.namaPegawai if instance.pimpinan_1 else None
        representation['pimpinan_2_nama'] = instance.pimpinan_2.namaPegawai if instance.pimpinan_2 else None
        representation['pimpinan_3_nama'] = instance.pimpinan_3.namaPegawai if instance.pimpinan_3 else None
        return representation

class CutiPNSSerializer(CutiSerializer):
    class Meta(CutiSerializer.Meta):
        model = CutiPNS
        fields = '__all__'

class CutiPPPKSerializer(CutiSerializer):
    class Meta(CutiSerializer.Meta):
        model = CutiPPPK
        fields = '__all__'

class CutiPPTSerializer(CutiSerializer):
    class Meta(CutiSerializer.Meta):
        model = CutiPPT
        fields = '__all__'

class CutiESIIISerializer(CutiSerializer):
    class Meta(CutiSerializer.Meta):
        model = CutiESIII
        fields = '__all__'