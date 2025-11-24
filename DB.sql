-- SCRIPT COMPLETO CORREGIDO
-- ========================================================

IF DB_ID(N'ClinicaDB') IS NULL
BEGIN
    CREATE DATABASE ClinicaDB;
END
GO

USE ClinicaDB;
GO

-- =========================
-- TABLAS EXISTENTES 
-- =========================

IF OBJECT_ID(N'dbo.Productos', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Productos (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Nombre NVARCHAR(100) NOT NULL,
        Stock INT NOT NULL,
        FechaVencimiento DATE NOT NULL
    );
END
GO

IF OBJECT_ID(N'dbo.Usuarios', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Usuarios (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Nombre NVARCHAR(100) NOT NULL,
        Password NVARCHAR(200) NOT NULL,
        Rol NVARCHAR(50) NOT NULL,
        Estado NVARCHAR(20) DEFAULT 'Activo'
    );
END
GO

IF OBJECT_ID(N'dbo.Movimientos', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Movimientos (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Producto NVARCHAR(100) NOT NULL,
        Tipo NVARCHAR(20) NOT NULL,
        Cantidad INT NOT NULL,
        Usuario NVARCHAR(50) NOT NULL,
        Fecha DATE NOT NULL
    );
END
GO

-- =========================
-- NUEVAS TABLAS PARA EL MÓDULO DE CITAS
-- =========================

IF OBJECT_ID(N'dbo.Especialidades', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Especialidades (
        IdEspecialidad INT IDENTITY(1,1) PRIMARY KEY,
        Nombre NVARCHAR(100) NOT NULL UNIQUE
    );
END
GO

IF OBJECT_ID(N'dbo.Doctores', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Doctores (
        IdDoctor INT IDENTITY(1,1) PRIMARY KEY,
        Nombre NVARCHAR(150) NOT NULL,
        EspecialidadId INT NULL,
        CONSTRAINT FK_Doctor_Especialidad FOREIGN KEY (EspecialidadId) REFERENCES dbo.Especialidades(IdEspecialidad)
    );
END
GO

IF OBJECT_ID(N'dbo.Pacientes', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Pacientes (
        IdPaciente INT IDENTITY(1,1) PRIMARY KEY,
        Nombre NVARCHAR(150) NOT NULL,
        Cedula NVARCHAR(50) NULL,
        Telefono NVARCHAR(50) NULL,
        Correo NVARCHAR(150) NULL
    );
END
GO

-- PRIMERO crear la tabla Citas normal
IF OBJECT_ID(N'dbo.Citas', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Citas (
        IdCita INT IDENTITY(1,1) PRIMARY KEY,
        IdPaciente INT NOT NULL,
        IdDoctor INT NOT NULL,
        FechaCita DATETIME NOT NULL,
        Estado NVARCHAR(20) NOT NULL DEFAULT 'Pendiente',
        Observaciones NVARCHAR(255) NULL,
        CONSTRAINT FK_Citas_Paciente FOREIGN KEY (IdPaciente) REFERENCES dbo.Pacientes(IdPaciente),
        CONSTRAINT FK_Citas_Doctor FOREIGN KEY (IdDoctor) REFERENCES dbo.Doctores(IdDoctor)
    );
END
GO

-- LUEGO crear CitasFlexibles SIMPLIFICADA
IF OBJECT_ID(N'dbo.CitasFlexibles', N'U') IS NOT NULL
    DROP TABLE dbo.CitasFlexibles;
GO

-- Crear CitasFlexibles SIMPLIFICADA - SOLO COLUMNAS NECESARIAS
CREATE TABLE dbo.CitasFlexibles (
    IdCita INT IDENTITY(1,1) PRIMARY KEY,
    Paciente NVARCHAR(150) NOT NULL,
    Doctor NVARCHAR(150) NOT NULL,
    Especialidad NVARCHAR(100) NOT NULL,
    FechaCita DATETIME NOT NULL,
    Observaciones NVARCHAR(255) NULL,
    Estado NVARCHAR(20) NOT NULL DEFAULT 'Pendiente',
    UsuarioCreacion NVARCHAR(100) NOT NULL,
    FechaCreacion DATETIME NOT NULL DEFAULT GETDATE()
);
GO

-- =========================
-- ÍNDICES
-- =========================

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Citas_IdDoctor_Fecha')
BEGIN
    CREATE INDEX IX_Citas_IdDoctor_Fecha ON dbo.Citas (IdDoctor, FechaCita);
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Pacientes_Nombre')
BEGIN
    CREATE INDEX IX_Pacientes_Nombre ON dbo.Pacientes (Nombre);
END
GO

-- =========================
-- DATOS DE PRUEBA
-- =========================

-- Productos
IF NOT EXISTS (SELECT 1 FROM dbo.Productos WHERE Nombre = 'Paracetamol 500mg')
BEGIN
    INSERT INTO dbo.Productos (Nombre, Stock, FechaVencimiento) VALUES
    ('Paracetamol 500mg', 50, '2025-12-31'),
    ('Amoxicilina 500mg', 30, '2025-11-30'),
    ('Ibuprofeno 400mg', 15, '2025-10-31'),
    ('Aspirina', 20, '2025-09-30'),
    ('Omeprazol 20mg', 5, '2025-08-31');
END
GO

-- Usuarios (password: "password" en SHA-256)
IF NOT EXISTS (SELECT 1 FROM dbo.Usuarios WHERE Nombre = 'admin')
BEGIN
    INSERT INTO dbo.Usuarios (Nombre, Password, Rol, Estado) VALUES
    ('admin', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Administrador', 'Activo'),
    ('medico1', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Médico', 'Activo'),
    ('enfermero1', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Enfermero', 'Activo'),
    ('recepcionista1', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Recepcionista', 'Activo');
END
GO

-- Movimientos iniciales
IF NOT EXISTS (SELECT 1 FROM dbo.Movimientos)
BEGIN
    INSERT INTO dbo.Movimientos (Producto, Tipo, Cantidad, Usuario, Fecha) VALUES
    ('Paracetamol 500mg', 'ENTRADA', 50, 'admin', '2025-01-01'),
    ('Amoxicilina 500mg', 'ENTRADA', 30, 'admin', '2025-01-02'),
    ('Ibuprofeno 400mg', 'ENTRADA', 15, 'admin', '2025-01-03'),
    ('Aspirina', 'ENTRADA', 20, 'admin', '2025-01-04'),
    ('Omeprazol 20mg', 'ENTRADA', 5, 'admin', '2025-01-05');
END
GO

-- Especialidades
IF NOT EXISTS (SELECT 1 FROM dbo.Especialidades WHERE Nombre = 'Cardiología')
BEGIN
    INSERT INTO dbo.Especialidades (Nombre) VALUES
    ('Cardiología'),
    ('Medicina General'),
    ('Pediatría'),
    ('Ginecología'),
    ('Dermatología'),
    ('Ortopedia');
END
GO

-- Doctores
IF NOT EXISTS (SELECT 1 FROM dbo.Doctores WHERE Nombre = 'Dr. Pedro Pérez')
BEGIN
    DECLARE @CardioId INT = (SELECT IdEspecialidad FROM dbo.Especialidades WHERE Nombre = 'Cardiología');
    DECLARE @MedGenId INT = (SELECT IdEspecialidad FROM dbo.Especialidades WHERE Nombre = 'Medicina General');
    DECLARE @PediaId INT = (SELECT IdEspecialidad FROM dbo.Especialidades WHERE Nombre = 'Pediatría');
    DECLARE @GinecoId INT = (SELECT IdEspecialidad FROM dbo.Especialidades WHERE Nombre = 'Ginecología');
    DECLARE @DermaId INT = (SELECT IdEspecialidad FROM dbo.Especialidades WHERE Nombre = 'Dermatología');
    DECLARE @OrtopId INT = (SELECT IdEspecialidad FROM dbo.Especialidades WHERE Nombre = 'Ortopedia');

    INSERT INTO dbo.Doctores (Nombre, EspecialidadId) VALUES
    ('Dr. Pedro Pérez', @CardioId),
    ('Dra. Ana Gómez', @MedGenId),
    ('Dr. Luis Ortega', @PediaId),
    ('Dra. Carmen Ruiz', @GinecoId),
    ('Dr. Roberto Sánchez', @DermaId),
    ('Dra. Laura Mendoza', @OrtopId);
END
GO

-- Pacientes
IF NOT EXISTS (SELECT 1 FROM dbo.Pacientes WHERE Nombre = 'Juan Pérez')
BEGIN
    INSERT INTO dbo.Pacientes (Nombre, Cedula, Telefono, Correo) VALUES
    ('Juan Pérez', '001-000000-0000A', '8888-0001', 'juan.perez@example.com'),
    ('María López', '001-000000-0000B', '8888-0002', 'maria.lopez@example.com'),
    ('Carlos Sánchez', '001-000000-0000C', '8888-0003', 'carlos.sanchez@example.com'),
    ('Laura García', '001-000000-0000D', '8888-0004', 'laura.garcia@example.com');
END
GO

-- Citas de ejemplo
IF NOT EXISTS (SELECT 1 FROM dbo.Citas)
BEGIN
    DECLARE @IdPac1 INT = (SELECT TOP 1 IdPaciente FROM dbo.Pacientes WHERE Nombre = 'Juan Pérez');
    DECLARE @IdPac2 INT = (SELECT TOP 1 IdPaciente FROM dbo.Pacientes WHERE Nombre = 'María López');
    DECLARE @IdPac3 INT = (SELECT TOP 1 IdPaciente FROM dbo.Pacientes WHERE Nombre = 'Carlos Sánchez');
    DECLARE @IdPac4 INT = (SELECT TOP 1 IdPaciente FROM dbo.Pacientes WHERE Nombre = 'Laura García');
    
    DECLARE @Doc1 INT = (SELECT TOP 1 IdDoctor FROM dbo.Doctores WHERE Nombre = 'Dr. Pedro Pérez');
    DECLARE @Doc2 INT = (SELECT TOP 1 IdDoctor FROM dbo.Doctores WHERE Nombre = 'Dra. Ana Gómez');
    DECLARE @Doc3 INT = (SELECT TOP 1 IdDoctor FROM dbo.Doctores WHERE Nombre = 'Dr. Luis Ortega');

    INSERT INTO dbo.Citas (IdPaciente, IdDoctor, FechaCita, Estado, Observaciones) VALUES
    (@IdPac1, @Doc1, DATEADD(DAY, 1, GETDATE()), 'Pendiente', 'Chequeo cardiovascular'),
    (@IdPac2, @Doc2, DATEADD(DAY, 2, GETDATE()), 'Pendiente', 'Control general'),
    (@IdPac3, @Doc3, DATEADD(DAY, 3, GETDATE()), 'Pendiente', 'Control pediátrico'),
    (@IdPac4, @Doc1, DATEADD(DAY, 4, GETDATE()), 'Pendiente', 'Consulta cardiológica');
END
GO

-- Insertar datos de prueba en CitasFlexibles (VERSIÓN CORREGIDA)
IF NOT EXISTS (SELECT 1 FROM dbo.CitasFlexibles)
BEGIN
    INSERT INTO dbo.CitasFlexibles (Paciente, Doctor, Especialidad, FechaCita, Estado, UsuarioCreacion, Observaciones) VALUES
    ('Juan Pérez', 'Dr. Pedro Pérez', 'Cardiología', DATEADD(DAY, 1, GETDATE()), 'Pendiente', 'sistema', 'Chequeo cardiovascular'),
    ('María López', 'Dra. Ana Gómez', 'Medicina General', DATEADD(DAY, 2, GETDATE()), 'Pendiente', 'sistema', 'Control general'),
    ('Carlos Sánchez', 'Dr. Luis Ortega', 'Pediatría', DATEADD(DAY, 3, GETDATE()), 'Pendiente', 'sistema', 'Control pediátrico');
END
GO

-- =========================
-- TRIGGER CORREGIDO
-- =========================
IF OBJECT_ID(N'dbo.trg_Movimientos_UpdateStock', N'TR') IS NOT NULL
    DROP TRIGGER dbo.trg_Movimientos_UpdateStock;
GO

CREATE TRIGGER dbo.trg_Movimientos_UpdateStock
ON dbo.Movimientos
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    
    UPDATE p
    SET Stock = CASE 
        WHEN i.Tipo = 'ENTRADA' THEN p.Stock + i.Cantidad
        WHEN i.Tipo IN ('SALIDA', 'BAJA') THEN p.Stock - i.Cantidad
        WHEN i.Tipo = 'REPOSICIÓN' THEN p.Stock + i.Cantidad
        ELSE p.Stock
    END
    FROM dbo.Productos p
    INNER JOIN inserted i ON p.Nombre = i.Producto;
END
GO

PRINT '=========================================';
PRINT '✅ BASE DE DATOS CLINICA DB CONFIGURADA CORRECTAMENTE';
PRINT '✅ Tabla CitasFlexibles creada SIN columnas problemáticas';
PRINT '✅ Datos de prueba insertados CORRECTAMENTE';
PRINT '✅ Script completo ejecutado sin errores';
PRINT '=========================================';
