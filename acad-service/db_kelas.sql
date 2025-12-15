CREATE TABLE mahasiswa (
    nim VARCHAR(15) PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    jurusan VARCHAR(50),
    angkatan INT
);

CREATE TABLE mata_kuliah (
    kode_mk VARCHAR(10) PRIMARY KEY,
    nama_mk VARCHAR(100) NOT NULL,
    sks INT NOT NULL,
    jurusan VARCHAR(50) NOT NULL,
    semester INT
);

CREATE TABLE krs (
    id_krs bigserial PRIMARY KEY,
    nim VARCHAR(15),
    kode_mk VARCHAR(10),
    nilai VARCHAR(2),
    semester INT,
    FOREIGN KEY (nim) REFERENCES mahasiswa(nim),
    FOREIGN KEY (kode_mk) REFERENCES mata_kuliah(kode_mk)
);

CREATE TABLE bobot_nilai (
    nilai VARCHAR(2) PRIMARY KEY,
    bobot FLOAT
);

INSERT INTO mahasiswa (nim, nama, jurusan, angkatan) VALUES
('25031554020', 'ANINDYA SARASWATI AYU DEWAYANI', 'Sains Data', 2025),
('25031554204', 'ALIA NURUL DZIHNI', 'Sains Data', 2025),
('25031554200', 'LUTFI MUHAMMAD IRFANSYACH', 'Sains Data', 2025);

-- ========== Mata Kuliah Sains Data ==========
-- Semester 1
INSERT INTO mata_kuliah (kode_mk, nama_mk, sks, jurusan, semester) VALUES
('SD101', 'Pancasila', 2, 'Sains Data', 1),
('SD102', 'Literasi Digital', 2, 'Sains Data', 1),
('SD103', 'Arsitektur Komputer dan Sistem Operasi', 3, 'Sains Data', 1),
('SD104', 'Matematika Dasar', 3, 'Sains Data', 1),
('SD105', 'Pemrograman Dasar', 2, 'Sains Data', 1),
('SD106', 'Aljabar Matriks', 3, 'Sains Data', 1),
('SD107', 'Matematika Diskrit', 3, 'Sains Data', 1);
-- Semester 2
INSERT INTO mata_kuliah (kode_mk, nama_mk, sks, jurusan, semester) VALUES
('SD201', 'Pendidikan Agama', 2, 'Sains Data', 2),
('SD202', 'Pendidikan Kewarganegaraan', 2, 'Sains Data', 2),
('SD203', 'Teori Probabilitas', 3, 'Sains Data', 2),
('SD204', 'Kalkulus Lanjut', 3, 'Sains Data', 2),
('SD205', 'Struktur Data dan Algoritma', 3, 'Sains Data', 2),
('SD206', 'Interaksi Manusia dan Komputer', 3, 'Sains Data', 2),
('SD207', 'Etika Kecerdasan Artifisial', 2, 'Sains Data', 2),
('SD208', 'Konservasi Sumber Daya Alam dan Lingkungan', 2, 'Sains Data', 2);

-- ========== 25031554020 ==========
-- Semester 1
INSERT INTO krs (nim, kode_mk, nilai, semester) VALUES
('25031554020', 'SD101', 'A', 1),
('25031554020', 'SD102', 'B+', 1),
('25031554020', 'SD103', 'B', 1),
('25031554020', 'SD104', 'B', 1),
('25031554020', 'SD105', 'A', 1),
('25031554020', 'SD106', 'C+', 1),
('25031554020', 'SD107', 'B', 1);
-- Semester 2
INSERT INTO krs (nim, kode_mk, nilai, semester) VALUES
('25031554020', 'SD201', 'A', 2),
('25031554020', 'SD202', 'A', 2),
('25031554020', 'SD203', 'B+', 2),
('25031554020', 'SD204', 'B-', 2),
('25031554020', 'SD205', 'B', 2),
('25031554020', 'SD206', 'C+', 2),
('25031554020', 'SD207', 'B', 2),
('25031554020', 'SD208', 'A', 2);

-- ========== 25031554204 ==========
-- Semester 1
INSERT INTO krs (nim, kode_mk, nilai, semester) VALUES
('25031554204', 'SD101', 'A', 1),
('25031554204', 'SD102', 'A', 1),
('25031554204', 'SD103', 'B+', 1),
('25031554204', 'SD104', 'B', 1),
('25031554204', 'SD105', 'A', 1),
('25031554204', 'SD106', 'A', 1),
('25031554204', 'SD107', 'B+', 1);
-- Semester 2
INSERT INTO krs (nim, kode_mk, nilai, semester) VALUES
('25031554204', 'SD201', 'A', 2),
('25031554204', 'SD202', 'A', 2),
('25031554204', 'SD203', 'B', 2),
('25031554204', 'SD204', 'B', 2),
('25031554204', 'SD205', 'A', 2),
('25031554204', 'SD206', 'B+', 2),
('25031554204', 'SD207', 'A', 2),
('25031554204', 'SD208', 'B+', 2);

-- ========== 25031554200 ==========
-- Semester 1
INSERT INTO krs (nim, kode_mk, nilai, semester) VALUES
('25031554200', 'SD101', 'B+', 1),
('25031554200', 'SD102', 'C', 1),
('25031554200', 'SD103', 'B', 1),
('25031554200', 'SD104', 'B', 1),
('25031554200', 'SD105', 'C+', 1),
('25031554200', 'SD106', 'B+', 1),
('25031554200', 'SD107', 'A', 1);
-- Semester 2
INSERT INTO krs (nim, kode_mk, nilai, semester) VALUES
('25031554200', 'SD201', 'B+', 2),
('25031554200', 'SD202', 'A', 2),
('25031554200', 'SD203', 'C', 2),
('25031554200', 'SD204', 'B', 2),
('25031554200', 'SD205', 'C', 2),
('25031554200', 'SD206', 'B-', 2),
('25031554200', 'SD207', 'B', 2),
('25031554200', 'SD208', 'C+', 2);

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