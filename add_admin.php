<?php
// Start the session
session_start();

// Redirect if form is not submitted
if (!isset($_POST['username'], $_POST['email'], $_POST['phone_no'], $_POST['passwd'], $_POST['conf_passwd'])) {
    header("Location: admin_dashboard.html ");
    exit;
}

// Retrieve form data
$username = $_POST['username'];
$email = $_POST['email'];
$phone_no=$_POST['phone_no'];
$password = $_POST['passwd'];
$confirmPassword = $_POST['conf_passwd'];

// Perform server-side validation
if (strlen($username) < 5) {
    echo "Username must be at least 5 characters long";
    exit;
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo "Invalid email address";
    exit;
}

if (strlen($password) < 8) {
    echo "Password must be at least 8 characters long";
    exit;
}

if ($password !== $confirmPassword) {
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

// Prepare SQL statement to check if the username or email already exists in admin table
$query_admin = $conn->prepare("SELECT * FROM admin WHERE username=? OR email=?");
$query_admin->bind_param("ss", $username, $email);
$query_admin->execute();
$result_admin = $query_admin->get_result();


if ($result_admin->num_rows > 0 ) {
    echo "Username or email already exists";
    exit;
}

// Hash the password
$hashedPassword = password_hash($password, PASSWORD_DEFAULT);

// Insert user data into the admin table
$query_admin_insert = $conn->prepare("INSERT INTO admin (username, email, phone_no, passwd) VALUES (?, ?, ?, ?)");
$query_admin_insert->bind_param("ssss", $username, $email, $phone_no, $hashedPassword);
$query_admin_insert->execute();



// Check if both inserts were successful
if ($query_admin_insert->affected_rows > 0 ) {
    // Registration successful, redirect user to a different page
    echo "Registration successful!";
    // You can redirect the user to a different page here
} else {
    echo "Error: Unable to register";
}

// Close database connection
$conn->close();
?>