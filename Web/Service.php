<?php
date_default_timezone_set('America/Bogota');
include_once "ConfigBD.php";

$Dato = $_POST["Dato"] ?? $_GET["Dato"] ?? '';
if (empty($Dato)) {
    echo json_encode(["status" => "error", "message" => "No telemetry data received"]);
    exit;
}

if (str_ends_with($Dato, "\r\n") || str_ends_with($Dato, "\n")) {
    $Dato = rtrim($Dato);
}

$Datos = explode(",", $Dato);
for ($i = 0; $i < 10; $i++) {
    if (!isset($Datos[$i]) || trim($Datos[$i]) === "NAN" || trim($Datos[$i]) === "nan" || trim($Datos[$i]) === "") {
        $Datos[$i] = 0;
    } else {
        $Datos[$i] = trim($Datos[$i]);
    }
}

$stmt = $db->prepare("INSERT INTO `Datos` (`T1`, `T2`, `TP`, `H1`, `H2`, `HP`, `NivelAgua`, `P1`, `P2`, `PP`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
$stmt->execute([
    $Datos[0], $Datos[1], $Datos[2], $Datos[3], $Datos[4],
    $Datos[5], $Datos[6], $Datos[7], $Datos[8], $Datos[9]
]);

echo "Ok";
?>
