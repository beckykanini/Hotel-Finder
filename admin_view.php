<?php
// Start the session
session_start();

// Check if the user is logged in as admin
if (!isset($_SESSION['admin_logged_in']) || $_SESSION['admin_logged_in'] !== true) {
    // hjheader("Location: login.php");
    // exit;
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

// Fetch data from database
$tables = ['guest', 'hotelier', 'hotel_data', 'admin'];
$data = [];

foreach ($tables as $table) {
    $query = "SELECT * FROM $table";
    $result = $conn->query($query);

    if ($result->num_rows > 0) {
        $data[$table] = $result->fetch_all(MYSQLI_ASSOC);
    } else {
        $data[$table] = [];
    }
}

// Close database connection
$conn->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - View Data</title>
    <link rel="stylesheet" href="admin_dashboard.css">
</head>
<body>
    <h2>View Data</h2>

    <div class="data-section">
        <h3>Guests</h3>
        <table>
            <tr>
                <th>Username</th>
                <th>Email</th>
            </tr>
            <?php foreach ($data['guest'] as $guest): ?>
                <tr>
                    <td><?php echo htmlspecialchars($guest['username']); ?></td>
                    <td><?php echo htmlspecialchars($guest['email']); ?></td>
                </tr>
            <?php endforeach; ?>
        </table>
    </div>

    <div class="data-section">
        <h3>Hoteliers</h3>
        <table>
            <tr>
                <th>Username</th>
                <th>Email</th>
            </tr>
            <?php foreach ($data['hotelier'] as $hotelier): ?>
                <tr>
                    <td><?php echo htmlspecialchars($hotelier['username']); ?></td>
                    <td><?php echo htmlspecialchars($hotelier['email']); ?></td>
                </tr>
            <?php endforeach; ?>
        </table>
    </div>

    <div class="data-section">
        <h3>Hotels</h3>
        <table>
            <tr>
                <th>Hotel Name</th>
                <th>Country</th>
                <th>Amenities</th>
                <th>Room Services</th>
                <th>Room Types</th>
            </tr>
            <?php foreach ($data['hotel_data'] as $hotel_data): ?>
                <tr>
                    <td><?php echo htmlspecialchars($hotel_data['hotel_name']); ?></td>
                    <td><?php echo htmlspecialchars($hotel_data['country']); ?></td>
                    <td><?php echo htmlspecialchars($hotel_data['amenities']); ?></td>
                    <td><?php echo htmlspecialchars($hotel_data['room_services']); ?></td>
                    <td><?php echo htmlspecialchars($hotel_data['room_types']); ?></td>
                </tr>
            <?php endforeach; ?>
        </table>
    </div>

    <div class="data-section">
        <h3>Admins</h3>
        <table>
            <tr>
                <th>Username</th>
                <th>Email</th>
            </tr>
            <?php foreach ($data['admin'] as $admin): ?>
                <tr>
                    <td><?php echo htmlspecialchars($admin['username']); ?></td>
                    <td><?php echo htmlspecialchars($admin['email']); ?></td>
                </tr>
            <?php endforeach; ?>
        </table>
    </div>
</body>
</html>