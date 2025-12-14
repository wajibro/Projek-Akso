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

@app.get("/api/acad/mahasiswa")
async def get_mahasiswas():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM mahasiswa"

            cursor.execute(query)
            rows = cursor.fetchall()

            return [{"nim": row[0], "nama": row[1], "jurusan": row[2], "angkatan": row[3]} for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/acad/ips")
async def calculate_ips(nim: str, semester: int):
    """
    Menghitung Indeks Prestasi Semester (IPS) untuk seorang mahasiswa pada semester tertentu.
    """
    try:
        with get_db_connection() as conn:
            # Menggunakan RealDictCursor untuk mendapatkan hasil sebagai dictionary
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # 1. Ambil data mahasiswa untuk validasi dan untuk disertakan dalam respons
            cursor.execute("SELECT nim, nama, jurusan, angkatan FROM mahasiswa WHERE nim = %s", (nim,))
            mahasiswa = cursor.fetchone()

            if not mahasiswa:
                raise HTTPException(status_code=404, detail=f"Mahasiswa dengan NIM {nim} tidak ditemukan.")

            # 2. Query untuk menghitung total (bobot * sks) dan total sks secara efisien
            #    JOIN dengan tabel bobot_nilai untuk konversi nilai huruf ke angka
            query = """
                SELECT 
                    SUM(bn.bobot * mk.sks) AS total_nilai_bobot,
                    SUM(mk.sks) AS total_sks
                FROM krs
                JOIN mata_kuliah mk ON krs.kode_mk = mk.kode_mk
                JOIN bobot_nilai bn ON krs.nilai = bn.nilai
                WHERE krs.nim = %s AND krs.semester = %s;
            """
            cursor.execute(query, (nim, semester))
            result = cursor.fetchone()

            # 3. Handle jika tidak ada data KRS untuk semester tersebut (mencegah division by zero)
            if not result or result['total_sks'] is None or result['total_sks'] == 0:
                return {**mahasiswa, "semester": semester, "ips": 0.0, "message": "Tidak ada data KRS untuk semester ini."}

            total_nilai_bobot = result['total_nilai_bobot']
            total_sks = result['total_sks']

            # 4. Hitung IPS dan kembalikan hasilnya
            ips = total_nilai_bobot / total_sks

            return {**mahasiswa, "semester": semester, "ips": round(ips, 2)}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))