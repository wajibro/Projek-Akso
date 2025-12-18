
# 🎓 Projek Akso - Sistem Akademik Mikroservis

Selamat datang di **Projek Akso**! Tugas UAS dengan sistem informasi akademik sederhana yang dibangun dengan arsitektur mikroservis.

## ✨ Tentang Proyek

Projek Akso kali ini tentang sebuah platform untuk mengelola data akademik mahasiswa, termasuk data mahasiswa, mata kuliah, dan Kartu Rencana Studi (KRS). Aplikasi ini dirancang dengan pendekatan mikroservis untuk memisahkan setiap bagian utama dari sistem.

---

## 🏛️ Arsitektur

Sistem ini terdiri dari beberapa layanan yang bekerja sama:

- **Nginx**: Bertindak sebagai *reverse proxy* yang menerima semua permintaan dari luar dan meneruskannya ke layanan yang sesuai.
- **Auth Service**: Mengelola otentikasi dan otorisasi pengguna.
- **Acad Service**: Mengurus semua logika bisnis yang terkait dengan data akademik.

```
+----------------+      +-------------------+
|     Client     |----->|       Nginx       |
+----------------+      +-------------------+
                           |           |
                           |           |
         +-----------------v-+         +------------------v--+
         |   Auth Service    |         |    Acad Service     |
         | (Node.js/Express) |         | (Python/FastAPI)    |
         +-------------------+         +----------+----------+
                                                  |
                                                  |
                                        +---------v---------+
                                        |    PostgreSQL     |
                                        |      Database     |
                                        +-------------------+
```

---

## 🚀 Teknologi yang Digunakan

- **Reverse Proxy**: [Nginx](https://www.nginx.com/)
- **Authentication Service**: [Node.js](https://nodejs.org/), [Express](https://expressjs.com/)
- **Academic Service**: [Python](https://www.python.org/), [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **Containerization**: [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

---

## 🛠️ Cara Menjalankan Proyek

Untuk menjalankan proyek ini secara lokal, pastikan Anda telah menginstal Docker dan Docker Compose.

1.  **Clone repository ini.**
2.  **Buka terminal di direktori utama proyek.**
3.  **Jalankan perintah berikut:**

    ```sh
    docker-compose up --build -d
    ```

4.  Aplikasi akan dapat diakses melalui `http://localhost:8081`.

---

## Endpoints

### 👨‍🎓 Layanan Akademik (`/api/acad`)

| Method | Endpoint                    | Deskripsi                               |
| :----- | :-------------------------- | :-------------------------------------- |
| `POST` | `/tambah_mahasiswa`         | Menambahkan data mahasiswa baru.        |
| `GET`  | `/cek_mahasiswa`            | Melihat detail seorang mahasiswa (NIM). |
| `GET`  | `/daftar_mahasiswa`         | Menampilkan semua mahasiswa.            |
| `POST` | `/tambah_krs`               | Menambahkan data KRS untuk mahasiswa.   |
| `GET`  | `/mata_kuliah`              | Menampilkan daftar mata kuliah.         |
| `GET`  | `/cek_ips`                  | Menghitung Indeks Prestasi Semester.    |

<br>