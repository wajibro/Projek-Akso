from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime
from contextlib import contextmanager

app = FastAPI(title="Product Service", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'acad_db'),
    'user': os.getenv('DB_USER', 'projek_akso'), 
    'password': os.getenv('DB_PASSWORD', 'projek_akso_cihuy')
}

def row_to_dict(row):
    if row is None:
        return None
    return dict(row)

class Mahasiswa(BaseModel):
    nim: str
    nama: str
    jurusan: str
    angkatan: int = Field(ge=0)

# Database connection pool
@contextmanager
def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

@app.on_event("startup")
async def startup_event():
    try:
        with get_db_connection() as conn:
            print("Acad Service: Connected to PostgreSQL")
    except Exception as e:
        print(f"Acad Service: PostgreSQL connection error: {e}")

# Tambah fitur menambahkan Mahasiswa
@app.post("/api/acad/tambah_mahasiswa")
async def add_mahasiswa(
    nim: str = Query(...),
    nama: str = Query(...),
    jurusan: str = Query(...),
    angkatan: int = Query(...)
):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Masukkan ke tabel mahasiswa yaitu (nim, nama, jurusan, angkatan)
            query = "INSERT INTO mahasiswa (nim, nama, jurusan, angkatan) VALUES (%s, %s, %s, %s)"
            values = (nim, nama, jurusan, angkatan)

            cursor.execute(query, values)

            # Mengembalikan data yang baru saja ditambahkan sesuai format response_model
            return {"nim": nim, "nama": nama, "jurusan": jurusan, "angkatan": angkatan,"\n Berhasil ditambahkan" : True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Tambah fitur tambah KRS
@app.post("/api/acad/tambah_krs")
async def add_krs(
    nim: str = Query(...,),
    kode_mk: str = Query(...),
    nilai: str = Query(...),
    semester: int = Query(...)
):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Periksa apakah mahasiswa dengan NIM tersebut ada
            cursor.execute("SELECT nim FROM mahasiswa WHERE nim = %s", (nim,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail=f"Mahasiswa dengan NIM {nim} tidak ditemukan.")

            # Periksa apakah mata kuliah dengan kode_mk tersebut ada
            cursor.execute("SELECT kode_mk FROM mata_kuliah WHERE kode_mk = %s", (kode_mk,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail=f"Mata kuliah dengan kode {kode_mk} tidak ditemukan.")

            # Masukkan data ke tabel krs
            query = "INSERT INTO krs (nim, kode_mk, nilai, semester) VALUES (%s, %s, %s, %s) RETURNING id_krs"
            values = (nim, kode_mk, nilai, semester)
            cursor.execute(query, values)
            new_krs_id = cursor.fetchone()[0]

            return {"id_krs": new_krs_id, "nim": nim, "kode_mk": kode_mk, "nilai": nilai, "semester": semester, "message": "KRS berhasil ditambahkan"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Tambah fitur cek data Mahasiswa berdasarkan NIM
@app.get("/api/acad/cek_mahasiswa")
async def get_mahasiswa_by_nim(nim: str):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Ambil nim, nama, jurusan, angkatan dari tabel mahasiswa berdasarkan nim
            query = "SELECT nim, nama, jurusan, angkatan FROM mahasiswa WHERE nim = %s"

            cursor.execute(query, (nim,))

            # Menggunakan fetchone untuk mendapatkan satu baris hasil
            mahasiswa = cursor.fetchone()

            if not mahasiswa:
                raise HTTPException(status_code=404, detail=f"Mahasiswa dengan NIM {nim} tidak ditemukan.")
            
            # Kembalikan data mahasiswa
            return mahasiswa 
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/acad/daftar_mahasiswa")
async def get_all_mahasiswa():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # Ambil nim, nama, jurusan, angkatan dari tabel mahasiswa diurutkan berdasarkan angkatan descending dan nama ascending
            query = "SELECT nim, nama, jurusan, angkatan FROM mahasiswa ORDER BY angkatan DESC, nama ASC"

            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Fitur untuk menampilkan mata kuliah dengan filter opsional
@app.get("/api/acad/mata_kuliah")
async def get_mata_kuliah_filtered(
    semester: Optional[int] = Query(None),
    jurusan: Optional[str] = Query(None)
):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = "SELECT kode_mk, nama_mk, sks, semester, jurusan FROM mata_kuliah"
            filters = []
            params = []

            if semester is not None:
                filters.append("semester = %s")
                params.append(semester)
            
            if jurusan:
                filters.append("jurusan = %s")
                params.append(jurusan)

            if filters:
                query += " WHERE " + " AND ".join(filters)
            
            query += " ORDER BY semester, nama_mk;"

            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/acad/cek_ips")
async def hitung_ips(nim: str, semester: int):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # Ambil nim, nama, jurusan, angkatan dari tabel mahasiswa berdasarkan nim
            cursor.execute("SELECT nim, nama, jurusan, angkatan FROM mahasiswa WHERE nim = %s", (nim,))
            mahasiswa = cursor.fetchone()

            if not mahasiswa:
                raise HTTPException(status_code=404, detail=f"Mahasiswa dengan NIM {nim} tidak ditemukan.")

            # Query untuk menghitung total (bobot * sks) dan total sks secara efisien
            # JOIN dengan tabel bobot_nilai untuk konversi nilai huruf ke angka
            query = "SELECT SUM(bn.bobot * mk.sks) AS total_nilai_bobot, SUM(mk.sks) AS total_sks FROM krs JOIN mata_kuliah mk ON krs.kode_mk = mk.kode_mk JOIN bobot_nilai bn ON krs.nilai = bn.nilai WHERE krs.nim = %s AND krs.semester = %s;"
            cursor.execute(query, (nim, semester))
            result = cursor.fetchone()

            # Handle jika tidak ada data KRS untuk semester tersebut (mencegah dibagi bilangan nol)
            if not result or result['total_sks'] is None or result['total_sks'] == 0:
                return {**mahasiswa, "Semester": semester, "IPS": 0.0, "message": "Tidak ada data KRS untuk semester ini."}

            total_sks = result['total_sks']
            total_nilai_bobot = result['total_nilai_bobot']

            # Hitung IPS dan kembalikan hasilnya
            ips = total_nilai_bobot / total_sks

            return {**mahasiswa, "Semester": semester, "IPS": round(ips, 2)}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))