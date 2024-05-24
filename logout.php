<?php
echo"Hello";
// Start the session
session_start();

// Unset all of the session variables
$_SESSION = array();

// Destroy the session
session_destroy();

// Redirect the user to the login page
// Respond with a success message
http_response_code(200);
echo "Logout successful";
header("Location: C:/xampp/htdocs/trial.html ");
exit;
?>