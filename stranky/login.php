<?php

$servername = "dbs.spskladno.cz";
$username = "student8";
$password = "spsnet";
$dbname = "vyuka8";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$data = json_decode(file_get_contents("php://input"), true);

$username = $data['username'];
$password = $data['password'];

$sql = "SELECT id, password, points FROM 1Ausers WHERE username = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $username);
$stmt->execute();
$stmt->bind_result($userId, $hashed_password, $points);
$stmt->fetch();

if ($hashed_password && password_verify($password, $hashed_password)) {
    echo json_encode([
        "success" => true,
        "userId" => $userId,
        "username" => $username,
        "points" => $points
    ]);
} else {
    echo json_encode(["success" => false, "message" => "Chybné jméno nebo heslo!"]);
}

$stmt->close();
$conn->close();
?>
