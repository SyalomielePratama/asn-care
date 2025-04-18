# asnCare API

Dokumentasi untuk penggunaan API `asnCare`. API ini menyediakan fungsionalitas untuk mengelola data pegawai dan kehadiran.

## Daftar Isi

1.  [Prasyarat](#prasyarat)
2.  [Setup](#setup)
3.  [Autentikasi](#autentikasi)
4.  [Endpoint API](#endpoint-api)
    * [Autentikasi Pengguna](#autentikasi-pengguna)
    * [Manajemen Pegawai](#manajemen-pegawai)
    * [Manajemen Kehadiran](#manajemen-kehadiran)
5.  [Format Data](#format-data)
6.  [Penanganan Error](#penanganan-error)
7.  [Konfigurasi CORS](#konfigurasi-cors)
8.  [Catatan Penting](#catatan-penting)

## 1. Prasyarat

Sebelum menggunakan API ini, pastikan Anda telah memiliki:

* **Python 3.x** terinstal di sistem Anda.
* **pip** (Python package installer).
* **Virtual Environment** (disarankan untuk isolasi dependensi).
* **Aplikasi REST Client** seperti Postman, Insomnia, atau `curl` untuk melakukan request ke API.

## 2. Setup

Ikuti langkah-langkah berikut untuk menyiapkan lingkungan pengembangan:

1.  **Clone Repository (jika ada):**
    ```bash
    git clone [URL_REPOSITORY_ANDA]
    cd asnCare
    ```

2.  **Buat dan Aktifkan Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Untuk Linux/macOS
    # venv\Scripts\activate  # Untuk Windows
    ```

3.  **Instal Dependensi:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Konfigurasi Variabel Lingkungan:**
    * Buat file `.env` di root proyek Anda.
    * Isi file `.env` dengan informasi sensitif seperti URL API eksternal, kredensial, secret key Django, dan origin CORS. Contoh:
        ```
        isi .env file disembunyikan, chat pribadi saya jika ingin meminta .env file
        ```
    * Pastikan Anda telah mengganti nilai-nilai di atas dengan informasi yang sesuai.

5.  **Jalankan Migrasi Database:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Fetch data pegawai (untuk admin):**
    ```bash
    python manage.py fetch_pegawai_data
    ```

7.  **Buat Superuser (untuk admin):**
    ```bash
    python manage.py createsuperuser
    ```
    Ikuti petunjuk untuk membuat akun administrator.

8.  **Jalankan Server Pengembangan:**
    ```bash
    python manage.py runserver
    ```
    API akan berjalan secara default di `http://127.0.0.1:8000/`.

## 3. Autentikasi

API ini menggunakan **JWT (JSON Web Tokens)** untuk autentikasi.

1.  **Mendapatkan Token Untuk Login Pengguna / admin :**
    * Lakukan `POST` request ke endpoint `/api/token/`.
    * Sertakan `username` dan `password` di body request dalam format JSON.
    * Endpoint ini untuk mendapatkan token.
    * **Catatan:** Endpoint ini  memerlukan autentikasi dari database Anda
    * **Contoh Request Body:**
        ```json
        {
            "username": "nama_pengguna",
            "password": "kata_sandi"
        }
        ```
    * **Contoh Response (Sukses):**
        ```json
        {
            "access": "your_access_token_here",
            "refresh": "your_refresh_token_here"
        }
        ```
    * Gunakan `access` token untuk mengakses sebagian besar endpoint. `refresh` token dapat digunakan untuk mendapatkan `access` token baru setelah masa berlakunya habis (melalui endpoint `/api/token/refresh/`).

2.  **Menggunakan Token:**
    * Untuk mengakses endpoint yang memerlukan autentikasi, Anda perlu menyertakan token JWT di header `Authorization` dengan format `Bearer <token>`.
    * Contoh header:
        ```
        Authorization: Bearer your_jwt_token_here
        ```

## 4. Endpoint API

Berikut adalah daftar endpoint API yang tersedia:

### Autentikasi Pengguna

* **`GET /api/user/users/`**: Mendapatkan daftar semua user di database lokal.
    * **Membutuhkan:** Autentikasi JWT dengan role `is_superuser`.
    * **Header Request:** `Authorization: Bearer <token>`.
    * **Response (Sukses):** Mengembalikan daftar user dalam format JSON.

* **`DELETE /api/user/users/<id>/`**: Menghapus user dengan ID tertentu dari database lokal.
    * **Membutuhkan:** Autentikasi JWT dengan role `is_superuser`.
    * **Header Request:** `Authorization: Bearer <token>`.
    * **Path Parameter:**
        * `id`: ID dari user yang ingin dihapus.
    * **Response (Sukses):** Mengembalikan status `204 No Content`.

* **`POST /api/token/`**: Mendapatkan access dan refresh token JWT untuk pengguna database lokal.
    * **Membutuhkan:** Tidak ada autentikasi token.
    * **Body Request:**
        ```json
        {
            "username": "nama_pengguna",
            "password": "kata_sandi"
        }
        ```
    * **Response (Sukses):** Mengembalikan access dan refresh token.

* **`POST /api/token/refresh/`**: Mendapatkan access token JWT baru menggunakan refresh token.
    * **Membutuhkan:** Tidak ada autentikasi token.
    * **Body Request:**
        ```json
        {
            "refresh": "your_refresh_token_here"
        }
        ```
    * **Response (Sukses):** Mengembalikan access token baru.

### Manajemen Pegawai

* **`GET /api/pegawai/`**: Mendapatkan daftar semua data pegawai.
    * **Membutuhkan:** Autentikasi JWT dengan role `is_superuser`.
    * **Header Request:** `Authorization: Bearer <token>`.
    * **Response (Sukses):** Mengembalikan daftar data pegawai dalam format JSON.

* **`POST /api/pegawai/`**: Menambahkan data pegawai baru.
    * **Membutuhkan:** Autentikasi JWT dengan role `is_superuser`.
    * **Header Request:** `Authorization: Bearer <token>`.
    * **Body Request:** Contoh:
        ```json
        {
            "email": "",
            "namaPegawai": "Nama Pegawai Baru",
            "idtbPegawai": 12345
            // ... field pegawai lainnya
        }
        ```
    * **Response (Sukses):** Mengembalikan data pegawai yang baru dibuat dengan status `201 Created`.

* **`GET /api/pegawai/<id_pegawai>/`**: Mendapatkan detail data pegawai berdasarkan ID.
    * **Membutuhkan:** Autentikasi JWT dengan role `is_superuser`.
    * **Header Request:** `Authorization: Bearer <token>`.
    * **Path Parameter:**
        * `id_pegawai`: ID pegawai (dari database lokal).
    * **Response (Sukses):** Mengembalikan detail data pegawai dalam format JSON.

* **`PUT /api/pegawai/<id_pegawai>/`**: Memperbarui data pegawai berdasarkan ID.
    * **Membutuhkan:** Autentikasi JWT dengan role `is_superuser`.
    * **Header Request:** `Authorization: Bearer <token>`.
    * **Path Parameter:**
        * `id_pegawai`: ID pegawai (dari database lokal).
    * **Body Request:** Data pegawai yang ingin diperbarui dalam format JSON.
    * **Response (Sukses):** Mengembalikan data pegawai yang telah diperbarui.

* **`DELETE /api/pegawai/<id_pegawai>/`**: Menghapus data pegawai berdasarkan ID.
    * **Membutuhkan:** Autentikasi JWT dengan role `is_superuser`.
    * **Header Request:** `Authorization: Bearer <token>`.
    * **Path Parameter:**
        * `id_pegawai`: ID pegawai (dari database lokal).
    * **Response (Sukses):** Mengembalikan status `204 No Content`.

* **`GET /api/pegawai/profile/`**: Mendapatkan profil pegawai yang sedang login.
    * **Membutuhkan:** Autentikasi JWT sebagai pegawai (`is_pegawai=True`).
    * **Header Request:** `Authorization: Bearer <token>`.
    * **Response (Sukses):** Mengembalikan detail data pegawai yang sedang login.

* **`PUT /api/pegawai/profile/`**: Memperbarui profil pegawai yang sedang login.
    * **Membutuhkan:** Autentikasi JWT sebagai pegawai (`is_pegawai=True`).
    * **Header Request:** `Authorization: Bearer <token>`.
    * **Body Request:** Data pegawai yang ingin diperbarui dalam format JSON.
    * **Response (Sukses):** Mengembalikan data pegawai yang telah diperbarui.

* **`POST /api/user/change-password/`**: Mengganti Password pegawai yang sedang login.
    * **Membutuhkan:** Autentikasi JWT sebagai pegawai (`is_pegawai=True`).
    * **Header Request:** `Authorization: Bearer <token>`.
    * **Body Request:** Data pegawai yang ingin diperbarui dalam format JSON.
        contoh : 
        ```json
        {
            "old_password": "password_lama_pegawai",
            "new_password": "password_baru_pegawai",
            "confirm_password": "password_baru_pegawai"
        }
        ```
    * **Response (Sukses):** Mengembalikan data pegawai yang telah diperbarui.

### Manajemen Kehadiran

* **`GET /api/kehadiran/`**: Mendapatkan daftar catatan kehadiran.
    * **Membutuhkan:** Autentikasi JWT. Superuser akan mendapatkan semua catatan, pegawai hanya akan mendapatkan catatan mereka sendiri.
    * **Header Request:** `Authorization: Bearer <token>`.
    * **Response (Sukses):** Mengembalikan daftar catatan kehadiran dalam format JSON.

* **`POST /api/kehadiran/`**: Menambahkan catatan kehadiran apel untuk pegawai yang sedang login.
    * **Membutuhkan:** Autentikasi JWT sebagai pegawai (`is_pegawai=True`).
    * **Header Request:** `Authorization: Bearer <token>`.
    * **Body Request:** Contoh:
        ```json
        {
            "tanggal_apel": "2025-03-27",
            "status_apel": "hadir",
            "keterangan": "Apel pagi berjalan lancar"
        }
        ```
    * **Response (Sukses):** Mengembalikan catatan kehadiran yang baru dibuat dengan status `201 Created`.

* **`GET /api/kehadiran/?tanggal_mulai=yyyy-mm-hh&tanggal_akhir=yyyy-mm-hh`**: Mendapatkan Riwayat Data Kehadiran Di tanggal Tertentu , catatan kehadiran apel untuk pegawai yang sedang login.
    * **Membutuhkan:** Autentikasi JWT sebagai pegawai (`is_pegawai=True`).
    * **Header Request:** `Authorization: Bearer <token>`.
    * **Response (Suksess):** Contoh:
        ```json
        {
            "id_kehadiran": 1,
            "pegawai": 1,
            "pegawai_nama": "Nama Pegawai",
            "tanggal_apel": "2025-03-03",
            "status_apel": "izin",
            "keterangan": "Keperluan Keluarga"
        },
        {
            "id_kehadiran": 2,
            "pegawai": 1,
            "pegawai_nama": "Nama Pegawai",
            "tanggal_apel": "2025-03-04",
            "status_apel": "hadir",
            "keterangan": null
        }
        ```
    * **Response (Sukses):** Mengembalikan catatan kehadiran yang baru dibuat dengan status `201 Created`.

### Pengajuan Cuti 

* **`POST /api/cuti/pns/`**: pengjuan cuti pegawai.
    * **Membutuhkan:** Autentikasi JWT sebagai pegawai (`is_pegawai=True`).
    * **Header Request:** `Authorization: Bearer <token>`.
    * **Body Request:** Data pegawai yang ingin diperbarui dalam format JSON.
        contoh : 
        ```json
        {
            "masa_jabatan_tahun": 3,
            "masa_jabatan_bulan": 2,
            "jenis_cuti": "tahunan",
            "alasan_cuti": "Liburan keluarga",
            "tanggal_mulai": "2025-05-10",
            "tanggal_selesai": "2025-05-12",
            "alamat_cuti": "Jl. Kenangan No. 1, Malang",
            "telepon": "081234567890",
            "pimpinan_1": 2,  // ID Pegawai dari pimpinan 1
            "pimpinan_2": 3,  // ID Pegawai dari pimpinan 2 (opsional)
            "pimpinan_3": null // ID Pegawai dari pimpinan 3 (opsional)
        }
        ```
    * **Response (Sukses):** Mengembalikan data cuti pegawai.
    * **Response (Gagal):** Jatah cuti tahunan Anda hanya 12 hari. Anda telah menggunakan {total_cuti_diambil} hari dan pengajuan cuti ini sebanyak {lama_cuti_diajukan} hari akan melebihi batas.
    * **Response (Gagal):** "Cuti melahirkan tidak boleh lebih dari 3 bulan.".

* **`GET /api/cuti/pns/`**: Ambil data cuti pegawai.
    * **Membutuhkan:** Autentikasi JWT sebagai pegawai (`is_pegawai=True`).
    * **Header Request:** `Authorization: Bearer <token>`.
    * **Response (Suksess):** 
        contoh : 
        ```json
       {
        "total_cuti_diambil": 12,
        "sisa_cuti": 0,
        "results": [
            {
            "id": 1,
            "nama": "asd",
            "nip": null,
            "jabatan": null,
            "pimpinan_1": 2,
            "pimpinan_2": 3,
            "pimpinan_3": null,
            "masa_jabatan_tahun": 3,
            "masa_jabatan_bulan": 5,
            "jenis_cuti": "tahunan",
            "alasan_cuti": "Liburan bersama keluarga",
            "tanggal_mulai": "2025-05-20",
            "tanggal_selesai": "2025-05-30",
            "alamat_cuti": "Jl. Kenangan No. 123, Malang",
            "telepon": "081234567890",
            "tanggal_dibuat": "2025-04-08T23:40:47.454722Z",
            "pimpinan_1_nama": "GATOT SUWARDIYONO",
            "pimpinan_2_nama": "IWAN HERI KRISTANTO",
            "pimpinan_3_nama": null
            },
            {
            "id": 2,
            "nama": "asd",
            "nip": null,
            "jabatan": null,
            "pimpinan_1": 2,
            "pimpinan_2": 3,
            "pimpinan_3": null,
            "masa_jabatan_tahun": 3,
            "masa_jabatan_bulan": 5,
            "jenis_cuti": "tahunan",
            "alasan_cuti": "Liburan bersama keluarga",
            "tanggal_mulai": "2025-06-20",
            "tanggal_selesai": "2025-06-20",
            "alamat_cuti": "Jl. Kenangan No. 123, Malang",
            "telepon": "081234567890",
            "tanggal_dibuat": "2025-04-08T23:41:14.361236Z",
            "pimpinan_1_nama": "GATOT SUWARDIYONO",
            "pimpinan_2_nama": "IWAN HERI KRISTANTO",
            "pimpinan_3_nama": null
            }
        ]
        }
        ```

* **`GET /api/cuti/sisa/`**: Ambil data cuti pegawai.
    * **Membutuhkan:** Autentikasi JWT sebagai pegawai (`is_pegawai=True`).
    * **Header Request:** `Authorization: Bearer <token>`.
    * **Response (Suksess):** 
        contoh : 
        ```json
            {
                "total_cuti_diambil": 0,
                "sisa_cuti": 12
            }
        ```

### Kenaikan Pangkat Dan Gaji

* **`GET /api/pegawai/profile/`**: Mendapatkan profil pegawai yang sedang login.
    * **Membutuhkan:** Autentikasi JWT sebagai pegawai (`is_pegawai=True`).
    * **Header Request:** `Authorization: Bearer <token>`.
    * **Response (Sukses):** Mengembalikan detail data pegawai yang sedang login.

* ** `CONTOH PENGGUNAAN`**: Pangkat dn Gaji
    * Contoh Penggunaan React
    ```jsx
            import React, { useEffect, useState } from 'react';
            import axios from 'axios';

            const Reminder = () => {
                const [pangkatMessage, setPangkatMessage] = useState("");
                const [gajiMessage, setGajiMessage] = useState("");
                const [profile, setPegawai] = useState(null); 

                useEffect(() => {
                    const fetchPegawai = async () => {
                        try {
                            const response = await axios.get('/api/pegawai/profile/', {
                                headers: {
                                    Authorization: `Bearer ${localStorage.getItem('token')}`
                                }
                            });
                            setPegawai(response.data);
                        } catch (error) {
                            console.error("Error fetching profile:", error);
                        }
                    };

                    fetchPegawai();
                }, []);

                useEffect(() => {
                    if (profile) {
                        // Informasi Kenaikan Pangkat
                        if (profile.waktu_kenaikan_pangkat) {
                            setPangkatMessage(`Waktu kenaikan pangkat: ${profile.waktu_kenaikan_pangkat}`);
                        } else {
                            setPangkatMessage("Informasi kenaikan pangkat tidak tersedia.");
                        }

                        // Informasi Kenaikan Gaji
                        if (profile.waktu_kenaikan_gaji) {
                            setGajiMessage(`Waktu kenaikan gaji: ${profile.waktu_kenaikan_gaji}`);
                        } else {
                            setGajiMessage("Informasi kenaikan gaji tidak tersedia.");
                        }
                    }
                }, [profile]);

                return (
                    <div>
                        <div className="row">
                            {/* Card 1: Kenaikan Gaji */}
                            <div className="col-md-6 mb-4">
                                <div className="card dashboard-card">
                                    <div className="card-body">
                                        <h5 className="card-title">Kenaikan Gaji</h5>
                                        <div className="card sub-card bg-warning text-white mt-3">
                                            <div className="card-body py-2 px-3">{gajiMessage}</div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Card 2: Kenaikan Pangkat */}
                            <div className="col-md-6 mb-4">
                                <div className="card dashboard-card">
                                    <div className="card-body">
                                        <h5 className="card-title">Kenaikan Pangkat</h5>
                                        <div className="card sub-card bg-danger text-white mt-3">
                                            <div className="card-body py-2 px-3">{pangkatMessage}</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };

            export default Reminder;
  
    ```

### Pensiun

* **`GET /api/pegawai/profile/`**: Mendapatkan profil pegawai yang sedang login.
    * **Membutuhkan:** Autentikasi JWT sebagai pegawai (`is_pegawai=True`).
    * **Header Request:** `Authorization: Bearer <token>`.
    * **Response (Sukses):** Mengembalikan detail data pegawai yang sedang login.

* ** `CONTOH PENGGUNAAN`**: Pensiun
    * Contoh Penggunaan React
    ```jsx
            const Pensiun = () => {
                const [profile, setProfile] = useState(null);
                const [retirementMessage, setRetirementMessage] = useState('');

                useEffect(() => {
                    const fetchProfile = async () => {
                        try {
                            const token = localStorage.getItem('accessToken'); // Atau cara Anda menyimpan token
                            const response = await axios.get('/api/pegawai/profile/', {
                                headers: {
                                    Authorization: `Bearer ${token}`,
                                },
                            });
                            setProfile(response.data);
                        } catch (error) {
                            console.error('Gagal mengambil profil pegawai:', error);
                        }
                    };

                    fetchProfile();
                }, []);

                useEffect(() => {
                    if (profile) {
                        if (profile.umur >= 60) {
                            setRetirementMessage('Anda sudah mencapai atau melewati usia pensiun. Harap segera mengajukan pensiun.');
                        } else {
                            const yearsLeft = 60 - profile.umur;
                            setRetirementMessage(`Anda memiliki ${yearsLeft} tahun lagi sebelum pensiun.`);
                        }
                    }
                }, [profile]);

                return (
                    <div>
                        <h1>Selamat Datang di Dashboard</h1>
                        {profile && (
                            <div>
                                <p>Nama: {profile.namaPegawai}</p>
                                <p>Email: {profile.email}</p>
                                <p>Usia: {profile.umur}</p>
                            </div>
                        )}

                        {retirementMessage && (
                            <div style={{ backgroundColor: 'yellow', padding: '10px', marginTop: '20px' }}>
                                <strong>Pemberitahuan:</strong> {retirementMessage}
                            </div>
                        )}
                    </div>
                );
            };

            export default Pensiun;  
    ```

## 5. Format Data

Semua pertukaran data dengan API ini menggunakan format **JSON**.

## 6. Penanganan Error

API akan mengembalikan response dengan kode status HTTP yang sesuai untuk menunjukkan hasil dari setiap request. Beberapa kode status umum yang mungkin Anda temui:

* **`200 OK`**: Request berhasil.
* **`201 Created`**: Sumber daya baru berhasil dibuat.
* **`204 No Content`**: Request berhasil dan tidak ada konten untuk dikembalikan (biasanya untuk operasi `DELETE`).
* **`400 Bad Request`**: Request tidak valid (misalnya, format data salah). Pesan error yang lebih detail mungkin disertakan dalam body response.
* **`401 Unauthorized`**: Autentikasi gagal atau token tidak valid.
* **`403 Forbidden`**: Anda tidak memiliki izin untuk mengakses sumber daya yang diminta.
* **`404 Not Found`**: Sumber daya yang diminta tidak ditemukan.
* **`500 Internal Server Error`**: Terjadi kesalahan server yang tidak terduga.

Body response untuk error biasanya akan berisi pesan JSON yang menjelaskan kesalahan tersebut.

## 7. Konfigurasi CORS

API ini telah dikonfigurasi untuk mengizinkan request dari origin yang ditentukan dalam variabel lingkungan `CORS_ALLOWED_ORIGINS` (biasanya diatur untuk frontend React Vite Anda). Metode HTTP yang diizinkan adalah `GET`, `POST`, `PUT`, dan `DELETE`.

## 8. Catatan Penting

* Jangan menyimpan token JWT di sisi klien (frontend) secara permanen. Gunakan mekanisme penyimpanan yang aman seperti `localStorage` atau `sessionStorage` dengan hati-hati, atau pertimbangkan pendekatan yang lebih aman seperti HTTP-only cookies.
* Pastikan untuk selalu mengirimkan token JWT yang valid di header `Authorization` untuk mengakses endpoint yang dilindungi.
* Data gambar (`fotoPegawai`, `link_file_apps_npwp`, `link_file_apps_karpeg`, `link_file_apps_kpe`) saat ini disimpan sebagai nilai kosong di database. Implementasi penanganan file gambar menggunakan Pillow perlu ditambahkan jika diperlukan.
* Setiap ID pegawai yang digunakan dalam API (terutama pada path parameter) merujuk pada ID internal database lokal (`id_pegawai`), bukan `idtbPegawai` dari API eksternal.

Semoga dokumentasi ini membantu Anda dalam menggunakan API `asnCare`. Jika Anda memiliki pertanyaan lebih lanjut, jangan ragu untuk bertanya.