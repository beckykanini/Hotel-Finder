<?php
// forgot_password.php

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = filter_var($_POST['email'], FILTER_SANITIZE_EMAIL);

    if (filter_var($email, FILTER_VALIDATE_EMAIL)) {
        // Database connection
        $servername = "localhost";
        $username = "root";
        $password = "";
        $dbname = "hrs";

        $conn = new mysqli($servername, $username, $password, $dbname);

        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        // Check if email exists
        $stmt = $conn->prepare("SELECT username FROM guest WHERE email = ?");
        $stmt->bind_param("s", $email);
        $stmt->execute();
        $stmt->store_result();

        if ($stmt->num_rows > 0) {
            // Generate a unique token
            $token = bin2hex(random_bytes(50));

            // Insert token into database
            $stmt = $conn->prepare("INSERT INTO password_resets (email, token) VALUES (?, ?)");
            $stmt->bind_param("ss", $email, $token);
            $stmt->execute();

            // Send reset email
            $resetLink = "http://yourwebsite.com/reset_password.php?token=" . $token;
            $subject = "Password Reset Request";
            $message = "To reset your password, please click the following link: " . $resetLink;
            $headers = "From: no-reply@yourwebsite.com";

            if (mail($email, $subject, $message, $headers)) {
                echo "A password reset link has been sent to your email.";
            } else {
                echo "Failed to send email.";
            }
        } else {
            echo "No account found with that email.";
        }

        $stmt->close();
        $conn->close();
    } else {
        echo "Invalid email format.";
    }
}
?>
