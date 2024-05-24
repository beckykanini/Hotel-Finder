<?php
// Start the session
session_start();

// Check if the user is logged in as admin
if (!isset($_SESSION['admin_logged_in']) || $_SESSION['admin_logged_in'] !== true) {
    header("Location: login.php");
    exit;
}

// Database connection parameters
$servername = "localhost";
$usernameDB = "root";
$passwordDB = "";
$dbname = "hrs";

// Create connection
$conn = new mysqli($servername, $usernameDB, $passwordDB, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Update hotelier
if (isset($_POST['update_hotelier'])) {
    $hotelier_id = $_POST['hotelier_id'];
    $hotelier_name = $_POST['hotelier_name'];
    $email = $_POST['email'];

    // Perform server-side validation if necessary

    $query = $conn->prepare("UPDATE hotelier SET hotelier_name=?, email=? WHERE id=?");
    $query->bind_param("ssi", $hotelier_name, $email, $hotelier_id);

    if ($query->execute()) {
        echo "Hotelier updated successfully!";
    } else {
        echo "Error updating hotelier: " . $query->error;
    }
}

// Fetch hotelier data to be updated
$hotelier_id = $_GET['id'];
$query = $conn->prepare("SELECT * FROM hotelier WHERE id=?");
$query->bind_param("i", $hotelier_id);
$query->execute();
$result = $query->get_result();
$hotelier = $result->fetch_assoc();

// Close database connection
$conn->close();
?>