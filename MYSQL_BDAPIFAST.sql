CREATE DATABASE BDAPIFast;

USE BDAPIFast;

CREATE TABLE producto (
    id VARCHAR(50) PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    pre DOUBLE NOT NULL DEFAULT 0.0,
    rang INT NOT NULL DEFAULT 0,
    Img VARCHAR(255) NOT NULL
);

INSERT INTO producto (id, nom, pre, rang, Img) VALUES
('P001', 'Teclado Mecánico', 59.99, 5, 'https://example.com/teclado.jpg'),
('P002', 'Mouse Gamer', 29.99, 4, 'https://example.com/mouse.jpg'),
('P003', 'Monitor 24"', 199.99, 5, 'https://example.com/monitor.jpg'),
('P004', 'Silla Ergonómica', 129.99, 4, 'https://example.com/silla.jpg'),
('P005', 'Laptop Core i7', 799.99, 5, 'https://example.com/laptop.jpg'),
('P006', 'Auriculares Bluetooth', 49.99, 4, 'https://example.com/auriculares.jpg'),
('P007', 'Disco SSD 1TB', 89.99, 5, 'https://example.com/ssd.jpg'),
('P008', 'Impresora Multifunción', 149.99, 3, 'https://example.com/impresora.jpg'),
('P009', 'Tablet 10"', 299.99, 4, 'https://example.com/tablet.jpg'),
('P010', 'Cámara Web HD', 39.99, 4, 'https://example.com/camara.jpg');
