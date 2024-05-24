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

// Update admin
if (isset($_POST['update_admin'])) {
    $guest_id = $_POST['guest_id'];
    $username = $_POST['username'];
    $email = $_POST['email'];

    // Perform server-side validation if necessary

    $query = $conn->prepare("UPDATE guest SET username=?, email=? WHERE id=?");
    $query->bind_param("ssi", $username, $email, $admin_id);

    if ($query->execute()) {
        echo "Admin updated successfully!";
    } else {
        echo "Error updating admin: " . $query->error;
    }
}

// Fetch admin data to be updated
$admin_id = $_GET['id'];
$query = $conn->prepare("SELECT * FROM guest WHERE id=?");
$query->bind_param("i", $admin_id);
$query->execute();
$result = $query->get_result();
$admin = $result->fetch_assoc();

// Close database connection
$conn->close();
?>