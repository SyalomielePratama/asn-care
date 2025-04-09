from django.contrib import admin
from .models import Pegawai, Kehadiran, CutiPNS, CutiPPPK, CutiPPT, CutiESIII

@admin.register(Pegawai)
class PegawaiAdmin(admin.ModelAdmin):
    list_display = ('id_pegawai', 'namaPegawai', 'nipBaru', 'email', 'instansiKerja')
    search_fields = ('namaPegawai', 'nipBaru', 'email')
    list_filter = ('instansiKerja', 'jenisPegawai')
    readonly_fields = ('id_pegawai',) # ID baru bersifat read-only di admin

@admin.register(Kehadiran)
class KehadiranAdmin(admin.ModelAdmin):
    list_display = ('id_kehadiran', 'pegawai', 'tanggal_apel', 'status_apel')
    search_fields = ('pegawai__namaPegawai', 'tanggal_apel')
    list_filter = ('status_apel',)
    readonly_fields = ('id_kehadiran',) # ID baru bersifat read-only di admin

@admin.register(CutiPNS)
class CutiPNSAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nip', 'jenis_cuti', 'tanggal_mulai', 'tanggal_selesai', 'tanggal_dibuat')
    search_fields = ('nama__namaPegawai', 'nip')
    list_filter = ('jenis_cuti', 'tanggal_mulai', 'tanggal_dibuat')

@admin.register(CutiPPPK)
class CutiPPPKAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nip', 'jenis_cuti', 'tanggal_mulai', 'tanggal_selesai', 'tanggal_dibuat')
    search_fields = ('nama__namaPegawai', 'nip')
    list_filter = ('jenis_cuti', 'tanggal_mulai', 'tanggal_dibuat')

@admin.register(CutiPPT)
class CutiPPTAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nip', 'jenis_cuti', 'tanggal_mulai', 'tanggal_selesai', 'tanggal_dibuat')
    search_fields = ('nama__namaPegawai', 'nip')
    list_filter = ('jenis_cuti', 'tanggal_mulai', 'tanggal_dibuat')

@admin.register(CutiESIII)
class CutiESIIIAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nip', 'jenis_cuti', 'tanggal_mulai', 'tanggal_selesai', 'tanggal_dibuat')
    search_fields = ('nama__namaPegawai', 'nip')
    list_filter = ('jenis_cuti', 'tanggal_mulai', 'tanggal_dibuat')