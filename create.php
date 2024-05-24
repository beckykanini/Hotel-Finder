<?php
// Start the session
session_start();

// Check if user form is submitted
if (!isset($_POST['username'], $_POST['email'], $_POST['passwd'], $_POST['conf_passwd'])) {
    header("Location: /admin.html");
    exit;
}

// Retrieve user form data
$username = $_POST['username'];
$email = $_POST['email'];
$passwd = $_POST['passwd'];
$conf_passwd = $_POST['conf_passwd'];

// Perform server-side validation
if (strlen($username) < 5) {
    echo "Username must be at least 5 characters long";
    exit;
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo "Invalid email address";
    exit;
}

if (strlen($passwd) < 8) {
    echo "Password must be at least 8 characters long";
    exit;
}

if ($passwd !== $conf_passwd) {
    echo "Passwords do not match";
    exit;
}

// Database connection parameters
$servername = "localhost";
$dbUsername = "root";
$passwordDB = "";
$dbname = "hrs";

// Create connection
$conn = new mysqli($servername, $dbUsername, $passwordDB, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Prepare SQL statement to check if the username or email already exists
$query = $conn->prepare("SELECT * FROM admin WHERE username=? OR email=?");
$query->bind_param("ss", $username, $email);
$query->execute();
$result = $query->get_result();

if ($result->num_rows > 0) {
    echo "Username or email already exists";
    exit;
}

// Hash the password
$hashedPassword = password_hash($passwd, PASSWORD_DEFAULT);

// Insert user data into the database using prepared statement
$query = $conn->prepare("INSERT INTO admin (username, email, passwd) VALUES (?, ?, ?)");
$query->bind_param("sss", $username, $email, $hashedPassword);

if ($query->execute()) {
    echo "Registration successful!";
} else {
    echo "Error: " . $query->error;
}

// Check if hotel form is submitted
if (isset($_POST['hotel_name'], $_POST['country'], $_POST['area'], $_POST['amenities'], $_POST['room_services'], $_POST['room_types'])) {
    // Retrieve hotel form data
    $hotel_name = $_POST['hotel_name'];
    $country = $_POST['country'];
    $area = $_POST['area'];
    $amenities = $_POST['amenities'];
    $room_services = $_POST['room_services'];
    $room_types = $_POST['room_types'];

    // Insert hotel data into table
    $query1 = $conn->prepare("INSERT INTO hotel_data (hotel_name, country, area, amenities, room_services, room_types) VALUES (?, ?, ?, ?, ?, ?)");
    $query1->bind_param("ssssss", $hotel_name, $country, $area, $amenities, $room_services, $room_types);

    if ($query1->execute()) {
        echo "Hotel data added successfully!";
    } else {
        echo "Error: " . $query1->error;
    }
}

// Close database connection
$conn->close();
?>