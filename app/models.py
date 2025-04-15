from django.db import models
from django.utils import timezone
from PIL import Image
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from datetime import date

User = get_user_model()

JENIS_CUTI_TAHUNAN = 'tahunan'
JENIS_CUTI_SAKIT = 'sakit'
JENIS_CUTI_BESAR = 'besar'
JENIS_CUTI_MELAHIRKAN = 'melahirkan'
JENIS_CUTI_ALASAN_PENTING = 'penting'
JENIS_CUTI_DILUAR_TANGGUNGAN = 'diluar'

JENIS_CUTI_CHOICES = [
    (JENIS_CUTI_TAHUNAN, 'Cuti Tahunan'),
    (JENIS_CUTI_SAKIT, 'Cuti Sakit'),
    (JENIS_CUTI_BESAR, 'Cuti Besar'),
    (JENIS_CUTI_MELAHIRKAN, 'Cuti Melahirkan'),
    (JENIS_CUTI_ALASAN_PENTING, 'Cuti Alasan Penting'),
    (JENIS_CUTI_DILUAR_TANGGUNGAN, 'Cuti Diluar Tanggungan Negara'),
]

class Pegawai(models.Model):
    id_pegawai = models.AutoField(primary_key=True) # ID baru untuk database
    idtbPegawai = models.IntegerField(null=True, blank=True)
    nipLama = models.CharField(max_length=255, null=True, blank=True)
    nipBaru = models.CharField(max_length=255, null=True, blank=True)
    namaPegawai = models.CharField(max_length=255, null=True, blank=True)
    gelarDepan = models.CharField(max_length=255, null=True, blank=True)
    gelarBelakang = models.CharField(max_length=255, null=True, blank=True)
    tempatLahir = models.CharField(max_length=255, null=True, blank=True)
    tanggalLahir = models.DateField(null=True, blank=True)
    agama = models.CharField(max_length=255, null=True, blank=True)
    jenisKelamin = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    NIK = models.CharField(max_length=255, null=True, blank=True)
    alamat = models.TextField(null=True, blank=True)
    telepon = models.CharField(max_length=255, null=True, blank=True)
    statusPernikahan = models.CharField(max_length=255, null=True, blank=True)
    kedudukanHukum = models.CharField(max_length=255, null=True, blank=True)
    jenisPegawai = models.CharField(max_length=255, null=True, blank=True)
    nomorKarpeg = models.CharField(max_length=255, null=True, blank=True)
    nomorNPWP = models.CharField(max_length=255, null=True, blank=True)
    nomorKPE = models.CharField(max_length=255, null=True, blank=True)
    fotoPegawai = models.ImageField(upload_to='foto_pegawai/', blank=True, null=True)
    idelektronik = models.CharField(max_length=255, null=True, blank=True)
    shift = models.CharField(max_length=255, null=True, blank=True)
    skpd = models.CharField(max_length=255, null=True, blank=True)
    flagStatus = models.IntegerField(null=True, blank=True)
    link_file_apps_karpeg = models.ImageField(upload_to='karpeg/', blank=True, null=True)
    format_karpeg = models.CharField(max_length=255, null=True, blank=True)
    ukuran_karpeg = models.IntegerField(null=True, blank=True)
    link_file_apps_npwp = models.ImageField(upload_to='npwp/', blank=True, null=True)
    format_npwp = models.CharField(max_length=255, null=True, blank=True)
    ukuran_npwp = models.IntegerField(null=True, blank=True)
    link_file_apps_kpe = models.ImageField(upload_to='kpe/', blank=True, null=True)
    format_kpe = models.CharField(max_length=255, null=True, blank=True)
    ukuran_kpe = models.IntegerField(null=True, blank=True)
    barcode_karpeg = models.CharField(max_length=255, null=True, blank=True)
    barcode_npwp = models.CharField(max_length=255, null=True, blank=True)
    barcode_kpe = models.CharField(max_length=255, null=True, blank=True)
    levelAksesId = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    kodepos = models.CharField(max_length=255, null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    idtbRwJabatan = models.IntegerField(null=True, blank=True)
    jenisJabatan = models.CharField(max_length=255, null=True, blank=True)
    instansiInduk = models.CharField(max_length=255, null=True, blank=True)
    instansiKerja = models.CharField(max_length=255, null=True, blank=True)
    unorInduk = models.CharField(max_length=255, null=True, blank=True)
    kodeUnor = models.CharField(max_length=255, null=True, blank=True)
    unorJabatan = models.CharField(max_length=255, null=True, blank=True)
    jenisKategori = models.CharField(max_length=255, null=True, blank=True)
    eselonJabatan = models.CharField(max_length=255, null=True, blank=True)
    idRefJabatan = models.IntegerField(null=True, blank=True)
    namaJabatan = models.CharField(max_length=255, null=True, blank=True)
    tmtJabatan = models.DateField(null=True, blank=True)
    nomorSkJabatan = models.CharField(max_length=255, null=True, blank=True)
    tanggalSkJabatan = models.DateField(null=True, blank=True)
    idRwJabatanSapk = models.IntegerField(null=True, blank=True)
    kodenamaJabatan = models.CharField(max_length=255, null=True, blank=True)
    namaEselon = models.CharField(max_length=255, null=True, blank=True)
    namaUnor = models.CharField(max_length=255, null=True, blank=True)
    idtbRwPendidikan = models.IntegerField(null=True, blank=True)
    tingkatPendidikan = models.CharField(max_length=255, null=True, blank=True)
    programStudi = models.CharField(max_length=255, null=True, blank=True)
    nomorIjazah = models.CharField(max_length=255, null=True, blank=True)
    tanggalIjazah = models.DateField(null=True, blank=True)
    namaLembaga = models.CharField(max_length=255, null=True, blank=True)
    statusPengangkatan = models.CharField(max_length=255, null=True, blank=True)
    namaTkPendidikan = models.CharField(max_length=255, null=True, blank=True)
    idtbRef_tkPendidikan = models.IntegerField(null=True, blank=True)
    idtbRwPangkat = models.IntegerField(null=True, blank=True)
    namaPangkat = models.CharField(max_length=255, null=True, blank=True)
    golonganPangkat = models.CharField(max_length=255, null=True, blank=True)
    mkgTahunPangkat = models.CharField(max_length=255, null=True, blank=True)
    mkgBulanPangkat = models.CharField(max_length=255, null=True, blank=True)
    nomorSkPangkat = models.CharField(max_length=255, null=True, blank=True)
    tanggalSkPangkat = models.DateField(null=True, blank=True)
    tmtPangkat = models.DateField(null=True, blank=True)
    nomorBknPangkat = models.CharField(max_length=255, null=True, blank=True)
    tanggalBknPangkat = models.DateField(null=True, blank=True)
    jenisKenaikanPangkat = models.CharField(max_length=255, null=True, blank=True)
    jumlahAngkaKredit = models.CharField(max_length=255, null=True, blank=True)
    idtbRwDiklat = models.IntegerField(null=True, blank=True)
    jenisDiklat = models.CharField(max_length=255, null=True, blank=True)
    tingkatanDiklat = models.CharField(max_length=255, null=True, blank=True)
    namaDiklat = models.CharField(max_length=255, null=True, blank=True)
    jumlahJam = models.CharField(max_length=255, null=True, blank=True)
    tanggalDiklat = models.CharField(max_length=255, null=True, blank=True)
    tahunDiklat = models.CharField(max_length=255, null=True, blank=True)
    nomorSertifikat = models.CharField(max_length=255, null=True, blank=True)
    instansiDiklat = models.CharField(max_length=255, null=True, blank=True)
    institusiPenyelenggara = models.CharField(max_length=255, null=True, blank=True)
    golongan = models.CharField(max_length=255, null=True, blank=True)
    predikat = models.CharField(max_length=255, null=True, blank=True)
    nilaiKinerja = models.CharField(max_length=255, null=True, blank=True)
    tahunLaporanSkp = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Tanggal pembuatan akun

    def __str__(self):
        return self.namaPegawai

    def save(self, *args, **kwargs):
        # Set ImageField values to blank (temporary)
        self.fotoPegawai = None
        super().save(*args, **kwargs)

    #Untuk Perhitungan Umur Pegawai
    @property
    def umur(self):
        if self.tanggalLahir:
            today = date.today()
            birth_date = self.tanggalLahir
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        return None
    
    def waktu_kenaikan_pangkat(self):
        if self.created_at:
            tahun_sekarang = date.today().year
            tahun_terakhir_kenaikan_pangkat = self.created_at.year + 4 * ((tahun_sekarang - self.created_at.year) // 4 + 1)
            selisih_tahun = tahun_terakhir_kenaikan_pangkat - tahun_sekarang
            
            # Hitung bulan
            bulan_sekarang = date.today().month
            bulan_kenaikan_pangkat = (bulan_sekarang + 12 * (selisih_tahun)) % 12
            
            if selisih_tahun == 0 and bulan_kenaikan_pangkat == 0:
                return 0, 0  # Kenaikan pangkat sekarang
            return selisih_tahun, bulan_kenaikan_pangkat  # Mengembalikan tahun dan bulan
        return None

    def waktu_kenaikan_gaji(self):
        if self.created_at:
            tahun_sekarang = date.today().year
            tahun_terakhir_kenaikan_gaji = self.created_at.year + 2 * ((tahun_sekarang - self.created_at.year) // 2 + 1)
            selisih_tahun = tahun_terakhir_kenaikan_gaji - tahun_sekarang
            
            # Hitung bulan
            bulan_sekarang = date.today().month
            bulan_kenaikan_gaji = (bulan_sekarang + 12 * (selisih_tahun)) % 12
            
            if selisih_tahun == 0 and bulan_kenaikan_gaji == 0:
                return 0, 0  # Kenaikan gaji sekarang
            return selisih_tahun, bulan_kenaikan_gaji  # Mengembalikan tahun dan bulan
        return None

@receiver(pre_save, sender=Pegawai)
def update_pegawai_user_email(sender, instance, **kwargs):
    try:
        old_pegawai = Pegawai.objects.get(pk=instance.pk)
        if old_pegawai.email != instance.email and instance.email:
            try:
                user = User.objects.get(email=old_pegawai.email)
                if user.is_pegawai:
                    user.email = instance.email
                    user.save()
            except User.DoesNotExist:
                pass
    except Pegawai.DoesNotExist:
        # Ini terjadi saat instance baru pertama kali dibuat, kita tidak perlu melakukan apa-apa
        pass

@receiver(post_delete, sender=Pegawai)
def delete_pegawai_user(sender, instance, **kwargs):
    try:
        user = User.objects.get(email=instance.email)
        user.delete()
    except User.DoesNotExist:
        pass

class Kehadiran(models.Model):
    id_kehadiran = models.AutoField(primary_key=True)
    pegawai = models.ForeignKey(Pegawai, on_delete=models.CASCADE)
    tanggal_apel = models.DateField()
    STATUS_CHOICES = [
        ('hadir', 'Hadir'),
        ('izin', 'Izin'),
        ('sakit', 'Sakit'),
    ]
    status_apel = models.CharField(max_length=10, choices=STATUS_CHOICES)
    keterangan = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('pegawai', 'tanggal_apel') # Satu pegawai hanya bisa satu catatan kehadiran per hari

    def __str__(self):
        return f"{self.pegawai.namaPegawai} - {self.tanggal_apel}"
    
class CutiBase(models.Model):
    nama = models.ForeignKey('Pegawai', on_delete=models.CASCADE, related_name='%(class)s_requests')
    nip = models.CharField(max_length=255, blank=True, null=True)
    jabatan = models.CharField(max_length=255, blank=True, null=True)
    masa_jabatan_tahun = models.IntegerField()
    masa_jabatan_bulan = models.IntegerField()
    jenis_cuti = models.CharField(max_length=20, choices=JENIS_CUTI_CHOICES)
    alasan_cuti = models.TextField()
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField()
    alamat_cuti = models.TextField()
    telepon = models.CharField(max_length=255)
    pimpinan_1 = models.ForeignKey('Pegawai', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_dipimpin_1')
    pimpinan_2 = models.ForeignKey('Pegawai', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_dipimpin_2')
    pimpinan_3 = models.ForeignKey('Pegawai', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_dipimpin_3')
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class CutiPNS(CutiBase):
    pass

class CutiPPPK(CutiBase):
    pass

class CutiPPT(CutiBase):
    pass

class CutiESIII(CutiBase):
    pass