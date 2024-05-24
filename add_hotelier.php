<?php
// Start the session
session_start();

// Redirect if form is not submitted
if (!isset($_POST['hotelier_name'], $_POST['email'], $_POST['phone_no'], $_POST['hotel_name'], $_POST['hotel_location'], $_POST['passwd'], $_POST['conf_passwd'])) {
    header("Location: /login.html");
    exit;
}

// Retrieve form data
$hotelier_name=$_POST['hotelier_name'];
$email=$_POST['email'];
$phone_no=$_POST['phone_no'];
$hotel_name=$_POST['hotel_name'];
$hotel_location=$_POST['hotel_location'];
$passwd= $_POST['passwd'];
$conf_passwd=$_POST['conf_passwd'];

// Perform server-side validation
if (strlen($hotelier_name) < 5) {
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
$usernameDB = "root";
$passwordDB = "";
$dbname = "hrs";

// Create connection
$conn = new mysqli($servername, $usernameDB, $passwordDB, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Prepare SQL statement to check if the username or email already exists
$query = $conn->prepare("SELECT * FROM hotelier WHERE hotelier_name=? OR email=?");
$query->bind_param("ss", $hotelier_name, $email);
$query->execute();
$result = $query->get_result();

if ($result->num_rows > 0) {
    echo "Hotelier name or email already exists";
    exit;
}

// Hash the password
$hashedPassword = password_hash($passwd, PASSWORD_DEFAULT);

// Insert user data into the database using prepared statement
$query = $conn->prepare("INSERT INTO hotelier (hotelier_name, phone_no, email, hotel_name, hotel_location, passwd, conf_passwd) VALUES (?, ?, ?, ?, ?, ?, ?)");
$query->bind_param("sssssss", $hotelier_name, $phone_no, $email, $hotel_name, $hotel_location, $hashedPassword, $conf_passwd);

if ($query->execute()) {
    // Registration successful, redirect user to a different page
    echo "Registration successful!";
    // You can redirect the user to a different page here
} else {
    echo "Error: " . $query->error;
}

// Close database connection
$conn->close();
?>