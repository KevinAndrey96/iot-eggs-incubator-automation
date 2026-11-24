-- IoT Egg Incubator Database Initialization Schema & Demo Telemetry
CREATE DATABASE IF NOT EXISTS `shape_incubadora` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `shape_incubadora`;

DROP TABLE IF EXISTS `Datos`;
CREATE TABLE `Datos` (
    `IdDato` INT AUTO_INCREMENT PRIMARY KEY,
    `FechaYHora` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `T1` DECIMAL(5,2) NOT NULL DEFAULT 37.50 COMMENT 'DS18B20 Temperature Sensor 1 (deg C)',
    `T2` DECIMAL(5,2) NOT NULL DEFAULT 37.60 COMMENT 'DS18B20 Temperature Sensor 2 (deg C)',
    `TP` DECIMAL(5,2) NOT NULL DEFAULT 37.55 COMMENT 'Average Temperature (deg C)',
    `H1` DECIMAL(5,2) NOT NULL DEFAULT 60.20 COMMENT 'DHT22 Relative Humidity Sensor 1 (%)',
    `H2` DECIMAL(5,2) NOT NULL DEFAULT 59.80 COMMENT 'DHT22 Relative Humidity Sensor 2 (%)',
    `HP` DECIMAL(5,2) NOT NULL DEFAULT 60.00 COMMENT 'Average Relative Humidity (%)',
    `NivelAgua` DECIMAL(5,2) NOT NULL DEFAULT 22.50 COMMENT 'Ultrasonic Reservoir Water Level (cm)',
    `P1` DECIMAL(6,2) NOT NULL DEFAULT 58.40 COMMENT 'HX711 Strain Gauge Load Cell 1 (grams)',
    `P2` DECIMAL(6,2) NOT NULL DEFAULT 59.10 COMMENT 'HX711 Strain Gauge Load Cell 2 (grams)',
    `PP` DECIMAL(6,2) NOT NULL DEFAULT 58.75 COMMENT 'Average Egg Tray Weight (grams)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Realistic 21-Day Gallus Gallus Domesticus (Chicken) Embryo Incubation Telemetry
INSERT INTO `Datos` (`FechaYHora`, `T1`, `T2`, `TP`, `H1`, `H2`, `HP`, `NivelAgua`, `P1`, `P2`, `PP`) VALUES
(NOW() - INTERVAL 24 HOUR, 37.50, 37.54, 37.52, 58.90, 59.20, 59.05, 24.50, 60.40, 60.80, 60.60),
(NOW() - INTERVAL 21 HOUR, 37.55, 37.58, 37.57, 59.40, 59.60, 59.50, 24.10, 60.20, 60.60, 60.40),
(NOW() - INTERVAL 18 HOUR, 37.60, 37.52, 37.56, 60.10, 59.80, 59.95, 23.80, 60.00, 60.40, 60.20),
(NOW() - INTERVAL 15 HOUR, 37.48, 37.62, 37.55, 60.40, 60.20, 60.30, 23.40, 59.80, 60.20, 60.00),
(NOW() - INTERVAL 12 HOUR, 37.52, 37.58, 37.55, 59.80, 60.10, 59.95, 23.00, 59.60, 60.00, 59.80),
(NOW() - INTERVAL 9 HOUR,  37.58, 37.54, 37.56, 60.30, 60.00, 60.15, 22.60, 59.40, 59.80, 59.60),
(NOW() - INTERVAL 6 HOUR,  37.55, 37.58, 37.56, 60.20, 60.10, 60.15, 22.20, 59.10, 59.50, 59.30),
(NOW() - INTERVAL 3 HOUR,  37.50, 37.52, 37.51, 60.00, 59.90, 59.95, 21.80, 58.80, 59.30, 59.05),
(NOW() - INTERVAL 1 HOUR,  37.54, 37.60, 37.57, 59.90, 60.20, 60.05, 21.40, 58.50, 59.10, 58.80),
(NOW(),                     37.60, 37.58, 37.59, 60.20, 60.10, 60.15, 21.10, 58.30, 58.80, 58.55);
