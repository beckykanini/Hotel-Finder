<?php
session_start();

// Check if form is submitted
if (isset($_POST['email'], $_POST['passwd'])) {
    // Retrieve form data
    $email = $_POST['email'];
    $passwd = $_POST['passwd'];

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

    // Prepare SQL statement to check the username and password
    $query = $conn->prepare("SELECT passwd FROM hotelier WHERE email=?");
    $query->bind_param("s", $email);
    $query->execute();
    $result = $query->get_result();

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        // Verify the password
        if (password_verify($passwd, $row['passwd'])) {
            // Password is correct, start the session
            $_SESSION['admin'] = $username;
            header("Location: /tophotels.html");
            exit;
        } else {
            echo "Wrong Password";
        }
    } else {
        echo "Invalid username";
    }

    // Close database connection
    $conn->close();
}
?>