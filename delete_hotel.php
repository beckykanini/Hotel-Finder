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

// Check if hotel ID is set
if (isset($_GET['id'])) {
    $hotel_id = $_GET['id'];

    // Prepare SQL statement to delete hotel
    $query = $conn->prepare("DELETE FROM hotel WHERE id=?");
    $query->bind_param("i", $hotel_id);

    if ($query->execute()) {
        echo "Hotel deleted successfully!";
    } else {
        echo "Error deleting hotel: " . $query->error;
    }
} else {
    echo "Hotel ID not specified.";
}

// Close database connection
$conn->close();
?>