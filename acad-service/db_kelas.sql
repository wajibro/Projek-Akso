CREATE TABLE mahasiswa (
    nim VARCHAR(10) PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    jurusan VARCHAR(50),
    angkatan INT
);

CREATE TABLE mata_kuliah (
    kode_mk VARCHAR(10) PRIMARY KEY,
    nama_mk VARCHAR(100) NOT NULL,
    sks INT NOT NULL,
    semester INT
);

CREATE TABLE krs (
    id_krs bigserial PRIMARY KEY,
    nim VARCHAR(10),
    kode_mk VARCHAR(10),
    nilai CHAR(2),
    semester INT,
    FOREIGN KEY (nim) REFERENCES mahasiswa(nim),
    FOREIGN KEY (kode_mk) REFERENCES mata_kuliah(kode_mk)
);

CREATE TABLE bobot_nilai (
    nilai CHAR(2) PRIMARY KEY,
    bobot FLOAT
);

INSERT INTO mahasiswa (nim, nama, jurusan, angkatan) VALUES
('25031554020', 'ANINDYA SARASWATI AYU DEWAYANI', 'Sains Data', 2025),
('25031554204', 'ALIA NURUL DZIHNI', 'Sains Data', 2025),
('25031554200', 'LUTFI MUHAMMAD IRFANSYACH', 'Sains Data', 2025);

INSERT INTO mata_kuliah (kode_mk, nama_mk, sks, semester) VALUES
('IF101', 'Pancasila', 2, 1),
('IF102', 'Literasi Digital', 2, 1),
('IF103', 'Arsitektur Komputer dan Sistem Operasi', 3, 1),
('IF104', 'Matematika Dasar', 3, 1),
('IF105', 'Pemrograman Dasar', 2, 1),
('IF106', 'Aljabar Matriks', 3, 1),
('IF107', 'Matematika Diskrit', 3, 1);

INSERT INTO mata_kuliah (kode_mk, nama_mk, sks, semester) VALUES
('IF201', 'Pendidikan Agama', 2, 2),
('IF202', 'Pendidikan Kewarganegaraan', 2, 2),
('IF203', 'Teori Probabilitas', 3, 2),
('IF204', 'Kalkulus Lanjut', 3, 2),
('IF205', 'Struktur Data dan Algoritma', 3, 2),
('IF206', 'Interaksi Manusia dan Komputer', 3, 2),
('IF207', 'Etika Kecerdasan Artifisial', 2, 2),
('IF208', 'Konservasi Sumber Daya Alam dan Lingkungan', 2, 2);

-- ========== 25031554020 ==========
-- Semester 1
INSERT INTO krs (nim, kode_mk, nilai, semester) VALUES
('25031554020', 'IF101', 'A', 1),
('25031554020', 'IF102', 'B+', 1),
('25031554020', 'IF103', 'B', 1),
('25031554020', 'IF104', 'B', 1),
('25031554020', 'IF105', 'A', 1),
('25031554020', 'IF106', 'C+', 1),
('25031554020', 'IF107', 'B', 1);
-- Semester 2
INSERT INTO krs (nim, kode_mk, nilai, semester) VALUES
('25031554020', 'IF201', 'A', 2),
('25031554020', 'IF202', 'A', 2),
('25031554020', 'IF203', 'B+', 2),
('25031554020', 'IF204', 'B-', 2),
('25031554020', 'IF205', 'B', 2),
('25031554020', 'IF206', 'C+', 2),
('25031554020', 'IF207', 'B', 2),
('25031554020', 'IF208', 'A', 2);

-- ========== 25031554204 ==========
-- Semester 1
INSERT INTO krs (nim, kode_mk, nilai, semester) VALUES
('25031554204', 'IF101', 'A', 1),
('25031554204', 'IF102', 'A', 1),
('25031554204', 'IF103', 'B+', 1),
('25031554204', 'IF104', 'B', 1),
('25031554204', 'IF105', 'A', 1),
('25031554204', 'IF106', 'A', 1),
('25031554204', 'IF107', 'B+', 1);
-- Semester 2
INSERT INTO krs (nim, kode_mk, nilai, semester) VALUES
('25031554204', 'IF201', 'A', 2),
('25031554204', 'IF202', 'A', 2),
('25031554204', 'IF203', 'B', 2),
('25031554204', 'IF204', 'B', 2),
('25031554204', 'IF205', 'A', 2),
('25031554204', 'IF206', 'B+', 2),
('25031554204', 'IF207', 'A', 2),
('25031554204', 'IF208', 'B+', 2);

-- ========== 25031554200 ==========
-- Semester 1
INSERT INTO krs (nim, kode_mk, nilai, semester) VALUES
('25031554200', 'IF101', 'B+', 1),
('25031554200', 'IF102', 'C', 1),
('25031554200', 'IF103', 'B', 1),
('25031554200', 'IF104', 'B', 1),
('25031554200', 'IF105', 'C+', 1),
('25031554200', 'IF106', 'B+', 1),
('25031554200', 'IF107', 'A', 1);
-- Semester 2
INSERT INTO krs (nim, kode_mk, nilai, semester) VALUES
('25031554200', 'IF201', 'B+', 2),
('25031554200', 'IF202', 'A', 2),
('25031554200', 'IF203', 'C', 2),
('25031554200', 'IF204', 'B', 2),
('25031554200', 'IF205', 'C', 2),
('25031554200', 'IF206', 'B-', 2),
('25031554200', 'IF207', 'B', 2),
('25031554200', 'IF208', 'C+', 2);

INSERT INTO bobot_nilai VALUES
('A', 4.0),
('A-', 3.75),
('B+', 3.5),
('B', 3.0),
('B-', 2.75),
('C+', 2.5),
('C',2.0),
('D', 1.0),
('E', 0.0);