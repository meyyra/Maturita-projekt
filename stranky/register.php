<?php
header('Content-Type: application/json');

// Připojení k databázi
$conn = new mysqli("dbs.spskladno.cz", "student8", "spsnet", "vyuka8");

if ($conn->connect_error) {
    echo json_encode(["success" => false, "error" => "Chyba při připojení k databázi"]);
    exit();
}

// Zpracování JSON dat
$data = json_decode(file_get_contents("php://input"), true);
$username = $data['username'];
$password = $data['password'];

// Kontrola, zda už jméno existuje
$stmt = $conn->prepare("SELECT * FROM 1Ausers WHERE username = ?");
$stmt->bind_param("s", $username);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows > 0) {
    echo json_encode(["success" => false, "error" => "Toto uživatelské jméno už existuje!"]);
    exit();
}

// Hashování hesla a uložení do DB
$hashed_password = password_hash($password, PASSWORD_DEFAULT);

$stmt = $conn->prepare("INSERT INTO 1Ausers (username, password) VALUES (?, ?)");
$stmt->bind_param("ss", $username, $hashed_password);

if ($stmt->execute()) {
    echo json_encode(["success" => true]);
} else {
    echo json_encode(["success" => false, "error" => "Chyba při registraci"]);
}

$conn->close();
?>
