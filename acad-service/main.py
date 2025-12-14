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
    'database': os.getenv('DB_NAME', 'products'),
    'user': os.getenv('DB_USER', 'productuser'),
    'password': os.getenv('DB_PASSWORD', 'productpass')
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

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "Acad Service is running",
        "timestamp": datetime.now().isoformat()
    }

# Tambah fitur menambahkan Mahasiswa
@app.post("/api/acad/tambah_mahasiswa", response_model=Mahasiswa)
async def add_mahasiswa(
    nim: str = Query(..., description="Nomor Induk Mahasiswa"),
    nama: str = Query(..., description="Nama lengkap mahasiswa"),
    jurusan: str = Query(..., description="Jurusan mahasiswa"),
    angkatan: int = Query(..., ge=2000, description="Tahun angkatan mahasiswa")
):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            query = "INSERT INTO mahasiswa (nim, nama, jurusan, angkatan) VALUES (%s, %s, %s, %s)"
            values = (nim, nama, jurusan, angkatan)

            cursor.execute(query, values)
            # Commit perubahan ke database agar tersimpan permanen
            conn.commit()

            # Mengembalikan data yang baru saja ditambahkan sesuai format response_model
            return {"nim": nim, "nama": nama, "jurusan": jurusan, "angkatan": angkatan,"\n Berhasil ditambahkan" : True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/acad/cek_mahasiswa")
async def get_mahasiswas():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM mahasiswa"

            cursor.execute(query)
            rows = cursor.fetchall()

            return [{"NIM": row[0], "Nama": row[1], "Jurusan": row[2], "Angkatan": row[3]} for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Tambah fitur tampilkan mata kuliah
@app.get("/api/acad/mata_kuliah")
async def get_mata_kuliah():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM mata_kuliah"

            cursor.execute(query)
            rows = cursor.fetchall()

            return [{"Kode": row[0], "Mata Kuliah": row[1], "SKS": row[2]} for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/acad/cek_ips")
async def hitung_ips(nim: str, semester: int):
    """
    Menghitung Indeks Prestasi Semester (IPS) untuk seorang mahasiswa pada semester tertentu.
    """
    try:
        with get_db_connection() as conn:
            # Menggunakan RealDictCursor untuk mendapatkan hasil sebagai dictionary
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # Ambil data mahasiswa untuk validasi dan untuk disertakan dalam respons
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

            total_nilai_bobot = result['total_nilai_bobot']
            total_sks = result['total_sks']

            # Hitung IPS dan kembalikan hasilnya
            ips = total_nilai_bobot / total_sks

            return {**mahasiswa, "Semester": semester, "IPS": round(ips, 2)}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))