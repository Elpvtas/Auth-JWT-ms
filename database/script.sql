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
) VALUES (
    1,
    'accionista',
    'John Doe1',
    '123 Main St',
    'johndoe@example.com',
    '$2b$12$nOnxeOwO1MXHUdR/9iaVbujOes.eUFjhlrKp90eDFc6co4KP4p0DO',
    FALSE,
    1,   -- ID del rol
    1,   -- ID de la ciudad
    NULL,
    NULL
);

INSERT INTO Empresa (id, nombre, descripcion, sector_economico_id) VALUES
(1, 'ECO', 'ECO INC', 7),
(2, 'MSFT', 'MSFT INC', 10),
(3, 'GOOGL', 'GOOGL INC', 3),
(4, 'AMZN', 'AMZN INC', 4),
(5, 'META', 'META INC', 6),
(6, 'TSLA', 'TSLA INC', 2),
(7, 'NVDA', 'NVDA INC', 6),
(8, 'BRK.B', 'BRK.B INC', 9),
(9, 'JPM', 'JPM INC', 5),
(10, 'JNJ', 'JNJ INC', 4),
(11, 'V', 'V INC', 4),
(12, 'UNH', 'UNH INC', 2),
(13, 'HD', 'HD INC', 7),
(14, 'PG', 'PG INC', 9),
(15, 'XOM', 'XOM INC', 10),
(16, 'MA', 'MA INC', 10),
(17, 'PFE', 'PFE INC', 6),
(18, 'KO', 'KO INC', 6),
(19, 'DIS', 'DIS INC', 9),
(20, 'NFLX', 'NFLX INC', 1),
(21, 'INTC', 'INTC INC', 7),
(22, 'BA', 'BA INC', 4),
(23, 'WMT', 'WMT INC', 7),
(24, 'CSCO', 'CSCO INC', 7),
(25, 'PYPL', 'PYPL INC', 8),
(26, 'T', 'T INC', 7),
(27, 'VZ', 'VZ INC', 10),
(28, 'UNP', 'UNP INC', 5),
(29, 'MMM', 'MMM INC', 8),
(30, 'CAT', 'CAT INC', 1),
(31, 'RTX', 'RTX INC', 2),
(32, 'GS', 'GS INC', 9),
(33, 'BABA', 'BABA INC', 3),
(34, 'MRK', 'MRK INC', 8),
(35, 'IBM', 'IBM INC', 5),
(36, 'ACN', 'ACN INC', 10),
(37, 'MS', 'MS INC', 7),
(38, 'LMT', 'LMT INC', 7),
(39, 'CVX', 'CVX INC', 2),
(40, 'AMGN', 'AMGN INC', 10),
(41, 'AMT', 'AMT INC', 3),
(42, 'CL', 'CL INC', 10),
(43, 'BIIB', 'BIIB INC', 7),
(44, 'SPG', 'SPG INC', 10),
(45, 'COF', 'COF INC', 9),
(46, 'MCD', 'MCD INC', 6),
(47, 'COP', 'COP INC', 4),
(48, 'WBA', 'WBA INC', 1),
(49, 'CB', 'CB INC', 8),
(50, 'NSC', 'NSC INC', 1),
(51, 'SLB', 'SLB INC', 6),
(52, 'SYK', 'SYK INC', 6),
(53, 'TMO', 'TMO INC', 9),
(54, 'DHR', 'DHR INC', 7),
(55, 'LHX', 'LHX INC', 1),
(56, 'ZTS', 'ZTS INC', 10),
(57, 'ISRG', 'ISRG INC', 1),
(58, 'SYY', 'SYY INC', 3),
(59, 'ADBE', 'ADBE INC', 10),
(60, 'MDT', 'MDT INC', 2),
(61, 'COST', 'COST INC', 10),
(62, 'MSCI', 'MSCI INC', 8),
(63, 'SBUX', 'SBUX INC', 4),
(64, 'GM', 'GM INC', 3),
(65, 'F', 'F INC', 2),
(66, 'ADP', 'ADP INC', 2),
(67, 'AXP', 'AXP INC', 7),
(68, 'FIS', 'FIS INC', 7),
(69, 'FISV', 'FISV INC', 4),
(70, 'AIG', 'AIG INC', 6),
(71, 'TDG', 'TDG INC', 4),
(72, 'PXD', 'PXD INC', 1),
(73, 'EOG', 'EOG INC', 10),
(74, 'PLD', 'PLD INC', 2),
(75, 'CME', 'CME INC', 3),
(76, 'VRTX', 'VRTX INC', 10),
(77, 'DE', 'DE INC', 2),
(78, 'BMY', 'BMY INC', 9),
(79, 'ZBH', 'ZBH INC', 7),
(80, 'KMB', 'KMB INC', 5),
(81, 'NTAP', 'NTAP INC', 4),
(82, 'APD', 'APD INC', 7),
(83, 'STZ', 'STZ INC', 8),
(84, 'WM', 'WM INC', 3),
(85, 'PSA', 'PSA INC', 1),
(86, 'EQIX', 'EQIX INC', 3),
(87, 'CCI', 'CCI INC', 10),
(88, 'PGR', 'PGR INC', 5),
(89, 'AFL', 'AFL INC', 10),
(90, 'OXY', 'OXY INC', 4),
(91, 'DD', 'DD INC', 8),
(92, 'LRCX', 'LRCX INC', 8),
(93, 'EFX', 'EFX INC', 2),
(94, 'MU', 'MU INC', 2),
(95, 'CSX', 'CSX INC', 8),
(96, 'BAX', 'BAX INC', 2),
(97, 'INTU', 'INTU INC', 6),
(98, 'HUM', 'HUM INC', 1),
(99, 'HLT', 'HLT INC', 8),
(100, 'TGT', 'TGT INC', 4),
(101, 'GIS', 'GIS INC', 3),
(102, 'CHTR', 'CHTR INC', 6),
(103, 'GILD', 'GILD INC', 8),
(104, 'MRNA', 'MRNA INC', 8),
(105, 'KLAC', 'KLAC INC', 6),
(106, 'PEP', 'PEP INC', 3),
(107, 'MELI', 'MELI INC', 6),
(108, 'XEL', 'XEL INC', 5),
(109, 'RSG', 'RSG INC', 5),
(110, 'CNC', 'CNC INC', 9),
(111, 'CBOE', 'CBOE INC', 9),
(112, 'EXC', 'EXC INC', 5),
(113, 'LUV', 'LUV INC', 2),
(114, 'REGN', 'REGN INC', 5),
(115, 'AMAT', 'AMAT INC', 8),
(116, 'DXC', 'DXC INC', 8),
(117, 'NOC', 'NOC INC', 4),
(118, 'C', 'C INC', 2),
(119, 'WDC', 'WDC INC', 5),
(120, 'UBER', 'UBER INC', 6),
(121, 'COO', 'COO INC', 6),
(122, 'CTSH', 'CTSH INC', 3),
(123, 'SBAC', 'SBAC INC', 8),
(124, 'AON', 'AON INC', 7),
(125, 'SRE', 'SRE INC', 10),
(126, 'HCA', 'HCA INC', 8),
(127, 'STT', 'STT INC', 5),
(128, 'VLO', 'VLO INC', 9),
(129, 'CARR', 'CARR INC', 8),
(130, 'VFC', 'VFC INC', 5),
(131, 'LULU', 'LULU INC', 9),
(132, 'TROW', 'TROW INC', 3),
(133, 'CTAS', 'CTAS INC', 3),
(134, 'RTN', 'RTN INC', 6),
(135, 'ABBV', 'ABBV INC', 7),
(136, 'BDX', 'BDX INC', 2),
(137, 'EMR', 'EMR INC', 2),
(138, 'TSN', 'TSN INC', 1),
(139, 'SWKS', 'SWKS INC', 2),
(140, 'WELL', 'WELL INC', 1),
(141, 'TFX', 'TFX INC', 5),
(142, 'CHD', 'CHD INC', 9),
(143, 'WMB', 'WMB INC', 10),
(144, 'GE', 'GE INC', 1),
(145, 'AVGO', 'AVGO INC', 6),
(146, 'WEC', 'WEC INC', 7),
(147, 'DOV', 'DOV INC', 2),
(148, 'FTV', 'FTV INC', 7),
(149, 'MCHP', 'MCHP INC', 10),
(150, 'USB', 'USB INC', 9),
(151, 'CPB', 'CPB INC', 9),
(152, 'NUE', 'NUE INC', 2),
(153, 'OKE', 'OKE INC', 3),
(154, 'AVY', 'AVY INC', 1),
(155, 'SO', 'SO INC', 2),
(156, 'MRO', 'MRO INC', 9),
(157, 'SJM', 'SJM INC', 9),
(158, 'TAP', 'TAP INC', 1),
(159, 'XRX', 'XRX INC', 4),
(160, 'NEM', 'NEM INC', 1),
(161, 'RCL', 'RCL INC', 1),
(162, 'ZBRA', 'ZBRA INC', 7),
(163, 'RHI', 'RHI INC', 8),
(164, 'PNC', 'PNC INC', 6),
(165, 'ABT', 'ABT INC', 10),
(166, 'APTV', 'APTV INC', 4),
(167, 'EQR', 'EQR INC', 5),
(168, 'JCI', 'JCI INC', 4),
(169, 'SNA', 'SNA INC', 1),
(170, 'IDXX', 'IDXX INC', 10),
(171, 'ETN', 'ETN INC', 3),
(172, 'ORLY', 'ORLY INC', 9),
(173, 'TRV', 'TRV INC', 8),
(174, 'GPC', 'GPC INC', 8),
(175, 'VTRS', 'VTRS INC', 7),
(176, 'FTNT', 'FTNT INC', 10),
(177, 'IQV', 'IQV INC', 1),
(178, 'HAS', 'HAS INC', 1),
(179, 'ORCL', 'ORCL INC', 5),
(180, 'TYL', 'TYL INC', 8),
(181, 'PKG', 'PKG INC', 5),
(182, 'SHW', 'SHW INC', 5),
(183, 'NVR', 'NVR INC', 9),
(184, 'FFIV', 'FFIV INC', 8),
(185, 'MCO', 'MCO INC', 6),
(186, 'HRL', 'HRL INC', 6),
(187, 'CBRE', 'CBRE INC', 8),
(188, 'EXR', 'EXR INC', 1),
(189, 'LYB', 'LYB INC', 2),
(190, 'RHT', 'RHT INC', 2),
(191, 'AEE', 'AEE INC', 6),
(192, 'TPR', 'TPR INC', 4),
(193, 'CLX', 'CLX INC', 8),
(194, 'MKTX', 'MKTX INC', 5),
(195, 'SPLK', 'SPLK INC', 5),
(196, 'NKE', 'NKE INC', 7),
(197, 'RMD', 'RMD INC', 10),
(198, 'HES', 'HES INC', 9),
(199, 'HII', 'HII INC', 2),
(200, 'HOLX', 'HOLX INC', 4),
(201, 'VRSN', 'VRSN INC', 7),
(202, 'VRTS', 'VRTS INC', 1),
(203, 'TRIP', 'TRIP INC', 7),
(204, 'FMC', 'FMC INC', 5),
(205, 'AAPL', 'AAPL INC', 8),
(206, 'BXP', 'BXP INC', 8),
(207, 'SNPS', 'SNPS INC', 4),
(208, 'KMX', 'KMX INC', 2),
(209, 'CPRT', 'CPRT INC', 1),
(210, 'ANET', 'ANET INC', 8),
(211, 'MKC', 'MKC INC', 2),
(212, 'IFF', 'IFF INC', 9),
(213, 'NWL', 'NWL INC', 4),
(214, 'GRMN', 'GRMN INC', 6),
(215, 'HRS', 'HRS INC', 4),
(216, 'TPX', 'TPX INC', 7),
(217, 'ALB', 'ALB INC', 1),
(218, 'ESS', 'ESS INC', 4),
(219, 'AEP', 'AEP INC', 3),
(220, 'GOOG', 'GOOG INC', 10),
(221, 'HPE', 'HPE INC', 9),
(222, 'PRU', 'PRU INC', 10),
(223, 'CE', 'CE INC', 4),
(224, 'CVS', 'CVS INC', 2),
(225, 'SNAP', 'SNAP INC', 5),
(226, 'ANSS', 'ANSS INC', 2),
(227, 'FB', 'FB INC', 9),
(228, 'SPGI', 'SPGI INC', 6),
(229, 'NEE', 'NEE INC', 2),
(230, 'MCK', 'MCK INC', 8),
(231, 'LOW', 'LOW INC', 10),
(232, 'OMC', 'OMC INC', 1),
(233, 'FLIR', 'FLIR INC', 8);


