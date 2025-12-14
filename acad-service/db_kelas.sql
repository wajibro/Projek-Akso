CREATE TABLE mahasiswa (
    nim VARCHAR(10) PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    jurusan VARCHAR(50),
    angkatan INT
);

CREATE TABLE mata_kuliah (
    kode_mk VARCHAR(10) PRIMARY KEY,
    nama_mk VARCHAR(100) NOT NULL,
    sks INT NOT NULL
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
('020', 'ANINDYA SARASWATI AYU DEWAYANI', 'Sains Data', 2025),
('204', 'ALIA NURUL DZIHNI', 'Sains Data', 2025),
('200', 'LUTFI MUHAMMAD IRFANSYACH', 'Sains Data', 2025);

INSERT INTO mata_kuliah (kode_mk, nama_mk, sks) VALUES
('IF101', 'Literasi Digital', 2),
('IF102', 'Matematika Dasar', 3),
('IF103', 'Pemrograman Dasar', 3),
('IF104', 'Arsitektur Komputer dan Sistem Operasi', 3),
('IF105', 'Pancasila', 2),
('IF106', 'Matematika Diskrit', 3),
('IF107', 'Aljabar Matriks', 3);

INSERT INTO krs (nim, kode_mk, nilai, semester) VALUES
-- Data untuk ANINDYA SARASWATI AYU DEWAYANI (020)
('020', 'IF101', 'A', 1),
('020', 'IF102', 'B+', 1),
('020', 'IF103', 'B', 1),
('020', 'IF105', 'A', 1),
('020', 'IF106', 'C+', 2),
('020', 'IF107', 'B', 2),
-- Data untuk ALIA NURUL DZIHNI (204)
('204', 'IF101', 'A', 1),
('204', 'IF102', 'A', 1),
('204', 'IF103', 'B+', 1),
('204', 'IF104', 'B', 2),
('204', 'IF105', 'A', 2),
-- Data untuk LUTFI MUHAMMAD IRFANSYACH (200)
('200', 'IF101', 'B+', 1),
('200', 'IF102', 'C', 1),
('200', 'IF104', 'B', 1),
('200', 'IF106', 'B+', 2),
('200', 'IF107', 'A', 2);

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