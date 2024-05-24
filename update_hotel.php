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

// Update hotel data
if (isset($_POST['update_hotel'])) {
    $hotel_id = $_POST['hotel_id'];
    $hotelName = $_POST['hotelName'];
    $location = $_POST['location'];
    $description = $_POST['description'];

    // Perform server-side validation if necessary

    $query = $conn->prepare("UPDATE hotel SET hotelName=?, location=?, description=? WHERE id=?");
    $query->bind_param("sssi", $hotelName, $location, $description, $hotel_id);

    if ($query->execute()) {
        echo "Hotel data updated successfully!";
    } else {
        echo "Error updating hotel data: " . $query->error;
    }
}

// Fetch hotel data to be updated
$hotel_id = $_GET['id'];
$query = $conn->prepare("SELECT * FROM hotel WHERE id=?");
$query->bind_param("i", $hotel_id);
$query->execute();
$result = $query->get_result();
$hotel = $result->fetch_assoc();

// Close database connection
$conn->close();
?>
