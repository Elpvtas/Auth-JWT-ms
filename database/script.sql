BD CAMACHO -- Tabla Rol
CREATE TABLE Rol (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME DEFAULT NULL
);

-- Tabla Sector_Economico
CREATE TABLE Sector_Economico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME DEFAULT NULL
);

-- Tabla Empresa con relación a Sector_Economico
CREATE TABLE Empresa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    sector_economico_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME DEFAULT NULL,
    FOREIGN KEY (sector_economico_id) REFERENCES Sector_Economico(id)
);

-- Tabla País
CREATE TABLE Pais (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME DEFAULT NULL
);

-- Tabla Ciudad con relación a País
CREATE TABLE Ciudad (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    pais_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME DEFAULT NULL,
    FOREIGN KEY (pais_id) REFERENCES Pais(id)
);

-- Tabla Usuario
CREATE TABLE Usuario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    full_name VARCHAR(100),
    address VARCHAR(200),
    email VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    disabled BOOLEAN DEFAULT FALSE,
    rol INT,
    city INT,
    update_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME DEFAULT NULL,
    FOREIGN KEY (rol) REFERENCES Rol(id),
    FOREIGN KEY (city) REFERENCES Ciudad(id)
);

-- Tabla Contrato con las dos llaves foráneas para Usuario
CREATE TABLE Contrato (
    numero_contrato INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora_inicio DATETIME NOT NULL,
    fecha_hora_fin DATETIME,
    comision DECIMAL(10, 2),
    inversionista_id INT,
    comisionista_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME DEFAULT NULL,
    FOREIGN KEY (inversionista_id) REFERENCES Usuario(id),
    FOREIGN KEY (comisionista_id) REFERENCES Usuario(id)
);

-- Tabla Auditoría
CREATE TABLE Auditoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    accion VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_hora DATETIME NOT NULL,
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
);

-- Tabla Orden
CREATE TABLE Orden (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_orden VARCHAR(50) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    fecha_hora DATETIME NOT NULL,
    comision DECIMAL(10, 2),
    usuario_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME DEFAULT NULL,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
);

-- Tabla Historial_Orden
CREATE TABLE Historial_Orden (
    id INT AUTO_INCREMENT PRIMARY KEY,
    precio DECIMAL(10, 2) NOT NULL,
    tipo_orden VARCHAR(50) NOT NULL,
    fecha_hora DATETIME NOT NULL,
    comision DECIMAL(10, 2),
    orden_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME DEFAULT NULL,
    FOREIGN KEY (orden_id) REFERENCES Orden(id)
);

-- Tabla Acción
CREATE TABLE Accion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    valor DECIMAL(10, 2),
    fecha_hora DATETIME,
    empresa_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME DEFAULT NULL,
    FOREIGN KEY (empresa_id) REFERENCES Empresa(id)
);

-- Tabla Historial_Accion
CREATE TABLE Historial_Accion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    valor DECIMAL(10, 2),
    fecha_hora DATETIME NOT NULL,
    accion_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME DEFAULT NULL,
    FOREIGN KEY (accion_id) REFERENCES Accion(id)
);

INSERT INTO Rol (nombre, descripcion, created_at)
VALUES
  ('Admin', 'Sysadmin', NOW()),
  ('Accionista', 'Persona que posee acciones en la empresa', NOW()),
  ('Comisionista', 'Persona que recibe una comisión por intermediar en transacciones', NOW());

INSERT INTO Pais (nombre) VALUES 
('Ecuador'),
('Colombia'),
('Perú');


-- Ciudades para Ecuador
INSERT INTO Ciudad (nombre, pais_id) VALUES 
('Quito', 1),
('Guayaquil', 1),
('Cuenca', 1);

-- Ciudades para Colombia
INSERT INTO Ciudad (nombre, pais_id) VALUES 
('Bogotá', 2),
('Medellín', 2),
('Cali', 2);

-- Ciudades para Perú
INSERT INTO Ciudad (nombre, pais_id) VALUES 
('Lima', 3),
('Arequipa', 3),
('Cusco', 3);

INSERT INTO Sector_Economico (nombre, descripcion, created_at)
VALUES
  ('Agricultura', 'Sector dedicado a la producción de productos agrícolas, como cultivos y ganado.', NOW()),
  ('Industria', 'Sector que abarca la producción de bienes a través de la transformación de recursos naturales.', NOW()),
  ('Servicios', 'Sector que incluye actividades económicas relacionadas con la prestación de servicios en diversas áreas como educación, salud, y turismo.', NOW()),
  ('Tecnología', 'Sector dedicado a la innovación, desarrollo y comercialización de productos y servicios tecnológicos.', NOW()),
  ('Energía', 'Sector que comprende la producción, distribución y comercialización de energía eléctrica, gas y otras fuentes de energía.', NOW()),
  ('Comercio', 'Sector dedicado a la compra y venta de bienes y servicios, tanto al por mayor como al por menor.', NOW()),
  ('Construcción', 'Sector que se encarga de la edificación de infraestructuras residenciales, comerciales e industriales.', NOW()),
  ('Transporte', 'Sector dedicado a la movilización de personas y mercancías, ya sea por carretera, ferrocarril, aéreo o marítimo.', NOW()),
  ('Finanzas', 'Sector que incluye actividades relacionadas con bancos, seguros, inversiones y mercados financieros.', NOW()),
  ('Turismo', 'Sector que abarca todas las actividades económicas relacionadas con el servicio y la atención a turistas.', NOW());



INSERT INTO Usuario (
    id,
    username,
    full_name,
    address,
    email,
    hashed_password,
    disabled,
    rol,
    city,
    update_at,
    deleted_at
) VALUES (
    1,
    'admin',
    'John Doe',
    '123 Main St',
    'johndoe@example.com',
    '$2b$12$nOnxeOwO1MXHUdR/9iaVbujOes.eUFjhlrKp90eDFc6co4KP4p0DO',
    FALSE,
    1,   -- ID del rol
    1,   -- ID de la ciudad
    NULL,
    NULL
);


INSERT INTO Usuario (
    id,
    username,
    full_name,
    address,
    email,
    hashed_password,
    disabled,
    rol,
    city,
    update_at,
    deleted_at
)
VALUES 
  (2,'Inversionista Juan', 'juan.inversionista@example.com', '$2b$12$nOnxeOwO1MXHUdR/9iaVbujOes.eUFjhlrKp90eDFc6co4KP4p0DO', 2, NOW()), -- rol_id 2 = Accionista
  (3,'Comisionista Laura', 'laura.comisionista@example.com', '$2b$12$nOnxeOwO1MXHUdR/9iaVbujOes.eUFjhlrKp90eDFc6co4KP4p0DO', 3, NOW()); -- rol_id 3 = Comisionista
